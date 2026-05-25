Task ID: T307
Task Title: 产出 observability sources-index v1
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 T162/T204，产出 observability sources-index v1，分 Tracing/OpenTelemetry、Langfuse/Phoenix/TensorZero、Metrics/Grafana/Prometheus 三组，每组给官方入口、3-5 个优先阅读链接、边界说明。

Result:

# Observability Sources Index v1

## 一、Tracing / OpenTelemetry

### 官方入口

| 工具 | 官方入口 |
|------|---------|
| **OpenTelemetry** | https://opentelemetry.io/ |
| **OpenTelemetry GitHub** | https://github.com/open-telemetry |

### 边界说明
OpenTelemetry 是 CNCF 标准的 traces/metrics 规范和 SDK，提供统一的数据采集接口，不直接提供存储和展示层。

### 精确优先阅读链接（4 个）

1. **OpenTelemetry 官网** — https://opentelemetry.io/ — traces/metrics 规范和 SDK 入口
2. **OpenTelemetry 概念文档** — https://opentelemetry.io/docs/concepts/observability-primer/#distributed-traces — 分布式 tracing 概念说明
3. **OpenTelemetry GitHub** — https://github.com/open-telemetry — 规范和 SDK 实现
4. **Langfuse OpenTelemetry 集成文档** — https://langfuse.com/docs/observability/overview — Langfuse 对 OTel 的支持方式

---

## 二、Observability 平台

### 官方入口

| 工具 | 官方入口 |
|------|---------|
| **Langfuse** | https://langfuse.com/ |
| **Phoenix（Arize）** | https://github.com/Arize-AI/phoenix |
| **TensorZero** | https://github.com/tensorzero/tensorzero |

### 边界说明
这三个平台都提供 LLM 专用的 tracing + metrics + prompt 管理能力，Langfuse 和 TensorZero 还包含 evaluation 功能，Phoenix 侧重 traces 和 LLM-as-Judge。

### 精确优先阅读链接（5 个）

1. **Langfuse 官方文档** — https://langfuse.com/docs/observability/overview — LLM 可观测性平台文档
2. **Langfuse GitHub** — https://github.com/langfuse/langfuse — Langfuse 主仓库
3. **Phoenix GitHub** — https://github.com/Arize-AI/phoenix — Arize 开源可观测性库
4. **TensorZero GitHub** — https://github.com/tensorzero/tensorzero — 开源 LLMOps 平台
5. **Agenta GitHub（含 observability）** — https://github.com/agenta-ai/agenta — 开源 LLMOps，含 evaluation 和 observability

---

## 三、Metrics / 可视化

### 官方入口

| 工具 | 官方入口 |
|------|---------|
| **Grafana** | https://grafana.com/ |
| **Prometheus** | https://prometheus.io/ |
| **vLLM Metrics** | https://docs.vllm.ai/ |

### 边界说明
Grafana + Prometheus 是指标存储和可视化的标准组合，vLLM 等推理引擎暴露 Prometheus 格式 metrics 端点，Grafana 用于 dashboard 展示。

### 精确优先阅读链接（4 个）

1. **Grafana 官网** — https://grafana.com/ — 指标可视化平台
2. **Prometheus 官网** — https://prometheus.io/ — 指标采集和存储
3. **vLLM Metrics 文档** — https://docs.vllm.ai/ — vLLM 暴露的 metrics 说明
4. **Grafana + Triton IS 集成文档** — https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/ — Triton IS 的 Prometheus/Grafana 集成方式

Sources:
1. https://opentelemetry.io/ — OpenTelemetry 官网
2. https://langfuse.com/docs/observability/overview — Langfuse 可观测性文档
3. https://github.com/Arize-AI/phoenix — Phoenix 主仓库
4. https://github.com/tensorzero/tensorzero — TensorZero 主仓库
5. https://grafana.com/ — Grafana 官网
6. https://prometheus.io/ — Prometheus 官网
7. https://docs.vllm.ai/ — vLLM 文档

Risk of Staleness:
- Langfuse、TensorZero、Agenta 更新频繁，具体 API 以实际安装版本为准
- OpenTelemetry 为 CNCF 标准，稳定性较高
- 各推理引擎的 metrics 端点格式可能随版本变化

Out of Scope Kept:
- 未写完整可观测性手册
- 未做厂商横评
- 未写日志存储相关
