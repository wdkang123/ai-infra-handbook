# T1315 Root Integration Execution Slice Pack Revision

## Task ID: T1315
## Title: Root Integration Execution Slice Pack Revision
## Owner: MINIMAX
## Status: READY

## Read First

- `tasks/review/T1305-review.md`

## Scope

直接就地修订以下文件，不新增平行文件：

1. `tasks/review-pending/T1305-root-slice-manifest-v1.md`
2. `tasks/review-pending/T1305-root-slice-contracts-v1.md`
3. `tasks/review-pending/T1305-root-codex-integration-batch-v1.md`

## Required Changes

1. handoff 文档路径与命名统一回 accepted 根级资产
2. gateway metrics 统一回 `ai_gateway_` 口径
3. root smoke 的前置条件与真实代理链路保持一致

## Guardrails

- 只修 review note 指定问题
- 不重写整包
- 完成后列出实际修改过的绝对路径
