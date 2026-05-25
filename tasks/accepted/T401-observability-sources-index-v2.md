Task ID: T401
Task Title: Observability Long-Run Pack v1
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 T307-v1 收紧，补齐更稳定的精确优先阅读链接，产出 observability sources-index v2。

Result:

# Observability Sources Index v2

## 一、Tracing / OpenTelemetry

### 官方入口

| 工具 | 官方入口 |
|------|---------|
| **OpenTelemetry** | https://opentelemetry.io/ |
| **OpenTelemetry Python SDK** | https://opentelemetry.io/docs/languages/python/ |
| **OpenTelemetry 概念文档** | https://opentelemetry.io/docs/concepts/observability-primer/#distributed-traces |

### 边界说明
OpenTelemetry 是 CNCF 标准的 traces/metrics 规范和 SDK，提供统一数据采集接口，不直接提供存储和展示层。数据可接入 Jaeger、Zipkin、Langfuse 等多种后端。

### 精确优先阅读链接（4 个）

1. **OpenTelemetry 官网** — https://opentelemetry.io/ — traces/metrics 规范和 SDK 入口
2. **OpenTelemetry Python SDK 文档** — https://opentelemetry.io/docs/languages/python/ — Python 语言 SDK 接入文档
3. **OpenTelemetry tracing 概念** — https://opentelemetry.io/docs/concepts/observability-primer/#distributed-traces — Trace/Span 概念说明
4. **OpenTelemetry GitHub** — https://github.com/open-telemetry — 规范和 SDK 实现

---

## 二、Observability 平台

### 官方入口

| 工具 | 官方入口 |
|------|---------|
| **Langfuse** | https://langfuse.com/ |
| **Phoenix（Arize）** | https://github.com/Arize-AI/phoenix |
| **TensorZero** | https://github.com/tensorzero/tensorzero |
| **Agenta** | https://github.com/agenta-ai/agenta |

### 边界说明
Langfuse 和 Phoenix 是 LLM 专用 observability 平台，提供 tracing、metrics、LLM-as-Judge 能力。TensorZero 同时包含 gateway + observability + evaluation。Agenta 是 LLMOps 平台，observability 为附含功能。

### 精确优先阅读链接（6 个）

1. **Langfuse 官方文档** — https://langfuse.com/docs/observability/overview — LLM 可观测性平台文档（tracing + metrics + prompt）
2. **Langfuse GitHub** — https://github.com/langfuse/langfuse — Langfuse 主仓库
3. **Phoenix GitHub** — https://github.com/Arize-AI/phoenix — Arize 开源可观测性库
4. **TensorZero GitHub** — https://github.com/tensorzero/tensorzero — 开源 LLMOps 平台
5. **Agenta GitHub** — https://github.com/agenta-ai/agenta — 开源 LLMOps（含 evaluation 和 observability）
6. **Langfuse OpenTelemetry 集成文档** — https://langfuse.com/docs/observability/otel — Langfuse 对 OTel 的原生支持

---

## 三、Metrics / 可视化

### 官方入口

| 工具 | 官方入口 |
|------|---------|
| **Grafana** | https://grafana.com/ |
| **Prometheus** | https://prometheus.io/ |
| **vLLM Metrics** | https://docs.vllm.ai/en/latest/concepts/metrics.html |

### 边界说明
Grafana + Prometheus 是 metrics 存储和可视化的标准组合。vLLM 和 SGLang 等推理引擎暴露 Prometheus 格式 metrics 端点，Grafana 用于 dashboard 展示。

### 精确优先阅读链接（5 个）

1. **Grafana 官网** — https://grafana.com/ — 指标可视化平台
2. **Prometheus 官网** — https://prometheus.io/ — 指标采集和存储
3. **vLLM Metrics 文档** — https://docs.vllm.ai/en/latest/concepts/metrics.html — vLLM 暴露的 metrics 完整说明
4. **SGLang Metrics 文档** — https://docs.sglang.ai/backend/metrics.html — SGLang metrics 端点说明
5. **Grafana + Triton IS 集成** — https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/exporting_metrics.html — Triton IS 的 Prometheus/Grafana 集成

Sources:
1. https://opentelemetry.io/ — OpenTelemetry 官网
2. https://opentelemetry.io/docs/languages/python/ — OTel Python SDK
3. https://langfuse.com/docs/observability/overview — Langfuse 可观测性文档
4. https://github.com/Arize-AI/phoenix — Phoenix 主仓库
5. https://github.com/tensorzero/tensorzero — TensorZero 主仓库
6. https://grafana.com/ — Grafana 官网
7. https://prometheus.io/ — Prometheus 官网
8. https://docs.vllm.ai/en/latest/concepts/metrics.html — vLLM metrics 文档
9. https://docs.sglang.ai/backend/metrics.html — SGLang metrics 文档

Risk of Staleness:
- Langfuse、TensorZero、Agenta 更新频繁，具体 SDK 接口以实际安装版本为准
- OpenTelemetry 为 CNCF 标准，稳定性较高
- 各推理引擎的 metrics 端点格式可能随版本变化

Out of Scope Kept:
- 未写完整可观测性手册
- 未做厂商横评
- 未写日志存储相关
