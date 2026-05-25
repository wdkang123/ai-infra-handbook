Task ID: T315
Task Title: 收紧 finetuning glossary batch 04 的笔误和边界措辞
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 T314 初稿和 T314-review 修订。只修 DPO 条目笔误和 Unsloth 条目边界措辞，不重写整批。

Result:

# Finetuning Glossary Batch 04

## 条目列表

---

### LoRA Rank

**定义**：LoRA 低秩矩阵的秩值 r，决定可训练参数量和模型容量。Rank 越高参数量越大，表达能力越强，但训练成本也更高。

**边界说明**：LoRA Rank 是 LoRA 配置的核心超参数，与 lora_alpha 共同决定 LoRA 层的表达能力；Rank 的选择需要权衡任务复杂度和训练资源。

**来源**：https://arxiv.org/abs/2106.09685

---

### Target Modules

**定义**：LoRA 应用到的模型层名称，如 `q_proj`、`k_proj`、`v_proj`、`o_proj`。只有被指定为 Target Modules 的层才会添加 LoRA 权重。

**边界说明**：Target Modules 决定了 LoRA 微调的粒度；通常选择 attention 相关层（q/k/v_proj）即可覆盖主要微调需求。

**来源**：https://github.com/huggingface/peft

---

### Adapter

**定义**：LoRA/QLoRA 等参数高效微调方法添加到预训练模型旁的小权重矩阵集合，也指包含这些权重和配置的微调产物文件。

**边界说明**：Adapter 是微调的产出物，可独立存储和加载；不同任务的 Adapter 可在推理时动态切换，实现多任务共享基础模型。

**来源**：https://github.com/huggingface/peft

---

### QLoRA

**定义**：Quantized LoRA，在 LoRA 基础上引入 4-bit NF4 量化、双重量化和分页优化，使得单卡 24GB GPU 微调 65B 模型成为可能。

**边界说明**：QLoRA 是 LoRA 的进阶形式，核心优化在量化策略；QLoRA 的训练效果通常略低于 BF16 LoRA，但显存效率更高。

**来源**：https://arxiv.org/abs/2305.14314

---

### NF4

**定义**：4-bit Normal Float，QLoRA 使用的量化数据类型，专为神经网络权重设计，在 4-bit 精度下保持较好的数值表示能力。

**边界说明**：NF4 是 QLoRA 的核心量化技术，区别于普通的 INT4 量化；NF4 的使用是 QLoRA 相比标准 LoRA 显存占用更低的关键。

**来源**：https://arxiv.org/abs/2305.14314

---

### PEFT

**定义**：Parameter-Efficient Fine-Tuning，Hugging Face 维护的参数高效微调统一框架，封装了 LoRA、QLoRA、Prefix Tuning、Prompt Tuning 等多种方法。

**边界说明**：PEFT 是接口/框架层，提供统一 API 调用各种微调方法；PEFT 本身不实现底层训练逻辑，底层依赖 Transformers 和 Accelerate。

**来源**：https://github.com/huggingface/peft

---

### TRL

**定义**：Transformers Reinforcement Learning，Hugging Face 的训练框架，提供 SFT Trainer、DPO Trainer、PPO Trainer 等完整训练流程。

**边界说明**：TRL 是训练流程层，封装了完整的训练循环；TRL 支持使用 PEFT 接口的 LoRA，也支持集成 Unsloth 作为加速后端。

**来源**：https://github.com/huggingface/trl

---

### SFT

**定义**：Supervised Fine-Tuning，在标注数据上做监督学习的标准微调流程，是 LoRA/QLoRA 等方法在预训练模型上落地的常用训练方式。

**边界说明**：SFT 是训练阶段名称，区别于 DPO/PPO 等偏好学习方式；SFT 适用于有标注数据的任务微调。

**来源**：https://github.com/huggingface/trl

---

### DPO

**定义**：Direct Preference Optimization，直接偏好优化，通过偏好数据（chosen/rejected 回答对）直接优化语言模型，无需单独的 reward model。

**边界说明**：DPO 是 RLHF/PPO 的简化替代方案，训练流程更简洁；DPO 仍然是 Preference Learning 的一种，区别于 SFT 的纯监督学习。

**来源**：https://github.com/huggingface/trl

---

### Unsloth

**定义**：专注于加速 LoRA/QLoRA 微调的开源项目，通过自研 CUDA kernel 实现训练加速，底层依赖 PEFT/TRL/PyTorch。

**边界说明**：Unsloth 是加速层，不改变 LoRA 方法本身；Unsloth 可与 TRL 集成作为加速后端使用，集成方式以官方文档为准。

**来源**：https://github.com/unslothai/unsloth

---

Sources:
1. https://arxiv.org/abs/2106.09685 — LoRA 原始论文
2. https://arxiv.org/abs/2305.14314 — QLoRA 原始论文
3. https://github.com/huggingface/peft — PEFT 主仓库
4. https://github.com/huggingface/trl — TRL 主仓库
5. https://github.com/unslothai/unsloth — Unsloth 主仓库

Risk of Staleness:
- PEFT/TRL 版本更新快，具体 API 以实际安装版本为准
- LoRA 新变体（DoRA、GaLoRA 等）快速涌现，PEFT 集成状态实时变化
- Unsloth 更新频繁，加速效果以实际测试为准

Out of Scope Kept:
- 未写训练教程
- 未写过长背景介绍
- 未写多节点训练相关
