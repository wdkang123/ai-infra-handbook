Task ID: T703
Task Title: Finetuning / Training Deep-Research Pack
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
补齐 PEFT/TRL/Unsloth/bitsandbytes/preference data/reward modeling 的稳定入口和更新入口。

Result:

# Finetuning Sources Index v4

## 核心微调方法

### LoRA

| 维度 | 内容 |
|------|------|
| **定位** | 低秩适配，参数高效微调 |
| **核心思想** | 预训练权重旁添加低秩分解矩阵，训练时只更新低秩矩阵 |
| **官方链接** | https://arxiv.org/abs/2106.09685 |
| **GitHub** | https://github.com/microsoft/LoRA |
| **边界说明** | 需要指定 rank、alpha、target_modules，超参数敏感 |

来源：https://arxiv.org/abs/2106.09685

### QLoRA

| 维度 | 内容 |
|------|------|
| **定位** | LoRA 的量化版本，4-bit NF 量化训练 |
| **核心思想** | 4-bit 量化预训练权重 + LoRA + 梯度 checkpointing |
| **官方链接** | https://arxiv.org/abs/2305.14314 |
| **GitHub** | https://github.com/artifacts/qlora |
| **边界说明** | 显存需求显著低于 LoRA，适合消费级 GPU |

来源：https://arxiv.org/abs/2305.14314

---

## 框架

### PEFT

| 维度 | 内容 |
|------|------|
| **定位** | 统一微调框架，支持 LoRA/AdaLoRA/QLoRA/Prompt Tuning |
| **官方链接** | https://github.com/huggingface/peft |
| **文档** | https://huggingface.co/docs/peft/ |
| **Release** | https://github.com/huggingface/peft/releases |
| **边界说明** | 推荐使用 peft 库管理所有 LoRA/QLoRA 实验 |

来源：https://github.com/huggingface/peft

### TRL（Transformer Reinforcement Learning）

| 维度 | 内容 |
|------|------|
| **定位** | HuggingFace 出品的 RL 训练框架（含 SFT/PPO/DPO） |
| **官方链接** | https://github.com/huggingface/trl |
| **文档** | https://huggingface.co/docs/trl/ |
| **Release** | https://github.com/huggingface/trl/releases |
| **支持方法** | SFT（SFTTrainer）、PPO（PPOTrainer）、DPO（DPOTrainer） |
| **边界说明** | 不含数据准备流程，需要配合其他工具 |

来源：https://github.com/huggingface/trl

### Unsloth

| 维度 | 内容 |
|------|------|
| **定位** | 加速库，2x 训练加速 + 50% 显存减少 |
| **官方链接** | https://github.com/unslothai/unsloth |
| **文档** | https://unsloth.ai/ |
| **Blog** | https://unsloth.ai/blog |
| **边界说明** | 主要针对 Ampere/Hopper GPU，其他型号可能效果有限 |

来源：https://github.com/unslothai/unsloth

### bitsandbytes

| 维度 | 内容 |
|------|------|
| **定位** | 量化库，支持 4-bit/8-bit 量化 |
| **官方链接** | https://github.com/TimDettmers/bitsandbytes |
| **Release** | https://github.com/TimDettmers/bitsandbytes/releases |
| **边界说明** | QLoRA 的 4-bit NF 量化依赖此库 |

来源：https://github.com/TimDettmers/bitsandbytes

---

## 偏好与奖励相关

### DPO（Direct Preference Optimization）

| 维度 | 内容 |
|------|------|
| **定位** | 直接偏好优化，无需单独训练 Reward Model |
| **核心思想** | 用偏好对数据（chosen/rejected）直接优化策略模型 |
| **官方链接** | https://arxiv.org/abs/2305.18290 |
| **开源实现** | https://github.com/carperai/trl |
| **边界说明** | 需要高质量偏好数据集 |

来源：https://arxiv.org/abs/2305.18290

### Reward Model

| 维度 | 内容 |
|------|------|
| **定位** | 奖励模型，用于 PPO 强化学习阶段 |
| **核心思想** | 训练一个模型预测人类偏好 |
| **边界说明** | DPO 可以跳过 Reward Model，但需要高质量偏好数据 |

来源：https://github.com/carperai/trl

### Preference Data

| 维度 | 内容 |
|------|------|
| **定位** | 偏好数据，包含同一个输入的两个候选回复及其人类偏好标签 |
| **格式** | prompt、chosen、rejected |
| **边界说明** | 偏好数据的质量直接影响 Reward Model 和 DPO 的效果 |

来源：https://arxiv.org/abs/2305.18290

---

## 数据格式

### ChatML

| 维度 | 内容 |
|------|------|
| **定位** | 对话格式标准，XML 标签标记角色和内容 |
| **官方链接** | https://huggingface.co/docs/transformers/main/chat_templating |
| **边界说明** | 支持多轮对话和系统提示，HuggingFace 提供 apply_chat_template() |

来源：https://huggingface.co/docs/transformers/main/chat_templating

### Alpaca 格式

| 维度 | 内容 |
|------|------|
| **定位** | instruction/input/output 三字段格式 |
| **官方链接** | https://github.com/tatsu-lab/stanford_alpaca |
| **边界说明** | 简单直接，但不支持多轮对话 |

来源：https://github.com/tatsu-lab/stanford_alpaca

---

## 与本项目关系

| 工具/方法 | 与 finetune-demo 关系 |
|-----------|---------------------|
| LoRA | 主要参数高效微调方法 |
| QLoRA | 低显存场景优先选择 |
| PEFT | finetune-demo 的实验管理框架 |
| TRL | SFT/DPO/PPO 训练执行 |
| Unsloth | 可选加速（需确认 GPU 兼容性） |
| bitsandbytes | QLoRA 量化的底层依赖 |
| DPO | 偏好优化（需要高质量偏好数据） |

## 优先阅读链接

1. https://arxiv.org/abs/2106.09685 — LoRA 原始论文
2. https://arxiv.org/abs/2305.14314 — QLoRA 论文
3. https://arxiv.org/abs/2305.18290 — DPO 论文
4. https://github.com/huggingface/peft — PEFT 官方库
5. https://github.com/huggingface/trl — TRL 官方库
6. https://github.com/unslothai/unsloth — Unsloth
7. https://github.com/TimDettmers/bitsandbytes — bitsandbytes

Sources:
1. https://arxiv.org/abs/2106.09685 — LoRA
2. https://arxiv.org/abs/2305.14314 — QLoRA
3. https://arxiv.org/abs/2305.18290 — DPO
4. https://github.com/huggingface/peft — PEFT
5. https://github.com/huggingface/trl — TRL
6. https://github.com/unslothai/unsloth — Unsloth
7. https://github.com/TimDettmers/bitsandbytes — bitsandbytes
8. https://github.com/tatsu-lab/stanford_alpaca — Alpaca
9. https://huggingface.co/docs/transformers/main/chat_templating — ChatML

Risk of Staleness:
- 各框架版本更新可能影响 API 兼容性
- Unsloth GPU 兼容性列表可能更新

Out of Scope Kept:
- 未写完整 RLHF 训练流程
- 未写数据准备详细步骤
- 未写分布式训练配置
