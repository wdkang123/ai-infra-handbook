# eval-module Import Map v1

## Task ID: T1203
## Title: eval-module Implementation Map Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# eval-module Import Dependency Map

本文档定义 `eval-module` 内部模块的导入依赖关系。

## Import Map

```
src/eval_module/
│
├── __init__.py
├── __version__.py             # 纯常量，无依赖
│
├── main.py                    # Typer CLI 入口
│   ├── import typer
│   ├── import rich.console, rich.table
│   ├── from .runners.lm_eval_runner import LmEvalRunner
│   └── from .results.result_store import ResultStore
│
├── results/
│   ├── __init__.py
│   │
│   ├── result_store.py        # 加载/保存 JSON（可选扩展）
│   │   ├── from pathlib import Path
│   │   ├── import json
│   │   └── from ..runners.lm_eval_runner import EvalResult
│   │
│   └── comparator.py          # 对比两个 EvalResult（可选扩展）
│       └── from ..runners.lm_eval_runner import EvalResult
│
└── runners/
    ├── __init__.py
    └── lm_eval_runner.py      # 封装 lm-eval，含 EvalResult dataclass
        ├── from dataclasses import dataclass, field
        ├── from typing import Any, Optional
        └── import lm_eval.api  # lm-evaluation-harness
```

## External Dependencies

| 模块 | 外部依赖 | 版本 |
|---|---|---|
| `main.py` | `typer`, `rich` | ≥0.9 |
| `lm_eval_runner.py` | `lm-eval` | ≥0.4.7 |
| `result_store.py` | 无外部依赖 | — |
| `comparator.py` | 无外部依赖 | — |

## CLI 命令流

```
main.py (Typer app)
  │
  ├── run → LmEvalRunner.run(task, model, num_fewshot)
  │              ├── lm_eval.api.make_bsr_task()
  │              ├── lm_eval.api.Evaluator.evaluate()
  │              └── → EvalResult
  │       → ResultStore.save(result, output_path)
  │
  ├── compare → ResultStore.load(baseline)
  │              → ResultStore.load(candidate)
  │              → Comparator.compare(baseline, candidate)
  │              → diff dict
  │       → ResultStore.save_comparison(diff, output_path)
  │
  └── list_tasks → LmEvalRunner.list_tasks()
```

---

Sources:
- T1003: main.py, runner blueprint
- T1103: result JSON samples (corrected: EvalResult fields)
- T303: accepted MVP design

Risk of Staleness:
- Import pattern follows lm-eval + Typer project structure; stable
