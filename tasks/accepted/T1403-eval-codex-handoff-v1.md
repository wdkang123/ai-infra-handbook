# eval-module Codex Handoff v1

## Task ID: T1403
## Title: eval-module Codex Task Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# eval-module Codex Handoff

本文档是可直接复制给 Codex 的任务卡 handoff 文本。

---

## T1403-T01: 包骨架 + CLI

**任务：** 为 `eval-module/` 创建 Typer CLI 骨架。

**main.py 要求：**
- 使用 Typer，三个子命令：`run`、`compare`、`list-tasks`
- `run` 命令参数：`--task`、`--model`、`--num-fewshot`、`--output`、`--backend-url`
- `compare` 命令参数：`--baseline`、`--candidate`、`--output`
- `list-tasks` 无需额外参数

**CLI 命令格式：**
```bash
eval-module run --task mmlu --model Qwen/Qwen2.5-0.5B-Instruct
eval-module compare --baseline results/baseline.json --candidate results/candidate.json
eval-module list-tasks
```

**禁止事项：** 不得在 T01 实现真实 runner/result store 调用

---

## T1403-T02: Result Store

**任务：** 实现 `results/result_store.py`。

**关键类：`ResultStore`**
- `__init__(output_dir="./results")` — 初始化存储目录
- `save(result: EvalResult, path)` — 将 `EvalResult` dataclass 序列化为 JSON
- `load(path)` — 从 JSON 反序列化为 `EvalResult` dataclass
- `save_comparison(diff, path)` — 保存对比报告

**EvalResult dataclass（来自 lm_eval_runner.py）：**
```python
@dataclass
class EvalResult:
    task: str
    model: str
    accuracy: float
    num_samples: int
    num_fewshot: int
    timestamp: str
    lm_eval_version: str
    backend: str  # "vllm"
    metrics: dict[str, float] = field(default_factory=dict)
```

**禁止事项：** 不实现 comparator（属于后续任务）

---

## T1403-T03: LmEvalRunner

**任务：** 实现 `runners/lm_eval_runner.py`。

**关键类：`LmEvalRunner`**
- `__init__(backend_config: dict)` — 接收 `{"type": "vllm", "base_url": "http://localhost:8000/v1"}`
- `list_tasks() -> list[str]` — 返回 `["mmlu", "gsm8k", "humaneval", ...]`
- `run(task, model, num_fewshot=5, limit=None, **kwargs) -> EvalResult` — 运行评测

**backend_config 参数：**
```python
{
    "type": "vllm",                          # or "openai"
    "base_url": "http://localhost:8000/v1", # 下游推理端点
    "api_key": ""                            # optional
}
```

**注意：** `run()` 在 placeholder 阶段可返回 mock EvalResult，但接口签名必须与蓝图一致。

**禁止事项：** 不实现 `compare()`（属于后续任务）

---

## T1403-T04: CLI 命令完整化

**任务：** 将 T02 和 T03 接入 `main.py` 的 CLI 子命令。

**run 子命令接入：**
- 调用 `LmEvalRunner(backend_config).run(task, model, num_fewshot, ...)`
- 调用 `ResultStore().save(result, output_path)`

**compare 子命令接入：**
- 当前只保持 `compare --help` 参数口径与 accepted `main.py` blueprint 一致
- 不在本 task pack 中实现 `Comparator()` 或真实 diff 逻辑
- 如需真实 comparison wiring，留待后续 E4/E5 扩展批次

**验证命令：**
```bash
python -m eval_module.main run --help
python -m eval_module.main compare --help
python -m eval_module.main list-tasks
```

---

Sources:
- T1003: accepted starter manifest
- T813: accepted validation checklist
- T1303: accepted execution slice
