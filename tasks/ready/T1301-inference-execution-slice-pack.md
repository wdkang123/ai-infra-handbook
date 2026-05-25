# T1301 inference-service Execution Slice Pack

## Task ID: T1301
## Title: inference-service Execution Slice Pack
## Owner: MINIMAX
## Status: READY

## Objective

基于 accepted `T1001 / T1101 / T1201 / T301 / T811` 等资产，为 `inference-service` 生成可直接服务 Codex 编码的 execution slices。

## Produce

1. `tasks/review-pending/T1301-inference-slice-manifest-v1.md`
2. `tasks/review-pending/T1301-inference-slice-order-v1.md`
3. `tasks/review-pending/T1301-inference-slice-contracts-v1.md`
4. `tasks/review-pending/T1301-inference-first-codex-batch-v1.md`

## Requirements

- slice order 要按文件依赖和验证门槛组织
- slice contracts 要写清目标文件、入口、验收命令、完成信号、cut line
- first codex batch 要适合第一轮真实编码

## Guardrails

- 不重写 accepted 文档
- 不扩 MVP 范围
- 不写自然周计划
