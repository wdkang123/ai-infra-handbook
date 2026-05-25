# T1005 Review

## Task ID: T1005
## Title: Root / Dev Workflow Starter File Pack
## Reviewer: CODEX
## Status: REVISE_REQUIRED

## 结论

本轮 starter pack 不通过，需要最小修订后再进入 `accepted/`。

## Findings

1. `T1005-integration-smoke-sh-blueprint-v2.md` 第 199-202 行把 inference metrics 成功条件写死成必须匹配 `vllm_`，但当前 `T1001-inference-server-py-blueprint-v1.md` 第 150 行的占位返回并不满足这个约定。跨包契约不一致，会导致 smoke blueprint 一开始就和服务 blueprint 对撞。
2. `T1005-integration-smoke-sh-blueprint-v2.md` 第 33 行与 `T1005-local-dev-sequence-sh-blueprint-v2.md` 第 35 行读取的是 `MODEL_NAME`，但 `T1005-root-makefile-blueprint-v2.md` 第 38 行对外暴露的是 `MODEL`。当前根级工作流蓝图没有把模型变量名对齐，`make infra-smoke MODEL=...` 这种常见用法会失去一致性。

## Required Fix

- 直接就地修订 `tasks/review-pending/` 下的 `T1005` 原文件，不新建平行版本。
- 统一根级工作流对模型变量名的约定，至少保证 `Makefile`、`local_dev_sequence.sh`、`integration_smoke_test.sh` 三者能用同一套变量传递。
- 把 smoke 对 inference `/metrics` 的断言改成与 `T1001` 修订后的契约一致，不要继续保留跨包冲突。
