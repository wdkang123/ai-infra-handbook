# T1203 eval-module Implementation Map Pack

## Task ID: T1203
## Title: eval-module Implementation Map Pack
## Owner: MINIMAX
## Status: READY

## Objective

基于 accepted 的 `T1003 / T1103 / T303 / T813` 等资产，为 `eval-module` 生成 implementation map。

## Produce

1. `tasks/review-pending/T1203-eval-file-order-v1.md`
2. `tasks/review-pending/T1203-eval-import-map-v1.md`
3. `tasks/review-pending/T1203-eval-patch-split-v1.md`
4. `tasks/review-pending/T1203-eval-validation-matrix-v1.md`
5. `tasks/review-pending/T1203-eval-risk-checklist-v1.md`

## Requirements

- 覆盖 `main.py / runners/lm_eval_runner.py / results/result_store.py / tests/conftest.py / tests/test_runner.py / scripts/run_benchmark.sh`
- validation matrix 至少覆盖 `run / compare / list-tasks`
- patch split 要体现 CLI、runner、result store 的最小实现顺序
