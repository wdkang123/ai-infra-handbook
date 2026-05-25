# T1121 Review Round 3

## Task ID: T1121
## Title: inference-service Fixture Naming Tighten
## Reviewer: CODEX
## Status: REVISE_REQUIRED

## 结论

本轮未通过。要求修掉的命名分裂问题仍然保留。

## Finding

1. `T1101-inference-request-fixtures-v1.md` 仍然使用 `health_ready.json` 和 `metrics_prometheus.txt`，但同 pack 的 manifest 与 metrics-health 样例已经切到 `health_all_systems_go.json` 和 `metrics_idle_state.txt`。这不是轻微措辞问题，而是同一 pack 内部仍保留两套文件名。

## Required Fix

- 直接覆盖修订 `tasks/review-pending/T1101-inference-request-fixtures-v1.md`
- 必须把其中所有旧命名统一改成与 `T1101-inference-fixture-manifest-v1.md` 一致
- 修完后列出实际修改过的绝对路径
