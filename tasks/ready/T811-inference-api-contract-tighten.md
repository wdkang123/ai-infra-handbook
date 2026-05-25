# Task Card

Task ID: T811
Title: inference-service API Contract Tighten
Owner: MINIMAX
Type: REVISION-单文件收紧
Priority: P1

## Input

基于：
- `tasks/review/T801-review.md`
- `tasks/review-pending/T801-inference-service-api-contract-v1.md`

## Expected Output

产出以下 1 个文件：

1. `tasks/review-pending/T811-inference-service-api-contract-v1-revised.md`

## Revision Goal

- 把 `/v1/completions`、`/v1/models` 从 `MVP 必须` 降级
- 保持最小 MVP 主线聚焦在 `/v1/chat/completions`、`/health`、`/metrics`

## Acceptance Criteria

- 只修最小问题
- 不重写整份 contract
