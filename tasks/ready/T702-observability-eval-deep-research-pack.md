# Task Card

Task ID: T702
Title: Observability / Evaluation Deep-Research Pack
Owner: MINIMAX
Type: PACK-深研究0接管专题包
Priority: P1

## Input

基于：
- `tasks/accepted/T204-observability-chapter-revision.md`
- `tasks/accepted/T205-evaluation-chapter-revision.md`
- `tasks/accepted/T306-benchmark-eval-sources-index-v1.md`
- `tasks/accepted/T307-observability-sources-index-v1.md`
- `tasks/accepted/T309-eval-benchmark-comparison-index-tighten.md`
- `tasks/accepted/T310-observability-comparison-index-v1.md`
- `tasks/accepted/T312-benchmark-leaderboard-chapter-revision.md`
- `tasks/accepted/T316-observability-eval-comparison-index-v2.md`
- `tasks/review-pending/T602-observability-sources-index-v3.md`
- `tasks/review-pending/T602-eval-benchmark-sources-index-v4.md`
- `tasks/review-pending/T602-observability-eval-decision-memo-v1.md`

## Expected Output

本专题包必须产出以下 8 个文件：

1. `tasks/review-pending/T702-observability-eval-pack-manifest.md`
2. `tasks/review-pending/T702-observability-sources-index-v4.md`
3. `tasks/review-pending/T702-eval-benchmark-sources-index-v5.md`
4. `tasks/review-pending/T702-observability-boundary-matrix-v1.md`
5. `tasks/review-pending/T702-eval-benchmark-boundary-matrix-v1.md`
6. `tasks/review-pending/T702-observability-practice-catalog-v4.md`
7. `tasks/review-pending/T702-eval-tooling-timeline-v1.md`
8. `tasks/review-pending/T702-observability-eval-decision-memo-v2.md`

## Deliverable Notes

### sources-index-v4 / v5

继续收紧 observability、evaluation、benchmark、leaderboard、arena 的入口与边界。

### boundary-matrix

分别澄清：
- tracing / metrics / monitoring / prompt observability
- evaluation / benchmark / leaderboard / arena

### practice-catalog-v4

补到 10 到 12 个实践条目，兼顾 tracing、metrics、offline eval、benchmark 对照。

### eval-tooling-timeline-v1

梳理 LM-Eval / HELM / BigCode Eval 的稳定入口与更新线索。

### decision-memo-v2

围绕默认 observability 起步组合、eval-module 边界、哪些内容不该进入 MVP，做资料级收紧。

### manifest

总结本包升级了什么、未定项和对下一包可复用输入。

## Template

使用 MiniMax 标准输出协议。

## Acceptance Criteria

- 必须写满 8 个输出文件
- 全部围绕 observability / evaluation 主线
- 所有重点链接必须是精确 URL
- 不扩写成完整产品方案

## Out of Scope

- 不写代码实现
