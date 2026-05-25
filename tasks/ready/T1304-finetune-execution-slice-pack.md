# T1304 finetune-demo Execution Slice Pack

## Task ID: T1304
## Title: finetune-demo Execution Slice Pack
## Owner: MINIMAX
## Status: READY

## Objective

基于 accepted `T1004 / T1104 / T1204 / T304 / T703` 等资产，为 `finetune-demo` 生成 execution slices。

## Produce

1. `tasks/review-pending/T1304-finetune-slice-manifest-v1.md`
2. `tasks/review-pending/T1304-finetune-slice-order-v1.md`
3. `tasks/review-pending/T1304-finetune-slice-contracts-v1.md`
4. `tasks/review-pending/T1304-finetune-first-codex-batch-v1.md`

## Requirements

- 必须覆盖 config、trainer、adapter/export、CLI/script 四条主线
- 命令口径必须与 accepted starter blueprints 一致

## Guardrails

- 不扩训练方法范围
- 不重写 implementation map
- 不写自然周计划
