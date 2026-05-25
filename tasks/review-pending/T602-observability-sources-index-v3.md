Task ID: T602
Task Title: Observability / Evaluation Zero-Touch Pack
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
收紧 observability 工具的稳定入口与边界（Langfuse/Phoenix/Grafana-Prometheus/OpenTelemetry）。

Result:

# Observability Sources Index v3

## OpenTelemetry

### 官方入口

| 维度 | 内容 |
|------|------|
| **文档** | https://opentelemetry.io/ |
| **GitHub** | https://github.com/open-telemetry |
| **规范** | https://opentelemetry.io/specs/otel/ |

### 核心能力

- Traces（调用链追踪）
- Metrics（指标采集）
- Logs（日志，草案阶段）
- SDK 支持 Python/Java/Go/Node.js

### 稳定入口

- 概念入门：https://opentelemetry.io/docs/concepts/
- Python SDK：https://opentelemetry.io/docs/languages/python/
- Traces 概念：https://opentelemetry.io/docs/concepts/signals/traces/

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

### 核心能力

- LLM 专用 tracing（prompt/response 记录）
- Token 用量统计
- LLM-as-Judge
- Prompt 版本管理
- 支持 self-hosted

### 稳定入口

- 快速开始：https://langfuse.com/docs/observability/overview
- Python SDK：https://langfuse.com/docs/sdk/python
- LLM-as-Judge：https://langfuse.com/docs/observability/llm-as-judge

### 边界说明

- 专注 LLM 场景，通用 traces 能力不如 Jaeger
- metrics 可视化能力弱于 Grafana
- self-hosted 需要额外运维

来源：https://langfuse.com/

---

## Phoenix（ Arize AI）

### 官方入口

| 维度 | 内容 |
|------|------|
| **文档** | https://docs.arize.com/phoenix/ |
| **GitHub** | https://github.com/Arize-AI/phoenix |
| **Playground** | https://app.arize.com/phoenix |

### 核心能力

- LLM trace 分析
- Span 嵌套可视化
- LLM-as-Judge
- 数据集版本对比

### 稳定入口

- 快速开始：https://docs.arize.com/phoenix/quickstart
- Python SDK：https://docs.arize.com/phoenix/sections/python
- 概念：https://docs.arize.com/phoenix/concepts

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

### 核心能力

- Prometheus：时序指标采集和存储
- Grafana：指标可视化 dashboard
- 大量开源 dashboard（vLLM、SGLang 等）
- Alerting（告警）

### 稳定入口

- Prometheus 安装：https://prometheus.io/docs/prometheus/latest/getting_started/
- Grafana 安装：https://grafana.com/docs/grafana/latest/setup/
- vLLM dashboard：https://grafana.com/grafana/dashboards/（搜索 vLLM）

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

Sources:
1. https://opentelemetry.io/ — OpenTelemetry
2. https://langfuse.com/ — Langfuse
3. https://github.com/Arize-AI/phoenix — Phoenix
4. https://grafana.com/ — Grafana
5. https://prometheus.io/ — Prometheus

Risk of Staleness:
- Langfuse SDK 更新快，具体 API 以实际版本为准
- OTel 日志（Logs）信号仍为草案
- 各工具版本可能影响接口稳定性

Out of Scope Kept:
- 未写完整可观测性平台建设方案
- 未写告警配置
- 未写日志存储方案
