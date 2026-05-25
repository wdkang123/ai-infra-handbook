Task ID: T503
Task Title: Finetuning Long-Run Pack v2
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于之前决策讨论，收紧 LoRA vs QLoRA vs 全参数微调的选型建议。

Result:

# Finetune Demo Decision Notes v1

## 概述

本文档基于之前的 finetuning 决策讨论，收紧 LoRA vs QLoRA vs 全参数微调的选型建议，为 Codex 提供工程级决策输入。

---

## 决策点一：LoRA vs QLoRA vs 全参数微调

### 选型维度对比

| 维度 | LoRA | QLoRA | 全参数微调 |
|------|------|-------|-----------|
| **显存需求** | 中（约为全参数的 1/3） | 低（< 10GB for 7B） | 高（全参数加载） |
| **训练速度** | 快 | 中（量化开销） | 慢 |
| **效果** | 接近全参数 | 略低于 LoRA | 最好 |
| **超参数复杂度** | 中（rank/alpha） | 高（rank/alpha + 量化位） | 低（学习率/epochs） |
| **适用场景** | 有足够显存（> 20GB） | 显存受限（消费级 GPU） | 效果优先 |

### 资料级建议

| 场景 | 推荐方案 | 理由 |
|------|---------|------|
| **MVP 阶段快速验证** | QLoRA（4-bit） | 显存门槛低，快速出结果 |
| **正式训练（> 20GB VRAM）** | LoRA | 效果更好，速度快于全参数 |
| **效果优先、不计成本** | 全参数微调 | 效果最好但成本最高 |
| **代码模型微调** | LoRA | 代码模型对精度要求高 |

来源：https://arxiv.org/abs/2106.09685
来源：https://arxiv.org/abs/2305.14314

---

## 决策点二：训练框架选型

### trl vs Unsloth

| 维度 | trl | Unsloth |
|------|-----|---------|
| **定位** | 标准 RLHF/SFT 框架 | 加速优化库 |
| **SFT 支持** | 是（SFTTrainer） | 是（FastLanguageModel） |
| **DPO 支持** | 是（DPOTrainer） | 否 |
| **加速效果** | 无额外加速 | 2x 加速 + 50% 显存减少 |
| **GPU 兼容性** | 通用 | Ampere/Hopper 为主 |
| **上手难度** | 中 | 低 |

### 资料级建议

- **MVP 阶段**：优先 Unsloth，上手简单，加速效果明显
- **需要 DPO**：必须使用 trl（Unsloth 不支持 DPO）
- **长期标准**：tr1 是 HuggingFace 官方维护，更适合长期架构

来源：https://github.com/huggingface/trl
来源：https://github.com/unslothai/unsloth

---

## 决策点三：训练过程的监控

### 监控工具选择

| 工具 | 集成位置 | 用途 |
|------|---------|------|
| **Langfuse** | finetune-demo 代码中埋点 | 训练 metrics 上报，实验对比 |
| **Prometheus** | 暴露 `/metrics` 端点 | GPU 利用率、显存占用采集 |
| **Grafana** | 连接 Prometheus | 训练过程可视化 |

### 资料级建议

- **MVP 阶段**：优先集成 Langfuse（与 observability 包一致），训练 metrics 上报到同一平台
- **可选叠加**：Prometheus + Grafana 用于详细资源监控

来源：https://langfuse.com/docs/observability/overview
来源：https://prometheus.io/

---

## 决策点四：finetune 后评测

### 评测工具联动

| 工具 | 与 finetune-demo 关系 |
|------|---------------------|
| **lm-eval** | finetune 后运行 benchmark 验证效果 |
| **Langfuse** | 评测结果与训练 metrics 关联分析 |

### 资料级建议

- **MVP 阶段**：finetune 后运行 MMLU/GSM8K 等 benchmark，确认效果提升
- **评测结果对比**：与 base model 分数对比，记录在 Langfuse 中

来源：https://github.com/EleutherAI/lm-evaluation-harness

---

## 总结：资料级建议（不下结论）

| 决策点 | 建议方向 | 关键依据 |
|--------|---------|---------|
| LoRA vs QLoRA vs 全参数 | MVP 用 QLoRA，正式用 LoRA | QLoRA 显存门槛低，LoRA 效果更好 |
| trl vs Unsloth | MVP 用 Unsloth，DPO 场景用 trl | Unsloth 简单快速，trl 支持 DPO |
| 训练监控 | 优先 Langfuse | 与 observability 包统一 |
| 训练后评测 | 必须 benchmark 验证 | lm-eval 集成简单 |

---

## 需要 Codex 最终判断

1. **MVP 阶段是否接受 QLoRA（4-bit）作为默认微调方法？**
2. **是否需要 DPO 能力？（如否则 Unsloth 可满足）**
3. **训练监控是否强制使用 Langfuse？**
4. **评测 benchmark 是否需要 LM-Eval Harness 自动化集成？**

Sources:
1. https://arxiv.org/abs/2106.09685 — LoRA
2. https://arxiv.org/abs/2305.14314 — QLoRA
3. https://arxiv.org/abs/2305.18290 — DPO
4. https://github.com/huggingface/peft — PEFT
5. https://github.com/huggingface/trl — TRL
6. https://github.com/unslothai/unsloth — Unsloth
7. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval
8. https://langfuse.com/docs/observability/overview — Langfuse

Risk of Staleness:
- LoRA/QLoRA 超参数最佳实践可能随新研究更新
- Unsloth GPU 兼容性可能扩展到更多型号
- PEFT/TRL API 可能随版本变化

Out of Scope Kept:
- 未写完整 RLHF 流程
- 未写数据准备详细步骤
- 未写分布式训练方案
