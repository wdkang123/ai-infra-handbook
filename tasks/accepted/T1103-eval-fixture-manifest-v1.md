# eval-module Fixture Manifest v1

## Task ID: T1103
## Title: eval-module Fixture Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# eval-module Fixture Manifest

本文档是 `eval-module` 全部 fixture 资产的索引清单，对应真实路径 `eval-module/configs/task_presets/`、`eval-module/tests/fixtures/results/`、`eval-module/tests/fixtures/reports/`。

## Fixture 文件清单

### Task Preset Fixtures

| 文件路径 | Task ID | 场景 |
|---|---|---|
| `configs/task_presets/mmlu.yaml` | mmlu | MMLU 5-shot multiple choice |
| `configs/task_presets/gsm8k.yaml` | gsm8k | GSM8K 0-shot math |
| `configs/task_presets/humaneval.yaml` | humaneval | HumanEval 代码生成 |

### Result JSON Fixtures

| 文件路径 | Task ID | 场景 |
|---|---|---|
| `tests/fixtures/results/mmlu_result_sample.json` | mmlu | MMLU 结果样例 |
| `tests/fixtures/results/gsm8k_result_sample.json` | gsm8k | GSM8K 结果样例 |
| `tests/fixtures/results/humaneval_result_sample.json` | humaneval | HumanEval 结果样例 |

### Compare Report Fixtures

| 文件路径 | 场景 |
|---|---|
| `tests/fixtures/reports/mmlu_compare_report.json` | MMLU baseline vs candidate |
| `tests/fixtures/reports/gsm8k_compare_report.json` | GSM8K baseline vs candidate |
| `tests/fixtures/reports/multi_task_compare_summary.json` | 多任务汇总对比 |

### CLI Example Fixtures

| 对应文件 | 说明 |
|---|---|
| `src/eval_module/main.py`（待实现） | CLI 入口点（Typer） |

---

## 与 Starter Blueprint 对齐（T1003）

| Blueprint 要点 | Fixture 对应 |
|---|---|
| `mmlu`、`gsm8k`、`humaneval` 任务 | `configs/task_presets/*.yaml` |
| `run / compare / list-tasks` CLI 命令 | `T1103-eval-cli-example-catalog-v1.md` |
| baseline / candidate / delta 对比格式 | `tests/fixtures/reports/*` |
| `pass@k` 指标 | 所有 result 和 compare 文件 |

---

## 与 T813 eval-module Validation Checklist 对齐

| Checklist 项目 | Fixture 覆盖 |
|---|---|
| MMLU 评测 | `mmlu_result_sample.json` |
| GSM8K 评测 | `gsm8k_result_sample.json` |
| HumanEval 评测 | `humaneval_result_sample.json` |
| compare 报告格式 | `*_compare_report.json` |

---

Sources:
1. https://github.com/EleutherAI/lm-evaluation-harness
2. https://github.com/opencompass/opencompass

Risk of Staleness:
- lm-eval task definitions and result schema are stable
