# T1313 eval-module Execution Slice Pack Revision

## Task ID: T1313
## Title: eval-module Execution Slice Pack Revision
## Owner: MINIMAX
## Status: READY

## Read First

- `tasks/review/T1303-review.md`

## Scope

直接就地修订以下文件，不新增平行文件：

1. `tasks/review-pending/T1303-eval-slice-contracts-v1.md`
2. `tasks/review-pending/T1303-eval-first-codex-batch-v1.md`

## Required Changes

1. 把 `LmEvalRunner` 的实例化和 `EvalResult` 的使用统一回 accepted `T1003` 蓝图口径
2. 把 `ResultStore` 示例从普通 dict 口径收回到 accepted 契约

## Guardrails

- 只修 review note 指定问题
- 不重写整包
- 完成后列出实际修改过的绝对路径
