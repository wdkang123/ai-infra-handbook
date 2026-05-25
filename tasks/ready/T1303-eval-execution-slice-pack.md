# T1303 eval-module Execution Slice Pack

## Task ID: T1303
## Title: eval-module Execution Slice Pack
## Owner: MINIMAX
## Status: READY

## Objective

基于 accepted `T1003 / T1103 / T1203 / T303 / T813` 等资产，为 `eval-module` 生成 execution slices。

## Produce

1. `tasks/review-pending/T1303-eval-slice-manifest-v1.md`
2. `tasks/review-pending/T1303-eval-slice-order-v1.md`
3. `tasks/review-pending/T1303-eval-slice-contracts-v1.md`
4. `tasks/review-pending/T1303-eval-first-codex-batch-v1.md`

## Requirements

- 必须覆盖 CLI、runner、result store/comparison、benchmark script 的切片边界
- `run / compare / list-tasks` 的执行口径必须对齐 accepted 资产

## Guardrails

- 不改 accepted CLI 参数口径
- 不扩 MVP 范围
- 不写自然周计划
