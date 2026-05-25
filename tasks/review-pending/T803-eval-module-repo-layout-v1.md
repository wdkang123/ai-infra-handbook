# eval-module Repo Layout v1

## Task ID: T803
## Task Title: eval-module Execution Prep Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T303 MVP 设计，准备 eval-module 实施前包。

---

# eval-module Repo Layout v1

## 概述

本文档定义 eval-module 模块的完整目录结构，对应 MVP 实施需求。

---

## 顶层结构

```
eval-module/
├── README.md
├── pyproject.toml
├── config.yaml
├── .env.example
├── src/
│   └── eval_module/
│       ├── __init__.py
│       ├── main.py
│       ├── config.py
│       ├── evaluator.py
│       ├── runners/
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── lm_eval_runner.py
│       │   └── helm_runner.py
│       ├── datasets/
│       │   ├── __init__.py
│       │   ├── dataset_manager.py
│       │   └── mmlu.py
│       │   └── gsm8k.py
│       ├── results/
│       │   ├── __init__.py
│       │   ├── result_store.py
│       │   └── comparator.py
│       └── api/
│           ├── __init__.py
│           └── evaluate.py
├── tests/
│   ├── __init__.py
│   ├── test_runner.py
│   ├── test_evaluator.py
│   └── test_integration.py
├── examples/
│   ├── mmlu_eval.py
│   └── gsm8k_eval.py
└── scripts/
    └── run_benchmark.sh
```

---

## 目录说明

### `src/eval_module/`

| 文件 | 说明 |
|------|------|
| `__init__.py` | 包初始化 |
| `main.py` | CLI 入口 |
| `config.py` | 配置加载 |
| `evaluator.py` | 评测器基类和主要实现 |
| `runners/` | 评测 runner 目录 |
| `datasets/` | 数据集管理 |
| `results/` | 结果存储和对比 |
| `api/` | API 端点 |

### `runners/`

| 文件 | 说明 |
|------|------|
| `base.py` | `BaseRunner` 抽象基类 |
| `lm_eval_runner.py` | lm-eval harness 集成 |
| `helm_runner.py` | Stanford HELM runner（参考） |

### `datasets/`

| 文件 | 说明 |
|------|------|
| `dataset_manager.py` | 数据集下载和管理 |
| `mmlu.py` | MMLU 数据集配置 |
| `gsm8k.py` | GSM8K 数据集配置 |

### `results/`

| 文件 | 说明 |
|------|------|
| `result_store.py` | 结果持久化（JSON） |
| `comparator.py` | 历史结果对比 |

---

## 关键文件内容概要

### `pyproject.toml`

```toml
[project]
name = "eval-module"
version = "0.1.0"
requires-python = ">=3.10"

dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.30.0",
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
    "pyyaml>=6.0",
    "httpx>=0.27.0",
    "lm-eval>=0.4.0",
    "jsonpickle>=3.0.0",
]
```

### `config.yaml`

```yaml
eval:
  backend: "lm-eval"  # lm-eval | helm
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

results:
  output_dir: "./results"
  format: "json"
```

---

## 与 MVP 设计（T303）的差异

| 维度 | T303 MVP | T803（本版） |
|------|---------|-------------|
| Runner 分离 | 提到 runner | 独立 `runners/` 目录 |
| 数据集管理 | 未提 | 独立 `datasets/` 目录 |
| 结果管理 | 提到 results | 独立 `results/` 目录 |
| Config 分离 | 未提 | 独立 `config.yaml` |
| Scripts | 未提 | 新增 `scripts/` |

---

Sources:
1. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval

Risk of Staleness:
- lm-eval 版本更新可能改变 API

Out of Scope Kept:
- 未写 LLM-as-Judge 实现
- 未写评测结果数据库
