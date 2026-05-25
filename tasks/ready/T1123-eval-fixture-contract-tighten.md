# T1123 eval-module Fixture Contract Tighten

## Task ID: T1123
## Title: eval-module Fixture Contract Tighten
## Owner: MINIMAX
## Status: READY

## Read First

- `tasks/review/T1113-review-round-2.md`

## Scope

直接就地修订以下文件：

1. `tasks/review-pending/T1103-eval-result-json-samples-v1.md`
2. `tasks/review-pending/T1103-eval-compare-report-samples-v1.md`
3. `tasks/review-pending/T1103-eval-cli-example-catalog-v1.md`

## Required Changes

- 把 `backend` 字段统一改回 accepted `EvalResult` 的口径
- 修好 `compare` 示例命令的 shell 续行

## Guardrails

- 不重写整包
- 不新增文件
- 完成后列出实际修改过的绝对路径
