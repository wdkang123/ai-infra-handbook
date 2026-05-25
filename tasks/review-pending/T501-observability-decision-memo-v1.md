Task ID: T501
Task Title: Observability Long-Run Pack v2
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 T401/T310，讨论 OTel 是否作为默认采集层、Langfuse/Phoenix/Grafana-Prometheus 各自适合什么位置。

Result:

# Observability Decision Memo v1

## 概述

本文档围绕 observability 工具选型的关键决策点，给出资料级输入，帮助 Codex 做最终判断。不下最终结论。

---

## 决策点一：OpenTelemetry 是否应作为默认采集层

### 支持作为默认的理由

- **行业标准**：OTel 是 CNCF 毕业项目，被广泛采用，生态成熟
- **多后端兼容**：一次埋点，可接入 Jaeger、Zipkin、Langfuse、Prometheus 等多种后端
- **跨语言支持**：Python/Java/Go/Node.js 等均有官方 SDK，便于扩展到其他模块

### 不支持作为 MVP 默认的理由

- **接入成本**：需要在代码中显式埋点，比直接用 Langfuse SDK 更费工
- **学习曲线**：OTel 的概念模型（TracerProvider/SpanExporter/Processor）需要额外学习
- **MVP 阶段冗余**：如果 Langfuse SDK 已经够用，OTel 的灵活性在 MVP 阶段是 overkill

### 资料级输入

OTel 适合作为**长期标准**，Langfuse 适合作为 **MVP 快速落地**。两者并非互斥，可先 Langfuse 再逐步迁移到 OTel。

来源：https://opentelemetry.io/

---

## 决策点二：Langfuse / Phoenix / Grafana-Prometheus 各自适合什么位置

### Langfuse — LLM 专用 tracing + 指标

**适合位置**：作为 inference-service 和 ai-gateway 的 tracing 和 token 用量统计的默认工具。

**理由**：
- Langfuse 原生支持 LLM 场景（prompt/response 记录、token 用量、LLM-as-Judge）
- 安装简单（pip install langfuse），接入成本低
- 有 self-hosted 模式，数据不上云

**局限**：
- 作为完整 observability 平台，metrics 可视化能力不如 Grafana

来源：https://langfuse.com/docs/observability/overview

### Phoenix — 深度 LLM trace 分析

**适合位置**：作为 Langfuse 的补充，用于需要深入分析 LLM trace 语义质量的场景。

**理由**：
- Phoenix 专注于 LLM trace 的语义分析（span 嵌套、prompt 调试）
- 与 Langfuse 有部分功能重叠，不建议同时启用

**局限**：
- 需要额外部署，不适合 MVP 快速启动

来源：https://github.com/Arize-AI/phoenix

### Grafana + Prometheus — 指标可视化

**适合位置**：作为 inference-service 的 metrics 可视化层，与 Langfuse 互补。

**理由**：
- vLLM 和 SGLang 原生暴露 Prometheus 格式 metrics
- Grafana 有大量现成 dashboard，开源生态成熟
- QPS/P99/GPU Util 等聚合指标在 Grafana 中更直观

**局限**：
- 需要额外部署 Prometheus + Grafana，运维成本较高
- 不适合"MVP 快速验证"阶段

来源：https://grafana.com/
来源：https://prometheus.io/

### 工具协作关系建议（资料级）

```
Langfuse（tracing + token 用量）← inference-service / ai-gateway
Grafana + Prometheus（metrics 可视化）← inference-service
Langfuse 或 Phoenix（可选：评测 trace 分析）← eval-module
```

---

## 决策点三：eval-module 的可观测性集成方式

### 评测结果上报的必要性

- **短期（MVP）**：eval-module 的评测结果可以只保存为本地 JSON，不强制上报 Langfuse
- **长期**：评测结果与推理 trace 关联分析是有价值的方向，但需要 Codex 确认优先级

来源：https://github.com/EleutherAI/lm-evaluation-harness

---

## 总结：资料级建议（不下结论）

| 决策点 | 建议方向 | 关键依据 |
|--------|---------|---------|
| OTel vs Langfuse SDK | MVP 用 Langfuse，长期可迁移 OTel | Langfuse 接入成本低，OTel 生态大 |
| Langfuse vs Phoenix | Langfuse 作为默认，Phoenix 作为进阶补充 | Langfuse 功能更全 |
| Grafana-Prometheus | MVP 可选，研究阶段建议引入 | vLLM 原生支持 Prometheus |
| eval-module 上报 | MVP 暂不上报，评测结果存本地 | 减少初期复杂度 |

## 需要 Codex 最终判断

1. MVP 阶段是否允许使用 Langfuse self-hosted，还是必须完全开源？
2. Grafana-Prometheus 是否在 MVP 必须引入，还是用 Langfuse metrics 即可？
3. OTel 的接入是否是后续迭代的必须项？

Sources:
1. https://opentelemetry.io/ — OpenTelemetry
2. https://langfuse.com/docs/observability/overview — Langfuse
3. https://github.com/Arize-AI/phoenix — Phoenix
4. https://grafana.com/ — Grafana
5. https://prometheus.io/ — Prometheus
6. https://docs.vllm.ai/ — vLLM
