# T1111 Review Round 2

## Task ID: T1111
## Title: inference-service Fixture Pack Revision
## Reviewer: CODEX
## Status: REVISE_REQUIRED

## 结论

本轮只剩文件命名口径没有完全收干净，需再补一刀。

## Finding

1. `T1101-inference-fixture-manifest-v1.md` 已经切到了 `health_all_systems_go.json` / `metrics_idle_state.txt` 这一套命名，但 `T1101-inference-request-fixtures-v1.md` 仍然在第 26 行和第 54 行使用 `health_ready.json` / `metrics_prometheus.txt`。同一 pack 里不能同时保留两套 fixture 文件名。

## Required Fix

- 直接覆盖修订 `tasks/review-pending/T1101-inference-request-fixtures-v1.md`
- 如有必要，可同步修订 `T1101-inference-fixture-manifest-v1.md` 中关于 `F10` 的说明文字
- 只做命名和口径收口，不重写整包
