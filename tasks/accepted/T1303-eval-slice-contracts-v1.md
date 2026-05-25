# eval-module Slice Contracts v1

## Task ID: T1303
## Title: eval-module Execution Slice Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# eval-module Slice Contracts

本文档定义每个 slice 的具体目标、入口、验收命令、前置条件和完成信号。

---

## E1: 包骨架 + CLI

**目标文件：**
- `pyproject.toml`
- `src/eval_module/__init__.py`
- `src/eval_module/__version__.py`
- `src/eval_module/main.py`
- `.env.example`

**入口：** `python -m eval_module.main --help`

**验收命令：**
```bash
cd eval-module
python -m eval_module.main --help
# 期望：显示 run / compare / list-tasks 三个子命令

python -m eval_module.main run --help
# 期望：显示 --task / --model / --num-fewshot 等参数

python -m eval_module.main list-tasks --help
# 期望：显示 list-tasks 命令
```

**前置条件：** 无

**完成信号：** Typer CLI 骨架可运行，三个子命令均可见

**Cut Line：** 不实现 runner、result store、comparator

---

## E2: Runner

**目标文件：**
- `src/eval_module/runners/__init__.py`
- `src/eval_module/runners/lm_eval_runner.py`

**入口：** 直接 import 或 E5 CLI 调用

**验收命令：**
```bash
# 实例化
cd eval-module
python -c "
from eval_module.runners.lm_eval_runner import LmEvalRunner
backend_config = {
    'type': 'vllm',
    'base_url': 'http://localhost:8000/v1',
}
r = LmEvalRunner(backend_config)
print('Instantiation OK')
"

# list_tasks
python -c "
from eval_module.runners.lm_eval_runner import LmEvalRunner
backend_config = {'type': 'vllm', 'base_url': 'http://localhost:8000/v1'}
r = LmEvalRunner(backend_config)
tasks = r.list_tasks()
print('Tasks:', tasks[:3])
"

# run (需 inference-service 运行)
curl -s http://localhost:8000/health > /dev/null && \
python -c "
from eval_module.runners.lm_eval_runner import LmEvalRunner
backend_config = {'type': 'vllm', 'base_url': 'http://localhost:8000/v1'}
r = LmEvalRunner(backend_config)
result = r.run('mmlu', 'Qwen/Qwen2.5-0.5B-Instruct', num_fewshot=5)
print('Result task:', result.task)
print('Result backend:', result.backend)
"
# 期望：mmlu accuracy 值
```

**前置条件：** E1 完成

**完成信号：** `LmEvalRunner` 可实例化，`list_tasks()` 返回非空列表

**Cut Line：** 不实现 result store、comparator

---

## E3: Result Store

**目标文件：**
- `src/eval_module/results/__init__.py`
- `src/eval_module/results/result_store.py`

**入口：** 直接 import

**验收命令：**
```bash
cd eval-module
python -c "
from eval_module.results.result_store import ResultStore
from eval_module.runners.lm_eval_runner import EvalResult
import tempfile, os, json

store = ResultStore()
tmp = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
tmp.close()

# save (EvalResult dataclass → JSON)
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
print('Save OK:', os.path.exists(tmp.name))

# load (JSON → EvalResult dataclass)
loaded = store.load(tmp.name)
print('Load OK:', loaded.task)
assert loaded.task == 'mmlu'
assert loaded.backend == 'vllm'

os.unlink(tmp.name)
"
```

**前置条件：** E1 完成

**完成信号：** `save()` 和 `load()` 成功，JSON 格式正确

**Cut Line：** 不实现 comparator

---

## E4: Comparator

**目标文件：**
- `src/eval_module/results/comparator.py`

**入口：** 直接 import 或 E5 CLI `compare` 子命令调用

**验收命令：**
```bash
cd eval-module
python -c "
from eval_module.results.comparator import Comparator
from eval_module.runners.lm_eval_runner import EvalResult

baseline = EvalResult(
    task='mmlu', model='Qwen/Qwen2.5-0.5B-Instruct',
    accuracy=0.5, num_samples=14242, num_fewshot=5,
    timestamp='2026-04-08T00:00:00Z', lm_eval_version='0.4.3',
    backend='vllm', metrics={'mmlu': 0.5}
)
candidate = EvalResult(
    task='mmlu', model='Qwen/Qwen2.5-0.5B-Instruct',
    accuracy=0.55, num_samples=14242, num_fewshot=5,
    timestamp='2026-04-08T01:00:00Z', lm_eval_version='0.4.3',
    backend='vllm', metrics={'mmlu': 0.55}
)

comp = Comparator()
diff = comp.compare(baseline, candidate)
print('Diff:', diff)
assert diff['delta']['accuracy'] == 0.05
print('Comparator OK')
"
```

**前置条件：** E3 完成

**完成信号：** `compare()` 返回 diff dict，`delta` 计算正确

**Cut Line：** 不写 LLM-as-Judge

---

## E5: CLI 命令完整化

**目标文件：**
- `src/eval_module/main.py`（修改）

**入口：** `python -m eval_module.main`

**验收命令：**
```bash
# run 子命令
python -m eval_module.main run --help
# 期望：--task / --model / --num-fewshot / --output 等参数

# compare 子命令
python -m eval_module.main compare --help
# 期望：--baseline / --candidate / --output 等参数

# list-tasks 子命令
python -m eval_module.main list-tasks
# 期望：mmlu / gsm8k 等任务列表
```

**前置条件：** E2 + E3 完成

**完成信号：** 三个子命令均可执行，参数解析正确

**Cut Line：** 不实现 interactive 模式

---

## E6: 测试骨架

**目标文件：**
- `tests/__init__.py`
- `tests/conftest.py`
- `tests/test_runner.py`

**入口：** `pytest tests/ -v`

**验收命令：**
```bash
cd eval-module
pytest tests/ -v
# 期望：所有测试通过
```

**前置条件：** E2 完成

**完成信号：** pytest 全部通过

**Cut Line：** 不写集成测试（属于 root integration）

---

Sources:
- T1003: accepted starter manifest
- T1103: fixture assets
- T813: accepted validation checklist
- T1203: accepted implementation map
