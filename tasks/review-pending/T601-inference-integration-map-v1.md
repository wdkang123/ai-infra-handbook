Task ID: T601
Task Title: Inference Core Zero-Touch Pack
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
说明 inference core 如何映射到 inference-service、ai-gateway、observability、benchmark/evaluation。

Result:

# Inference Integration Map v1

## 概述

本文档说明 inference core 能力如何映射到项目中四个关键模块：inference-service、ai-gateway、observability、benchmark/evaluation。

---

## 1. inference-service 的 inference core 集成

### 引擎选择

| 引擎 | 集成位置 | 用途 |
|------|---------|------|
| **vLLM** | inference-service 主要推理引擎 | OpenAI 兼容 API，支持 Paged Attention |
| **SGLang** | inference-service 备选引擎 | RadixAttention，适合多轮对话 |

### 暴露的接口

```
inference-service
    ├── /v1/chat/completions（OpenAI 兼容）
    ├── /v1/completions
    ├── /metrics（Prometheus 格式）
    └── /health
```

### 最小目录结构（提案）

```
inference-service/
    ├── engines/
    │     ├── vllm_engine.py      # vLLM 引擎封装
    │     └── sglang_engine.py     # SGLang 引擎封装
    ├── api/
    │     └── openai_proxy.py      # OpenAI API 代理
    └── metrics/
          └── prometheus.py         # metrics 暴露
```

来源：https://docs.vllm.ai/

---

## 2. ai-gateway 的 inference core 集成

### 路由关系

```
客户端请求
    ↓
ai-gateway（路由 / 鉴权 / 限流）
    ↓
inference-service（vLLM/SGLang）
```

### 集成点

| 集成点 | 说明 |
|--------|------|
| **上游接口** | gateway 接收 client 请求 |
| **下游调用** | gateway 调用 inference-service 的 OpenAI 兼容 API |
| **metrics 上报** | gateway 记录 token 用量和延迟 |

### 最小目录结构（提案）

```
ai-gateway/
    ├── proxy/
    │     └── openai_proxy.py      # 代理到 inference-service
    ├── middleware/
    │     ├── auth.py
    │     ├── rate_limiter.py
    │     └── router.py
    └── metrics/
          └── token_tracker.py     # token 用量跟踪
```

来源：https://docs.vllm.ai/en/latest/getting_started/quickstart.html

---

## 3. observability 的 inference core 集成

### metrics 采集路径

```
inference-service（vLLM /metrics）
    ↓
Prometheus（抓取 + 存储）
    ↓
Grafana（可视化）
```

### 关键 metrics

| metric | 含义 |
|--------|------|
| `vllm:num_requests_running` | 运行中请求数 |
| `vllm:num_tokens_total` | 总 token 数 |
| `vllm:gpu_cache_usage` | GPU 显存使用率 |
| `vllm:prefix_cache_hit_rate` | 前缀缓存命中率（SGLang） |

### tracing 集成

| 工具 | 集成位置 | 用途 |
|------|---------|------|
| **Langfuse SDK** | inference-service 代码埋点 | trace + token 用量 |
| **OTel SDK** | 可选，作为 Langfuse 前置 | 标准化采集 |

来源：https://docs.vllm.ai/en/latest/metrics.html

---

## 4. benchmark/evaluation 的 inference core 集成

### 评测执行路径

```
eval-module
    ↓ lm-eval API
inference-service（vLLM / SGLang backend）
    ↓
评测结果 → eval-module 持久化
```

### 集成点

| 集成点 | 说明 |
|--------|------|
| **backend 指定** | lm-eval 的 `--model vllm` 指向 inference-service |
| **metrics 对接** | 评测过程中观测 GPU 利用率等 |
| **结果关联** | 评测结果可与 tracing 数据关联分析 |

### 最小实践

```bash
lm_eval --model vllm \
    --model_args base_url=http://inference-service:8000/v1 \
    --tasks mmlu,gsm8k
```

来源：https://github.com/EleutherAI/lm-evaluation-harness

---

## 模块间协作总图

```
ai-gateway
    ↓ 路由请求
inference-service（vLLM/SGLang）
    ├── /metrics → Prometheus → Grafana（metrics 可视化）
    ├── Langfuse SDK → Langfuse（tracing + token 统计）
    └── /v1/chat → lm-eval → eval-module（benchmark 评测）

eval-module → 评测结果 → Langfuse（可选关联）
```

---

## 与其他包的协作

- **T602（Observability/Evaluation Pack）**：Langfuse / Prometheus / Grafana 的集成说明
- **T603（Finetuning Pack）**：训练完成后用 inference-service 跑 benchmark 验证

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://sglang.readthedocs.io/ — SGLang
3. https://docs.vllm.ai/en/latest/metrics.html — vLLM metrics
4. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval

Risk of Staleness:
- 各模块接口可能随版本变化
- 具体实现以实际代码为准

Out of Scope Kept:
- 未写代码实现
- 未写完整部署配置
- 未写多引擎切换逻辑
