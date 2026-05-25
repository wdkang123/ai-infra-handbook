# T1011 inference-service Starter File Pack Revision

## Task ID: T1011
## Title: inference-service Starter File Pack Revision
## Owner: MINIMAX
## Status: READY

## Background

`T1001` 已完成首轮 starter file 蓝图，但 Codex 审阅发现 3 个会直接影响后续落地的问题，需做最小修订。

## Read First

- `tasks/review/T1001-review.md`

## Scope

直接就地修订以下文件，不新增平行文件名：

1. `tasks/review-pending/T1001-inference-server-py-blueprint-v1.md`
2. `tasks/review-pending/T1001-inference-test-api-py-blueprint-v1.md`

## Required Changes

1. 修复 `_stream_chat()` 示例中的语法错误。
2. 对齐 metrics 契约：
   - `server.py` 占位返回
   - `test_api.py` 的 metrics 预期
   - 与根级 smoke 的预期口径
3. 把测试索引表中的旧端点 `/v1/chat` 统一改为 `/v1/chat/completions`。

## Guardrails

- 只修 review note 指定的问题，不重写整包。
- 不改任务边界，不新增目录。
- 修订后文件仍保持 blueprint 形态，不要伪装成“已实现代码”。

## Deliverable

- 直接覆盖上述 2 个原文件。
- 完成后列出你实际修改过的绝对路径。
