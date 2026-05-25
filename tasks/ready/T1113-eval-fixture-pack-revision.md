# T1113 eval-module Fixture Pack Revision

## Task ID: T1113
## Title: eval-module Fixture Pack Revision
## Owner: MINIMAX
## Status: READY

## Read First

- `tasks/review/T1103-review.md`

## Scope

直接就地修订以下文件，不新增平行文件：

1. `tasks/review-pending/T1103-eval-fixture-manifest-v1.md`
2. `tasks/review-pending/T1103-eval-cli-example-catalog-v1.md`
3. `tasks/review-pending/T1103-eval-result-json-samples-v1.md`
4. `tasks/review-pending/T1103-eval-compare-report-samples-v1.md`

## Required Changes

1. 把 CLI 入口、命令集合、`compare` 参数改回 accepted `T1003` blueprint 契约
2. 把结果 JSON / compare report schema 改回 accepted `EvalResult` 口径

## Guardrails

- 只修 review note 指定问题
- 不重写整包
- 完成后列出实际修改过的绝对路径
