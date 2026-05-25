Task ID: T503
Task Title: Finetuning Long-Run Pack v2
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 T401/T402/T403，产出更完整的 finetuning sources-index v2。

Result:

# Finetuning Sources Index v2

## 核心微调方法

### LoRA（Low-Rank Adaptation）

| 维度 | 内容 |
|------|------|
| **定位** | 低秩适配，最常用的参数高效微调方法 |
| **核心思想** | 在预训练权重旁添加低秩分解矩阵，训练时只更新低秩矩阵 |
| **官方链接** | https://arxiv.org/abs/2106.09685 |
| **开源实现** | https://github.com/microsoft/LoRA |
| **边界说明** | 需要指定 rank、alpha、target_modules，超参数敏感 |

### QLoRA（Quantized LoRA）

| 维度 | 内容 |
|------|------|
| **定位** | LoRA 的量化版本，支持 4-bit NF 量化训练 |
| **核心思想** | 4-bit 量化预训练权重 + LoRA + 梯度checkpointing |
| **官方链接** | https://arxiv.org/abs/2305.14314 |
| **开源实现** | https://github.com/artifacts/qlora |
| **边界说明** | 显存需求显著低于 LoRA，适合小显存场景 |

### PEFT（Parameter-Efficient Fine-Tuning）

| 维度 | 内容 |
|------|------|
| **定位** | 统一框架，支持 LoRA/AdaLoRA/QLoRA 等多种方法 |
| **官方链接** | https://github.com/huggingface/peft |
| **边界说明** | 本项目推荐使用 PEFT 框架管理 LoRA/QLoRA 实验 |

## 训练框架

### TRL（Transformer Reinforcement Learning）

| 维度 | 内容 |
|------|------|
| **定位** | HuggingFace 出品的 RL 训练框架（含 SFT/PPO/DPO） |
| **支持方法** | SFT（监督微调）、PPO、DPO |
| **官方链接** | https://github.com/huggingface/trl |
| **边界说明** | 不包含数据准备流程，需要配合其他工具 |

### TRLX

| 维度 | 内容 |
|------|------|
| **定位** | CarperAI 出品的大规模 RLHF 训练框架 |
| **官方链接** | https://github.com/carperai/trlx |
| **边界说明** | 已不再活跃维护，CarperAI 转向 TRL |

### Unsloth

| 维度 | 内容 |
|------|------|
| **定位** | 加速库，声称 2x 训练加速 + 50% 显存减少 |
| **支持方法** | LoRA/QLoRA（动态批处理、gradient checkpointing 优化） |
| **官方链接** | https://github.com/unslothai/unsloth |
| **边界说明** | 需确认 GPU 型号兼容性（主要针对 Ampere/Hopper） |

### bitsandbytes

| 维度 | 内容 |
|------|------|
| **定位** | 量化库，支持 4-bit/8-bit 量化 |
| **官方链接** | https://github.com/TimDettmers/bitsandbytes |
| **边界说明** | QLoRA 的量化依赖此库 |

## 数据格式

### SFT（Supervised Fine-Tuning）格式

| 格式 | 描述 | 官方链接 |
|------|------|---------|
| **ChatML** | 对话格式，含 role/content/system 字段 | https://huggingface.co/docs/transformers/main/chat_templating |
| **Alpaca** | instruction/input/output 三字段 | https://github.com/tatsu-lab/stanford_alpaca |
| **ShareGPT** | 用户/助手对话导出格式 | https://huggingface.co/datasets/anon8231489123/ShareGPT_Vicuna_unfiltered |

## 评估方法

### DPO（Direct Preference Optimization）

| 维度 | 内容 |
|------|------|
| **定位** | 直接偏好优化，无需 Reward Model |
| **核心思想** | 用偏好对数据直接优化策略模型 |
| **官方链接** | https://arxiv.org/abs/2305.18290 |
| **开源实现** | https://github.com/carperai/trl |

### Reward Model

| 维度 | 内容 |
|------|------|
| **定位** | 奖励模型，用于 PPO 强化学习阶段 |
| **核心思想** | 训练一个模型预测人类偏好 |
| **边界说明** | 需要偏好数据集（chosen/rejected 对） |

## 与本项目关系

| 工具/方法 | 与 finetune-demo 关系 |
|-----------|---------------------|
| LoRA | 主要使用的参数高效微调方法 |
| QLoRA | 低显存场景的优先选择 |
| PEFT | finetune-demo 的实验管理框架 |
| TRL | SFT/DPO 训练执行 |
| Unsloth | 可选加速（需确认 GPU 兼容性） |
| bitsandbytes | QLoRA 量化的底层依赖 |

## 优先阅读链接

1. https://arxiv.org/abs/2106.09685 — LoRA 原始论文
2. https://arxiv.org/abs/2305.14314 — QLoRA 论文
3. https://arxiv.org/abs/2305.18290 — DPO 论文
4. https://github.com/huggingface/peft — PEFT 官方库
5. https://github.com/huggingface/trl — TRL 官方库
6. https://github.com/unslothai/unsloth — Unsloth

## 风险与边界

- LoRA 超参数（rank/alpha）对结果影响大，需要实验调优
- QLoRA 的 4-bit 量化可能影响训练稳定性
- Unsloth 加速效果依赖具体 GPU 型号
- DPO 需要高质量偏好数据集，数据准备成本高

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
- Unsloth 的 GPU 兼容性列表可能更新

Out of Scope Kept:
- 未写完整训练流程
- 未写数据准备详细步骤
- 未写 RLHF 完整实现
