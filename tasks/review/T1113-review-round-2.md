# T1113 Review Round 2

## Task ID: T1113
## Title: eval-module Fixture Pack Revision
## Reviewer: CODEX
## Status: REVISE_REQUIRED

## 结论

本轮已经接近通过，但还剩 2 个会误导实现的细节问题。

## Findings

1. `T1103-eval-result-json-samples-v1.md` 仍把 `backend` 字段写成了 URL（如 `http://localhost:8000/v1`），但 accepted `T1003` blueprint 的 `EvalResult.backend` 明确是 backend 类型，例如 `vllm`。
2. `T1103-eval-cli-example-catalog-v1.md` 的完整工作流示例里，`compare` 命令在 `--candidate` 那一行后少了续行反斜杠，按 shell 实际执行会把下一行 `--output ...` 当成单独命令。

## Required Fix

- 直接覆盖修订以下原文件：
  - `tasks/review-pending/T1103-eval-result-json-samples-v1.md`
  - `tasks/review-pending/T1103-eval-compare-report-samples-v1.md`
  - `tasks/review-pending/T1103-eval-cli-example-catalog-v1.md`
- 把 `backend` 统一改回 accepted blueprint 的口径
- 修好 `compare` 示例的 shell 续行
- 不重写整包
