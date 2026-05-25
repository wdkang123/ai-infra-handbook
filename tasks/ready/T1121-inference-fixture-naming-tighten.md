# T1121 inference-service Fixture Naming Tighten

## Task ID: T1121
## Title: inference-service Fixture Naming Tighten
## Owner: MINIMAX
## Status: READY

## Read First

- `tasks/review/T1111-review-round-2.md`

## Scope

直接就地修订以下文件：

1. `tasks/review-pending/T1101-inference-request-fixtures-v1.md`
2. 如有必要，可同步修订 `tasks/review-pending/T1101-inference-fixture-manifest-v1.md`

## Required Changes

- 把 pack 内部的 fixture 文件命名统一成同一套口径
- 不再保留 `health_ready.json` / `metrics_prometheus.txt` 这类旧命名

## Guardrails

- 不重写整包
- 不新增文件
- 完成后列出实际修改过的绝对路径
