# Task Card

Task ID: T502
Title: Evaluation / Benchmark Long-Run Pack v2
Owner: MINIMAX
Type: PACK-长跑专题包
Priority: P1

## Input

基于：
- `tasks/accepted/T205-evaluation-chapter-revision.md`
- `tasks/accepted/T309-eval-benchmark-comparison-index-tighten.md`
- `tasks/accepted/T312-benchmark-leaderboard-chapter-revision.md`
- `tasks/accepted/T306-benchmark-eval-sources-index-v1.md`
- `tasks/review/T402-review.md`

## Expected Output

本专题包必须产出以下 5 个文件：

1. `tasks/review-pending/T502-eval-benchmark-pack-manifest-v2.md`
2. `tasks/review-pending/T502-eval-benchmark-sources-index-v3.md`
3. `tasks/review-pending/T502-benchmark-dataset-map-v1.md`
4. `tasks/review-pending/T502-eval-tool-selection-notes-v1.md`
5. `tasks/review-pending/T502-benchmark-practice-catalog-v1.md`

## Deliverable Notes

### sources-index-v3

在 v2 基础上进一步收紧 evaluation / benchmark / leaderboard / arena 的边界与入口。

### benchmark-dataset-map-v1

整理：
- MMLU
- GSM8K
- HumanEval
- MBPP
- Arena / Elo

与工具、指标之间的关系。

### eval-tool-selection-notes-v1

比较 LM-Eval / HELM / BigCode Eval，给出“工程输入级说明”，不下最终结论。

### benchmark-practice-catalog-v1

整理 6 到 8 个低门槛实践：
- lm-eval
- leaderboard 对照
- arena 观察
- dataset entry

### manifest

总结本包完成项、未定项、需要 Codex 判断的点。

## Template

使用 MiniMax 标准输出协议。

## Acceptance Criteria

- 必须写满 5 个输出文件
- 全部围绕 evaluation / benchmark 主线
- 所有重点链接必须是精确 URL
- 不扩写成完整评测手册

## Allowed Sources

- 已通过的 evaluation / benchmark 相关资产

## Out of Scope

- 不写代码实现
- 不做榜单评论文章
