# T1133 eval Backend And CLI Fix

## Task ID: T1133
## Title: eval Backend And CLI Fix
## Owner: MINIMAX
## Status: READY

## Read First

- `tasks/review/T1123-review-round-3.md`

## Scope

直接就地修订：

1. `tasks/review-pending/T1103-eval-result-json-samples-v1.md`
2. `tasks/review-pending/T1103-eval-compare-report-samples-v1.md`
3. `tasks/review-pending/T1103-eval-cli-example-catalog-v1.md`

## Required Changes

- 把 `backend` 从 URL 改成 accepted `EvalResult` 口径
- 修复完整工作流示例中 `compare` 命令的 shell 续行

## Guardrails

- 不新增文件
- 不重写整包
- 完成后列出实际修改过的绝对路径
