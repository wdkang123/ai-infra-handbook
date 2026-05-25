Task ID: T602
Task Title: Observability / Evaluation Zero-Touch Pack
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
T602 Observability/Evaluation Zero-Touch Pack 收口 manifest。

Result:

# Observability / Evaluation Zero-Touch Pack Manifest

## 包概述

本包为 Observability / Evaluation 专题的 0 接管链式长跑包，7 个文件全部完成，围绕可观测性和评测的选型、实践路径、决策输入展开。

## 已完成交付物

### 1. T602-observability-sources-index-v3
OpenTelemetry / Langfuse / Phoenix / Grafana-Prometheus 的稳定入口与边界说明。

### 2. T602-eval-benchmark-sources-index-v4
Evaluation / Benchmark / Leaderboard / Arena 的边界收紧与稳定入口，数据集和评测框架来源。

### 3. T602-observability-eval-comparison-index-v3
6 个对象的定位/层级/场景/与本项目关系比较，Langfuse/Phoenix/Grafana-Prometheus/LM-Eval/HELM/BigCode Eval。

### 4. T602-observability-practice-catalog-v3
6 个可观测性实践（O01-O06）+ 6 个评测实践（E01-E06），合计 12 个低门槛实践。

### 5. T602-eval-benchmark-practice-catalog-v2
11 个评测实践（B01-B11），覆盖数据集选择、评测执行、结果分析、Leaderboard/Arena 观察。

### 6. T602-observability-eval-decision-memo-v1
三个决策点的资料级输入：默认 observability 起步组合、evaluation 与 benchmark 职责分工、eval-module MVP 边界。

### 7. T602-observability-eval-pack-manifest
本文件，总结完成项、未定项、对下一包可复用输入。

## 各交付物关系

```
sources-index-v3 / v4（入口 + 边界）
    ↓
comparison-index-v3（工具选型比较）
    ↓
practice-catalog-v3 / v2（12 + 11 个实践）
    ↓
decision-memo-v1（决策输入）
    ↓
manifest（本文件）
```

## 对下一包可复用的输入

### 供 T603（Finetuning/Training）使用
- Langfuse 作为训练 metrics 上报工具
- eval-module 的评测结果可关联训练效果验证
- lm-eval 作为 finetune 后效果验证的工具

### 供 T604（Cross-Project Systemization）使用
- T602-observability-eval-decision-memo-v1 的决策输入
- eval-module MVP 边界（评测执行 + 结果 JSON，暂不上报）
- observability 起步组合建议

## 需要 Codex 最终判断的点

1. **Langfuse self-hosted 是否 MVP 必须**？
2. **Prometheus + Grafana 是否 MVP 引入**？
3. **LLM-as-Judge 是否 MVP 包含**？
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
