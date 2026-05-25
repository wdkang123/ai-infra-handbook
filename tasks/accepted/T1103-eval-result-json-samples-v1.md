# eval-module Result JSON Samples v1

## Task ID: T1103
## Title: eval-module Fixture Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# eval-module Result JSON Samples

本文档定义 eval-module 评测结果的 JSON 样本，对应真实文件 `eval-module/tests/fixtures/results/`。结构与 accepted `T1003-eval-runner-py-blueprint-v1.md` 中的 `EvalResult` dataclass 对齐。

## EvalResult 结构（来自 T1003 blueprint）

```python
EvalResult:
  task: str
  model: str
  accuracy: float
  num_samples: int
  num_fewshot: int
  timestamp: str
  lm_eval_version: str
  backend: str
  metrics: dict[str, float]        # 可选指标（如 pass@8 等）
  raw_output: dict[str, Any] | None  # 可选原始 lm-eval 输出
```

---

## MMLU Result Sample

**对应文件：** `eval-module/tests/fixtures/results/mmlu_result_sample.json`

```json
{
  "task": "mmlu",
  "model": "Qwen2.5-0.5B-Instruct",
  "accuracy": 0.4844,
  "num_samples": 450,
  "num_fewshot": 5,
  "timestamp": "2026-04-08T10:00:00Z",
  "lm_eval_version": "0.4.7",
  "backend": "vllm",
  "metrics": {
    "pass@1": 0.4844,
    "accuracy": 0.4844
  },
  "raw_output": null
}
```

---

## GSM8K Result Sample

**对应文件：** `eval-module/tests/fixtures/results/gsm8k_result_sample.json`

```json
{
  "task": "gsm8k",
  "model": "Qwen2.5-0.5B-Instruct",
  "accuracy": 0.3692,
  "num_samples": 1319,
  "num_fewshot": 0,
  "timestamp": "2026-04-08T10:30:00Z",
  "lm_eval_version": "0.4.7",
  "backend": "vllm",
  "metrics": {
    "pass@1": 0.3692
  },
  "raw_output": null
}
```

---

## HumanEval Result Sample

**对应文件：** `eval-module/tests/fixtures/results/humaneval_result_sample.json`

```json
{
  "task": "humaneval",
  "model": "Qwen2.5-0.5B-Instruct",
  "accuracy": 0.1402,
  "num_samples": 164,
  "num_fewshot": 0,
  "timestamp": "2026-04-08T11:00:00Z",
  "lm_eval_version": "0.4.7",
  "backend": "vllm",
  "metrics": {
    "pass@1": 0.1402
  },
  "raw_output": null
}
```

---

## 字段级说明

| 字段 | 类型 | 说明 |
|---|---|---|
| `task` | string | 任务标识符（mmlu / gsm8k / humaneval） |
| `model` | string | 被评测模型名称 |
| `accuracy` | float | 主要准确率指标（0.0 ~ 1.0） |
| `num_samples` | int | 有效样本数 |
| `num_fewshot` | int | few-shot 样本数 |
| `timestamp` | string | ISO8601 时间戳 |
| `lm_eval_version` | string | lm-evaluation-harness 版本 |
| `backend` | string | 推理后端类型（如 `vllm`） |
| `metrics` | dict | 额外指标（如 pass@8, mcc 等） |
| `raw_output` | dict\|null | 原始 lm-eval 输出（调试用） |

---

Sources:
1. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval
2. https://github.com/openai/human-eval — HumanEval

Risk of Staleness:
- lm-eval result format is stable; `pass@k` and `accuracy` are standard metrics
