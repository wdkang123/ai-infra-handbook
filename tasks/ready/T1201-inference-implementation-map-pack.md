# T1201 inference-service Implementation Map Pack

## Task ID: T1201
## Title: inference-service Implementation Map Pack
## Owner: MINIMAX
## Status: READY

## Objective

基于 accepted 的 `T1001 / T1101 / T301 / T811` 等资产，为 `inference-service` 生成可直接服务编码的 implementation map。

## Produce

1. `tasks/review-pending/T1201-inference-file-order-v1.md`
2. `tasks/review-pending/T1201-inference-import-map-v1.md`
3. `tasks/review-pending/T1201-inference-patch-split-v1.md`
4. `tasks/review-pending/T1201-inference-validation-matrix-v1.md`
5. `tasks/review-pending/T1201-inference-risk-checklist-v1.md`

## Requirements

- file order 至少覆盖 `config.py / main.py / server.py / tests/conftest.py / tests/test_api.py / scripts/serve.sh`
- import map 要体现 `main.py -> config.py -> server.py` 等依赖方向
- patch split 要适合 Codex 分批实现
- validation matrix 要覆盖 `/health /metrics /v1/chat/completions`

## Guardrails

- 不重写 accepted blueprint
- 不写自然周计划
