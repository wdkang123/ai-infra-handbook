# T1012 ai-gateway Starter File Pack Revision

## Task ID: T1012
## Title: ai-gateway Starter File Pack Revision
## Owner: MINIMAX
## Status: READY

## Background

`T1002` 已完成首轮 starter file 蓝图，但 Codex 审阅发现鉴权逻辑与响应模型表述仍需最小修订。

## Read First

- `tasks/review/T1002-review.md`

## Scope

直接就地修订以下文件，不新增平行文件名：

1. `tasks/review-pending/T1002-ai-gateway-server-py-blueprint-v1.md`

## Required Changes

1. 修正鉴权启停逻辑，确保只有 `enabled = false` 时才绕过鉴权。
2. 补齐或改正 `ChatCompletionsResponse` 的响应模型表述，避免 `server.py` 蓝图里出现未定义模型。

## Guardrails

- 只修 review note 指定的问题，不重写整包。
- 不改任务边界，不新增目录。
- 修订后文件仍保持 blueprint 形态，不要伪装成“已实现代码”。

## Deliverable

- 直接覆盖上述原文件。
- 完成后列出你实际修改过的绝对路径。
