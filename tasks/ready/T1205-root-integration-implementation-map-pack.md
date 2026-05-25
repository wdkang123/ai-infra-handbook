# T1205 Root Integration Implementation Map Pack

## Task ID: T1205
## Title: Root Integration Implementation Map Pack
## Owner: MINIMAX
## Status: READY

## Objective

基于 accepted 的 `T1005 / T1105 / T805` 等资产，为根级联调流程生成 implementation map。

## Produce

1. `tasks/review-pending/T1205-root-file-order-v1.md`
2. `tasks/review-pending/T1205-root-script-dependency-map-v1.md`
3. `tasks/review-pending/T1205-root-patch-split-v1.md`
4. `tasks/review-pending/T1205-root-validation-matrix-v1.md`
5. `tasks/review-pending/T1205-root-risk-checklist-v1.md`

## Requirements

- 覆盖 `Makefile / scripts/local_dev_sequence.sh / scripts/integration_smoke_test.sh / .env.example / BLOCKERS.md`
- validation matrix 至少覆盖 all-serve、infra-smoke、all-stop
- script dependency map 要体现根级脚本与四个子项目的调用关系
