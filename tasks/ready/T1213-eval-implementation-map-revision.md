# T1213 eval-module Implementation Map Revision

## Task ID: T1213
## Title: eval-module Implementation Map Revision
## Owner: MINIMAX
## Status: READY

## Read First

- `tasks/review/T1203-review.md`

## Scope

直接就地修订以下文件，不新增平行文件：

1. `tasks/review-pending/T1203-eval-file-order-v1.md`
2. `tasks/review-pending/T1203-eval-import-map-v1.md`
3. `tasks/review-pending/T1203-eval-patch-split-v1.md`
4. `tasks/review-pending/T1203-eval-validation-matrix-v1.md`
5. `tasks/review-pending/T1203-eval-risk-checklist-v1.md`

## Required Changes

1. 全包对齐 accepted `T1003 / T1103 / T303 / T813`
2. 主执行入口统一写成 `LmEvalRunner.run(...)`
3. `EvalResult` 归属和字段口径回到 accepted runner blueprint
4. 不把额外 results 子包结构升级成默认 MVP 主路径

## Guardrails

- 只修 review note 指定问题
- 不重写整包
- 完成后列出实际修改过的绝对路径
