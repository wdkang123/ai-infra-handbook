Task ID: T173
Task Title: 搜集 LoRA / QLoRA / PEFT 官方资料与核心链接
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
搜集 LoRA、QLoRA、PEFT 在 AI Infra / finetuning 路线中的资料包，包含术语边界、官方论文/仓库、核心定位、最近更新线索、优先阅读链接。

Result:

## 一、术语边界说明

### LoRA（Low-Rank Adaptation）
微软 2021 年提出的参数高效微调方法。核心思想：在预训练模型的权重矩阵旁添加低秩分解矩阵（A、B），只训练这两个小矩阵而非全量参数，大幅减少可训练参数数量。

- 原始论文：https://arxiv.org/abs/2106.09685
- 官方仓库：https://github.com/microsoft/LoRA

### QLoRA（Quantized LoRA）
华盛顿大学 2023 年提出的方法，结合 4-bit 量化与 LoRA，进一步降低显存占用，使得在单卡 24GB GPU 上微调 65B 模型成为可能。

- 原始论文：https://arxiv.org/abs/2305.14314
- 官方仓库：https://github.com/artidoro/qlora

### PEFT（Parameter-Efficient Fine-Tuning）
Hugging Face 维护的库，封装了 LoRA、QLoRA、Prefix Tuning、Prompt Tuning、AdaLoRA 等多种参数高效微调方法。是目前最主流的 PEFT 框架。

- 官方仓库：https://github.com/huggingface/peft

### 三者关系
- **LoRA** 是底层方法
- **QLoRA** 是 LoRA + 量化，是 LoRA 的一种进阶形式
- **PEFT** 是实现上述方法的库，同时包含 LoRA 以外的其他 PEFT 方法

## 二、官方论文 / 仓库 / 文档

| 资料 | 官方入口 |
|------|---------|
| **LoRA 原始论文** | https://arxiv.org/abs/2106.09685 |
| **QLoRA 原始论文** | https://arxiv.org/abs/2305.14314 |
| **LoRA GitHub** | https://github.com/microsoft/LoRA |
| **QLoRA GitHub** | https://github.com/artidoro/qlora |
| **Hugging Face PEFT** | https://github.com/huggingface/peft |
| **Hugging Face TRL**（含 SFT/DPO/PPO）| https://github.com/huggingface/trl |

## 三、核心定位与适用场景

| 方法 | 定位 | 适用场景 | 显存需求 |
|------|------|---------|---------|
| LoRA | 全参数微调的高效替代 | 领域适配、任务定制 | 中等（~单卡 A100）|
| QLoRA | 极致显存优化 | 个人开发者、小团队微调 | 低（单卡 24GB）|
| PEFT | 统一框架 | 通用微调工程 | 取决于底层方法 |
| Prefix/Prompt Tuning | 更激进参数节省 | 极端场景 | 极低 |

## 四、最近 6-12 个月更新线索（有精确来源的）

- **PEFT 持续更新**：LoRA+ 新技术集成（GA、RS、DoRA 等新 LoRA 变体）
  - 来源：https://github.com/huggingface/peft/releases
- **TRL v0.14+**：SFTTrainer、DPOTrainer 等集成 Unsloth 加速
  - 来源：https://github.com/huggingface/trl/releases
- **Unsloth**：2x 训练速度、50% 显存占用的 LoRA 微调优化内核
  - 来源：https://github.com/unslothai/unsloth

注：DoRA（Weight-Decomposed LoRA）、GaLoRA 等新变体为 2024-2025 年研究进展，可关注 PEFT 库的集成更新。

## 五、精确优先阅读链接（7 个）

1. **LoRA 论文**：https://arxiv.org/abs/2106.09685
2. **QLoRA 论文**：https://arxiv.org/abs/2305.14314
3. **PEFT GitHub**：https://github.com/huggingface/peft
4. **TRL GitHub**：https://github.com/huggingface/trl
5. **Unsloth GitHub**：https://github.com/unslothai/unsloth
6. **LoRA 官方 GitHub**：https://github.com/microsoft/LoRA
7. **QLoRA 官方 GitHub**：https://github.com/artidoro/qlora

Sources:
1. https://arxiv.org/abs/2106.09685 — LoRA 原始论文
2. https://arxiv.org/abs/2305.14314 — QLoRA 原始论文
3. https://github.com/huggingface/peft — PEFT 主仓库
4. https://github.com/huggingface/trl — TRL 主仓库
5. https://github.com/unslothai/unsloth — Unsloth 主仓库
6. https://github.com/microsoft/LoRA — LoRA 官方仓库
7. https://github.com/artidoro/qlora — QLoRA 官方仓库

Risk of Staleness:
- PEFT 库版本更新快，具体 API 以实际安装版本为准
- LoRA 新变体（DoRA、GaLoRA 等）快速涌现，PEFT 集成状态实时变化
- Unsloth 更新频繁，加速效果以实际测试为准

Out of Scope Kept:
- 未写完整训练章节
- 未写微调路线总论
- 未做微调框架排名
