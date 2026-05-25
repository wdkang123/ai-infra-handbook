Task ID: T604
Task Title: Cross-Project Systemization Pack
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
把 request/response/trace/metric/evaluation result/finetune artifact 之间的流向说明清楚。

Result:

# Data and Telemetry Flow Map v1

## 概述

本文档说明各数据类型在各模块之间的流向，包括 request、response、trace、metric、evaluation result、finetune artifact。

---

## 数据类型定义

| 数据类型 | 说明 | 格式 |
|---------|------|------|
| **Request** | 用户请求（prompt） | JSON |
| **Response** | 模型回复 | JSON |
| **Trace** | 调用链追踪数据 | Langfuse span |
| **Metric** | 指标数据（QPS/延迟/GPU） | Prometheus |
| **Eval Result** | 评测结果（分数） | JSON |
| **Finetune Artifact** | LoRA adapter 文件 | bin/safetensors |

---

## Request / Response 流向

### 推理请求流向

```
用户
    ↓ request
ai-gateway（鉴权 / 限流 / 计量）
    ↓ request
inference-service（vLLM/SGLang）
    ↓ response
ai-gateway
    ↓ response
用户
```

### 评测请求流向

```
eval-module
    ↓ request（prompt）
inference-service（vLLM/SGLang）
    ↓ response
eval-module（计算分数）
    ↓ eval result
评测结果 JSON / Langfuse
```

### 微调请求流向

```
finetune-demo
    ↓ 训练数据
PEFT/TRL（执行微调）
    ↓ finetune artifact（adapter）
finetune-demo 保存 adapter
    ↓ adapter + base model
inference-service 加载推理
    ↓ response
eval-module 评测
```

---

## Trace 流向

### Langfuse Trace

```
ai-gateway（Langfuse SDK span）
    ↓ trace
Langfuse（存储 + 展示）

inference-service（Langfuse SDK span）
    ↓ trace
Langfuse

eval-module（Langfuse SDK span，可选）
    ↓ trace
Langfuse
```

### 串联说明

- ai-gateway 的 span 和 inference-service 的 span 在 Langfuse dashboard 中可以串联成完整调用链
- 需要 trace_id 在请求头中传递

来源：https://langfuse.com/docs/observability/overview

---

## Metric 流向

### Prometheus Metrics

```
inference-service（/metrics 端点）
    ↓ Prometheus 抓取
Prometheus（存储）
    ↓
Grafana（可视化 dashboard）
```

### 关键 metrics

| metric | 来源 | 说明 |
|--------|------|------|
| `vllm:num_requests_running` | inference-service | 运行中请求数 |
| `vllm:num_tokens_total` | inference-service | 总 token 数 |
| `vllm:gpu_cache_usage` | inference-service | GPU 显存使用率 |
| `vllm:prefix_cache_hit_rate` | inference-service（SGLang） | 前缀缓存命中率 |

来源：https://docs.vllm.ai/en/latest/metrics.html

---

## Eval Result 流向

### 评测结果流

```
eval-module
    ↓ 运行评测
评测结果 JSON
    ↓ 保存
本地文件 / Langfuse（可选）
    ↓
与历史结果对比
```

### 评测结果关联

```
评测结果（eval result）
    ↓
Langfuse span（可选关联）
    ↓
推理 trace（同一请求的 tracing 数据）
```

来源：https://github.com/EleutherAI/lm-evaluation-harness

---

## Finetune Artifact 流向

### Adapter 流

```
finetune-demo
    ↓ PEFT/TRL 训练
LoRA adapter（safetensors 格式）
    ↓
finetune-demo 保存到指定路径
    ↓
inference-service 加载（base model + adapter）
    ↓
微调后推理验证
    ↓
eval-module 跑 benchmark
```

---

## 完整流向总图

```
用户请求
    ↓
ai-gateway
    ├── Trace（Langfuse SDK）→ Langfuse
    └── Request → inference-service
              ↓
              inference-service
              ├── Trace（Langfuse SDK）→ Langfuse
              ├── Metrics → Prometheus → Grafana
              └── Response → gateway → 用户

finetune-demo
    ↓ 训练
adapter → inference-service 加载
    ↓
eval-module
    ├── Trace → Langfuse
    ├── Eval Result → JSON / Langfuse
    └── Benchmark 对比
```

---

## 数据流边界说明

| 数据类型 | 生产者 | 消费者 | 存储 |
|---------|-------|-------|------|
| Request/Response | ai-gateway / 用户 | inference-service | 不持久化 |
| Trace | 各模块 Langfuse SDK | Langfuse | Langfuse（self-hosted 或云端） |
| Metric | inference-service | Prometheus | Prometheus |
| Eval Result | eval-module | 文件 / Langfuse | 本地 JSON 或 Langfuse |
| Finetune Artifact | finetune-demo | inference-service | 本地文件系统 |

Sources:
1. https://langfuse.com/docs/observability/overview — Langfuse
2. https://docs.vllm.ai/en/latest/metrics.html — vLLM metrics
3. https://prometheus.io/ — Prometheus
4. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval

Risk of Staleness:
- 各系统接口可能随版本变化

Out of Scope Kept:
- 未写数据持久化详细方案
- 未写 trace_id 传递机制
- 未写错误处理流程
