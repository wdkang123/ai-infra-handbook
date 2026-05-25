Task ID: T501
Task Title: Observability Long-Run Pack v2
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 T310-v1/T316-v2，产出更完整的 observability 工具 comparison-index-v2。

Result:

# Observability Comparison Index v2

## 比较对象

- OpenTelemetry
- Langfuse
- Phoenix
- TensorZero
- Grafana / Prometheus

## 定位比较

| 对象 | 定位 | 来源 |
|------|------|------|
| **OpenTelemetry** | CNCF 标准，提供 traces/metrics 数据采集的规范和 SDK，不直接提供存储和展示 | https://opentelemetry.io/ |
| **Langfuse** | LLM 可观测性平台，支持 tracing、metrics、prompt 管理和 LLM-as-Judge | https://langfuse.com/ |
| **Phoenix** | Arize 开源可观测性库，专注 LLM traces 和 LLM-as-Judge | https://github.com/Arize-AI/phoenix |
| **TensorZero** | 开源 LLMOps 平台，统一 gateway + observability + evaluation | https://github.com/tensorzero/tensorzero |
| **Grafana / Prometheus** | 指标存储与可视化标准组合，接收推理引擎暴露的 Prometheus 格式 metrics | https://grafana.com/ |

## 所处层级比较

| 对象 | 所处层级 | 说明 | 来源 |
|------|---------|------|------|
| **OpenTelemetry** | 规范/采集层 | 标准化数据采集接口，数据流向可配置 | https://opentelemetry.io/ |
| **Langfuse** | 平台层 | 端到端可观测性平台，数据存储和展示均内置 | https://langfuse.com/ |
| **Phoenix** | 平台层 | traces 分析和 LLM-as-Judge 平台 | https://github.com/Arize-AI/phoenix |
| **TensorZero** | 平台层 | LLMOps 平台，observability + evaluation + gateway | https://github.com/tensorzero/tensorzero |
| **Grafana / Prometheus** | 展示/存储层 | Prometheus 采集存储，Grafana 负责可视化 dashboard | https://grafana.com/ |

层级关系：
```
规范层：OpenTelemetry（数据采集标准）
    ↓
平台层：Langfuse / Phoenix / TensorZero（存储 + 展示）
    ↓
展示层：Grafana / Prometheus（metrics 可视化）
```

## 典型使用场景

| 对象 | 典型使用场景 | 来源 |
|------|-------------|------|
| **OpenTelemetry** | 需要统一采集 traces/metrics 并接入多种后端存储 | https://opentelemetry.io/ |
| **Langfuse** | LLM 应用需要 tracing + metrics + prompt 版本管理的完整可观测性 | https://langfuse.com/ |
| **Phoenix** | 需要 LLM 专用 traces 分析和 LLM-as-Judge 能力 | https://github.com/Arize-AI/phoenix |
| **TensorZero** | 需要统一 gateway + observability + evaluation 的完整 LLMOps | https://github.com/tensorzero/tensorzero |
| **Grafana / Prometheus** | 监控推理服务的 QPS、延迟、GPU 利用率等指标 | https://grafana.com/ |

## 与本项目关系

| 对象 | 与本项目关系 | 来源 |
|------|------------|------|
| **OpenTelemetry** | 作为标准接口，inference-service 可通过 OTel SDK 采集数据 | https://opentelemetry.io/ |
| **Langfuse** | eval-module 的评测结果可上报 Langfuse 做可观测性关联 | https://langfuse.com/ |
| **Phoenix** | 作为 traces 分析工具的参考，inference-service 可对接 | https://github.com/Arize-AI/phoenix |
| **TensorZero** | 作为 LLMOps 完整方案的参考架构 | https://github.com/tensorzero/tensorzero |
| **Grafana / Prometheus** | inference-service 暴露 Prometheus metrics 端点，Grafana 做可视化 | https://grafana.com/ |

## MVP 适配性评估

| 对象 | MVP 适配性 | 说明 |
|------|-----------|------|
| **OpenTelemetry** | 中 | 标准但接入成本较高，适合长期架构 |
| **Langfuse** | 高 | 接入简单，LLM 原生支持，适合 MVP |
| **Phoenix** | 低 | 功能与 Langfuse 有重叠，非 MVP 必须 |
| **TensorZero** | 低 | 功能全面但复杂，适合完整 LLMOps 场景 |
| **Grafana / Prometheus** | 中 | 指标可视化能力强，但需要额外部署 |

Sources:
1. https://opentelemetry.io/ — OpenTelemetry 官网
2. https://langfuse.com/ — Langfuse 官网
3. https://github.com/Arize-AI/phoenix — Phoenix 主仓库
4. https://github.com/tensorzero/tensorzero — TensorZero 主仓库
5. https://grafana.com/ — Grafana 官网

Risk of Staleness:
- Langfuse、TensorZero、Agenta 更新频繁，具体 API 以实际安装版本为准
- OpenTelemetry 为 CNCF 标准，稳定性较高
- 各推理引擎的 metrics 端点格式可能随版本变化

Out of Scope Kept:
- 未写完整可观测性手册
- 未做厂商横评
- 未写日志存储相关

Need Codex Review On:
- inference-service 和 eval-module 中实际使用的可观测性工具选型（以实际实现为准）
