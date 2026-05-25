Task ID: T501
Task Title: Observability Long-Run Pack v2
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
Observability Long-Run Pack v2，基于 T401/T310/T316，产出5个文件：manifest、decision-memo、comparison-index-v2、practice-catalog-v2、integration-notes。

Result:

# Observability Long-Run Pack Manifest v2

## 包概述

本包为 Observability 专题的第二版长跑包，在 v1 基础上补充决策备忘录、更完整的 comparison-index-v2、从单机到多组件的 practice-catalog-v2、以及模块级 integration-notes。

## 已完成交付物

### 1. T501-observability-pack-manifest-v2
本文件。总结本包交付物清单和用途。

### 2. T501-observability-decision-memo-v1
围绕 OTel 是否作为默认采集层、Langfuse/Phoenix/Grafana-Prometheus 各自适合什么位置，给出资料级决策输入，不下最终结论。

### 3. T501-observability-comparison-index-v2
把 observability 工具比较拉得更完整，但仍保持索引风格（OTel/Langfuse/Phoenix/TensorZero/Grafana-Prometheus）。

### 4. T501-observability-practice-catalog-v2
在 v1 基础上补更多"从单机到多组件"的最小实践。

### 5. T501-observability-integration-notes-v1
说明 observability 如何映射到 inference-service、ai-gateway、eval-module 三个模块。

## 各交付物关系

```
decision-memo（决策输入）
    ↓
integration-notes（模块映射）
    ↓
comparison-index-v2（工具全图）
    ↓
practice-catalog-v2（实践路径）
    ↓
manifest（本文件）
```

## 需要 Codex 判断的点

1. **OTel 是否作为默认采集层**：OTel 是标准但接入成本高，是否适合作为 MVP 默认？
2. **Langfuse 的定位**：作为 MVP 默认 tracing 工具还是备选？
3. **Grafana-Prometheus vs 云原生监控**：本项目是否有必要在 MVP 阶段引入完整 Grafana 栈？
4. **eval-module 的可观测性集成方式**：评测结果上报是否是 MVP 必须？

## 与其他包的关系

- **T502（Eval/Benchmark Pack v2）**：eval-module 的评测结果可上报 Langfuse，与 observability 形成协作
- **T503（Finetuning Pack v2）**：finetune-demo 训练过程的监控复用 observability 能力

## 风险与依赖

- Langfuse 等工具更新频繁，具体 SDK 接口以实际安装版本为准
- OpenTelemetry 为 CNCF 标准，稳定性较高
- 各推理引擎的 metrics 端点格式可能随版本变化

Sources:
1. https://opentelemetry.io/ — OpenTelemetry
2. https://langfuse.com/docs/observability/overview — Langfuse
3. https://grafana.com/ — Grafana
4. https://prometheus.io/ — Prometheus
5. https://docs.vllm.ai/ — vLLM
