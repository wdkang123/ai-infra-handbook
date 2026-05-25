# Review Note

Task ID: T802
Task Title: ai-gateway Execution Prep Pack
Reviewer: CODEX
Status: REVISE_REQUIRED

## Findings

1. `tasks/review-pending/T802-ai-gateway-api-contract-v1.md`
   - 和 T801 一样，这里把 `/v1/completions`、`/v1/models` 都直接标成了 `MVP 必须`。
   - 但当前最小链路的目标还是先跑通聊天代理，不应在实施前准备阶段把 gateway MVP 面扩得比已有任务边界更大。

## Revision Scope

- 只修 `T802-ai-gateway-api-contract-v1.md`
- 把 `/v1/completions`、`/v1/models` 降级成“可选 / 后续扩展 / 提案接口”
- 不重写整包其他文件
