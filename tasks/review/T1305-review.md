# T1305 Review

## Task ID: T1305
## Title: Root Integration Execution Slice Pack
## Reviewer: CODEX
## Status: REVISE_REQUIRED

## 结论

`T1305` 已经接近可用，但还保留了两处会把根级联调资产带偏的路径和指标口径问题。

## Findings

1. [T1305-root-slice-manifest-v1.md](tasks/review-pending/T1305-root-slice-manifest-v1.md#L21) 和 [T1305-root-slice-contracts-v1.md](tasks/review-pending/T1305-root-slice-contracts-v1.md#L117) 把跨项目 handoff 文件写成了 `docs/cross-project-handoff.md`，但当前已接受根级资产的真实口径是 [T1005-codex-handoff-v2.md](tasks/accepted/T1005-codex-handoff-v2.md) 对应的 `CODEX_IMPLEMENTATION_HANDOFF.md`。
2. [T1305-root-slice-contracts-v1.md](tasks/review-pending/T1305-root-slice-contracts-v1.md#L104) 把 gateway `/metrics` 的验证写成 `grep vllm_`，但已接受的 [T1005-integration-smoke-sh-blueprint-v2.md](tasks/accepted/T1005-integration-smoke-sh-blueprint-v2.md) 里，gateway metrics 应检查 `ai_gateway_`。
3. [T1305-root-slice-manifest-v1.md](tasks/review-pending/T1305-root-slice-manifest-v1.md#L20) 和 [T1305-root-slice-contracts-v1.md](tasks/review-pending/T1305-root-slice-contracts-v1.md#L106) 把 R3 前置条件写成 `S2/G2`，但 root smoke 真正依赖的是 gateway 代理链路已成型，更合理的前置条件应至少覆盖 gateway 的 route/proxy slice，而不只是 auth slice。

## Required Fix

- 直接就地修订 `T1305` 原文件，不新增平行版本。
- 把 handoff 文档路径和命名统一回 accepted 根级资产。
- 把 gateway metrics 验证统一回 `ai_gateway_` 口径。
- 把 root smoke 的前置条件写成与真实代理链路一致的 slice 依赖。
