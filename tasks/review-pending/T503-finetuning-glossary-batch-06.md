Task ID: T503
Task Title: Finetuning Long-Run Pack v2
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
第六批 finetuning 相关术语表。

Result:

# Finetuning Glossary Batch 06

## L01：Low-Rank Adaptation（LoRA）

**定义**：一种参数高效微调方法，通过在预训练权重旁添加低秩分解矩阵，只训练新增的低秩参数来适配下游任务。

**边界说明**：
- 核心参数：rank（r）、alpha、target_modules（哪些层应用 LoRA）
- rank 越大，参数量越大，效果通常更好但训练更慢
- 理论上 LoRA 的更新可以合并回原权重，推理时无额外开销

**来源**：https://arxiv.org/abs/2106.09685

---

## L02：Quantized LoRA（QLoRA）

**定义**：LoRA 的量化版本，在 4-bit NF（NormalFloat）量化预训练权重上附加 LoRA 适配器，实现显著的显存降低。

**边界说明**：
- 三要素：4-bit 量化预训练权重 + LoRA + 梯度 checkpointing
- 量化精度损失对训练稳定性的影响需要验证
- 与 LoRA 相比，显存需求显著减少，适合消费级 GPU

**来源**：https://arxiv.org/abs/2305.14314

---

## L03：PEFT（Parameter-Efficient Fine-Tuning）

**定义**：HuggingFace 出品的统一框架，封装了 LoRA、AdaLoRA、QLoRA、Prompt Tuning 等多种参数高效微调方法。

**边界说明**：
- 推荐使用 `peft` 库管理所有 LoRA/QLoRA 实验
- 提供统一的 `get_peft_model()` 接口加载适配器
- 支持适配器合并（`merge_and_unload()`）

**来源**：https://github.com/huggingface/peft

---

## L04：Superviesd Fine-Tuning（SFT）

**定义**：监督微调，在标注数据上直接训练模型使其学习特定任务行为。

**边界说明**：
- SFT 是 RLHF 的第一阶段（Reward Model 之前）
- 训练数据格式需要统一（ChatML / Alpaca / ShareGPT）
- 与 RLHF 相比，SFT 简单直接但依赖标注质量

**来源**：https://github.com/huggingface/trl

---

## L05：Direct Preference Optimization（DPO）

**定义**：直接偏好优化，通过偏好对（chosen/rejected）直接优化语言模型，无需单独训练 Reward Model。

**边界说明**：
- 核心思想：用神经网络隐式表示 Reward，用偏好对直接优化策略
- 相比 PPO，DPO 简化了训练流程
- 需要高质量的偏好数据集

**来源**：https://arxiv.org/abs/2305.18290

---

## L06：PPO（Proximal Policy Optimization）

**定义**：近端策略优化，一种强化学习算法，用于 RLHF 阶段优化语言模型。

**边界说明**：
- PPO 是 RLHF 的核心算法，通过 Reward Model 反馈更新策略
- 训练过程复杂，超参数多
- 与 DPO 相比，PPO 更通用但训练难度更高

**来源**：https://github.com/huggingface/trl

---

## L07：Reward Model

**定义**：奖励模型，用于预测人类偏好的神经网络，是 RLHF 中 PPO 阶段的信号来源。

**边界说明**：
- 通常用偏好数据集（chosen/rejected 对）训练
- 训练一个 Reward Model 需要额外的标注成本
- DPO 提出后，部分场景可以跳过 Reward Model

**来源**：https://github.com/carperai/trl

---

## L08：ChatML（Chat Markup Language）

**定义**：一种对话格式标准，用 XML 标签（`<|im_start|>`、`<|im_end|>`）标记对话角色和内容。

**边界说明**：
- 支持多轮对话和系统提示
- 相比纯文本格式，ChatML 更结构化
- HuggingFace 提供 `apply_chat_template()` 统一处理

**来源**：https://huggingface.co/docs/transformers/main/chat_templating

---

## L09：Gradient Checkpointing

**定义**：梯度检查点技术，通过在前向传播时不保存全部中间激活值，在反向传播时重新计算来降低显存占用。

**边界说明**：
- 代价是增加计算时间（约 20-30%）换取显存减少
- QLoRA 的三要素之一
- 与量化结合效果显著

**来源**：https://github.com/facebookresearch/fairscale/

---

## L10：bitsandbytes

**定义**：一个量化库，支持 4-bit/8-bit 量化，用于减少模型显存占用。

**边界说明**：
- QLoRA 的 4-bit NF 量化依赖此库
- 提供 `BitsAndBytesConfig` 与 HuggingFace Transformers 集成
- 8-bit 量化用于推理加速，4-bit 用于 QLoRA 训练

**来源**：https://github.com/TimDettmers/bitsandbytes

---

## L11：Target Modules

**定义**：LoRA 应用的目标模块，指定在哪些层的权重上附加低秩适配器。

**边界说明**：
- 对于 LLMs，通常选择 `q_proj` 和 `v_proj`（attention 的 Q 和 V 投影）
- 全量应用 LoRA 可选 `all`（效果更好但参数量更大）
- target_modules 选择对最终效果有影响

**来源**：https://github.com/microsoft/LoRA

---

## L12：Adapter Merging

**定义**：将 LoRA 适配器权重合并回原始预训练权重的过程。

**边界说明**：
- 合并后推理不再需要额外的适配器权重
- 用于将多个任务的 LoRA 权重合并为单一模型
- `peft` 库提供 `merge_and_unload()` 接口

**来源**：https://github.com/huggingface/peft

Sources:
1. https://arxiv.org/abs/2106.09685 — LoRA
2. https://arxiv.org/abs/2305.14314 — QLoRA
3. https://arxiv.org/abs/2305.18290 — DPO
4. https://github.com/huggingface/peft — PEFT
5. https://github.com/huggingface/trl — TRL
6. https://github.com/TimDettmers/bitsandbytes — bitsandbytes
7. https://huggingface.co/docs/transformers/main/chat_templating — ChatML
8. https://github.com/facebookresearch/fairscale/ — Gradient Checkpointing

Risk of Staleness:
- LoRA/QLoRA 超参数设置可能随新研究更新最佳实践
- PEFT API 可能随版本变化

Out of Scope Kept:
- 未收录 RLHF 完整术语
- 未写训练实战中的调参技巧
- 未写分布式训练相关术语
