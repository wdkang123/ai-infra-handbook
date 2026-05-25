Task ID: T501
Task Title: Observability Long-Run Pack v2
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
说明 observability 如何映射到 inference-service、ai-gateway、eval-module 三个模块。

Result:

# Observability Integration Notes v1

## 概述

本文档说明 observability 能力如何映射到项目中三个核心模块：inference-service、ai-gateway、eval-module。

---

## 1. inference-service 的可观测性集成

### 暴露的 metrics 端点

inference-service 内置的 vLLM/SGLang 引擎已原生暴露 Prometheus 格式 metrics：

```
/metrics  → Prometheus 格式指标（QPS、延迟、GPU 利用率、token throughput）
```

### 推荐集成方式

| 工具 | 集成位置 | 用途 |
|------|---------|------|
| **Prometheus** | 抓取 `/metrics` | 采集 GPU/推理指标 |
| **Grafana** | 连接 Prometheus | 可视化 dashboard |
| **Langfuse SDK** | 在 inference-service 代码中埋点 | tracing + token 用量上报 |

### 最小实践路径

```
inference-service（vLLM/SGLang）
    ↓ /metrics 端点
Prometheus（抓取 + 存储）
    ↓
Grafana（可视化 QPS/P99/GPU Util）
```

可选叠加 Langfuse SDK：
```
inference-service（Langfuse SDK 埋点）
    ↓
Langfuse（trace + token 用量 dashboard）
```

来源：https://docs.vllm.ai/
来源：https://langfuse.com/docs/observability/overview

---

## 2. ai-gateway 的可观测性集成

### 暴露的 metrics 端点

ai-gateway 记录以下可观测数据：

- 请求路由日志（哪个模型、哪个后端）
- token 用量（prompt tokens + completion tokens）
- 错误率和延迟分布

### 推荐集成方式

| 工具 | 集成位置 | 用途 |
|------|---------|------|
| **Langfuse SDK** | 在 gateway 代码中埋点 | 完整请求链路 tracing |
| **OTel SDK** | 可选，作为 Langfuse 的前置采集层 | 标准化数据，可接入多后端 |

### 最小实践路径

```
客户端请求
    ↓
ai-gateway（Langfuse span 记录路由 + token）
    ↓
inference-service（Langfuse span 记录推理）
    ↓
Langfuse dashboard（完整调用链 + token 统计）
```

Langfuse 的 trace 可以串联 gateway 到 inference-service 的完整请求路径。

来源：https://langfuse.com/docs/observability/overview
来源：https://opentelemetry.io/

---

## 3. eval-module 的可观测性集成

### 评测结果的可观测性

eval-module 运行评测后产生以下数据：

- 评测分数（accuracy、BLEU、Pass@K 等）
- 评测耗时
- 数据集信息
- 评测版本

### 推荐集成方式

| 工具 | 集成位置 | 用途 |
|------|---------|------|
| **Langfuse SDK** | 在 eval-module 中埋点 | 评测结果上报，与推理 trace 关联 |
| **本地 JSON 文件** | MVP 阶段默认 | 评测结果持久化，不强制上报 |

### 最小实践路径（MVP）

```
eval-module
    ↓ 运行评测
评测结果 → 本地 JSON 文件（不强制上报 Langfuse）
```

### 可选叠加 Langfuse（长期）

```
eval-module
    ↓ Langfuse span 上报
Langfuse dashboard（评测分数 + 关联推理 trace）
```

评测结果与推理 trace 关联的价值在于：可以分析同一 prompt 下模型表现与推理服务质量的关系。

来源：https://langfuse.com/docs/observability/overview
来源：https://github.com/EleutherAI/lm-evaluation-harness

---

## 模块间可观测性协作图

```
ai-gateway          inference-service         eval-module
    │                       │                       │
    │ Langfuse SDK          │ Langfuse SDK          │
    │（路由+token trace）    │（推理 trace）          │ Langfuse SDK（可选）
    │                       │                       │（评测结果上报）
    └───────────────────────┴───────────────────────┘
                            │
                            ↓
                    Langfuse Dashboard
                    （trace + token 统计）

inference-service
    │
    │ /metrics 端点
    ↓
Prometheus ← → Grafana
（metrics 采集） （可视化 dashboard）
```

---

## 各模块集成优先级

| 模块 | 工具 | MVP 必须 | 推荐阶段 |
|------|------|---------|---------|
| inference-service | Prometheus metrics | 是 | 默认启用 |
| inference-service | Grafana 可视化 | 中 | 研究阶段引入 |
| inference-service | Langfuse SDK | 高 | 早期接入 |
| ai-gateway | Langfuse SDK | 高 | 早期接入 |
| eval-module | 本地 JSON | 是 | MVP 默认 |
| eval-module | Langfuse SDK | 低 | 后续迭代 |

---

## 与其他包的协作

- **T502（Eval/Benchmark Pack）**：eval-module 的评测结果上报 Langfuse 后，可与 observability 数据联合分析
- **T503（Finetuning Pack）**：finetune-demo 的训练过程 metrics 可复用 Prometheus + Grafana 栈

Sources:
1. https://docs.vllm.ai/ — vLLM metrics
2. https://langfuse.com/docs/observability/overview — Langfuse
3. https://opentelemetry.io/ — OpenTelemetry
4. https://prometheus.io/ — Prometheus
5. https://grafana.com/ — Grafana
6. https://github.com/EleutherAI/lm-evaluation-harness — LM-Eval Harness

Risk of Staleness:
- 各模块的可观测性接口可能随 SDK 版本变化
- Langfuse self-hosted vs 云端配置方式有差异

Out of Scope Kept:
- 未写完整监控告警配置
- 未写 eval-module 的评测结果持久化方案
- 未写训练过程的 metrics 采集详细配置
