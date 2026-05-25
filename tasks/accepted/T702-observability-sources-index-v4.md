Task ID: T702
Task Title: Observability / Evaluation Deep-Research Pack
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
继续收紧 observability 工具的入口与边界，补官方 release/changelog 入口。

Result:

# Observability Sources Index v4

## OpenTelemetry

### 官方入口

| 维度 | 内容 |
|------|------|
| **文档** | https://opentelemetry.io/ |
| **GitHub** | https://github.com/open-telemetry |
| **规范** | https://opentelemetry.io/specs/otel/ |
| **博客** | https://opentelemetry.io/blog/ |

### 稳定入口

- 概念入门：https://opentelemetry.io/docs/concepts/
- Python SDK：https://opentelemetry.io/docs/languages/python/
- Traces 概念：https://opentelemetry.io/docs/concepts/signals/traces/
- Metrics 概念：https://opentelemetry.io/docs/concepts/signals/metrics/

### Release / Changelog

- Python SDK Releases：https://github.com/open-telemetry/opentelemetry-python/releases
- Specification Changelog：https://opentelemetry.io/specs/otel/changelog/

### 边界说明

- OTel 是规范 + SDK，不直接提供存储和展示
- 数据后端（Jaeger、Langfuse、Prometheus）需要单独接入
- 日志（Logs）信号仍处于草案阶段，生产使用需谨慎

来源：https://opentelemetry.io/

---

## Langfuse

### 官方入口

| 维度 | 内容 |
|------|------|
| **文档** | https://langfuse.com/docs/ |
| **GitHub** | https://github.com/langfuse/langfuse |
| **Playground** | https://cloud.langfuse.com/ |
| **Blog** | https://langfuse.com/blog |

### 稳定入口

- 快速开始：https://langfuse.com/docs/observability/overview
- Python SDK：https://langfuse.com/docs/sdk/python
- LLM-as-Judge：https://langfuse.com/docs/observability/llm-as-judge
- Integrations：https://langfuse.com/docs/integrations/overview

### Release / Changelog

- GitHub Releases：https://github.com/langfuse/langfuse/releases
- Changelog：https://langfuse.com/changelog

### 边界说明

- 专注 LLM 场景，通用 traces 能力不如 Jaeger
- metrics 可视化能力弱于 Grafana
- self-hosted 需要额外运维

来源：https://langfuse.com/

---

## Phoenix（Arize AI）

### 官方入口

| 维度 | 内容 |
|------|------|
| **文档** | https://docs.arize.com/phoenix/ |
| **GitHub** | https://github.com/Arize-AI/phoenix |
| **Playground** | https://app.arize.com/phoenix |
| **Blog** | https://arize.com/blog/ |

### 稳定入口

- 快速开始：https://docs.arize.com/phoenix/quickstart
- Python SDK：https://docs.arize.com/phoenix/sections/python
- 概念：https://docs.arize.com/phoenix/concepts

### Release / Changelog

- GitHub Releases：https://github.com/Arize-AI/phoenix/releases
- Arize Blog：https://arize.com/blog/

### 边界说明

- 功能与 Langfuse 有部分重叠
- 主要面向模型评估和调试，不含完整 metric 可视化
- 主要在 Arize 云平台使用，self-hosted 能力有限

来源：https://github.com/Arize-AI/phoenix

---

## Grafana / Prometheus

### 官方入口

| 维度 | 内容 |
|------|------|
| **Grafana 文档** | https://grafana.com/docs/ |
| **Prometheus 文档** | https://prometheus.io/docs/ |
| **GitHub** | https://github.com/grafana/grafana |

### 稳定入口

- Prometheus 安装：https://prometheus.io/docs/prometheus/latest/getting_started/
- Grafana 安装：https://grafana.com/docs/grafana/latest/setup/
- vLLM dashboard：https://grafana.com/grafana/dashboards/（搜索 vLLM）

### Release / Changelog

- Prometheus Releases：https://github.com/prometheus/prometheus/releases
- Grafana Releases：https://github.com/grafana/grafana/releases
- Grafana Dashboard：https://grafana.com/orgs/vllm/dashboards

### 边界说明

- 需要额外部署，不适合 MVP 快速验证
- vLLM/SGLang 原生暴露 Prometheus 格式 metrics
- 不直接支持 LLM traces，需要额外配置

来源：https://grafana.com/
来源：https://prometheus.io/

---

## 与本项目关系

| 工具 | 与 inference-service | 与 eval-module |
|------|---------------------|---------------|
| **OpenTelemetry** | 标准化 traces/metrics 采集 | 可采集评测过程 metrics |
| **Langfuse** | tracing + token 用量 | 评测结果上报 |
| **Phoenix** | LLM trace 分析（参考） | LLM-as-Judge |
| **Prometheus** | 采集 /metrics | 采集评测资源 metrics |
| **Grafana** | metrics 可视化 | 评测结果可视化 |

## 优先阅读链接

1. https://langfuse.com/docs/observability/overview — Langfuse 快速开始
2. https://opentelemetry.io/docs/concepts/signals/traces/ — OTel traces 概念
3. https://docs.arize.com/phoenix/quickstart — Phoenix 快速开始
4. https://prometheus.io/docs/prometheus/latest/getting_started/ — Prometheus 快速开始
5. https://grafana.com/docs/grafana/latest/setup/ — Grafana 安装
6. https://langfuse.com/changelog — Langfuse Changelog

Sources:
1. https://opentelemetry.io/ — OpenTelemetry
2. https://langfuse.com/ — Langfuse
3. https://github.com/Arize-AI/phoenix — Phoenix
4. https://grafana.com/ — Grafana
5. https://prometheus.io/ — Prometheus
6. https://github.com/open-telemetry/opentelemetry-python — OTel Python SDK

Risk of Staleness:
- Langfuse SDK 更新快，具体 API 以实际版本为准
- OTel 日志（Logs）信号仍为草案

Out of Scope Kept:
- 未写完整可观测性平台建设方案
- 未写告警配置
- 未写日志存储方案
