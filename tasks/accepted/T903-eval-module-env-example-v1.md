# eval-module .env.example Blueprint v1

## Task ID: T903
## Title: eval-module Scaffold Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T803 config surface，产出 .env.example 模板。

---

# eval-module .env.example Blueprint v1

## 概述

本文档定义 eval-module 的 `.env.example` 模板。

## 模板全文

```bash
# ============================================================
# eval-module — .env.example
# ============================================================

# ---------- Eval Backend ----------
EVAL_BACKEND=lm-eval
LM_EVAL_VERSION=0.4.3

# ---------- Downstream Inference ----------
# 必须指向 inference-service 的 /v1 端点
EVAL_BACKEND_TYPE=vllm
EVAL_BACKEND_BASE_URL=http://localhost:8000/v1
EVAL_BACKEND_API_KEY=  # 本地无需 key

# ---------- Datasets ----------
DATASET_MMLU_ENABLED=true
DATASET_MMLU_FEWSHOT=5

DATASET_GSM8K_ENABLED=true
DATASET_GSM8K_FEWSHOT=5

DATASET_HUMANEVAL_ENABLED=false
DATASET_TRUTHFULQA_ENABLED=false

# ---------- Results ----------
EVAL_RESULTS_DIR=./results
EVAL_RESULTS_FORMAT=json
EVAL_COMPARE_ENABLED=false
```

## 字段说明

| 字段 | 说明 | MVP 必须 |
|------|------|---------|
| `EVAL_BACKEND` | 评测执行器 | 是 |
| `EVAL_BACKEND_BASE_URL` | inference-service 地址 | 是 |
| `DATASET_MMLU_ENABLED` | 启用 MMLU | 是 |
| `DATASET_GSM8K_ENABLED` | 启用 GSM8K | 是 |

## 与 inference-service 的端口对齐

```
eval-module   →  calls  →  http://localhost:8000/v1
                                 ↑
                           inference-service (port 8000)
```

---

Sources:
1. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval

Risk of Staleness:
- lm-eval 环境变量尚未完全标准化

Out of Scope Kept:
- 未写评测结果数据库配置
