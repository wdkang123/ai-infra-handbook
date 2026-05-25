# eval-module Patch Split v1

## Task ID: T1203
## Title: eval-module Implementation Map Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# eval-module Patch Split Proposal

本文档定义 eval-module 的分批实现顺序。

## Patch 批次概览

| Patch | 名称 | 目标文件 | 验证方式 |
|---|---|---|---|
| P0 | 骨架 | `pyproject.toml / __init__.py / results/__init__.py` | `from eval_module.runners.lm_eval_runner import EvalResult` |
| P1 | CLI 骨架 | `main.py`（run/compare/list-tasks mock） | `--help` 输出正确 |
| P2 | lm-eval Runner | `runners/lm_eval_runner.py` | 真实评测（非流式） |
| P3 | ResultStore（可选） | `result_store.py` | 保存/加载 JSON roundtrip |
| P4 | Comparator（可选） | `comparator.py` | compare 两个 result JSON |
| P5 | 脚本 | `scripts/run_benchmark.sh` | `./scripts/run_benchmark.sh mmlu` |
| P6 | 测试骨架 | `tests/conftest.py / test_runner.py` | `pytest tests/` |

---

## Patch 0: 骨架

**文件：**
- `pyproject.toml`
- `src/eval_module/__init__.py`
- `src/eval_module/__version__.py`
- `src/eval_module/results/__init__.py`
- `src/eval_module/runners/__init__.py`

**验证：**
```bash
cd eval-module
python -c "from eval_module.runners.lm_eval_runner import EvalResult, LmEvalRunner; print('OK')"
```

---

## Patch 1: CLI 骨架

**文件：**
- `src/eval_module/main.py`（mock 实现，不调真实 lm-eval）

**验证：**
```bash
python -m eval_module.main --help
# 期望：usage: eval_module.main [-h] {run,compare,list-tasks} ...

python -m eval_module.main list-tasks
# 期望：Available benchmark tasks...

python -m eval_module.main run --help
# 期望：--task, --model, --backend-url, --num-fewshot, --output

python -m eval_module.main compare --help
# 期望：--baseline, --candidate, --output
```

---

## Patch 2: lm-eval Runner（核心）

**文件：**
- `src/eval_module/runners/__init__.py`
- `src/eval_module/runners/lm_eval_runner.py`
- `main.py`（修改：调用真实 runner）

**实现要点：**
```python
class LmEvalRunner:
    def __init__(self, backend_config: dict[str, Any]):
        self.backend_type = backend_config.get("type", "vllm")
        self.base_url = backend_config.get("base_url", "http://localhost:8000/v1")

    def run(self, task: str, model: str, num_fewshot: int = 5) -> EvalResult:
        # 调用 lm_eval.api.evaluator_with_logprobs()
        # 返回 EvalResult
```

**验证：**
```bash
# 需要 inference-service 运行
python -m eval_module.main run \
  --task gsm8k \
  --model Qwen2.5-0.5B-Instruct \
  --backend-url http://localhost:8000/v1 \
  --num-fewshot 0 \
  --output ./results/gsm8k_result.json
# 期望：./results/gsm8k_result.json 存在且格式正确
```

**对应 fixture：** T1103 `T1103-eval-result-json-samples-v1.md`

---

## Patch 3: ResultStore

**文件：**
- `src/eval_module/results/result_store.py`

**验证：**
```bash
python -c "
from eval_module.results import EvalResult, ResultStore
from pathlib import Path
r = EvalResult(task='mmlu', model='test', accuracy=0.5, num_samples=100, num_fewshot=5, timestamp='2026-01-01T00:00:00Z', lm_eval_version='0.4.7', backend='vllm', metrics={}, raw_output=None)
store = ResultStore()
store.save(r, Path('/tmp/test_result.json'))
loaded = store.load(Path('/tmp/test_result.json'))
print(loaded.task, loaded.accuracy)
# 期望：mmlu 0.5
"
```

---

## Patch 4: Comparator

**文件：**
- `src/eval_module/results/comparator.py`

**验证：**
```bash
python -c "
from eval_module.results import EvalResult, ResultStore, Comparator
b = EvalResult(task='gsm8k', model='base', accuracy=0.35, num_samples=100, num_fewshot=0, timestamp='2026-01-01T00:00:00Z', lm_eval_version='0.4.7', backend='vllm', metrics={}, raw_output=None)
c = EvalResult(task='gsm8k', model='finetuned', accuracy=0.40, num_samples=100, num_fewshot=0, timestamp='2026-01-01T01:00:00Z', lm_eval_version='0.4.7', backend='vllm', metrics={}, raw_output=None)
comp = Comparator()
diff = comp.compare(b, c)
print(diff)
# 期望：{'accuracy_absolute': 0.05, 'accuracy_relative_pct': 14.29}
"
```

**对应 fixture：** T1103 `T1103-eval-compare-report-samples-v1.md`

---

## Patch 5: 基准测试脚本

**文件：**
- `scripts/run_benchmark.sh`
- `configs/task_presets/*.yaml`

**验证：**
```bash
cd ai-infra
bash scripts/run_benchmark.sh mmlu \
  --model Qwen2.5-0.5B-Instruct \
  --backend-url http://localhost:8000/v1
# 期望：运行成功，生成 result JSON
```

---

## Patch 依赖关系图

```
P0 (骨架 + 数据模型)
  │
  ├── P1 (CLI 骨架)          ← 依赖 P0 的 import，但不调真实 runner
  │       │
  │       ├── P2 (lm-eval Runner) ← 依赖 P0，P1 中 run 命令调用真实 runner
  │       │
  │       └── P4 (Comparator)     ← 依赖 P0，P1 中 compare 命令调用
  │
  ├── P3 (ResultStore)        ← 独立可测试
  │
  └── P5 (scripts)           ← 依赖 P1+P2+P3
          │
          └── P6 (测试)        ← 依赖 P1~P5 全部
```

**注意：** P2 需要真实 GPU + inference-service 运行。P3/P4 可完全离线测试。

---

Sources:
- T1003: main.py, runner blueprint
- T1103: task presets, result JSON samples
- T303: accepted MVP design
- T813: accepted validation checklist

Risk of Staleness:
- lm-eval API stable since v0.4; patch ordering follows standard lm-eval project structure
