# eval-module Task Cards v1

## Task ID: T1403
## Title: eval-module Codex Task Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# eval-module Task Cards

本文档定义每个任务卡的具体输入资产、目标文件、验收命令、完成信号和 cut line。

---

## T1403-T01: 包骨架 + CLI

**Task Name:** 包骨架 + CLI

**对应 Slice:** E1

**输入资产：**
- `T1003-eval-starter-manifest.md`
- `T1003-eval-main-py-blueprint-v1.md`

**目标文件：**
```
eval-module/
├── pyproject.toml
├── src/eval_module/
│   ├── __init__.py
│   ├── __version__.py
│   └── main.py
├── .env.example
```

**验收命令：**
```bash
cd eval-module
python -m eval_module.main --help
# 期望：显示 run / compare / list-tasks 三个子命令
```

**完成信号：** Typer CLI 骨架可运行，三个子命令均可见

**Cut Line：** 不实现 runner、result store

---

## T1403-T02: Result Store

**Task Name:** Result Store

**对应 Slice:** E3

**输入资产：**
- `T1003-eval-result-store-py-blueprint-v1.md`
- `T1403-T01/`

**目标文件：**
```
eval-module/src/eval_module/results/
├── __init__.py
└── result_store.py
```

**验收命令：**
```bash
cd eval-module
python -c "
from eval_module.results.result_store import ResultStore
from eval_module.runners.lm_eval_runner import EvalResult
import tempfile, os

store = ResultStore()
tmp = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
tmp.close()

result = EvalResult(
    task='mmlu',
    model='Qwen/Qwen2.5-0.5B-Instruct',
    accuracy=0.5,
    num_samples=14242,
    num_fewshot=5,
    timestamp='2026-04-08T00:00:00Z',
    lm_eval_version='0.4.3',
    backend='vllm',
    metrics={'mmlu': 0.5},
)
store.save(result, tmp.name)
loaded = store.load(tmp.name)
assert loaded.task == 'mmlu'
assert loaded.backend == 'vllm'
os.unlink(tmp.name)
print('ResultStore OK')
"
```

**完成信号：** `save()` 和 `load()` 成功处理 `EvalResult` dataclass

**Cut Line：** 不实现 comparator

---

## T1403-T03: LmEvalRunner

**Task Name:** LmEvalRunner

**对应 Slice:** E2

**输入资产：**
- `T1003-eval-runner-py-blueprint-v1.md`
- `T1403-T01/`

**目标文件：**
```
eval-module/src/eval_module/runners/
├── __init__.py
└── lm_eval_runner.py
```

**验收命令：**
```bash
cd eval-module
python -c "
from eval_module.runners.lm_eval_runner import LmEvalRunner
backend_config = {'type': 'vllm', 'base_url': 'http://localhost:8000/v1'}
r = LmEvalRunner(backend_config)
print('Instantiation OK')
"

python -c "
from eval_module.runners.lm_eval_runner import LmEvalRunner
backend_config = {'type': 'vllm', 'base_url': 'http://localhost:8000/v1'}
r = LmEvalRunner(backend_config)
tasks = r.list_tasks()
print('Tasks:', tasks[:3])
assert 'mmlu' in tasks
"
```

**完成信号：** `LmEvalRunner` 可实例化，`list_tasks()` 返回非空列表

**Cut Line：** 不实现 result store、comparator

---

## T1403-T04: CLI 命令完整化

**Task Name:** CLI 命令完整化

**对应 Slice:** E5

**输入资产：**
- `T1003-eval-main-py-blueprint-v1.md`
- `T1403-T02/` + `T1403-T03/`

**目标文件：**
```
eval-module/src/eval_module/
└── main.py（修改）
```

**验收命令：**
```bash
cd eval-module

python -m eval_module.main run --help
# 期望：--task / --model / --num-fewshot / --output 等参数

python -m eval_module.main compare --help
# 期望：--baseline / --candidate / --output 等参数

python -m eval_module.main list-tasks
# 期望：mmlu / gsm8k 等任务列表
```

**完成信号：** 三个子命令均可执行，参数解析正确

**Cut Line：** 不实现 interactive 模式

---

Sources:
- T1003: accepted starter manifest
- T1103: fixture assets
- T1303: accepted execution slice
- T813: accepted validation checklist
