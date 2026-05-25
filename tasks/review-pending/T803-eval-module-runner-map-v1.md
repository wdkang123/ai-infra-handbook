# eval-module Runner Map v1

## Task ID: T803
## Task Title: eval-module Execution Prep Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T303 MVP 设计，准备 eval-module 实施前包。

---

# eval-module Runner Map v1

## 概述

本文档定义 eval-module 如何集成 lm-eval harness 作为评测执行器。

---

## Runner 架构

```
eval-module
    │
    ├── LmEvalRunner（主要）
    │     └── 调用 lm_eval API
    │           │
    │           └── vLLM / SGLang / OpenAI backend
    │
    └── HelmRunner（参考）
          └── 调用 Stanford HELM
```

---

## LmEvalRunner

### 支持的 backend

| backend | 说明 | 配置方式 |
|---------|------|---------|
| `vllm` | vLLM 引擎 | `base_url` |
| `sglang` | SGLang 引擎 | `base_url` |
| `openai` | OpenAI API | `base_url` + `api_key` |
| `anthropic` | Anthropic API | `base_url` + `api_key` |

来源：https://github.com/EleutherAI/lm-evaluation-harness

### lm-eval 调用方式

```python
import lm_eval

# 基本调用
results = lm_eval.simple_eval(
    model="vllm",
    model_args="pretrained=Qwen/Qwen2.5-0.5B-Instruct,base_url=http://localhost:8000/v1",
    tasks=["mmlu"]
)

# 高级调用
results = lm_eval.evaluator.evaluate(
    lm_eval.api.GLM(),
    lm_eval.tasks.get_task_dict(["mmlu", "gsm8k"]),
    num_fewshot=5
)
```

来源：https://github.com/EleutherAI/lm-evaluation-harness

### 任务配置

```python
from lm_eval import tasks

# 获取任务定义
task_dict = tasks.get_task_dict(["mmlu", "gsm8k"])

# 自定义 few-shot 数量
for task_name, task_obj in task_dict.items():
    task_obj.set_config(num_fewshot=5)
```

---

## 支持的任务列表

### MVP 必须任务

| 任务 | 说明 | lm-eval task name | 数据集大小 |
|------|------|-------------------|----------|
| MMLU | 多学科选择题 | `mmlu` | 14,242 |
| GSM8K | 数学题 | `gsm8k` | 8,472 |

### 可选任务

| 任务 | 说明 | lm-eval task name | 数据集大小 |
|------|------|-------------------|----------|
| HumanEval | 代码补全 | `humaneval` | 164 |
| TruthfulQA | 真实性问答 | `truthfulqa` | 817 |
| HellaSwag | 常识推理 | `hellaswag` | 10,042 |
| ARC | 推理题 | `arc_challenge` | 1,132 |

来源：https://github.com/EleutherAI/lm-evaluation-harness/tree/main/lm_eval/tasks

---

## 结果解析

### lm-eval 返回格式

```python
{
    "results": {
        "mmlu": {
            "acc": 0.6534,
            "acc_stderr": 0.0042
        }
    },
    "config": {
        "model": "vllm",
        "model_args": "...",
        "num_fewshot": 5,
        "tasks": ["mmlu"]
    },
    "versions": {
        "mmlu": 1
    }
}
```

### 解析为标准格式

```python
def parse_results(raw_results: dict, task: str) -> EvalResult:
    return EvalResult(
        task=task,
        accuracy=raw_results["results"][task]["acc"],
        num_samples=len(raw_results["samples"][task]),
        timestamp=datetime.now().isoformat(),
        lm_eval_version=raw_results.get("config", {}).get("version")
    )
```

---

## HelmRunner（参考架构）

### 不作为 MVP 主要 runner 的原因

| 维度 | lm-eval | Stanford HELM |
|------|---------|-------------|
| 工程接入 | 简单（pip install） | 复杂 |
| API 支持 | 完善 | 有限 |
| 评测任务 | 丰富 | 丰富 |
| 文档质量 | 好 | 一般 |

来源：https://crfm.stanford.edu/helm/

---

## Runner 选择决策

| 场景 | 推荐 Runner | 理由 |
|------|-----------|------|
| MVP benchmark 评测 | LmEvalRunner | 简单、成熟 |
| 多框架对比 | LmEvalRunner + HelmRunner | 各自擅长 |
| 代码模型评测 | BigCodeEvalRunner | 专用 |

---

Sources:
1. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval
2. https://crfm.stanford.edu/helm/ — Stanford HELM
3. https://github.com/bigcode-project/bigcode-eval-harness — BigCode Eval

Risk of Staleness:
- lm-eval 版本更新可能改变 API

Out of Scope Kept:
- 未写 BigCodeEvalRunner 实现
- 未写 HelmRunner 实现
