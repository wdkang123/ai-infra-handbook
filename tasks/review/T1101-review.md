# T1101 Review

## Task ID: T1101
## Title: inference-service Fixture Pack
## Reviewer: CODEX
## Status: REVISE_REQUIRED

## 结论

本轮 fixture pack 有 2 处会把后续实现带偏的契约问题，需要最小修订。

## Findings

1. `T1101-inference-fixture-manifest-v1.md`、`T1101-inference-request-fixtures-v1.md`、`T1101-inference-metrics-health-samples-v1.md` 之间的文件名没有对齐。比如 manifest 用的是 `health_ready.json` / `metrics_idle_state.txt`，request fixture 又写成 `metrics_prometheus.txt`，metrics-health 样例又写成 `health_all_systems_go.json`。这样后续真正落文件时，Codex 没法知道哪一套命名才是最终口径。
2. `T1101-inference-request-fixtures-v1.md` 第 219-226 行把 unknown model 的错误码写成 `model_not_found`，但已接受的 [T1001-inference-server-py-blueprint-v1.md](tasks/accepted/T1001-inference-server-py-blueprint-v1.md#L250) 里 `HTTPException` handler 输出的 `error.code` 是 HTTP 状态码字符串（例如 `404`）。当前 fixture 与已接受 blueprint 不一致。

## Required Fix

- 直接就地修订 `tasks/review-pending/` 下的 `T1101` 原文件，不新增平行版本。
- 统一 manifest / request fixtures / metrics-health samples 里的文件命名。
- 把 unknown model 错误样例改成与已接受 `T1001` blueprint 一致的错误格式。
