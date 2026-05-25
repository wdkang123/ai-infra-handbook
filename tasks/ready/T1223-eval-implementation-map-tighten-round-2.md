# T1223 eval-module Implementation Map Tighten Round 2

## Task ID: T1223
## Title: eval-module Implementation Map Tighten Round 2
## Owner: MINIMAX
## Status: READY

## Read First

- `tasks/review/T1213-review-round-2.md`

## Scope

直接就地修订以下文件，不新增平行文件：

1. `tasks/review-pending/T1203-eval-import-map-v1.md`
2. `tasks/review-pending/T1203-eval-risk-checklist-v1.md`

## Required Changes

1. 去掉 `eval_result.py` 残留描述
2. 把 `runner.evaluate()` 统一改回 accepted 口径的 `run(...)`

## Guardrails

- 只修 review note 指定问题
- 不重写整包
- 完成后列出实际修改过的绝对路径
