# eval-module Task Pack Manifest v1

## Task ID: T1403
## Title: eval-module Codex Task Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# eval-module Task Pack Manifest

本文档索引 eval-module 的所有 Codex 实现任务卡。

## 任务卡清单

| Task ID | 任务名称 | 输入资产 | 目标文件 | 验证入口 |
|---|---|---|---|---|
| T1403-T01 | 包骨架 + CLI | T1003 starter manifest | `main.py / pyproject.toml` | `python -m eval_module.main --help` |
| T1403-T02 | Result Store | T1003 result_store blueprint + T1403-T01 | `results/result_store.py` | `save()` + `load()` 成功 |
| T1403-T03 | LmEvalRunner | T1003 runner blueprint + T1403-T01 | `runners/lm_eval_runner.py` | `run("mmlu")` 返回 EvalResult |
| T1403-T04 | CLI 命令完整化 | T1003 main.py blueprint + T1403-T02 + T1403-T03 | `main.py`（修改） | `run / compare / list-tasks` 均可用 |

---

## 与 Slice 的对应关系

| Task ID | 对应 Slice |
|---|---|
| T1403-T01 | E1 |
| T1403-T02 | E3 |
| T1403-T03 | E2 |
| T1403-T04 | E5 |

---

## Cut Line

以下内容不进入当前 task pack：
- Comparator（E4）
- 测试骨架（E6）
- LLM-as-Judge

---

Sources:
- T1003: accepted starter manifest
- T1103: fixture assets
- T1303: accepted execution slice
- T303: accepted MVP design
- T813: accepted validation checklist
