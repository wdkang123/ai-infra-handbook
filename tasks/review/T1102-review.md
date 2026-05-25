# T1102 Review

## Task ID: T1102
## Title: ai-gateway Fixture Pack
## Reviewer: CODEX
## Status: REVISE_REQUIRED

## 结论

本轮 fixture pack 不通过，主要问题是 auth / error 契约和已接受的 `T1002` blueprint 没有对齐。

## Findings

1. `T1102-gateway-auth-request-fixtures-v1.md` 把“有效 Bearer token”的期望写成“鉴权中间件返回 `None`”，但已接受的 [T1002-ai-gateway-auth-middleware-blueprint-v1.md](tasks/accepted/T1002-ai-gateway-auth-middleware-blueprint-v1.md#L51) 明确约定成功时返回已验证的 token 字符串。
2. `T1102-gateway-auth-request-fixtures-v1.md` 和 `T1102-gateway-routing-config-samples-v1.md` 使用的是 `valid_keys`，但已接受的 `T1002` blueprint 约定字段名是 `api_keys`。
3. `T1102-gateway-auth-request-fixtures-v1.md` 及 `T1102-gateway-error-response-samples-v1.md` 把错误 scheme 的 message 写成 `Invalid authentication scheme. Expected: Bearer`，但已接受 blueprint 的 message 是 `Invalid Authorization header format. Expected: Bearer <key>`。
4. `T1102-gateway-error-response-samples-v1.md` 和 `T1102-gateway-proxy-response-samples-v1.md` 把 unknown model 的 `error.code` 写成 `model_not_found`，但已接受的 [T1002-ai-gateway-server-py-blueprint-v1.md](tasks/accepted/T1002-ai-gateway-server-py-blueprint-v1.md#L225) 会输出 HTTP 状态码字符串 `404`。

## Required Fix

- 直接就地修订 `tasks/review-pending/` 下的 `T1102` 原文件，不新增平行版本。
- 所有 auth / routing / error sample 必须对齐已接受 `T1002` blueprint 的字段名、返回值和错误消息。
