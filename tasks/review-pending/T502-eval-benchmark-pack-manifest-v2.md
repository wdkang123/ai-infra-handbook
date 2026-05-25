Task ID: T502
Task Title: Eval/Benchmark Long-Run Pack v2
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 T401/T402/T404，产出 Eval/Benchmark 长跑包 v2：5个文件覆盖 benchmark 数据集映射、工具选型、实践路径。

Result:

# Eval/Benchmark Long-Run Pack Manifest v2

## 包概述

本包为 Eval/Benchmark 专题的第二版长跑包，基于 T401/T402/T404 的积累，补充 benchmark 数据集映射、工具选型说明、实践路径，以及更完整的 source-index。

## 已完成交付物

### 1. T502-eval-benchmark-pack-manifest-v2
本文件。总结本包交付物清单和用途。

### 2. T502-eval-benchmark-sources-index-v3
在 v2 基础上更新 benchmark/leaderboard/arena 边界描述，更完整收录数据集和工具源。

### 3. T502-benchmark-dataset-map-v1
收录常用 benchmark 数据集（MMLU、GSM8K、HumanEval 等）的分类、评测维度和来源。

### 4. T502-eval-tool-selection-notes-v1
基于 T404 的工具 notes，收紧 lm-eval/HELM/bigcode-eval 的选型建议，给出工程级判断。

### 5. T502-benchmark-practice-catalog-v1
从单机到多组件的 benchmark 评测最小实践路径。

## 各交付物关系

```
sources-index-v3（数据集和工具的完整来源）
    ↓
dataset-map（数据集分类和边界）
    ↓
tool-selection-notes（工具选型建议）
    ↓
practice-catalog（最小实践路径）
    ↓
manifest（本文件）
```

## 需要 Codex 判断的点

1. **benchmark 数据集优先级**：本项目 MVP 阶段应该支持哪些 benchmark（MMLU/GSM8K/HumanEval）？
2. **评测工具默认选型**：lm-eval 是否作为默认评测工具？
3. **评测结果持久化**：评测结果存在本地文件还是上报 Langfuse？
4. **Leaderboard / Arena 集成**：是否需要支持将评测结果同步到公开 Leaderboard？

## 与其他包的关系

- **T501（Observability Pack）**：评测结果可上报 Langfuse，与推理 trace 关联分析
- **T503（Finetuning Pack）**：finetune 后需要 benchmark 验证效果，评测结果可对比历史版本

## 风险与依赖

- lm-eval 版本更新可能影响 API 兼容性
- 各 benchmark 数据集的版本更新可能影响评测结果可比性
- 各推理引擎对 lm-eval 的 backend 支持度有差异

Sources:
1. https://github.com/EleutherAI/lm-evaluation-harness — LM-Eval Harness
2. https://crfm.stanford.edu/helm/ — Stanford HELM
3. https://github.com/bigcode-project/bigcode-eval-harness — BigCode Eval Harness
4. https://github.com/EleutherAI/lm-evaluation-harness/blob/main/docs/model_eval_pr_template.md — lm-eval 文档
