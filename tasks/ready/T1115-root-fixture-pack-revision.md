# T1115 Root Integration Fixture Pack Revision

## Task ID: T1115
## Title: Root Integration Fixture Pack Revision
## Owner: MINIMAX
## Status: READY

## Read First

- `tasks/review/T1105-review.md`

## Scope

直接就地修订以下文件，不新增平行文件：

1. `tasks/review-pending/T1105-root-smoke-expected-output-v1.md`
2. 如有必要，可同步修订 `tasks/review-pending/T1105-root-fixture-manifest-v1.md`

## Required Changes

1. 把 IT-06 unknown model 的错误码改成与 accepted gateway blueprint 一致
2. 若 manifest 中引用了旧口径，一并对齐

## Guardrails

- 只修 review note 指定问题
- 不重写整包
- 完成后列出实际修改过的绝对路径
