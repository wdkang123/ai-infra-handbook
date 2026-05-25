# eval-module Config Surface v1

## Task ID: T803
## Task Title: eval-module Execution Prep Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T303 MVP 设计，准备 eval-module 实施前包。

---

# eval-module Config Surface v1

## 概述

本文档定义 eval-module 的配置项清单，对应 `config.yaml` 和环境变量。

---

## 配置项总览

| 配置类 | 配置项数 | MVP 必须 |
|--------|---------|---------|
| Eval | 2 | 2 |
| Backend | 3 | 3 |
| Datasets | 6 | 4 |
| Results | 3 | 3 |
| **合计** | **14** | **12** |

---

## Eval 配置

| 配置项 | 环境变量 | 默认值 | 说明 | MVP 必须 |
|--------|---------|-------|------|---------|
| `eval.backend` | `EVAL_BACKEND` | `lm-eval` | 评测执行器 | 是 |
| `eval.lm_eval_version` | `LM_EVAL_VERSION` | `0.4.3` | lm-eval 版本 | 是 |

---

## Backend 配置

| 配置项 | 环境变量 | 默认值 | 说明 | MVP 必须 |
|--------|---------|-------|------|---------|
| `backend.type` | `EVAL_BACKEND_TYPE` | `vllm` | 推理 backend 类型 | 是 |
| `backend.base_url` | `EVAL_BACKEND_BASE_URL` | `http://localhost:8000/v1` | 推理服务地址 | 是 |
| `backend.api_key` | `EVAL_BACKEND_API_KEY` | `` | API Key（如需要） | 否 |

---

## Datasets 配置

| 配置项 | 环境变量 | 默认值 | 说明 | MVP 必须 |
|--------|---------|-------|------|---------|
| `datasets.mmlu.enabled` | `DATASET_MMLU_ENABLED` | `true` | 启用 MMLU | 是 |
| `datasets.mmlu.num_fewshot` | `DATASET_MMLU_FEWSHOT` | `5` | MMLU few-shot 数 | 是 |
| `datasets.gsm8k.enabled` | `DATASET_GSM8K_ENABLED` | `true` | 启用 GSM8K | 是 |
| `datasets.gsm8k.num_fewshot` | `DATASET_GSM8K_FEWSHOT` | `5` | GSM8K few-shot 数 | 是 |
| `datasets.humaneval.enabled` | `DATASET_HUMANEVAL_ENABLED` | `false` | 启用 HumanEval | 否 |
| `datasets.truthfulqa.enabled` | `DATASET_TRUTHFULQA_ENABLED` | `false` | 启用 TruthfulQA | 否 |

---

## Results 配置

| 配置项 | 环境变量 | 默认值 | 说明 | MVP 必须 |
|--------|---------|-------|------|---------|
| `results.output_dir` | `EVAL_RESULTS_DIR` | `./results` | 结果输出目录 | 是 |
| `results.format` | `EVAL_RESULTS_FORMAT` | `json` | 结果格式 | 是 |
| `results.compare_with_baseline` | `EVAL_COMPARE_ENABLED` | `false` | 是否自动对比 | 否 |

---

## 配置加载优先级

```
CLI 参数 > 环境变量 > config.yaml > 默认值
```

---

## config.yaml 示例

```yaml
eval:
  backend: "lm-eval"
  lm_eval_version: "0.4.3"

backend:
  type: "vllm"
  base_url: "http://localhost:8000/v1"

datasets:
  mmlu:
    enabled: true
    num_fewshot: 5
  gsm8k:
    enabled: true
    num_fewshot: 5
  humaneval:
    enabled: false
  truthfulqa:
    enabled: false

results:
  output_dir: "./results"
  format: "json"
  compare_with_baseline: false
```

---

Sources:
1. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval

Risk of Staleness:
- lm-eval 版本更新可能改变配置项

Out of Scope Kept:
- 未写评测结果数据库配置
