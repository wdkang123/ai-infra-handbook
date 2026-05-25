Task ID: T402
Task Title: Evaluation / Benchmark Long-Run Pack v1
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
Evaluation/Benchmark Long-Run Pack，基于 T205/T306/T309/T312/T313，产出4个文件：manifest、sources-index v2、glossary batch 05、eval-module tooling notes。

Result:

# Evaluation / Benchmark Long-Run Pack Manifest

## 包概述

本包围绕 **Evaluation / Benchmark** 主题，产出 4 个互相独立的交付物。

## 已完成交付物

### 1. T402-eval-benchmark-pack-manifest
本文件。总结本包交付物清单和用途。

### 2. T402-eval-benchmark-sources-index-v2
在 v1 基础上收紧 evaluation/benchmark/leaderboard/arena 的链接入口，补齐更稳定的精确 URL。

**用途**：作为评测工具选型和深入学习的入口索引。

### 3. T402-benchmark-glossary-batch-05
8 个 benchmark/leaderboard 相关术语（Accuracy、Pass@K、Elo、Benchmark、Leaderboard、Arena、MMLU、GSM8K）。

**用途**：统一评测领域术语定义，避免跨团队理解歧义。

### 4. T402-eval-module-tooling-notes-v1
说明 LM-Eval Harness、Stanford HELM、BigCode Eval Harness 与 eval-module 的可能关系，不写最终实现结论。

**用途**：为 eval-module 的工具选型提供参考依据。

## 各交付物关系

```
sources-index v2（工具索引）
    ↓
glossary batch 05（术语统一）
    ↓
eval-module tooling notes（工具选型）
    ↓
manifest（本文件）
```

## 需要 Codex 判断的点

1. **eval-module 的评测工具选型**：LM-Eval Harness 是开源首选，但具体 API 接口设计需要 Codex 最终确认
2. **Stanford HELM 的参考价值**：HELM 偏学术研究，是否需要在本项目中有对应实现？
3. **BigCode Eval Harness 的集成优先级**：如果本项目不涉及代码模型评测，是否可以暂时跳过？
4. **评测结果是否需要持久化存储**：eval-module 的评测历史记录方案还未确定

## 与其他包的关系

- **T401（Observability Pack）**：eval-module 的评测结果可上报 Langfuse，与 observability 形成协作（见 T401 project-map）
- **T403（Finetuning Pack）**：finetune-demo 微调后的模型由 eval-module 做评测，两者形成训练→评测的闭环

## 风险与依赖

- LMSYS Arena 和 Open LLM Leaderboard 按季度更新，排名变化较快
- LM-Eval Harness 版本更新可能影响 benchmark 兼容性
- 各 benchmark 数据集版本可能影响结果可比性

Sources:
1. https://github.com/EleutherAI/lm-evaluation-harness — LM-Eval Harness
2. https://crfm.stanford.edu/helm/ — Stanford HELM
3. https://github.com/bigcode-project/bigcode-eval-harness — BigCode Eval Harness
4. https://chat.lmsys.org/ — LMSYS Chatbot Arena
5. https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard — Open LLM Leaderboard
