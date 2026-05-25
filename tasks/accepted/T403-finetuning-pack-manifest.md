Task ID: T403
Task Title: Finetuning Long-Run Pack v1
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
Finetuning Long-Run Pack，基于 T207/T198/T209/T315/T304，产出4个文件：manifest、comparison-index v2、practice-catalog v1、training-map v1。

Result:

# Finetuning Long-Run Pack Manifest

## 包概述

本包围绕 **Finetuning** 主题，产出 4 个互相独立的交付物，共同构成 finetuning 资产的完整拼图。

## 已完成交付物

### 1. T403-finetuning-pack-manifest
本文件。总结本包交付物清单和用途。

### 2. T403-finetuning-comparison-index-v2
比较 LoRA、QLoRA、PEFT、TRL、Unsloth 五个对象在定位、层级、场景、项目关系上的差异。

**用途**：为 finetune-demo 的微调路径选择提供参考依据。

### 3. T403-finetuning-practice-catalog-v1
整理 6 个最小实践入口（LoRA basic、QLoRA basic、PEFT basic、TRL SFT、DPO entry、Unsloth entry）。

**用途**：为开发者提供从零到第一个微调产物的快速路径。

### 4. T403-finetune-demo-training-map-v1
说明 finetune-demo 的训练路径拆分和资料入口，不写实现结论。

**用途**：说明 finetune-demo 的模块拆分和微调方法对应关系。

## 各交付物关系

```
comparison-index v2（方法对比）
    ↓
practice-catalog v1（最小实践）
    ↓
training-map v1（模块拆分）
    ↓
manifest（本文件）
```

## 需要 Codex 判断的点

1. **finetune-demo 的默认微调方法**：LoRA 还是 QLoRA 作为 MVP 默认路径？
2. **Unsloth 是否纳入 MVP**：Unsloth 加速效果明确，但作为外部依赖是否在 MVP 范围？
3. **DPO 是否在 MVP 范围**：DPO 训练需要偏好数据，是否属于 MVP 必须？
4. **PEFT 的接口设计**：是否直接暴露 PEFT API，还是封装成 Trainer 类？

## 与其他包的关系

- **T402（Eval/Benchmark Pack）**：finetune-demo 产出的模型由 eval-module 做评测，形成训练→评测闭环
- **T401（Observability Pack）**：finetuning 训练过程的监控可复用 observability 能力（tensorboard 等），但不在本包范围内

## 风险与依赖

- PEFT/TRL 版本更新快，具体 API 以实际安装版本为准
- Unsloth 更新频繁，加速效果以实际测试为准
- LoRA 新变体（DoRA、GaLoRA 等）快速涌现，PEFT 集成状态实时变化

Sources:
1. https://github.com/huggingface/peft — PEFT
2. https://github.com/huggingface/trl — TRL
3. https://github.com/unslothai/unsloth — Unsloth
4. https://arxiv.org/abs/2106.09685 — LoRA 论文
5. https://arxiv.org/abs/2305.14314 — QLoRA 论文
