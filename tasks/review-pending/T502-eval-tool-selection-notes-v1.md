Task ID: T502
Task Title: Eval/Benchmark Long-Run Pack v2
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 T404 的工具 notes，收紧 lm-eval/HELM/bigcode-eval 的选型建议，给出工程级判断。

Result:

# Eval Tool Selection Notes v1

## 概述

本文档基于 T404 eval-module tooling notes 的基础，给出更明确的工程级工具选型建议，帮助 Codex 做最终决策。

---

## LM-Eval Harness — 默认评测工具

### 为什么作为默认

- **工程集成成本低**：Python API + CLI，可直接在 eval-module 中调用
- **benchmark 覆盖广**：MMLU、GSM8K、HumanEval 等主流数据集均已内置
- **backend 支持丰富**：vLLM、SGLang、OpenAI API、HuggingFace Transformers 均可作为推理后端
- **开源活跃**：EleutherAI 维护，版本稳定更新

### 接入方式

```python
# eval-module 调用 lm-eval Python API
from lm_eval import evaluator

results = evaluator.simple_evaluate(
    model="vllm",
    model_args="pretrained=your-model-path",
    tasks=["mmlu", "gsm8k"],
    batch_size=8
)
```

### 局限

- **不含数据存储**：评测结果需要 eval-module 自行持久化
- **不含版本对比**：历史评测结果对比需要 eval-module 自己实现
- **不含 LLM-as-Judge**：需要额外集成

来源：https://github.com/EleutherAI/lm-evaluation-harness

---

## Stanford HELM — 不做直接集成

### 为什么不作为默认

- **接入成本高**：主要是 Web 界面和 API，工程集成复杂
- **偏学术研究**：HELM 的评测维度设计偏学术，工程落地成本大
- **功能与 lm-eval 有重叠**：lm-eval 可覆盖 HELM 的核心场景

### 如何参考

- HELM 的评测维度设计可作为 eval-module 评测场景规划的参考
- 不建议作为工程集成目标

来源：https://crfm.stanford.edu/helm/

---

## BigCode Eval Harness — 可选集成

### 何时集成

- 当本项目需要评测代码模型（CodeLlama、StarCoder 等）时
- HumanEval、MBPP、Pass@K 等指标需要 bigcode-eval 的专门实现

### 如何接入

```python
# eval-module 可选集成 bigcode-eval
from bigcode_eval import evaluator

results = evaluator.evaluate(
    model="codellama",
    tasks=["humaneval", "mbpp"],
    limit=100
)
```

### 何时跳过

- MVP 阶段如果无代码模型需求，可暂不集成
- 功能与 lm-eval 有部分重叠，不需要同时启用

来源：https://github.com/bigcode-project/bigcode-eval-harness

---

## 工具协作关系建议

```
eval-module
    ↓ 调用
LM-Eval Harness（主要评测执行层）
    ↓ 下游
inference-service（vLLM/SGLang backend）
    ↓ 或
外部模型 API（GPT-4 作为 Judge，可选）

可选：
eval-module
    ↓ 调用
BigCode Eval Harness（仅代码模型场景）
    ↓ 下游
inference-service
```

---

## 选型决策表

| 维度 | LM-Eval Harness | Stanford HELM | BigCode Eval |
|------|-----------------|--------------|--------------|
| 工程集成成本 | 低 | 高 | 低 |
| benchmark 覆盖 | 广 | 广 | 代码专项 |
| 推理 backend 支持 | vLLM/SGLang/OpenAI | 多种 | 多种 |
| 数据存储 | 不含 | 含（部分） | 不含 |
| 版本对比能力 | 不含 | 含（部分） | 不含 |
| MVP 推荐 | **是（默认）** | 否（参考） | 可选（代码模型） |

---

## 需要 Codex 最终判断

1. **lm-eval 作为默认评测工具是否确认？**
2. **代码模型评测是否是 MVP 必须？（如否则 bigcode-eval 可暂缓）**
3. **评测结果的持久化方案是否需要在设计阶段确定？**

Sources:
1. https://github.com/EleutherAI/lm-evaluation-harness — LM-Eval Harness
2. https://crfm.stanford.edu/helm/ — Stanford HELM
3. https://github.com/bigcode-project/bigcode-eval-harness — BigCode Eval Harness
4. https://github.com/EleutherAI/lm-evaluation-harness/blob/main/docs/model_eval_pr_template.md — lm-eval 文档

Risk of Staleness:
- lm-eval v0.4 版本 API 有变化，具体以官方文档为准
- 各推理引擎对 lm-eval backend 的支持度可能有版本差异

Out of Scope Kept:
- 未写完整代码实现
- 未写评测结果存储方案
- 未写 LLM-as-Judge 集成方式
