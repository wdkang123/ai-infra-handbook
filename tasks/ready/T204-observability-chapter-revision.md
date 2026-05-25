# Task Card

Task ID: T204
Title: 收紧 Observability 章节初稿中的指标来源和最小实践
Owner: MINIMAX
Type: C-普通章节任务
Priority: P1

## Input

基于：
- `tasks/review-pending/T194-observability-chapter-draft.md`
- `tasks/review/T194-review.md`
- `tasks/accepted/T162-observability-eval-sources-result.md`

## Expected Output

对 `T194` 做最小修订版，只修审阅指出的问题，不重写整章。

## Template

使用 MiniMax 标准输出协议。

## Acceptance Criteria

- 第 5 节只保留来源明确、适合 observability 章节的核心指标
- 最小实践与输出物只承诺 trace / log / token usage 这类当前示例能支撑的内容
- 延伸阅读以 observability 为主，evaluation 只保留轻量边界引用
- 保持 10 节结构

## Allowed Sources

- 已通过的 T162 官方来源
- T194 当前章节草稿

## Out of Scope

- 不重写整章
- 不扩写成 evaluation 章节
