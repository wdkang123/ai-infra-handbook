# eval-module Compare Report Samples v1

## Task ID: T1103
## Title: eval-module Fixture Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# eval-module Compare Report Samples

本文档定义 eval-module 对比报告的样本，对应真实文件 `eval-module/tests/fixtures/reports/`。compare 命令对比两个 `EvalResult` JSON 文件，对齐 T1003 blueprint 的 `Comparator` 实现。

## Compare Report 结构

compare 接收两个 `EvalResult` JSON 文件，对比后输出报告：

```json
{
  "compare_id": "string",
  "timestamp": "ISO8601",
  "baseline": { ... },   // EvalResult fields
  "candidate": { ... },  // EvalResult fields
  "delta": {
    "accuracy_absolute": float,
    "accuracy_relative_pct": float
  }
}
```

---

## Sample A: MMLU 对比报告

**对应文件：** `eval-module/tests/fixtures/reports/mmlu_compare_report.json`

```json
{
  "compare_id": "mmlu-qwen25-05b-vs-baseline-20260408",
  "timestamp": "2026-04-08T12:00:00Z",
  "baseline": {
    "task": "mmlu",
    "model": "Qwen2.5-0.5B-Instruct",
    "accuracy": 0.4711,
    "num_samples": 450,
    "num_fewshot": 5,
    "timestamp": "2026-04-08T09:00:00Z",
    "lm_eval_version": "0.4.7",
    "backend": "vllm",
    "metrics": {
      "pass@1": 0.4711,
      "accuracy": 0.4711
    },
    "raw_output": null
  },
  "candidate": {
    "task": "mmlu",
    "model": "Qwen2.5-0.5B-Instruct-finetuned",
    "accuracy": 0.4911,
    "num_samples": 450,
    "num_fewshot": 5,
    "timestamp": "2026-04-08T10:00:00Z",
    "lm_eval_version": "0.4.7",
    "backend": "vllm",
    "metrics": {
      "pass@1": 0.4911,
      "accuracy": 0.4911
    },
    "raw_output": null
  },
  "delta": {
    "accuracy_absolute": 0.0200,
    "accuracy_relative_pct": 4.24
  }
}
```

---

## Sample B: GSM8K 对比报告

**对应文件：** `eval-module/tests/fixtures/reports/gsm8k_compare_report.json`

```json
{
  "compare_id": "gsm8k-qwen25-05b-vs-baseline-20260408",
  "timestamp": "2026-04-08T12:15:00Z",
  "baseline": {
    "task": "gsm8k",
    "model": "Qwen2.5-0.5B-Instruct",
    "accuracy": 0.3512,
    "num_samples": 1319,
    "num_fewshot": 0,
    "timestamp": "2026-04-08T09:30:00Z",
    "lm_eval_version": "0.4.7",
    "backend": "vllm",
    "metrics": {
      "pass@1": 0.3512
    },
    "raw_output": null
  },
  "candidate": {
    "task": "gsm8k",
    "model": "Qwen2.5-0.5B-Instruct-finetuned",
    "accuracy": 0.4026,
    "num_samples": 1319,
    "num_fewshot": 0,
    "timestamp": "2026-04-08T10:30:00Z",
    "lm_eval_version": "0.4.7",
    "backend": "vllm",
    "metrics": {
      "pass@1": 0.4026
    },
    "raw_output": null
  },
  "delta": {
    "accuracy_absolute": 0.0514,
    "accuracy_relative_pct": 14.64
  }
}
```

---

## Sample C: 多任务对比报告（汇总）

**对应文件：** `eval-module/tests/fixtures/reports/multi_task_compare_summary.json`

```json
{
  "compare_id": "multi-task-20260408",
  "timestamp": "2026-04-08T13:00:00Z",
  "task": "mmlu",
  "baseline_accuracy": 0.4711,
  "candidate_accuracy": 0.4911,
  "delta_accuracy": 0.0200
}
```

---

## Delta 字段说明

| 字段 | 类型 | 说明 |
|---|---|---|
| `accuracy_absolute` | float | 绝对差值（candidate - baseline） |
| `accuracy_relative_pct` | float | 相对提升百分比 |

Delta 判定规则（仓库样例约定）：
- `delta > 0` → candidate 优于 baseline
- `delta < 0` → candidate 劣于 baseline
- `|delta| < 0.01` → 基本持平

---

## Compare CLI 命令

```bash
# 对比两个结果 JSON 文件
python -m eval_module.main compare \
  --baseline ./results/baseline_mmlu.json \
  --candidate ./results/candidate_mmlu.json \
  --output results/compare/mmlu_report.json
```

---

Sources:
1. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval
2. https://github.com/opencompass/opencompass — OpenCompass compare format

Risk of Staleness:
- Result comparison schema is project-internal; defined per T813
