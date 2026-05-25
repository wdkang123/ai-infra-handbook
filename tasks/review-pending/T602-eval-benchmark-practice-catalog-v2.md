Task ID: T602
Task Title: Observability / Evaluation Zero-Touch Pack
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
整理评测相关实践，涵盖离线评测、benchmark 对照、arena 观察。

Result:

# Eval/Benchmark Practice Catalog v2

## 概述

本文档在 v1 基础上补充更多评测实践，覆盖数据集选择、评测执行、结果分析全流程。

---

## 数据集选择实践

---

### B01：确定 MVP 评测数据集

**目标**：确认本项目 MVP 阶段应支持哪些 benchmark。

推荐 MVP 评测数据集：

| 数据集 | 评测维度 | 说明 |
|--------|---------|------|
| **MMLU** | 通用语言理解 | 57个学科，覆盖广 |
| **GSM8K** | 数学推理 | 小学数学题，验证基本推理 |
| **HumanEval** | 代码生成 | 164题，代码能力验证 |

来源：https://arxiv.org/abs/2009.03300
来源：https://arxiv.org/abs/2110.14168
来源：https://arxiv.org/abs/2107.03374

---

### B02：查看 lm-eval 支持的数据集列表

**目标**：了解 lm-eval 已内置的数据集。

```bash
lm_eval --tasks help
```

来源：https://github.com/EleutherAI/lm-evaluation-harness

---

## 评测执行实践

---

### B03：多 benchmark 综合评测

**目标**：一次运行多个 benchmark。

```bash
lm_eval --model vllm \
    --model_args pretrained=your-model-path \
    --tasks mmlu,gsm8k,humaneval \
    --batch_size 8
```

来源：https://github.com/EleutherAI/lm-evaluation-harness

---

### B04：SGLang 作为 lm-eval backend

**目标**：验证 SGLang 支持 lm-eval。

```bash
lm_eval --model vllm \
    --model_args backend=sglang,base_url=http://sglang:8000/v1 \
    --tasks mmlu
```

来源：https://sglang.readthedocs.io/

---

### B05：代码模型评测（HumanEval + MBPP）

**目标**：对代码模型做专项评测。

```bash
lm_eval --model vllm \
    --model_args pretrained=codellama/CodeLlama-7b-Instruct \
    --tasks humaneval,mbpp \
    --batch_size 8
```

来源：https://github.com/EleutherAI/lm-evaluation-harness

---

## 结果分析实践

---

### B06：评测结果 JSON 结构解析

**目标**：了解 lm-eval 输出结构。

```json
{
  "results": {
    "mmlu": {
      "acc_norm": 0.65,
      "acc": 0.63
    }
  },
  "config": {
    "model": "vllm",
    "tasks": ["mmlu"]
  }
}
```

来源：https://github.com/EleutherAI/lm-evaluation-harness

---

### B07：历史评测结果对比

**目标**：对比不同版本模型的表现。

```python
import json

with open("baseline_eval.json") as f:
    baseline = json.load(f)
with open("finetuned_eval.json") as f:
    finetuned = json.load(f)

for dataset in baseline["results"]:
    b = baseline["results"][dataset].get("acc_norm", 0)
    f = finetuned["results"][dataset].get("acc_norm", 0)
    print(f"{dataset}: {b:.4f} → {f:.4f} ({f-b:+.4f})")
```

来源：https://github.com/EleutherAI/lm-evaluation-harness

---

### B08：评测结果上报 Langfuse

**目标**：评测结果与推理 trace 关联分析。

```python
from langfuse import Langfuse
langfuse = Langfuse()

with langfuse.span(name="eval_run") as span:
    results = evaluator.simple_evaluate(
        model="vllm",
        model_args="pretrained=your-model",
        tasks=["mmlu"]
    )
    span.set_attribute("mmlu_accuracy", results["results"]["mmlu"]["acc_norm"])
```

来源：https://langfuse.com/docs/observability/overview

---

## Benchmark 观察实践

---

### B09：提交结果到 Open LLM Leaderboard

**目标**：将内部评测结果对接到公开排行榜。

```bash
# 导出评测结果为指定格式
# 通过 HuggingFace API 提交
# 参考：https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard
```

来源：https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard

---

### B10：LMSYS Arena 对战观察

**目标**：观察模型在 Arena 中的对战表现（不建设，自身体系外）。

```bash
# 浏览器访问
https://chat.lmsys.org/?leaderboard
```

来源：https://chat.lmsys.org/?leaderboard

---

### B11：使用 BigCode Eval 跑代码 benchmark

**目标**：使用 bigcode-eval 做代码模型专项评测。

```bash
python -m bigcode_eval.main \
    --model codellama/CodeLlama-7b-Instruct \
    --tasks humaneval \
    --batch_size 8
```

来源：https://github.com/bigcode-project/bigcode-eval-harness

---

## 实践分类总览

| 实践 | 分类 | 门槛 | 组件数 |
|------|------|------|-------|
| B01 确定 MVP 数据集 | 数据集选择 | 低 | 1 |
| B02 查看支持数据集 | 数据集选择 | 极低 | 1 |
| B03 多 benchmark 综合 | 评测执行 | 低 | 1 |
| B04 SGLang backend | 评测执行 | 低 | 2 |
| B05 代码模型评测 | 评测执行 | 低 | 1 |
| B06 结果结构解析 | 结果分析 | 低 | 1 |
| B07 历史对比 | 结果分析 | 低 | 1 |
| B08 Langfuse 上报 | 结果分析 | 中 | 2 |
| B09 Leaderboard 提交 | Benchmark 观察 | 中 | 2 |
| B10 Arena 观察 | Benchmark 观察 | 极低 | 1 |
| B11 BigCode Eval | 代码评测 | 低 | 1 |

Sources:
1. https://github.com/EleutherAI/lm-evaluation-harness — LM-Eval Harness
2. https://sglang.readthedocs.io/ — SGLang
3. https://arxiv.org/abs/2009.03300 — MMLU
4. https://arxiv.org/abs/2110.14168 — GSM8K
5. https://arxiv.org/abs/2107.03374 — HumanEval
6. https://github.com/bigcode-project/bigcode-eval-harness — BigCode Eval
7. https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard — Open LLM Leaderboard
8. https://chat.lmsys.org/?leaderboard — LMSYS Arena
9. https://langfuse.com/docs/observability/overview — Langfuse

Risk of Staleness:
- lm-eval API 可能有版本变化
- 各数据集版本可能更新

Out of Scope Kept:
- 未写完整评测流程文档
- 未写自定义数据集导入方法
- 未写内部 Leaderboard 建设方案
