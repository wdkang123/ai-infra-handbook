# Task Card

Task ID: T501
Title: Observability Long-Run Pack v2
Owner: MINIMAX
Type: PACK-长跑专题包
Priority: P1

## Input

基于：
- `tasks/accepted/T401-observability-project-map-v1.md`
- `tasks/accepted/T401-observability-practice-catalog-v1.md`
- `tasks/accepted/T401-observability-sources-index-v2.md`
- `tasks/accepted/T310-observability-comparison-index-v1.md`
- `tasks/accepted/T316-observability-eval-comparison-index-v2.md`

## Expected Output

本专题包必须产出以下 5 个文件：

1. `tasks/review-pending/T501-observability-pack-manifest-v2.md`
2. `tasks/review-pending/T501-observability-decision-memo-v1.md`
3. `tasks/review-pending/T501-observability-comparison-index-v2.md`
4. `tasks/review-pending/T501-observability-practice-catalog-v2.md`
5. `tasks/review-pending/T501-observability-integration-notes-v1.md`

## Deliverable Notes

### decision-memo

围绕以下问题给出“资料级决策输入”，不下最终结论：
- OTel 是否应作为默认采集层
- Langfuse / Phoenix / Grafana-Prometheus 各自适合什么位置

### comparison-index-v2

把 observability 工具比较拉得更完整，但仍保持索引风格。

### practice-catalog-v2

在 v1 基础上补更多“从单机到多组件”的最小实践。

### integration-notes-v1

说明 observability 如何映射到：
- inference-service
- ai-gateway
- eval-module

### manifest

总结本包用途、完成项、未定项。

## Template

使用 MiniMax 标准输出协议。

## Acceptance Criteria

- 必须写满 5 个输出文件
- 全部围绕 observability 主线
- 所有重点链接必须是精确 URL
- 不输出最终架构结论

## Allowed Sources

- 已通过的 observability 相关资产

## Out of Scope

- 不写代码实现
