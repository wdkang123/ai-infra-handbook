# eval-module Validation Matrix v1

## Task ID: T1203
## Title: eval-module Implementation Map Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# eval-module Validation Matrix

本文档定义 eval-module 各 patch 的验收测试矩阵。

## Validation Matrix

| ID | 命令 | 场景 | 预期结果 | 验证命令 | 依赖 Patch |
|---|---|---|---|---|---|
| E01 | `eval-module run` | MMLU 基本运行 | result JSON 存在 | `python -m eval_module.main run --task mmlu ...` | P2 |
| E02 | `eval-module run` | GSM8K 基本运行 | result JSON 存在 | `python -m eval_module.main run --task gsm8k ...` | P2 |
| E03 | `eval-module run` | HumanEval 基本运行 | result JSON 存在 | `python -m eval_module.main run --task humaneval ...` | P2 |
| E04 | `eval-module run` | 指定 num_fewshot | JSON 含正确 num_fewshot | `--num-fewshot 3` → JSON num_fewshot=3 | P2 |
| E05 | `eval-module run` | 指定 limit | JSON num_samples ≤ limit | `--limit 10` → JSON num_samples=10 | P2 |
| E06 | `eval-module run` | 指定 output 路径 | 文件存在 | `--output /tmp/test.json` | P2 |
| E07 | `eval-module compare` | 两个结果对比 | diff JSON 含 delta | `compare --baseline a.json --candidate b.json` | P4 |
| E08 | `eval-module list-tasks` | 列出任务 | 含 mmlu/gsm8k/humaneval | `list-tasks` | P1 |
| E09 | `ResultStore.save/load` | JSON 持久化 roundtrip | 数据不变 | Python test | P3 |
| E10 | `eval-module run` | backend unavailable | 优雅错误 | inference-service 停机时运行 | P2 |

---

## E01-E03: run 命令验证

```bash
# E01: MMLU
python -m eval_module.main run \
  --task mmlu \
  --model Qwen2.5-0.5B-Instruct \
  --backend-url http://localhost:8000/v1 \
  --num-fewshot 5 \
  --output /tmp/mmlu_result.json

# 检查输出
python -c "
import json
with open('/tmp/mmlu_result.json') as f:
    r = json.load(f)
print('task:', r['task'])
print('accuracy:', r['accuracy'])
print('num_samples:', r['num_samples'])
print('backend:', r['backend'])  # 期望: 'vllm'（不是 URL）
"
```

**期望 JSON（对齐 EvalResult）：**
```json
{
  "task": "mmlu",
  "model": "Qwen2.5-0.5B-Instruct",
  "accuracy": 0.4844,
  "num_samples": 450,
  "num_fewshot": 5,
  "timestamp": "...",
  "lm_eval_version": "0.4.7",
  "backend": "vllm",
  "metrics": {"pass@1": 0.4844, "accuracy": 0.4844},
  "raw_output": null
}
```

**对应 fixture：** T1103 `mmlu_result_sample.json`

---

## E07: compare 命令验证

```bash
python -m eval_module.main compare \
  --baseline /tmp/baseline.json \
  --candidate /tmp/candidate.json \
  --output /tmp/compare_report.json

python -c "
import json
with open('/tmp/compare_report.json') as f:
    r = json.load(f)
print('baseline accuracy:', r['baseline']['accuracy'])
print('candidate accuracy:', r['candidate']['accuracy'])
print('delta:', r['delta']['accuracy_absolute'])
"
```

**期望 JSON（对齐 T1103 compare report）：**
```json
{
  "compare_id": "...",
  "timestamp": "...",
  "baseline": { "task": "gsm8k", "model": "...", "accuracy": 0.3512, ... },
  "candidate": { "task": "gsm8k", "model": "...", "accuracy": 0.4026, ... },
  "delta": {
    "accuracy_absolute": 0.0514,
    "accuracy_relative_pct": 14.64
  }
}
```

**对应 fixture：** T1103 `gsm8k_compare_report.json`

---

## E09: ResultStore roundtrip

```python
# tests/test_result_store.py
from eval_module.results import EvalResult, ResultStore
from pathlib import Path

def test_save_load_roundtrip(tmp_path):
    original = EvalResult(
        task="gsm8k",
        model="test-model",
        accuracy=0.4,
        num_samples=100,
        num_fewshot=0,
        timestamp="2026-01-01T00:00:00Z",
        lm_eval_version="0.4.7",
        backend="vllm",
        metrics={"pass@1": 0.4},
        raw_output=None,
    )
    store = ResultStore()
    path = tmp_path / "result.json"
    store.save(original, path)
    loaded = store.load(path)
    assert loaded.task == original.task
    assert loaded.accuracy == original.accuracy
    assert loaded.metrics == original.metrics
```

---

Sources:
- T1003: main.py, runner blueprint (corrected: backend is string type)
- T1103: result JSON samples, compare report samples
- T303: accepted MVP design
- T813: accepted validation checklist

Risk of Staleness:
- CLI and result format are project-internal; lm-eval stable
