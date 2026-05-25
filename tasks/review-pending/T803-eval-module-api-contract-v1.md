# eval-module API Contract v1

## Task ID: T803
## Task Title: eval-module Execution Prep Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T303 MVP 设计，准备 eval-module 实施前包。

---

# eval-module API Contract v1

## 概述

本文档定义 eval-module 的评测接口契约。

---

## 接口总览

| 接口 | 方法 | 说明 | MVP 必须 |
|------|------|------|---------|
| `evaluate()` | Python API | 运行 benchmark 评测 | 是 |
| `load_results()` | Python API | 加载历史结果 | 是 |
| `compare()` | Python API | 对比两个结果 | 是 |
| `/evaluate` | POST | HTTP API 评测入口 | 否 |

---

## Python API

### `Evaluator.evaluate()`

```python
from eval_module import Evaluator

evaluator = Evaluator(
    backend="lm-eval",
    backend_config={
        "type": "vllm",
        "base_url": "http://localhost:8000/v1"
    }
)

result = evaluator.evaluate(
    task="mmlu",
    model="Qwen/Qwen2.5-0.5B-Instruct",
    num_fewshot=5
)
```

### 返回值

```python
{
    "task": "mmlu",
    "model": "Qwen/Qwen2.5-0.5B-Instruct",
    "accuracy": 0.65,
    "num_samples": 14242,
    "timestamp": "2026-04-03T12:00:00Z",
    "version": "0.4.3"
}
```

---

## Runner 接口

### `BaseRunner`

```python
class BaseRunner(ABC):
    @abstractmethod
    def run(self, task: str, model: str, num_fewshot: int = 0, **kwargs) -> EvalResult:
        """运行单个 benchmark"""
        ...

    @abstractmethod
    def list_tasks(self) -> List[str]:
        """列出可用 tasks"""
        ...
```

### `LmEvalRunner`

```python
class LmEvalRunner(BaseRunner):
    def run(self, task: str, model: str, num_fewshot: int = 0, **kwargs) -> EvalResult:
        # 调用 lm_eval API
        results = lm_eval(
            model="vllm",
            model_args=f"base_url={self.base_url},pretrained={model}",
            tasks=[task],
            num_fewshot=num_fewshot
        )
        return self._parse_results(results, task)

    def list_tasks(self) -> List[str]:
        # 返回 lm-eval 支持的 task 列表
        return ["mmlu", "gsm8k", "humaneval", ...]
```

来源：https://github.com/EleutherAI/lm-evaluation-harness

---

## lm-eval 任务列表（常用）

| 任务 | 说明 | 适用模型 | MVP 建议 |
|------|------|---------|---------|
| `mmlu` | 多学科选择题 | 通用 | 是 |
| `gsm8k` | 数学题 | 通用 | 是 |
| `humaneval` | 代码补全 | 代码模型 | 否 |
| `truthfulqa` | 真实性问答 | 通用 | 否 |
| `hellaswag` | 常识推理 | 通用 | 否 |

来源：https://github.com/EleutherAI/lm-evaluation-harness/tree/main/lm_eval/tasks

---

## CLI 接口

### 基本评测

```bash
eval-module run \
    --backend lm-eval \
    --task mmlu \
    --model Qwen/Qwen2.5-0.5B-Instruct \
    --num-fewshot 5 \
    --output ./results/mmlu_result.json
```

### 结果对比

```bash
eval-module compare \
    --baseline ./results/baseline.json \
    --candidate ./results/candidate.json \
    --output ./results/comparison.json
```

---

## 结果 JSON 格式

### 单次评测结果

```json
{
  "task": "mmlu",
  "model": "Qwen/Qwen2.5-0.5B-Instruct",
  "accuracy": 0.6534,
  "num_samples": 14242,
  "num_fewshot": 5,
  "timestamp": "2026-04-03T12:00:00Z",
  "lm_eval_version": "0.4.3",
  "backend": "vllm",
  "metrics": {
    "mmlu": 0.6534
  }
}
```

### 对比结果

```json
{
  "baseline": {
    "task": "mmlu",
    "model": "base",
    "accuracy": 0.65
  },
  "candidate": {
    "task": "mmlu",
    "model": "finetuned",
    "accuracy": 0.68
  },
  "diff": {
    "accuracy_delta": 0.03
  }
}
```

---

## HTTP API（可选）

### `POST /evaluate`

```json
{
  "task": "mmlu",
  "model": "Qwen/Qwen2.5-0.5B-Instruct",
  "num_fewshot": 5,
  "backend": {
    "type": "vllm",
    "base_url": "http://localhost:8000/v1"
  }
}
```

---

Sources:
1. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval
2. https://github.com/EleutherAI/lm-evaluation-harness/tree/main/lm_eval/tasks — lm-eval tasks

Risk of Staleness:
- lm-eval 版本更新可能改变 API

Out of Scope Kept:
- 未写 LLM-as-Judge HTTP API
- 未写评测结果数据库
