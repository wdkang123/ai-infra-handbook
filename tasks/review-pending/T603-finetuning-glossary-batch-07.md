Task ID: T603
Task Title: Finetuning / Training Zero-Touch Pack
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
收录 DPO/RLHF/Reward Model/Preference Data/Adapter Merge/Safetensors/Checkpoint/Quantization 术语。

Result:

# Finetuning Glossary Batch 07

## T01：DPO（Direct Preference Optimization）

**定义**：直接偏好优化，通过偏好对（chosen/rejected）直接优化语言模型，无需单独训练 Reward Model。

**边界说明**：
- 核心思想：用神经网络隐式表示 Reward，用偏好对直接优化策略
- 相比 PPO，DPO 简化了训练流程
- 需要高质量的偏好数据集

**来源**：https://arxiv.org/abs/2305.18290

---

## T02：RLHF（Reinforcement Learning from Human Feedback）

**定义**：从人类反馈中学习的强化学习范式，包含 Reward Model 训练和策略优化两个阶段。

**边界说明**：
- 标准 RLHF 流程：SFT → Reward Model → PPO → DPO（变体）
- 成本主要在偏好数据标注
- DPO 是 RLHF 的简化变体

**来源**：https://github.com/huggingface/trl

---

## T03：Reward Model

**定义**：奖励模型，用于预测人类偏好的神经网络，是 RLHF 中 PPO 阶段的信号来源。

**边界说明**：
- 通常用偏好数据集（chosen/rejected 对）训练
- 训练一个 Reward Model 需要额外的标注成本
- DPO 提出后，部分场景可以跳过 Reward Model

**来源**：https://github.com/carperai/trl

---

## T04：Preference Data

**定义**：偏好数据，包含同一个输入的两个候选回复及其人类偏好标签（chosen/rejected），用于训练 Reward Model 或 DPO。

**边界说明**：
- 偏好数据的质量直接影响 Reward Model 和 DPO 的效果
- 收集成本高，是 RLHF/DPO 的主要瓶颈
- 数据格式通常包含：prompt、chosen、rejected

**来源**：https://arxiv.org/abs/2305.18290

---

## T05：Adapter Merging

**定义**：将 LoRA 适配器权重合并回原始预训练权重的过程。

**边界说明**：
- 合并后推理不再需要额外的适配器权重
- 用于将多个任务的 LoRA 权重合并为单一模型
- `peft` 库提供 `merge_and_unload()` 接口

**来源**：https://github.com/huggingface/peft

---

## T06：Safetensors

**定义**：一种安全的模型权重序列化格式，由 HuggingFace 开发，用于替代 pickle 格式。

**边界说明**：
- 主要优势：防止恶意 pickle 反序列化攻击
- 加载速度比 pickle 快
- 支持懒加载（lazy loading）

**来源**：https://github.com/huggingface/safetensors

---

## T07：Checkpoint

**定义**：训练过程中的模型状态快照，包含权重、优化器状态等，用于恢复训练或做版本管理。

**边界说明**：
- 全量 checkpoint 包含所有权重和优化器状态
- LoRA checkpoint 只保存适配器权重
- checkpoint 管理是训练流程的重要部分

**来源**：https://github.com/huggingface/peft

---

## T08：Quantization（量化）

**定义**：将模型权重从高精度（FP32/FP16）转换为低精度（INT8/INT4）以减少显存和加速推理/训练的技术。

**边界说明**：
- 训练场景：QLoRA 使用 4-bit NF 量化
- 推理场景：GPTQ/AWQ 用于推理加速
- 量化精度损失对效果的影响需要验证

**来源**：https://github.com/TimDettmers/bitsandbytes

---

## T09：Target Modules

**定义**：LoRA 应用的目标模块，指定在哪些层的权重上附加低秩适配器。

**边界说明**：
- 对于 LLMs，通常选择 `q_proj` 和 `v_proj`（attention 的 Q 和 V 投影）
- 全量应用 LoRA 可选 `all`（效果更好但参数量更大）
- target_modules 选择对最终效果有影响

**来源**：https://github.com/microsoft/LoRA

---

## T10：Gradient Checkpointing

**定义**：梯度检查点技术，通过在前向传播时不保存全部中间激活值，在反向传播时重新计算来降低显存占用。

**边界说明**：
- 代价是增加计算时间（约 20-30%）换取显存减少
- QLoRA 的三要素之一
- 与量化结合效果显著

**来源**：https://github.com/facebookresearch/fairscale/

---

## T11：Adapter

**定义**：在预训练模型旁添加的额外模块，用于在不修改原模型权重的情况下实现任务适配。

**边界说明**：
- LoRA 是 Adapter 的一种实现
- Adapter 可以随时加载/卸载，不影响原模型
- 多任务场景：一个 base model + 多个 Adapter

**来源**：https://github.com/huggingface/peft

---

## T12：bitsandbytes

**定义**：一个量化库，支持 4-bit/8-bit 量化，用于减少模型显存占用。

**边界说明**：
- QLoRA 的 4-bit NF 量化依赖此库
- 提供 `BitsAndBytesConfig` 与 HuggingFace Transformers 集成
- 8-bit 量化用于推理加速，4-bit 用于 QLoRA 训练

**来源**：https://github.com/TimDettmers/bitsandbytes

Sources:
1. https://arxiv.org/abs/2305.18290 — DPO
2. https://github.com/huggingface/trl — TRL
3. https://github.com/carperai/trl — CarperAI TRL
4. https://github.com/huggingface/peft — PEFT
5. https://github.com/huggingface/safetensors — Safetensors
6. https://github.com/TimDettmers/bitsandbytes — bitsandbytes
7. https://github.com/microsoft/LoRA — LoRA
8. https://github.com/facebookresearch/fairscale/ — Gradient Checkpointing

Risk of Staleness:
- DPO/RLHF 超参数最佳实践可能随新研究更新
- 各库 API 可能随版本变化

Out of Scope Kept:
- 未写完整 RLHF 训练流程
- 未写分布式训练相关术语
- 未写训练实战中的调参技巧
