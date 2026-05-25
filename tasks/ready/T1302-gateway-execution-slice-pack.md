# T1302 ai-gateway Execution Slice Pack

## Task ID: T1302
## Title: ai-gateway Execution Slice Pack
## Owner: MINIMAX
## Status: READY

## Objective

基于 accepted `T1002 / T1102 / T1202 / T302 / T812` 等资产，为 `ai-gateway` 生成 execution slices。

## Produce

1. `tasks/review-pending/T1302-gateway-slice-manifest-v1.md`
2. `tasks/review-pending/T1302-gateway-slice-order-v1.md`
3. `tasks/review-pending/T1302-gateway-slice-contracts-v1.md`
4. `tasks/review-pending/T1302-gateway-first-codex-batch-v1.md`

## Requirements

- 必须覆盖 auth、route/proxy、rate limit、health/metrics 四条主线
- slice contracts 要和 accepted gateway assets 完全对齐

## Guardrails

- 不改 accepted 端口、端点、错误口径
- 不扩 MVP 范围
- 不写自然周计划
