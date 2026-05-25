Task ID: T703
Task Title: Finetuning / Training Deep-Research Pack
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
收录 SFT/DPO/RLHF/Preference Pair/Reward Model/Adapter/Merge/Quantized Training 术语。

Result:

# Finetuning Glossary Batch 08

## F01：SFT（Supervised Fine-Tuning）

**定义**：监督微调，在标注数据上直接训练模型使其学习特定任务行为。

**边界说明**：
- SFT 是 RLHF 的第一阶段（Reward Model 之前）
- 训练数据格式需要统一（ChatML / Alpaca / ShareGPT）
- 与 RLHF 相比，SFT 简单直接但依赖标注质量

**来源**：https://github.com/huggingface/trl

---

## F02：DPO（Direct Preference Optimization）

**定义**：直接偏好优化，通过偏好对（chosen/rejected）直接优化语言模型，无需单独训练 Reward Model。

**边界说明**：
- 核心思想：用神经网络隐式表示 Reward，用偏好对直接优化策略
- 相比 PPO，DPO 简化了训练流程
- 需要高质量的偏好数据集

**来源**：https://arxiv.org/abs/2305.18290

---

## F03：RLHF（Reinforcement Learning from Human Feedback）

**定义**：从人类反馈中学习的强化学习范式，包含 Reward Model 训练和策略优化两个阶段。

**边界说明**：
- 标准 RLHF 流程：SFT → Reward Model → PPO → DPO（变体）
- 成本主要在偏好数据标注
- DPO 是 RLHF 的简化变体

**来源**：https://github.com/huggingface/trl

---

## F04：Preference Pair

**定义**：偏好对，包含同一个输入的两个候选回复及其人类偏好标签（chosen/rejected）。

**边界说明**：
- 偏好对的格式通常为：`{prompt, chosen, rejected}`
- 偏好数据质量直接影响 Reward Model 和 DPO 的效果
- 收集成本高，是 RLHF/DPO 的主要瓶颈

**来源**：https://arxiv.org/abs/2305.18290

---

## F05：Reward Model

**定义**：奖励模型，用于预测人类偏好的神经网络，是 RLHF 中 PPO 阶段的信号来源。

**边界说明**：
- 通常用偏好数据集（chosen/rejected 对）训练
- 训练一个 Reward Model 需要额外的标注成本
- DPO 提出后，部分场景可以跳过 Reward Model

**来源**：https://github.com/carperai/trl

---

## F06：Adapter

**定义**：在预训练模型旁添加的额外模块，用于在不修改原模型权重的情况下实现任务适配。

**边界说明**：
- LoRA 是 Adapter 的一种实现
- Adapter 可以随时加载/卸载，不影响原模型
- 多任务场景：一个 base model + 多个 Adapter

**来源**：https://github.com/huggingface/peft

---

## F07：Merge

**定义**：将 LoRA 适配器权重合并回原始预训练权重的过程。

**边界说明**：
- 合并后推理不再需要额外的适配器权重
- 用于将多个任务的 LoRA 权重合并为单一模型
- `peft` 库提供 `merge_and_unload()` 接口

**来源**：https://github.com/huggingface/peft

---

## F08：Quantized Training

**定义**：在训练过程中使用量化技术（INT8/INT4）减少显存占用的技术。

**边界说明**：
- QLoRA 是量化训练的典型实现
- 与推理后量化（GPTQ/AWQ）的区别：量化训练在训练时就使用低精度
- 量化精度损失对训练稳定性的影响需要验证

**来源**：https://arxiv.org/abs/2305.14314

---

## F09：Checkpoint

**定义**：训练过程中的模型状态快照，包含权重、优化器状态等，用于恢复训练或做版本管理。

**边界说明**：
- 全量 checkpoint 包含所有权重和优化器状态
- LoRA checkpoint 只保存适配器权重
- checkpoint 管理是训练流程的重要部分

**来源**：https://github.com/huggingface/peft

---

## F10：bitsandbytes

**定义**：一个量化库，支持 4-bit/8-bit 量化，用于减少模型显存占用。

**边界说明**：
- QLoRA 的 4-bit NF 量化依赖此库
- 提供 `BitsAndBytesConfig` 与 HuggingFace Transformers 集成
- 8-bit 量化用于推理加速，4-bit 用于 QLoRA 训练

**来源**：https://github.com/TimDettmers/bitsandbytes

---

## F11：Target Modules

**定义**：LoRA 应用的目标模块，指定在哪些层的权重上附加低秩适配器。

**边界说明**：
- 对于 LLMs，通常选择 `q_proj` 和 `v_proj`（attention 的 Q 和 V 投影）
- 全量应用 LoRA 可选 `all`（效果更好但参数量更大）
- target_modules 选择对最终效果有影响

**来源**：https://github.com/microsoft/LoRA

---

## F12：Gradient Checkpointing

**定义**：梯度检查点技术，通过在前向传播时不保存全部中间激活值，在反向传播时重新计算来降低显存占用。

**边界说明**：
- 代价是增加计算时间（约 20-30%）换取显存减少
- QLoRA 的三要素之一
- 与量化结合效果显著

**来源**：https://github.com/facebookresearch/fairscale/

---

## F13：Safetensors

**定义**：一种安全的模型权重序列化格式，由 HuggingFace 开发，用于替代 pickle 格式。

**边界说明**：
- 主要优势：防止恶意 pickle 反序列化攻击
- 加载速度比 pickle 快
- 支持懒加载（lazy loading）

**来源**：https://github.com/huggingface/safetensors

---

## F14：ChatML（Chat Markup Language）

**定义**：一种对话格式标准，用 XML 标签（`<|im_start|>`、`<|im_end|>`）标记对话角色和内容。

**边界说明**：
- 支持多轮对话和系统提示
- 相比纯文本格式，ChatML 更结构化
- HuggingFace 提供 `apply_chat_template()` 统一处理

**来源**：https://huggingface.co/docs/transformers/main/chat_templating

Sources:
1. https://arxiv.org/abs/2305.18290 — DPO
2. https://github.com/huggingface/trl — TRL
3. https://github.com/carperai/trl — CarperAI TRL
4. https://github.com/huggingface/peft — PEFT
5. https://github.com/TimDettmers/bitsandbytes — bitsandbytes
6. https://github.com/microsoft/LoRA — LoRA
7. https://github.com/facebookresearch/fairscale/ — Gradient Checkpointing
8. https://github.com/huggingface/safetensors — Safetensors
9. https://huggingface.co/docs/transformers/main/chat_templating — ChatML

Risk of Staleness:
- DPO/RLHF 超参数最佳实践可能随新研究更新
- 各库 API 可能随版本变化

Out of Scope Kept:
- 未写完整 RLHF 训练流程
- 未写分布式训练相关术语
- 未写训练实战中的调参技巧
