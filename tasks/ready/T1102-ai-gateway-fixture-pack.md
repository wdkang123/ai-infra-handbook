# T1102 ai-gateway Fixture Pack

## Task ID: T1102
## Title: ai-gateway Fixture Pack
## Owner: MINIMAX
## Status: READY

## Objective

为 `ai-gateway` 生成第一批 implementation-ready fixture / sample asset。

## Produce

1. `tasks/review-pending/T1102-gateway-auth-request-fixtures-v1.md`
2. `tasks/review-pending/T1102-gateway-routing-config-samples-v1.md`
3. `tasks/review-pending/T1102-gateway-error-response-samples-v1.md`
4. `tasks/review-pending/T1102-gateway-proxy-response-samples-v1.md`
5. `tasks/review-pending/T1102-gateway-fixture-manifest-v1.md`

## Requirements

- 鉴权 fixture 至少覆盖：
  - valid bearer
  - missing auth
  - wrong auth scheme
  - invalid key
- routing config 至少覆盖一个 `vllm-local -> http://localhost:8000/v1`
- error response 样例覆盖 401 / 404 / 429
- proxy response 样例要和 inference-service chat completion 结构对齐

## Guardrails

- 只做 fixture / sample asset，不写新章节
- 不引入多租户 / 成本计费 / 非 MVP 内容
