# eval-module File Order v1

## Task ID: T1203
## Title: eval-module Implementation Map Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# eval-module File Implementation Order

本文档定义 `eval-module/` 目录的编码实现顺序，基于 accepted `T1003 / T1103 / T303 / T813` blueprints。

## 文件实现顺序

### Phase 0: 骨架

| Order | 文件路径 | 目的 | 依赖 |
|---|---|---|---|
| 0.1 | `src/__init__.py` | 包声明 | 无 |
| 0.2 | `src/eval_module/__init__.py` | 模块命名空间 | 无 |
| 0.3 | `src/eval_module/__version__.py` | `__version__` | 无 |
| 0.4 | `pyproject.toml` | 项目元数据 | 无 |
| 0.5 | `src/eval_module/results/__init__.py` | results 子包 | 无 |
| 0.6 | `src/eval_module/runners/__init__.py` | runners 子包 | 无 |

### Phase 1: 结果持久化（可选扩展）

| Order | 文件路径 | 目的 | 依赖 |
|---|---|---|---|
| 1.1 | `src/eval_module/results/result_store.py` | ResultStore（加载/保存 JSON） | Phase 0 |

**实现要点：** `result_store.py` 为可选扩展，对齐 T1103 fixture。`EvalResult` dataclass 实际定义在 `runners/lm_eval_runner.py`（Phase 2）。

### Phase 2: lm-evaluation-harness Runner

| Order | 文件路径 | 目的 | 依赖 |
|---|---|---|---|
| 2.1 | `src/eval_module/runners/lm_eval_runner.py` | LmEvalRunner 类 + EvalResult dataclass | Phase 0 |
| 2.2 | `src/eval_module/runners/__init__.py` | 导出 runner | Phase 2.1 |

**实现要点：** 来自 accepted `T1003-eval-runner-py-blueprint-v1.md`，封装 `lm_eval.api.Evaluator`，提供 `run(task, model, num_fewshot)` 方法，返回 `EvalResult`（定义在同一文件）。

### Phase 3: CLI 入口

| Order | 文件路径 | 目的 | 依赖 |
|---|---|---|---|
| 3.1 | `src/eval_module/main.py` | Typer CLI（run/compare/list-tasks） | Phase 2 |

**实现要点：** 来自 accepted `T1003-eval-main-py-blueprint-v1.md`。三个命令：
- `run`: 调用 `LmEvalRunner.run()`
- `compare`: 调用 `Comparator.compare()`
- `list-tasks`: 调用 `LmEvalRunner.list_tasks()`

### Phase 4: Comparator（可选扩展）

| Order | 文件路径 | 目的 | 依赖 |
|---|---|---|---|
| 4.1 | `src/eval_module/results/comparator.py` | Comparator 类 | Phase 2 |

**实现要点：** `compare(baseline_result, candidate_result)` → diff dict（accuracy_absolute, accuracy_relative_pct）。Phase 4 为可选扩展，不是 MVP 必须。

### Phase 5: 基准测试脚本

| Order | 文件路径 | 目的 | 依赖 |
|---|---|---|---|
| 5.1 | `scripts/run_benchmark.sh` | 快速运行基准测试脚本 | Phase 3 |
| 5.2 | `configs/task_presets/mmlu.yaml` | MMLU 任务预设 | Phase 0 |
| 5.3 | `configs/task_presets/gsm8k.yaml` | GSM8K 任务预设 | Phase 0 |
| 5.4 | `configs/task_presets/humaneval.yaml` | HumanEval 任务预设 | Phase 0 |

**实现要点：** T1103 `T1103-eval-task-presets-v1.md` 为预设文件蓝本。

### Phase 6: 测试骨架

| Order | 文件路径 | 目的 | 依赖 |
|---|---|---|---|
| 6.1 | `tests/__init__.py` | 测试包 | 无 |
| 6.2 | `tests/conftest.py` | pytest fixtures | Phase 3 |
| 6.3 | `tests/test_runner.py` | runner 单元测试 | Phase 2 + 6.2 |
| 6.4 | `tests/test_result_store.py` | result store 测试 | Phase 1 + 6.2 |

---

## 目录结构

```
eval-module/
├── src/eval_module/
│   ├── __init__.py
│   ├── __version__.py
│   ├── main.py               ← Phase 3 (CLI)
│   ├── runners/
│   │   ├── __init__.py
│   │   └── lm_eval_runner.py  ← Phase 2 (含 EvalResult dataclass)
│   └── results/              ← 可选扩展
│       ├── __init__.py
│       ├── result_store.py    ← Phase 1 (optional)
│       └── comparator.py     ← Phase 4 (optional)
├── configs/
│   └── task_presets/
│       ├── mmlu.yaml         ← Phase 5
│       ├── gsm8k.yaml       ← Phase 5
│       └── humaneval.yaml     ← Phase 5
├── scripts/
│   └── run_benchmark.sh       ← Phase 5
├── tests/
│   ├── __init__.py
│   ├── conftest.py           ← Phase 6
│   └── test_runner.py         ← Phase 6
├── pyproject.toml             ← Phase 0
└── .env.example               ← Phase 0
```

---

Sources:
- T1003: main.py, runner blueprint
- T1103: task presets, result JSON samples
- T303: accepted MVP design
- T813: accepted validation checklist

Risk of Staleness:
- Phase ordering follows lm-eval + Typer project structure; stable
