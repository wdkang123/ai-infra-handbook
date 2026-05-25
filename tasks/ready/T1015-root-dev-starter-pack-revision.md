# T1015 Root / Dev Workflow Starter File Pack Revision

## Task ID: T1015
## Title: Root / Dev Workflow Starter File Pack Revision
## Owner: MINIMAX
## Status: READY

## Background

`T1005` 已完成首轮 starter file 蓝图，但 Codex 审阅发现根级工作流变量命名和 smoke 断言与其他包尚未对齐。

## Read First

- `tasks/review/T1005-review.md`

## Scope

直接就地修订以下文件，不新增平行文件名：

1. `tasks/review-pending/T1005-root-makefile-blueprint-v2.md`
2. `tasks/review-pending/T1005-local-dev-sequence-sh-blueprint-v2.md`
3. `tasks/review-pending/T1005-integration-smoke-sh-blueprint-v2.md`

## Required Changes

1. 统一根级工作流的模型变量约定，保证 `Makefile`、`local_dev_sequence.sh`、`integration_smoke_test.sh` 三者一致。
2. 把 smoke 对 inference `/metrics` 的断言改成与 `T1001` 修订后的契约一致，不保留跨包冲突。

## Guardrails

- 只修 review note 指定的问题，不重写整包。
- 不改任务边界，不新增目录。
- 修订后文件仍保持 blueprint 形态，不要伪装成“已实现代码”。

## Deliverable

- 直接覆盖上述 3 个原文件。
- 完成后列出你实际修改过的绝对路径。
