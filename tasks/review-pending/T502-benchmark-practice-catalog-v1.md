Task ID: T502
Task Title: Eval/Benchmark Long-Run Pack v2
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
从单机到多组件的 benchmark 评测最小实践路径。

Result:

# Benchmark Practice Catalog v1

## 概述

本文档提供从单机到多组件的 benchmark 评测最小实践路径，帮助在 MVP 阶段快速跑通评测流程。

---

## 单机单步骤实践（低门槛）

---

### B01：使用 lm-eval 运行单个 benchmark

**目标**：在标准数据集上跑通评测，验证 inference-service 可用性。

```bash
pip install lm-eval

lm_eval --model vllm \
    --model_args pretrained=your-model-path \
    --tasks mmlu \
    --batch_size 8
```

来源：https://github.com/EleutherAI/lm-evaluation-harness

---

### B02：访问 Open LLM Leaderboard 查看评测标准

**目标**：了解开源社区的 benchmark 评测标准，确定本项目评测优先级。

```bash
# 浏览器访问
https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard
```

来源：https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard

---

### B03：通过 vLLM backend 运行 GSM8K 评测

**目标**：验证 lm-eval + vLLM 集成链路可用。

```bash
lm_eval --model vllm \
    --model_args pretrained=your-model-path,dtype=float16 \
    --tasks gsm8k \
    --batch_size 8
```

来源：https://docs.vllm.ai/

---

## 单机多步骤实践

---

### B04：运行多 benchmark 综合评测

**目标**：一次运行多个 benchmark（MMLU + GSM8K + HumanEval），获取综合评估。

```bash
lm_eval --model vllm \
    --model_args pretrained=your-model-path \
    --tasks mmlu,gsm8k,humaneval \
    --batch_size 8
```

来源：https://github.com/EleutherAI/lm-evaluation-harness

---

### B05：生成评测结果 JSON 并保存

**目标**：评测结果持久化，供后续版本对比。

```python
import json
from lm_eval import evaluator

results = evaluator.simple_evaluate(
    model="vllm",
    model_args="pretrained=your-model-path",
    tasks=["mmlu", "gsm8k"]
)

with open("eval_results.json", "w") as f:
    json.dump(results, f, indent=2)
```

来源：https://github.com/EleutherAI/lm-evaluation-harness

---

### B06：对比两个模型的评测结果

**目标**：验证 eval-module 的版本对比能力。

```python
# 运行基线模型
baseline = run_eval(model="baseline-model", tasks=["mmlu"])

# 运行新模型
candidate = run_eval(model="candidate-model", tasks=["mmlu"])

# 对比结果
for task in ["mmlu"]:
    diff = candidate[task] - baseline[task]
    print(f"{task}: {baseline[task]:.4f} → {candidate[task]:.4f} ({diff:+.4f})")
```

来源：https://github.com/EleutherAI/lm-evaluation-harness

---

## 多组件协同实践

---

### B07：eval-module + inference-service 评测串联

**目标**：验证 eval-module 调用 inference-service 完成评测的完整流程。

```
eval-module
    ↓ 调用 lm-eval API
inference-service（vLLM backend）
    ↓ /metrics 端点
Prometheus（可选：采集评测 QPS）
    ↓
评测结果 JSON → eval-module 持久化
```

来源：https://github.com/EleutherAI/lm-evaluation-harness
来源：https://docs.vllm.ai/

---

### B08：eval-module + Langfuse 上报评测结果

**目标**：评测结果上报 Langfuse，与推理 trace 关联分析。

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

### B09：评测结果对接到 Open LLM Leaderboard

**目标**：将内部评测结果提交到公开排行榜。

```bash
# 1. 导出评测结果为指定格式
# 2. 通过 HuggingFace API 提交
# 参考：https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard
```

来源：https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard

---

### B10：使用 LLM-as-Judge 做主观评测

**目标**：用 GPT-4 作为 Judge 评估模型回复质量。

```python
from langfuse import Langfuse
langfuse = Langfuse()

def judge_with_gpt4(prompt, response):
    judge_result = call_gpt4_judge(prompt, response)
    with langfuse.span(name="judge_eval") as span:
        span.set_attribute("judge_score", judge_result.score)
        span.set_attribute("judgment", judge_result.reasoning)
    return judge_result
```

来源：https://langfuse.com/docs/observability/llm-as-judge

---

## 实践分类总览

| 实践 | 分类 | 门槛 | 组件数 |
|------|------|------|-------|
| B01 lm-eval 单 benchmark | 单机单步骤 | 低 | 1 |
| B02 Open LLM Leaderboard | 单机单步骤 | 极低 | 1 |
| B03 vLLM + GSM8K | 单机单步骤 | 低 | 1 |
| B04 多 benchmark 综合评测 | 单机多步骤 | 低 | 1 |
| B05 评测结果持久化 | 单机多步骤 | 低 | 1 |
| B06 版本对比 | 单机多步骤 | 低 | 1 |
| B07 eval + inference 串联 | 多组件 | 中 | 2 |
| B08 eval + Langfuse 上报 | 多组件 | 中 | 2 |
| B09 Open LLM Leaderboard 对接 | 多组件 | 中 | 2 |
| B10 LLM-as-Judge | 多组件 | 中 | 2 |

Sources:
1. https://github.com/EleutherAI/lm-evaluation-harness — LM-Eval Harness
2. https://docs.vllm.ai/ — vLLM
3. https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard — Open LLM Leaderboard
4. https://langfuse.com/docs/observability/overview — Langfuse
5. https://langfuse.com/docs/observability/llm-as-judge — LLM-as-Judge

Risk of Staleness:
- lm-eval API 可能有版本变化
- vLLM backend 配置方式可能有变化

Out of Scope Kept:
- 未写完整评测流程文档
- 未写自定义数据集导入方法
- 未写评测告警配置
