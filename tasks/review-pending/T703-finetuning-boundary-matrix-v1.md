Task ID: T703
Task Title: Finetuning / Training Deep-Research Pack
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
澄清方法 vs 框架 vs 工具、LoRA vs QLoRA、SFT/DPO/RLHF 的关系。

Result:

# Finetuning Boundary Matrix v1

## 边界一：方法 vs 框架 vs 工具

### 方法（Method）

| 属性 | 内容 |
|------|------|
| **定义** | 微调的核心算法思想 |
| **代表** | LoRA、QLoRA、Prompt Tuning、Full Fine-tuning |
| **边界说明** | 方法是抽象概念，不依赖具体实现 |

### 框架（Framework）

| 属性 | 内容 |
|------|------|
| **定义** | 实现某种方法的代码库 |
| **代表** | PEFT、TRL |
| **边界说明** | 框架是方法的工程实现，一个框架可以支持多种方法 |

### 工具（Tool）

| 属性 | 内容 |
|------|------|
| **定义** | 辅助训练的工具库 |
| **代表** | bitsandbytes（量化）、Unsloth（加速） |
| **边界说明** | 工具不直接实现方法，但是方法实现的辅助 |

### 关系澄清

```
方法：LoRA
    ↓ 实现
框架：PEFT / TRL
    ↓ 使用
工具：bitsandbytes（量化） + Unsloth（加速）
```

来源：https://github.com/huggingface/peft
来源：https://github.com/huggingface/trl

---

## 边界二：LoRA vs QLoRA

### LoRA

| 属性 | 内容 |
|------|------|
| **定义** | 低秩适配，在预训练权重旁添加低秩分解矩阵 |
| **量化** | FP16/BF16 |
| **显存需求** | 中（约为全参数 1/3） |
| **效果** | 接近全参数 |
| **超参数** | rank（r）、alpha、target_modules |

### QLoRA

| 属性 | 内容 |
|------|------|
| **定义** | LoRA 的量化版本，4-bit NF 量化预训练权重 |
| **量化** | 4-bit NF + LoRA + 梯度 checkpointing |
| **显存需求** | 低（< 10GB for 7B） |
| **效果** | 略低于 LoRA |
| **超参数** | rank、alpha + 量化位 |

### 关键区别

| 维度 | LoRA | QLoRA |
|------|------|-------|
| **量化精度** | FP16/BF16 | 4-bit NF |
| **显存需求** | 中 | 低 |
| **量化开销** | 无 | 有（训练时量化） |
| **效果** | 更好 | 略差 |
| **适用场景** | 显存充足 | 显存受限 |

来源：https://arxiv.org/abs/2106.09685
来源：https://arxiv.org/abs/2305.14314

---

## 边界三：SFT vs DPO vs RLHF

### SFT（Supervised Fine-Tuning）

| 属性 | 内容 |
|------|------|
| **定义** | 监督微调，在标注数据上直接训练模型 |
| **训练方式** | 直接拟合标注数据 |
| **需要 Reward Model** | 否 |
| **需要 Preference Data** | 否 |
| **复杂度** | 低 |
| **边界说明** | SFT 是 RLHF 的第一阶段，也是 DPO 的前置 |

### DPO（Direct Preference Optimization）

| 属性 | 内容 |
|------|------|
| **定义** | 直接偏好优化，用偏好对直接优化策略模型 |
| **训练方式** | 用偏好对（chosen/rejected）直接优化 |
| **需要 Reward Model** | 否（隐式） |
| **需要 Preference Data** | 是 |
| **复杂度** | 中 |
| **边界说明** | DPO 可以跳过 Reward Model 训练，但仍需要偏好数据 |

### RLHF（Reinforcement Learning from Human Feedback）

| 属性 | 内容 |
|------|------|
| **定义** | 从人类反馈中学习的强化学习范式 |
| **训练方式** | Reward Model → PPO 强化学习 |
| **需要 Reward Model** | 是 |
| **需要 Preference Data** | 是（训练 Reward Model） |
| **复杂度** | 高 |
| **边界说明** | 标准 RLHF 包含 SFT + Reward Model + PPO |

### 关系澄清

```
SFT（监督微调）
    ↓
RLHF（Reward Model + PPO）
或
SFT → DPO（直接偏好优化）
```

### 选择指引

| 场景 | 推荐 | 理由 |
|------|------|------|
| 快速出结果 | SFT | 简单直接 |
| 有高质量偏好数据 | DPO | 效果更好 |
| 需要最精细控制 | RLHF | 最通用但最复杂 |

来源：https://arxiv.org/abs/2106.09685
来源：https://arxiv.org/abs/2305.18290
来源：https://github.com/huggingface/trl

---

## 边界四：Framework vs Training Library

### PEFT

| 属性 | 内容 |
|------|------|
| **定位** | 参数高效微调统一框架 |
| **支持方法** | LoRA、AdaLoRA、QLoRA、Prompt Tuning |
| **是否含训练循环** | 否（需要配合 Trainer） |
| **与 TRL 关系** | 可配合，提供 adapter 管理 |

### TRL

| 属性 | 内容 |
|------|------|
| **定位** | 完整训练框架 |
| **支持方法** | SFT（SFTTrainer）、PPO、DPO（DPOTrainer） |
| **是否含训练循环** | 是 |
| **与 PEFT 关系** | 可配合使用 |

### 关系澄清

- **PEFT** 管 adapter（LoRA/QLoRA 配置）
- **TRL** 管训练循环（SFT/DPO/PPO 执行）
- 两者可以配合：`SFTTrainer` + `PeftModel`

来源：https://github.com/huggingface/peft
来源：https://github.com/huggingface/trl

---

## 边界五：Adapter Merging vs Model Merging

### Adapter Merging

| 属性 | 内容 |
|------|------|
| **定义** | 将 LoRA 适配器权重合并回原始预训练权重 |
| **产物** | 合并后的完整模型权重 |
| **用途** | 推理时不再需要额外的 adapter |
| **工具** | `peft.MergeFromUnload()` |

### Model Merging

| 属性 | 内容 |
|------|------|
| **定义** | 将多个不同模型的权重平均 |
| **产物** | 多个模型的融合权重 |
| **用途** | 模型集成（不常见） |
| **工具** | mergekit 等 |

### 边界澄清

- Adapter Merging 是把 adapter 合并回原模型
- Model Merging 是把多个不同模型合并成一个

来源：https://github.com/huggingface/peft

---

## 常见混淆总结

| 混淆 | 事实 |
|------|------|
| "LoRA 和 PEFT 是同一个东西" | LoRA 是方法，PEFT 是实现 LoRA 的框架 |
| "DPO 可以替代 RLHF" | DPO 是 RLHF 的简化变体，不完全等价 |
| "QLoRA 是 LoRA 的量化版本" | QLoRA = 4-bit 量化 + LoRA + gradient checkpointing |
| "TRL 可以替代 PEFT" | TRL 管训练循环，PEFT 管 adapter 配置 |

Sources:
1. https://arxiv.org/abs/2106.09685 — LoRA
2. https://arxiv.org/abs/2305.14314 — QLoRA
3. https://arxiv.org/abs/2305.18290 — DPO
4. https://github.com/huggingface/peft — PEFT
5. https://github.com/huggingface/trl — TRL

Risk of Staleness:
- 各框架版本更新可能改变边界

Out of Scope Kept:
- 未写代码实现
- 未写具体训练配置
