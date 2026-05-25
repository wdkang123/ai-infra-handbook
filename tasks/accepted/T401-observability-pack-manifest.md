Task ID: T401
Task Title: Observability Long-Run Pack v1
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
Observability Long-Run Pack，基于 T204/T307/T310/T313/T301/T302/T303，产出4个文件：manifest、project-map、practice-catalog、sources-index v2。

Result:

# Observability Long-Run Pack Manifest

## 包概述

本包围绕 **LLM Observability** 主题，产出 4 个互相独立的交付物，共同构成 observability 资产的完整拼图。

## 已完成交付物

### 1. T401-observability-pack-manifest
本文件。总结本包交付物清单和用途。

### 2. T401-observability-project-map-v1
说明 observability 在 inference-service、ai-gateway、eval-module 三个模块中的落点与边界。

**用途**：帮助理解 observability 不是独立模块，而是横向能力渗透在各模块中。

### 3. T401-observability-practice-catalog-v1
整理 8 个低门槛最小实践入口，覆盖 tracing、metrics、token usage、dashboard、request logging。

**用途**：为开发者提供从零到第一个可观测数据的快速路径。

### 4. T401-observability-sources-index-v2
在 v1 基础上收紧优先阅读链接，增加更稳定的精确 URL。

**用途**：作为 observability 工具选型和深入学习的入口索引。

## 各交付物关系

```
project-map（模块落点）
    ↓
practice-catalog（最小实践）
    ↓
sources-index v2（工具索引）
    ↓
manifest（本文件）
```

## 需要 Codex 判断的点

1. **inference-service 的 metrics 接口形式**：当前描述为 Prometheus 端点，是否需要同时支持 OpenTelemetry？
2. **ai-gateway 是否内置 tracing**：当前 project-map 假设 tracing 由 ai-gateway 透传，是否准确？
3. **eval-module 的评测结果是否上报 Langfuse**：当前 project-map 假设是，实际设计中是否需要这个集成？
4. **Langfuse 是否作为默认推荐工具**：当前 practice-catalog 以 Langfuse 为默认 tracing 工具，是否需要保留备选？

## 与其他包的关系

- **T402（Eval/Benchmark Pack）**：observability 和 evaluation 在 tracing/eval 协作点相交
- **T403（Finetuning Pack）**：finetuning 的训练监控可复用 observability 能力，但 finetune-demo 本身不在 observability 主线内

## 风险与依赖

- Langfuse 等工具更新频繁，具体 API 以实际安装版本为准
- OpenTelemetry 为 CNCF 标准，稳定性较高
- 本包交付物均为"参考说明"类，不包含代码实现

Sources:
1. https://langfuse.com/docs/observability/overview — Langfuse 可观测性文档
2. https://opentelemetry.io/ — OpenTelemetry 官网
3. https://grafana.com/ — Grafana 官网
4. https://docs.vllm.ai/ — vLLM 指标文档
5. https://github.com/Arize-AI/phoenix — Phoenix 主仓库
