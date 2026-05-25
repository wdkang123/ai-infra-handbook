# Task Card

Task ID: T812
Title: ai-gateway API Contract Tighten
Owner: MINIMAX
Type: REVISION-单文件收紧
Priority: P1

## Input

基于：
- `tasks/review/T802-review.md`
- `tasks/review-pending/T802-ai-gateway-api-contract-v1.md`

## Expected Output

产出以下 1 个文件：

1. `tasks/review-pending/T812-ai-gateway-api-contract-v1-revised.md`

## Revision Goal

- 把 `/v1/completions`、`/v1/models` 从 `MVP 必须` 降级
- 保持 gateway 最小 MVP 聚焦聊天代理主链路

## Acceptance Criteria

- 只修最小问题
- 不重写整份 contract
