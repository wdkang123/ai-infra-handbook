# eval-module Scaffold Manifest

## Task ID: T903
## Title: eval-module Scaffold Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T803 repo layout、API contract、config surface、test plan、validation checklist（已收紧为 T813），产出脚手架输入模板。

---

# eval-module Scaffold Manifest

## 概述

本文档定义 eval-module 脚手架的输入清单。

## 脚手架文件清单

| 序号 | 文件路径（蓝图） | 对应文件 | 说明 |
|------|----------------|----------|------|
| 1 | `eval-module/pyproject.toml` | `pyproject.toml` | 项目元数据和依赖 |
| 2 | `eval-module/.env.example` | `.env.example` | 环境变量模板 |
| 3 | `eval-module/Makefile` | `Makefile` | 构建和运行入口 |
| 4 | `eval-module/scripts/run_benchmark.sh` | `scripts/run_benchmark.sh` | benchmark 运行脚本 |
| 5 | `eval-module/tests/conftest.py` | `tests/conftest.py` | pytest fixture |
| 6 | `eval-module/tests/fixtures/` | `tests/fixtures/` | 测试 fixture |
| 7 | `eval-module/examples/sample_results/` | `examples/sample_results/` | 结果样例目录 |

## pyproject.toml 依赖组

基础依赖已在 `[project.dependencies]`，安装即包含核心运行时。

| 组名 | 依赖 | 用途 |
|------|------|------|
| `test` | pytest, pytest-asyncio, pytest-cov, httpx, pytest-mock | 测试 |
| `dev` | ruff, mypy, pre-commit | 开发工具 |

## 关键 CLI 入口

```bash
# 安装（从 eval-module/ 目录执行）
pip install -e "."

# 开发安装
pip install -e ".[test,dev]"

# 运行 MMLU 评测
eval-module run --task mmlu --model Qwen/Qwen2.5-0.5B-Instruct --num-fewshot 5

# 对比结果
eval-module compare --baseline ./results/baseline.json --candidate ./results/candidate.json

# 运行测试
pytest tests/ -v
```

## 目录结构（蓝图）

```
eval-module/
├── pyproject.toml
├── .env.example
├── Makefile
├── config.yaml
├── src/
│   └── eval_module/
│       ├── __init__.py
│       ├── main.py          # CLI 入口
│       ├── config.py        # 配置加载
│       ├── evaluator.py     # 评测器
│       ├── runners/
│       │   ├── base.py
│       │   └── lm_eval_runner.py
│       ├── datasets/
│       │   └── dataset_manager.py
│       └── results/
│           ├── result_store.py
│           └── comparator.py
├── tests/
│   ├── conftest.py
│   ├── fixtures/
│   │   ├── mmlu_result.json
│   │   └── gsm8k_result.json
│   └── test_runner.py
├── examples/
│   └── sample_results/
│       ├── mmlu_sample.json
│       └── comparison_sample.json
└── scripts/
    └── run_benchmark.sh
```

## 与 inference-service 的集成点

- eval-module 通过 lm-eval 的 vLLM backend 调用 `http://localhost:8000/v1`
- `EVAL_BACKEND_BASE_URL` 必须指向 inference-service

## 关键实现里程碑

| 里程碑 | 产出 | 验证 |
|--------|------|------|
| M1: CLI 可执行 | `eval-module run --help` 正常 | T803 validation checklist |
| M2: MMLU 可跑 | accuracy 分数返回 | `examples/sample_results/` |
| M3: GSM8K 可跑 | accuracy 分数返回 | 同上 |
| M4: 结果可对比 | `eval-module compare` 正常 | T803 validation checklist |

---

Sources:
1. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval
2. https://github.com/EleutherAI/lm-evaluation-harness/tree/main/lm_eval/tasks — lm-eval tasks

Risk of Staleness:
- lm-eval 版本更新可能改变 CLI 参数和行为

Out of Scope Kept:
- 未写 LLM-as-Judge 评测
- 未写 HTTP API 端点
