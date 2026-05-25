# eval-module Starter File Manifest

## Task ID: T1003
## Title: eval-module Starter File Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T903 scaffold blueprints（T903 pyproject / runner-cli / test-fixture / sample-results），产出 eval-module 源码蓝图文件。

---

# eval-module Starter File Manifest

## 概述

本文档索引 eval-module 的所有 starter file 蓝图，供 Codex 实施时参照。

## 蓝图文件清单

| 序号 | 文件路径（蓝图） | 对应真实文件 | 说明 |
|------|----------------|-------------|------|
| 1 | `T1003-eval-main-py-blueprint-v1.md` | `src/eval_module/main.py` | Typer CLI 入口 |
| 2 | `T1003-eval-runner-py-blueprint-v1.md` | `src/eval_module/runners/lm_eval_runner.py` | lm-eval runner |
| 3 | `T1003-eval-result-store-py-blueprint-v1.md` | `src/eval_module/results/result_store.py` | 结果持久化 |
| 4 | `T1003-eval-conftest-py-blueprint-v1.md` | `tests/conftest.py` | pytest fixtures |
| 5 | `T1003-eval-test-runner-py-blueprint-v1.md` | `tests/test_runner.py` | runner 单元测试 |
| 6 | `T1003-eval-run-benchmark-sh-blueprint-v1.md` | `scripts/run_benchmark.sh` | benchmark 启动脚本 |
| 7 | (沿用 T903 scaffold) | `scripts/serve.sh` | 启动脚本（沿用 T903 runner-cli blueprint） |

## 源码目录结构（蓝图）

```
eval-module/
├── src/
│   └── eval_module/
│       ├── __init__.py
│       ├── main.py              # Typer CLI
│       ├── evaluator.py         # 评测器（门面）
│       ├── runners/
│       │   ├── __init__.py
│       │   └── lm_eval_runner.py # lm-eval 封装
│       └── results/
│           ├── __init__.py
│           ├── result_store.py   # 结果持久化
│           └── comparator.py     # 结果对比
├── tests/
│   ├── conftest.py
│   ├── test_runner.py
│   └── test_result_store.py
├── scripts/
│   └── run_benchmark.sh
├── examples/
│   └── sample_results/
├── pyproject.toml
├── .env.example
└── config.yaml
```

## MVP CLI 命令

| 命令 | 说明 |
|------|------|
| `eval-module run --task mmlu --model Qwen/Qwen2.5-0.5B-Instruct` | 运行 MMLU |
| `eval-module compare --baseline x.json --candidate y.json` | 对比结果 |
| `eval-module list-tasks` | 列出可用任务 |

## 与 inference-service 集成

- eval-module 通过 HTTP 调用 `http://localhost:8000/v1` 进行推理
- 不需要 GPU（lm-eval 通过 vLLM API 评测）

---

Sources:
1. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval
2. https://typer.tiangolo.com/ — Typer

Risk of Staleness:
- lm-eval API 在 0.4.x 相对稳定
