# eval-module Sample Results Catalog v1

## Task ID: T903
## Title: eval-module Scaffold Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T803 API contract 和 T803 validation checklist（已收紧为 T813），产出结果样例模板。

---

# eval-module Sample Results Catalog v1

## 概述

本文档定义 eval-module 的评测结果 JSON 样例，供 Codex 实施时参照格式。

## 目录结构

```
examples/sample_results/
├── mmlu_result.json          # MMLU 单次评测结果
├── gsm8k_result.json          # GSM8K 单次评测结果
├── comparison_result.json     # 对比结果
└── README.md                  # 说明文档
```

## `examples/sample_results/mmlu_result.json`

```json
{
  "task": "mmlu",
  "model": "Qwen/Qwen2.5-0.5B-Instruct",
  "accuracy": 0.6534,
  "num_samples": 14242,
  "num_fewshot": 5,
  "timestamp": "2026-04-03T12:00:00Z",
  "lm_eval_version": "0.4.3",
  "backend": "vllm",
  "metrics": {
    "mmlu": 0.6534
  },
  "subjects": {
    "abstract_algebra": 0.35,
    "anatomy": 0.52,
    "astronomy": 0.67,
    "business_ethics": 0.61,
    "clinical_knowledge": 0.58,
    "college_biology": 0.72,
    "college_chemistry": 0.40,
    "college_computer_science": 0.65,
    "college_mathematics": 0.33,
    "college_medicine": 0.55,
    "college_physics": 0.38,
    "computer_security": 0.68,
    "conceptual_physics": 0.52,
    "econometrics": 0.48,
    "electrical_engineering": 0.54,
    " embryology": 0.45,
    "environmental_science": 0.65,
    "ethics": 0.62,
    "formal_logic": 0.38,
    "global_facts": 0.55,
    "high_school_biology": 0.74,
    "high_school_chemistry": 0.50,
    "high_school_computer_science": 0.72,
    "high_school_european_history": 0.65,
    "high_school_geography": 0.72,
    "high_school_government_and_politics": 0.70,
    "high_school_macroeconomics": 0.55,
    "high_school_mathematics": 0.40,
    "high_school_microeconomics": 0.58,
    "high_school_physics": 0.42,
    "high_school_psychology": 0.78,
    "high_school_statistics": 0.55,
    "high_school_us_history": 0.68,
    "high_school_world_history": 0.67,
    "human_aging": 0.60,
    "human_sexuality": 0.65,
    "international_law": 0.62,
    "jurisprudence": 0.58,
    "logical_fallacies": 0.60,
    "machine_learning": 0.52,
    "management": 0.67,
    "marketing": 0.74,
    "medical_genetics": 0.62,
    "microeconomics": 0.58,
    "miscellaneous": 0.65,
    "moral_disputes": 0.60,
    "moral_scenarios": 0.48,
    "nutrition": 0.62,
    "philosophy": 0.58,
    "prehistory": 0.68,
    "professional_accounting": 0.48,
    "professional_law": 0.42,
    "professional_medicine": 0.55,
    "professional_nursing": 0.65,
    "professional_psychology": 0.58,
    "public_relations": 0.60,
    "security_studies": 0.65,
    "sociology": 0.72,
    "sports": 0.70,
    "statistics": 0.50,
    "taxation": 0.62,
    "us_foreign_policy": 0.70,
    "virology": 0.52,
    "world_religions": 0.68
  }
}
```

来源：https://github.com/EleutherAI/lm-evaluation-harness/tree/main/lm_eval/tasks/mmlu

## `examples/sample_results/gsm8k_result.json`

```json
{
  "task": "gsm8k",
  "model": "Qwen/Qwen2.5-0.5B-Instruct",
  "accuracy": 0.5023,
  "num_samples": 1319,
  "num_fewshot": 5,
  "timestamp": "2026-04-03T12:05:00Z",
  "lm_eval_version": "0.4.3",
  "backend": "vllm",
  "metrics": {
    "gsm8k": 0.5023
  },
  "split_stats": {
    "test": {
      "accuracy": 0.5023,
      "total": 1319,
      "correct": 663,
      "incorrect": 656
    }
  }
}
```

来源：https://github.com/EleutherAI/lm-evaluation-harness/tree/main/lm_eval/tasks/gsm8k

## `examples/sample_results/comparison_result.json`

```json
{
  "baseline": {
    "task": "mmlu",
    "model": "Qwen/Qwen2.5-0.5B-Instruct (base)",
    "accuracy": 0.6534,
    "num_samples": 14242,
    "timestamp": "2026-04-03T12:00:00Z",
    "lm_eval_version": "0.4.3"
  },
  "candidate": {
    "task": "mmlu",
    "model": "Qwen/Qwen2.5-0.5B-Instruct (finetuned)",
    "accuracy": 0.6845,
    "num_samples": 14242,
    "timestamp": "2026-04-05T12:00:00Z",
    "lm_eval_version": "0.4.3"
  },
  "diff": {
    "accuracy_delta": 0.0311,
    "relative_improvement": 4.76,
    "improvement_percent": "+3.11pp"
  },
  "verdict": "candidate outperforms baseline"
}
```

## 结果字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `task` | string | 任务名称 |
| `model` | string | 模型名称 |
| `accuracy` | float | 整体准确率 |
| `num_samples` | int | 样本数量 |
| `num_fewshot` | int | few-shot 数 |
| `timestamp` | ISO8601 | 评测时间 |
| `lm_eval_version` | string | lm-eval 版本 |
| `backend` | string | 推理 backend |
| `metrics` | dict | 任务特定指标 |

## MMLU 子任务说明

MMLU 包含 57 个子任务，评测结果中 `subjects` 字段记录每个子任务的准确率。

## 对比结果判断标准

| 条件 | verdict |
|------|---------|
| `accuracy_delta > 0` | candidate outperforms baseline |
| `accuracy_delta == 0` | no change |
| `accuracy_delta < 0` | candidate underperforms baseline |

---

Sources:
1. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval
2. https://github.com/EleutherAI/lm-evaluation-harness/tree/main/lm_eval/tasks/mmlu — MMLU task
3. https://github.com/EleutherAI/lm-evaluation-harness/tree/main/lm_eval/tasks/gsm8k — GSM8K task

Risk of Staleness:
- lm-eval 结果格式可能随版本变化

Out of Scope Kept:
- 未写自动报告生成（HTML/PDF）
- 未写历史趋势图表
