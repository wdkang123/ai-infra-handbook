Task ID: T702
Task Title: Observability / Evaluation Deep-Research Pack
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
T702 Observability / Evaluation Deep-Research Pack 收口 manifest。

Result:

# Observability / Evaluation Deep-Research Pack Manifest

## 包概述

本包为 Observability / Evaluation 专题的深研究 0 接管包，8 个文件全部完成，围绕可观测性和评测的边界澄清、工具时间线、决策输入展开。

## 已完成交付物

### 1. T702-observability-sources-index-v4
在 v3 基础上补全了官方 release/changelog/blog 入口。

### 2. T702-eval-benchmark-sources-index-v5
继续收紧 evaluation/benchmark/leaderboard/arena 的边界，补全官方入口。

### 3. T702-observability-boundary-matrix-v1
澄清四个边界：Tracing vs Metrics vs Monitoring、Prompt Observability、Langfuse vs Phoenix vs Grafana、OTel vs 工具实现。

### 4. T702-eval-benchmark-boundary-matrix-v1
澄清五个边界：Evaluation vs Benchmark、Benchmark vs Leaderboard、Leaderboard vs Arena、LM-Eval vs HELM vs BigCode Eval、eval-module 与评测框架的关系。

### 5. T702-observability-practice-catalog-v4
13 个实践条目（O01-O07 tracing/metrics + E01-E06 offline eval/benchmark），覆盖 tracing、metrics、offline eval、benchmark 对照。

### 6. T702-eval-tooling-timeline-v1
LM-Eval / HELM / BigCode Eval 的关键更新线索、稳定入口、版本选择建议。

### 7. T702-observability-eval-decision-memo-v2
在 v1 基础上收紧四个决策点：默认起步组合、eval vs benchmark 分工、eval-module MVP 边界、Langfuse self-hosted vs cloud。

### 8. T702-observability-eval-pack-manifest
本文件，总结本包升级了什么、未定项、对下一包可复用输入。

## 本包升级了什么（相比 v3）

| 维度 | v3 | v4（收紧） |
|------|-----|-----------|
| Sources | 官方文档链接 | 补全 release/changelog 入口 |
| Boundaries | 基本对比 | 细化到 5 类边界澄清 |
| Timeline | 部分 | 新增 eval-tooling-timeline |
| Decision | 3 个决策点 | 收紧为 4 个，新增 self-hosted vs cloud |
| Practices | 12 个 | 增加到 13 个 |

## 对下一包可复用的输入

### 供 T703（Finetuning/Training）使用
- Langfuse 作为训练 metrics 上报工具（已明确 Cloud vs self-hosted）
- eval-module 的评测结果可关联训练效果验证

### 供 T704（Cross-Project）使用
- T702-observability-eval-decision-memo-v2 的决策输入
- eval-module MVP 边界（评测执行 + 结果 JSON，暂不上报）

## 需要 Codex 最终判断的点

1. **Langfuse Cloud 是否在 MVP 必须**？还是 self-hosted 可接受？
2. **Prometheus + Grafana 是否在 MVP 引入**？
3. **LLM-as-Judge 是否在 MVP 包含**？
4. **eval-module 结果是否上报 Langfuse**？

## 风险与依赖

- Langfuse SDK 更新快，具体 API 以实际安装版本为准
- lm-eval 版本更新可能影响 API 兼容性
- OTel 日志（Logs）信号仍为草案，生产使用需确认版本

Sources:
1. https://langfuse.com/docs/observability/overview — Langfuse
2. https://opentelemetry.io/ — OpenTelemetry
3. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval
4. https://grafana.com/ — Grafana
5. https://prometheus.io/ — Prometheus
