# T1025 Root Smoke MODEL Pass-through Fix

## Task ID: T1025
## Title: Root Smoke MODEL Pass-through Fix
## Owner: MINIMAX
## Status: READY

## Read First

- `tasks/review/T1015-review-round-2.md`

## Scope

直接就地修订以下文件：

1. `tasks/review-pending/T1005-root-makefile-blueprint-v2.md`

## Required Changes

- 让 `infra-smoke` 调用 `integration_smoke_test.sh` 时显式传递 `MODEL`
- 如有必要，可顺手统一为 `VAR=value bash script.sh` 这种明确写法

## Guardrails

- 不重写其他部分
- 不新增文件
- 完成后列出实际修改过的绝对路径
