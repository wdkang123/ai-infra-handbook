# T1202 ai-gateway Implementation Map Pack

## Task ID: T1202
## Title: ai-gateway Implementation Map Pack
## Owner: MINIMAX
## Status: READY

## Objective

基于 accepted 的 `T1002 / T1102 / T302 / T812` 等资产，为 `ai-gateway` 生成 implementation map。

## Produce

1. `tasks/review-pending/T1202-gateway-file-order-v1.md`
2. `tasks/review-pending/T1202-gateway-import-map-v1.md`
3. `tasks/review-pending/T1202-gateway-patch-split-v1.md`
4. `tasks/review-pending/T1202-gateway-validation-matrix-v1.md`
5. `tasks/review-pending/T1202-gateway-risk-checklist-v1.md`

## Requirements

- 覆盖 `auth.py / config.py / main.py / server.py / tests/conftest.py / tests/test_proxy.py`
- validation matrix 至少覆盖 auth 401、route 404、rate limit 429、proxy 200
- patch split 要能支撑按中间件 / 路由 / 错误处理分步实现
