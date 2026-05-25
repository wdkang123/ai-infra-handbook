# T1001 Review

## Task ID: T1001
## Title: inference-service Starter File Pack
## Reviewer: CODEX
## Status: REVISE_REQUIRED

## 结论

本轮 starter pack 不通过，需要最小修订后再进入 `accepted/`。

## Findings

1. `T1001-inference-server-py-blueprint-v1.md` 第 213 行的 `_stream_chat()` 示例存在明确语法错误：`enumerate(["[PLACE", "HOLDER", "]"]:` 缺少右括号。后续如果按蓝图直接落地，`server.py` 将无法通过最基本的语法检查。
2. `T1001-inference-server-py-blueprint-v1.md` 第 150 行的 `/metrics` 占位返回只包含 `inference_service_requests_total`，但同 pack 的 `T1001-inference-test-api-py-blueprint-v1.md` 第 94-100 行和根级 `T1005` 冒烟脚本都把 `vllm_*` 当成必须观测项。当前蓝图之间的 metrics 契约没有对齐。
3. `T1001-inference-test-api-py-blueprint-v1.md` 第 267-273 行的测试索引表又写回了 `POST /v1/chat`，与正文和 `server.py` 蓝图里的 `POST /v1/chat/completions` 不一致，后续会把测试名录带偏。

## Required Fix

- 直接就地修订 `tasks/review-pending/` 下的 `T1001` 原文件，不新建平行版本。
- 修掉 `_stream_chat()` 的语法错误。
- 对齐 metrics 契约：`server.py`、`test_api.py` 与根级 smoke 预期至少要在“是否包含 `vllm_*` 指标”这一点上保持一致。
- 把测试索引表中的旧端点表述统一改成 `/v1/chat/completions`。
