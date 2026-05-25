Task ID: T503
Task Title: Finetuning Long-Run Pack v2
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 T401/T402/T403，产出 Finetuning 长跑包 v2：5个文件覆盖来源索引、术语表、实践路径、决策笔记。

Result:

# Finetuning Long-Run Pack Manifest v2

## 包概述

本包为 Finetuning 专题的第二版长跑包，基于 T401/T402/T403 的积累，补充更新的来源索引、第六批术语表、更完整的 finetune-demo 实践路径、以及决策笔记。

## 已完成交付物

### 1. T503-finetuning-pack-manifest-v2
本文件。总结本包交付物清单和用途。

### 2. T503-finetuning-sources-index-v2
在 v1 基础上更新 LoRA/QLoRA/PEFT/trl 相关来源，新增 Unsloth 和 bitsandbytes 的来源收录。

### 3. T503-finetuning-glossary-batch-06
第六批术语表，收录 LoRA/QLoRA/PEFT 相关的核心概念定义。

### 4. T503-finetune-demo-practice-catalog-v2
在 v1 基础上补全从单机到多组件的 finetuning 最小实践路径。

### 5. T503-finetune-demo-decision-notes-v1
基于之前决策讨论，收紧 LoRA vs QLoRA vs 全参数微调的选型建议。

## 各交付物关系

```
sources-index-v2（工具和来源的完整收录）
    ↓
glossary-batch-06（核心术语定义）
    ↓
practice-catalog-v2（最小实践路径）
    ↓
decision-notes-v1（选型决策建议）
    ↓
manifest（本文件）
```

## 需要 Codex 判断的点

1. **finetuning 工具默认选型**：LoRA vs QLoRA vs 全参数微调，如何选择？
2. **训练框架选型**：trl vs Unsloth，哪个更适合 MVP 阶段？
3. **训练过程的监控**：训练 metrics 如何与 observability 包协作？
4. **finetune 后的评测**：评测 benchmark 是否需要与 eval-module 联动？

## 与其他包的关系

- **T501（Observability Pack）**：训练过程的 metrics 可复用 Prometheus + Grafana 栈
- **T502（Eval/Benchmark Pack）**：finetune 后需要 benchmark 验证效果

## 风险与依赖

- LoRA/PEFT 的超参数配置复杂，需要根据实际模型调整
- Unsloth 加速效果依赖 GPU 型号
- 训练过程的 checkpoint 管理需要额外设计

Sources:
1. https://arxiv.org/abs/2106.09685 — LoRA 原始论文
2. https://arxiv.org/abs/2305.14314 — QLoRA 论文
3. https://github.com/huggingface/peft — PEFT 库
4. https://github.com/huggingface/trl — TRL 库
5. https://github.com/unslothai/unsloth — Unsloth
