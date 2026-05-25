# T1402 ai-gateway Codex Task Pack

## Task ID: T1402
## Title: ai-gateway Codex Task Pack
## Owner: MINIMAX
## Status: READY

## Objective

基于 accepted `T1002 / T1102 / T1202 / T1302 / T302 / T812` 等资产，为 `ai-gateway` 生成第一批 Codex 实现任务卡。

## Produce

1. `tasks/review-pending/T1402-gateway-task-pack-manifest-v1.md`
2. `tasks/review-pending/T1402-gateway-task-order-v1.md`
3. `tasks/review-pending/T1402-gateway-task-cards-v1.md`
4. `tasks/review-pending/T1402-gateway-codex-handoff-v1.md`

## Requirements

- 首批任务卡至少覆盖 G1/G4 与后续 G2 的切换关系
- auth、health/metrics、route/proxy 的边界要写清楚

## Guardrails

- 不改端口、端点、错误口径
- 不扩 MVP 范围
- 不写自然周计划
