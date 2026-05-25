# T1305 Root Integration Execution Slice Pack

## Task ID: T1305
## Title: Root Integration Execution Slice Pack
## Owner: MINIMAX
## Status: READY

## Objective

基于 accepted `T1005 / T1105 / T1205 / T805` 等资产，为根级联调流程生成 execution slices。

## Produce

1. `tasks/review-pending/T1305-root-slice-manifest-v1.md`
2. `tasks/review-pending/T1305-root-slice-order-v1.md`
3. `tasks/review-pending/T1305-root-slice-contracts-v1.md`
4. `tasks/review-pending/T1305-root-codex-integration-batch-v1.md`

## Requirements

- 必须覆盖 Makefile、local dev、smoke test、cross-project handoff
- 端口、端点、服务顺序必须与 accepted root assets 一致

## Guardrails

- 不再新增根级 helper scripts 主线
- 不改 accepted Makefile 调用方式
- 不写自然周计划
