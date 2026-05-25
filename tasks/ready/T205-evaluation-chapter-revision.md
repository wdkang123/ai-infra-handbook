# Task Card

Task ID: T205
Title: 收紧 Evaluation 章节初稿中的最小实践与数量型表述
Owner: MINIMAX
Type: C-普通章节任务
Priority: P1

## Input

基于：
- `tasks/review-pending/T195-evaluation-chapter-draft.md`
- `tasks/review/T195-review.md`
- `tasks/accepted/T162-observability-eval-sources-result.md`
- `tasks/accepted/T175-benchmark-sources-result.md`

## Expected Output

对 `T195` 做最小修订版，只修审阅指出的问题，不重写整章。

## Template

使用 MiniMax 标准输出协议。

## Acceptance Criteria

- 最小实践的命令链和文字描述必须一致
- 删除或改弱 `70+`、`50+` 这类数量型表述
- 保持 10 节结构
- 不扩写成 benchmark 手册

## Allowed Sources

- 已通过的 T162 / T175 官方来源
- T195 当前章节草稿

## Out of Scope

- 不重写整章
- 不做 leaderboard 设计
