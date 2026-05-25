Task ID: T401
Task Title: Observability Long-Run Pack v1
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 T204/T301/T302/T303，说明 observability 在 inference-service、ai-gateway、eval-module 三个模块中的落点与边界。

Result:

# Observability Project Map v1

## 模块落点总览

Observability 在本项目中不是独立模块，而是横向能力，分布在 inference-service、ai-gateway、eval-module 三个模块中各自承担不同角色。

## inference-service — metrics 数据源

### 落点
inference-service 作为推理引擎的 HTTP/gRPC 包装层，是可观测性数据的最主要来源。

### 暴露的 observability 接口
- **Prometheus metrics 端点**（`/metrics`）：QPS、P99 Latency、GPU Util、TPM（Tokens Per Minute）等
- **健康检查端点**（`/health`）：服务存活状态
- **可选 tracing span**：在请求处理路径上记录关键环节的耗时

### 边界
- inference-service **负责采集和暴露** metrics 数据
- 数据**存储和展示**由外部工具（Grafana/Langfuse）负责
- tracing 的完整链路（从 gateway 到 engine）需要与 ai-gateway 协同

来源：https://docs.vllm.ai/
来源：https://grafana.com/

## ai-gateway — 请求日志与 token 用量

### 落点
ai-gateway 作为统一流量入口，负责记录请求日志和 token 用量统计。

### 暴露的 observability 接口
- **请求日志**：每次请求的 model、prompt tokens、completion tokens、延迟
- **token 用量统计**：per-model、per-user 的 TPM/RPM 统计
- **Prometheus metrics 端点**（`/metrics`）：RPS、错误率
- **可对接 tracing**：通过 OpenTelemetry 协议透传 trace span 到下游

### 边界
- ai-gateway **记录用量**，不记录模型输出的语义内容
- token 用量是成本结算和 SLO 监控的基础
- ai-gateway 可以透传 tracing span，但 tracing 的根节点在 gateway

来源：https://github.com/langfuse/langfuse

## eval-module — 评测结果上报

### 落点
eval-module 执行评测后，结果可上报到可观测性平台，与推理指标联动分析。

### 暴露的 observability 接口
- **评测结果记录**：每次评测的分数、版本对比
- **可选 Langfuse 集成**：评测结果和推理 trace 关联分析
- **评测 trace**：评测请求的完整调用路径

### 边界
- eval-module 的可观测性**不影响推理服务本身**
- 评测结果上报是可选能力，不是 MVP 必须
- 评测与 observability 的协作点在于：在同一个 trace 中同时看到推理参数和评测分数

来源：https://github.com/EleutherAI/lm-evaluation-harness
来源：https://langfuse.com/docs/observability/overview

## 三模块协同关系

```
ai-gateway（记录请求 + token 用量）
    ↓ tracing span
inference-service（暴露 metrics + 推理耗时）
    ↓
eval-module（评测结果，可上报 Langfuse）
```

| 模块 | 主要 observability 贡献 | 数据方向 |
|------|----------------------|---------|
| inference-service | Prometheus metrics（QPS/P99/GPU/TPM） | 向下游推送 |
| ai-gateway | 请求日志 + token 用量 + tracing 透传 | 向上游记录 |
| eval-module | 评测结果上报（可选） | 按需上报 |

## 与 observability 工具的对应关系

| 项目模块 | 可对接的 observability 工具 |
|---------|--------------------------|
| inference-service | Prometheus + Grafana（metrics）、OpenTelemetry（tracing） |
| ai-gateway | Langfuse（tracing + 用量）、Prometheus（metrics） |
| eval-module | Langfuse（评测结果关联分析）、OpenTelemetry（tracing） |

Sources:
1. https://docs.vllm.ai/ — vLLM metrics 文档
2. https://grafana.com/ — Grafana 官网
3. https://langfuse.com/docs/observability/overview — Langfuse 可观测性文档
4. https://opentelemetry.io/ — OpenTelemetry 官网
5. https://github.com/Arize-AI/phoenix — Phoenix 主仓库

Risk of Staleness:
- 各模块的 metrics 端点格式可能随版本变化
- Langfuse 等工具的 SDK 接口更新较快

Out of Scope Kept:
- 未写具体代码实现
- 未写数据存储设计
- 未写告警规则
