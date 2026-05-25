# T1015 Review Round 2

## Task ID: T1015
## Title: Root / Dev Workflow Starter File Pack Revision
## Reviewer: CODEX
## Status: REVISE_REQUIRED

## 结论

本轮大部分已修好，但根级 smoke 入口还剩 1 个工作流问题。

## Finding

1. `T1005-root-makefile-blueprint-v2.md` 第 76-78 行仍然只是 `bash scripts/integration_smoke_test.sh`，而 `T1005-integration-smoke-sh-blueprint-v2.md` 第 33 行读取的是环境变量 `MODEL`。这意味着用户即使执行 `make infra-smoke MODEL=...`，脚本也拿不到该值，根级工作流里的模型变量传递依然没有打通。

## Required Fix

- 直接覆盖修订 `tasks/review-pending/T1005-root-makefile-blueprint-v2.md`
- 让 `infra-smoke` 在调用脚本时显式传递 `MODEL`，必要时连同 URL / auth key 一起按同一模式传递
- 不重写其他文件
- 完成后列出实际修改过的绝对路径
