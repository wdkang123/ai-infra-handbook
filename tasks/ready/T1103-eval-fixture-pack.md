# T1103 eval-module Fixture Pack

## Task ID: T1103
## Title: eval-module Fixture Pack
## Owner: MINIMAX
## Status: READY

## Objective

为 `eval-module` 生成 implementation-ready 评测样例资产。

## Produce

1. `tasks/review-pending/T1103-eval-task-presets-v1.md`
2. `tasks/review-pending/T1103-eval-result-json-samples-v1.md`
3. `tasks/review-pending/T1103-eval-compare-report-samples-v1.md`
4. `tasks/review-pending/T1103-eval-cli-example-catalog-v1.md`
5. `tasks/review-pending/T1103-eval-fixture-manifest-v1.md`

## Requirements

- task preset 至少包含 `mmlu`、`gsm8k`、`humaneval`
- result JSON 要给出字段级样例
- compare report 要给出 baseline / candidate / delta 的具体示例
- CLI example 要和 starter blueprint 的 `run / compare / list-tasks` 对齐

## Guardrails

- 只做 fixture / sample asset，不写新章节
- 若某项是项目内约定样例，明确标注为“仓库样例约定”
