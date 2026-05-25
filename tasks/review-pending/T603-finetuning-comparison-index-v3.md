Task ID: T603
Task Title: Finetuning / Training Zero-Touch Pack
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
把方法、框架、工具的边界分开写，不混成一张营销型总表。

Result:

# Finetuning Comparison Index v3

## 方法比较

### 微调方法定位

| 方法 | 定位 | 显存需求 | 效果 | 来源 |
|------|------|---------|------|------|
| **全参数微调** | 训练全部权重 | 高（全参数加载） | 最好 | — |
| **LoRA** | 低秩适配，参数高效 | 中（约为全参数 1/3） | 接近全参数 | https://arxiv.org/abs/2106.09685 |
| **QLoRA** | LoRA + 4-bit 量化 | 低（< 10GB for 7B） | 略低于 LoRA | https://arxiv.org/abs/2305.14314 |
| **Prompt Tuning** | 只训练 prompt embedding | 极低 | 弱于 LoRA | — |

### 方法边界说明

- **全参数微调**：需要足够显存，适合效果优先场景
- **LoRA**：平衡效果和成本，适合大多数场景
- **QLoRA**：显存受限时的首选，适合消费级 GPU
- **Prompt Tuning**：参数最少但效果弱，适合超大规模模型

来源：https://arxiv.org/abs/2106.09685
来源：https://arxiv.org/abs/2305.14314

---

## 框架比较

### 框架定位

| 框架 | 定位 | 支持方法 | 来源 |
|------|------|---------|------|
| **PEFT** | 参数高效微调统一框架 | LoRA / AdaLoRA / QLoRA / Prompt Tuning | https://github.com/huggingface/peft |
| **TRL** | RLHF 训练框架 | SFT / PPO / DPO | https://github.com/huggingface/trl |
| **Unsloth** | 训练加速库 | LoRA / QLoRA | https://github.com/unslothai/unsloth |

### 框架边界说明

| 框架 | 优势 | 局限 |
|------|------|------|
| **PEFT** | 统一接口，实验管理方便 | 不含训练循环 |
| **TRL** | RLHF 全流程支持 | 不含数据准备 |
| **Unsloth** | 加速效果明显 | 不支持 DPO，仅 LoRA/QLoRA |

来源：https://github.com/huggingface/peft
来源：https://github.com/huggingface/trl
来源：https://github.com/unslothai/unsloth

---

## 工具比较

### 量化工具

| 工具 | 定位 | 支持精度 | 来源 |
|------|------|---------|------|
| **bitsandbytes** | 量化库 | 4-bit / 8-bit | https://github.com/TimDettmers/bitsandbytes |
| **GPTQ** | 训练后量化 | 4-bit | https://github.com/AutoGPTQ/AutoGPTQ |
| **AWQ** | 训练后量化 | 4-bit | https://github.com/mit-han-lab/llm-awq |

### 量化工具边界说明

- **bitsandbytes**：QLoRA 训练依赖，与 HuggingFace 集成好
- **GPTQ / AWQ**：推理量化，训练后使用，不适合训练场景

来源：https://github.com/TimDettmers/bitsandbytes

---

## 偏好优化比较

### 方法

| 方法 | 定位 | 是否需要 Reward Model | 来源 |
|------|------|---------------------|------|
| **DPO** | 直接偏好优化 | 不需要 | https://arxiv.org/abs/2305.18290 |
| **PPO + Reward Model** | 传统 RLHF | 需要 | https://github.com/huggingface/trl |

### 边界说明

- **DPO**：简化流程，需要高质量偏好数据集
- **PPO**：更通用，但训练复杂，超参数多

来源：https://arxiv.org/abs/2305.18290

---

## 与本项目关系

| 对象 | 与 finetune-demo 关系 |
|------|---------------------|
| **LoRA** | 主要微调方法 |
| **QLoRA** | 低显存场景 |
| **PEFT** | 实验管理框架 |
| **TRL** | SFT/DPO 训练 |
| **Unsloth** | 可选加速 |
| **bitsandbytes** | QLoRA 底层依赖 |
| **DPO** | 偏好优化（后续迭代） |

## MVP 适配性评估

| 对象 | MVP 适配性 | 说明 |
|------|-----------|------|
| **LoRA** | 高 | 主要微调方法 |
| **QLoRA** | 高 | 低显存首选 |
| **PEFT** | 高 | 统一接口 |
| **TRL** | 中 | RLHF 才需要 |
| **Unsloth** | 中 | 加速效果好，但 GPU 兼容性需确认 |
| **DPO** | 低 | 需要高质量偏好数据 |

Sources:
1. https://arxiv.org/abs/2106.09685 — LoRA
2. https://arxiv.org/abs/2305.14314 — QLoRA
3. https://arxiv.org/abs/2305.18290 — DPO
4. https://github.com/huggingface/peft — PEFT
5. https://github.com/huggingface/trl — TRL
6. https://github.com/unslothai/unsloth — Unsloth
7. https://github.com/TimDettmers/bitsandbytes — bitsandbytes

Risk of Staleness:
- LoRA/QLoRA 超参数最佳实践可能随新研究更新
- PEFT/TRL API 可能随版本变化

Out of Scope Kept:
- 未写完整 RLHF 训练流程
- 未写数据准备详细步骤
- 未写分布式训练配置
