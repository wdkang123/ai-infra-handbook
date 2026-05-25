# T1105 Review

## Task ID: T1105
## Title: Root Integration Fixture Pack
## Reviewer: CODEX
## Status: REVISE_REQUIRED

## 结论

本轮 fixture pack 接近可用，但根级 smoke 预期里仍有 1 处和已接受 blueprint 不一致的错误样例。

## Finding

1. `T1105-root-smoke-expected-output-v1.md` 第 179 行把 IT-06 unknown model 的 `error.code` 写成了 `model_not_found`，但已接受的 gateway blueprint [T1002-ai-gateway-server-py-blueprint-v1.md](tasks/accepted/T1002-ai-gateway-server-py-blueprint-v1.md#L225) 输出的是 HTTP 状态码字符串 `404`。根级 smoke 预期应与下游 accepted 契约保持一致。

## Required Fix

- 直接就地修订 `tasks/review-pending/` 下的 `T1105-root-smoke-expected-output-v1.md`
- 如 manifest 或其他 root fixture 中也引用了同一错误样例口径，一并对齐
- 不重写整包
