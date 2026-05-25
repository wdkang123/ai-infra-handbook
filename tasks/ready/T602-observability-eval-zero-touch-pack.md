# Task Card

Task ID: T602
Title: Observability / Evaluation Zero-Touch Pack
Owner: MINIMAX
Type: PACK-0接管链式专题包
Priority: P1

## Input

基于：
- `tasks/accepted/T162-observability-eval-sources-result.md`
- `tasks/accepted/T204-observability-chapter-revision.md`
- `tasks/accepted/T205-evaluation-chapter-revision.md`
- `tasks/accepted/T306-benchmark-eval-sources-index-v1.md`
- `tasks/accepted/T307-observability-sources-index-v1.md`
- `tasks/accepted/T309-eval-benchmark-comparison-index-tighten.md`
- `tasks/accepted/T310-observability-comparison-index-v1.md`
- `tasks/accepted/T312-benchmark-leaderboard-chapter-revision.md`
- `tasks/accepted/T316-observability-eval-comparison-index-v2.md`
- `tasks/review-pending/T601-inference-integration-map-v1.md`
- `tasks/review-pending/T601-inference-stack-decision-memo-v1.md`

## Expected Output

本专题包必须产出以下 7 个文件：

1. `tasks/review-pending/T602-observability-eval-pack-manifest.md`
2. `tasks/review-pending/T602-observability-sources-index-v3.md`
3. `tasks/review-pending/T602-eval-benchmark-sources-index-v4.md`
4. `tasks/review-pending/T602-observability-eval-comparison-index-v3.md`
5. `tasks/review-pending/T602-observability-practice-catalog-v3.md`
6. `tasks/review-pending/T602-eval-benchmark-practice-catalog-v2.md`
7. `tasks/review-pending/T602-observability-eval-decision-memo-v1.md`

## Deliverable Notes

### sources-index-v3 / v4

继续收紧 observability、evaluation、benchmark、leaderboard、arena 的边界和稳定入口。

### comparison-index-v3

重点比较：
- Langfuse
- Phoenix
- Grafana / Prometheus
- LM-Eval
- HELM
- BigCode Eval

只做索引级比较，不做营销式评分。

### practice-catalog-v3 / v2

合计整理 10 到 12 个低门槛实践：
- tracing / prompt logging
- metrics dashboard
- 离线评测
- benchmark 对照
- arena 观察

### decision-memo-v1

围绕以下问题给出资料级输入：
- 默认 observability 起步组合应该是什么
- evaluation 与 benchmark 在项目里的职责分工
- 哪些内容适合进入 eval-module MVP，哪些不适合

### manifest

总结完成项、未定项、对下一包可复用的输入。

## Template

使用 MiniMax 标准输出协议。

## Acceptance Criteria

- 必须写满 7 个输出文件
- 全部围绕 observability / evaluation 主线
- 所有重点链接必须是精确 URL
- 不扩写成完整平台产品白皮书

## Out of Scope

- 不写代码实现
