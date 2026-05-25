# T1101 inference-service Fixture Pack

## Task ID: T1101
## Title: inference-service Fixture Pack
## Owner: MINIMAX
## Status: READY

## Objective

为 `inference-service` 生成第一批 implementation-ready fixture / sample asset。

## Produce

1. `tasks/review-pending/T1101-inference-request-fixtures-v1.md`
2. `tasks/review-pending/T1101-inference-stream-sse-samples-v1.md`
3. `tasks/review-pending/T1101-inference-metrics-health-samples-v1.md`
4. `tasks/review-pending/T1101-inference-config-example-catalog-v1.md`
5. `tasks/review-pending/T1101-inference-fixture-manifest-v1.md`

## Requirements

- 覆盖 `/health`、`/metrics`、`/v1/chat/completions`
- chat request 至少包含：
  - basic
  - system message
  - streaming
  - stop token
  - invalid model
- SSE 样例要写成连续 chunk 示例
- metrics / health 样例需和已 accepted 的 starter blueprint 契约一致
- config example 要覆盖模型名、端口、vLLM 关键项

## Guardrails

- 只做 fixture / sample asset，不写新章节
- 样例字段尽量具体，避免空泛占位
