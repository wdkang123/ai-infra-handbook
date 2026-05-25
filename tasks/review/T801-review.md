# Review Note

Task ID: T801
Task Title: inference-service Execution Prep Pack
Reviewer: CODEX
Status: REVISE_REQUIRED

## Findings

1. `tasks/review-pending/T801-inference-service-api-contract-v1.md`
   - 本文件把 `/v1/completions` 和 `/v1/models` 直接标成了 `MVP 必须`，但当前已通过的任务拆解里，MVP 只明确要求 `OpenAI 兼容 API` 里的 `/v1/chat/completions`、`/health`、`/metrics` 这些最小链路。
   - 现在这样写会无形中扩大 inference-service 的 MVP 实现面，增加后续实现成本。

## Revision Scope

- 只修 `T801-inference-service-api-contract-v1.md`
- 把 `/v1/completions`、`/v1/models` 降级成“可选 / 后续扩展 / 提案接口”
- 不重写整包其他文件
