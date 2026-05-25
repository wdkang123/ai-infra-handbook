# T1123 Review Round 3

## Task ID: T1123
## Title: eval-module Fixture Contract Tighten
## Reviewer: CODEX
## Status: REVISE_REQUIRED

## 结论

本轮未通过。`backend` 字段口径和 CLI 示例续行这两个点都还没真正改掉。

## Findings

1. `T1103-eval-result-json-samples-v1.md` 以及 `T1103-eval-compare-report-samples-v1.md` 仍把 `backend` 写成推理 URL（例如 `http://localhost:8000/v1`），但 accepted `T1003` blueprint 的 `EvalResult.backend` 是 backend 类型。
2. `T1103-eval-cli-example-catalog-v1.md` 的完整工作流示例中，`compare` 命令在 `--candidate ./results/candidate.json` 这一行后仍然缺少续行反斜杠，shell 示例依旧不合法。

## Required Fix

- 直接覆盖修订以下文件：
  - `tasks/review-pending/T1103-eval-result-json-samples-v1.md`
  - `tasks/review-pending/T1103-eval-compare-report-samples-v1.md`
  - `tasks/review-pending/T1103-eval-cli-example-catalog-v1.md`
- 把 `backend` 改成 accepted `EvalResult` 口径，例如 `vllm`
- 把 CLI 示例中的 shell 续行补完整
- 修完后列出实际修改过的绝对路径
