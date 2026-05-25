# T1103 Review

## Task ID: T1103
## Title: eval-module Fixture Pack
## Reviewer: CODEX
## Status: REVISE_REQUIRED

## 结论

本轮 fixture pack 不通过，主要是 CLI 和结果 schema 都已经偏离已接受的 `T1003` starter blueprint。

## Findings

1. `T1103-eval-cli-example-catalog-v1.md` 和 `T1103-eval-fixture-manifest-v1.md` 把 CLI 入口写成 `src/eval_module/cli.py`，还新增了 `list-models` 子命令；但已接受的 [T1003-eval-main-py-blueprint-v1.md](tasks/accepted/T1003-eval-main-py-blueprint-v1.md#L17) 明确入口是 `src/eval_module/main.py`，并且只有 `run / compare / list-tasks` 三个命令。
2. `T1103-eval-cli-example-catalog-v1.md` 把 `compare` 写成对比两个 backend URL，并要求 `--model --task`；但已接受 `T1003` blueprint 约定的是对比两个结果 JSON 文件：`--baseline <result.json> --candidate <result.json>`。
3. `T1103-eval-result-json-samples-v1.md` 和 `T1103-eval-compare-report-samples-v1.md` 使用的是 `task_id / task_name / summary / per_sample_results` 这套新 schema，但已接受的 [T1003-eval-runner-py-blueprint-v1.md](tasks/accepted/T1003-eval-runner-py-blueprint-v1.md#L36) 已经定义了 `EvalResult(task, model, accuracy, num_samples, num_fewshot, timestamp, lm_eval_version, backend, metrics, raw_output)`。

## Required Fix

- 直接就地修订 `tasks/review-pending/` 下的 `T1103` 原文件，不新增平行版本。
- CLI 用法、入口文件、子命令集合、`compare` 参数，以及结果 JSON / compare report 的字段结构，都必须回到已接受 `T1003` blueprint 的契约上。
