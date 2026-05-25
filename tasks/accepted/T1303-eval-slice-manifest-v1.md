# eval-module Slice Manifest v1

## Task ID: T1303
## Title: eval-module Execution Slice Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# eval-module Execution Slice Manifest

本文档索引 eval-module 的所有 execution slices，供 Codex 编码时参照。

## Slice 总览

| Slice ID | 名称 | 目标文件 | 验证入口 | 前置条件 |
|---|---|---|---|---|
| E1 | 包骨架 + CLI | `main.py / pyproject.toml` | `python -m eval_module.main run --help` | 无 |
| E2 | Runner | `runners/lm_eval_runner.py` | `run("mmlu")` 返回 EvalResult | E1 |
| E3 | Result Store | `results/result_store.py` | `save()` + `load()` 成功 | E1 |
| E4 | Comparator | `results/comparator.py` | `compare()` 返回 diff | E3 |
| E5 | CLI 命令完整化 | `main.py`（修改：`run / compare / list-tasks`） | 三个子命令均可用 | E2 + E3 |
| E6 | 测试骨架 | `tests/conftest.py / tests/test_runner.py` | `pytest tests/` | E2 |

---

## Slice 覆盖范围

| 主线 | 覆盖 Slice |
|---|---|
| CLI 入口 | E1, E5 |
| Runner（lm-eval） | E2, E6 |
| Result Store | E3 |
| Comparator | E4 |
| CLI 完整化 | E5 |

---

## Cut Line

以下内容不进入当前 slice 集合：
- `/v1/completions`（后续扩展）
- `/v1/models`（后续扩展）
- LLM-as-Judge 评测
- 自动化 benchmark 脚本（由 T1003 提供 `scripts/run_benchmark.sh`）

---

Sources:
- T1003: accepted starter manifest
- T1103: fixture assets
- T303: accepted MVP design
- T813: accepted validation checklist
- T1203: accepted implementation map

Risk of Staleness:
- lm-eval API 在 0.4.x 相对稳定，但 major version 可能 breaking change
