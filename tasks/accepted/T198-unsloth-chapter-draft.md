# Unsloth

## 1. 这是什么

Unsloth 是一个专注于加速 LLM 微调的开源项目，通过自研 CUDA kernel 使 LoRA/QLoRA 微调速度提升 2x、显存占用减少约 50%（官方数据）。**Unsloth 不是完整的训练平台**，而是**微调加速层**，底层依赖 PyTorch、PEFT、TRL。

核心定位：提供优化过的 CUDA kernel，在 PEFT 接口下加速 LoRA/QLoRA 训练阶段，而非推理阶段。

## 2. 为什么重要

在 LLM 微调实践中，训练速度和显存是关键瓶颈：

1. **训练加速**：2x 速度提升意味着相同硬件下可做更多实验
2. **显存优化**：50% 显存减少使更大模型可在有限硬件上微调
3. **低门槛入门**：提供免费 Google Colab Notebooks，降低上手门槛
4. **主流模型支持**：Qwen、DeepSeek、Gemma、LLaMA 等主流开源模型均可使用

## 3. 核心原理

### 加速机制
Unsloth 通过以下方式加速 LoRA/QLoRA 训练：
- 优化过的 CUDA kernel 减少矩阵运算开销
- 显存布局优化减少内存访问延迟
- 混合精度训练优化

来源：https://github.com/unslothai/unsloth

### 与 PEFT 的关系
Unsloth 在 PEFT 接口下封装，提供 `PeftModel` 兼容层，训练代码与标准 PEFT 基本一致。

来源：https://github.com/huggingface/peft

### 与 TRL 的关系
Hugging Face TRL 的 SFTTrainer、DPOTrainer 已集成 Unsloth 作为可选后端，切换成本低。

来源：https://github.com/huggingface/trl

### 层级关系
```
PEFT（接口层）
  ↓
Unsloth / 原生 PyTorch（加速层）
  ↓
PyTorch（计算层）
```

## 4. 常见方案 / 组件

| 工具 | 定位 | 官方入口 |
|------|------|---------|
| **Unsloth** | 微调加速层，CUDA kernel 优化 | https://github.com/unslothai/unsloth |
| **Hugging Face PEFT** | 统一微调框架接口 | https://github.com/huggingface/peft |
| **Hugging Face TRL** | SFT/DPO/PPO 训练框架 | https://github.com/huggingface/trl |
| **Google Colab Notebooks** | 免费快速入门 notebook | https://github.com/unslothai/notebooks |
| **llama.cpp fork** | Unsloth 团队维护的 llama.cpp 优化版 | https://github.com/unslothai/llama.cpp |

来源：https://github.com/unslothai/unsloth
来源：https://github.com/unslothai/notebooks

## 5. 关键指标

| 指标 | 全称 | 说明 | 来源 |
|------|------|------|------|
| **Training Speed** | 训练速度 | tokens/second，相比原生提升 2x | https://github.com/unslothai/unsloth |
| **Memory Usage** | 显存占用 | 相比原生减少约 50% | https://github.com/unslothai/unsloth |
| **Supported Models** | 支持模型数 | Qwen、DeepSeek、Gemma、LLaMA 等 | https://github.com/unslothai/unsloth |
| **LoRA Rank** | 支持的 LoRA 秩 | 通常 8/16/32/64 | https://docs.unsloth.ai/ |

## 6. 常见误区

1. **"Unsloth 是完整训练平台"**：Unsloth 是加速层，需要配合 PEFT/TRL 使用，不是独立训练平台
2. **"Unsloth 和 PEFT 是竞争关系"**：Unsloth 在 PEFT 接口下运行，是 PEFT 的加速后端之一
3. **"Unsloth 加速推理"**：Unsloth 优化的是训练阶段，不是推理阶段
4. **"用了 Unsloth 就不需要 TRL"**：Unsloth 只负责底层计算加速，SFT/DPO 等训练流程仍需 TRL

## 7. 与项目关系

在 AI Infra 学习路径中，Unsloth 是微调加速的工具选项：

- finetune-demo 模块可选择 Unsloth 作为 LoRA 微调的加速后端
- 与 PEFT 是依赖关系：Unsloth 封装为 PEFT 的加速实现
- 与 TRL 的关系：SFTTrainer、DPOTrainer 可选择 Unsloth 后端

## 8. 最小实践任务

**目标**：使用 Unsloth 免费 Colab Notebook 快速启动 LoRA 微调，验证训练可正常运行。

```bash
# 1. 直接使用官方 Notebooks（推荐，无需本地安装）
# 访问：https://github.com/unslothai/notebooks
# 选择对应的模型 notebook（如 Qwen2.5）

# 2. 本地安装（可选）
pip install unsloth

# 3. 使用 Unsloth 加载模型
from unsloth import FastLanguageModel
import torch

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="Qwen/Qwen2.5-0.5B-Instruct",
    max_seq_length=2048,
    dtype=torch.float16,
    load_in_4bit=True,
)

# 4. 添加 LoRA
model = FastLanguageModel.get_peft_model(
    model,
    r=16,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_alpha=16,
    lora_dropout=0.05,
)

# 5. 开始训练（使用标准 PEFT API）
# 可直接复用 Hugging Face Trainer 或 TRL SFTTrainer
```

来源：https://github.com/unslothai/unsloth
来源：https://github.com/unslothai/notebooks

## 9. 输出物

- Unsloth 安装完成（或使用官方 Notebook）
- 成功加载 Qwen2.5-0.5B-Instruct 模型
- LoRA 微调配置完成（r=16）

## 10. 延伸阅读

1. https://github.com/unslothai/unsloth — Unsloth 主仓库
2. https://unsloth.ai/ — Unsloth 官方主页
3. https://github.com/unslothai/notebooks — 免费 Colab Notebooks 集合
4. https://docs.unsloth.ai/ — Unsloth 官方文档
5. https://github.com/huggingface/trl — TRL（含 Unsloth 集成）
6. https://github.com/huggingface/peft — PEFT 主仓库

Sources:
1. https://github.com/unslothai/unsloth — Unsloth 主仓库
2. https://unsloth.ai/ — Unsloth 官方主页
3. https://github.com/unslothai/notebooks — Notebooks 集合
4. https://docs.unsloth.ai/ — Unsloth 官方文档
5. https://github.com/huggingface/trl — TRL 主仓库
6. https://github.com/huggingface/peft — PEFT 主仓库

Risk of Staleness:
- Unsloth 版本更新快，官方 Notebooks 以实际安装版本为准
- 加速效果为官方数据，实际性能因模型、硬件、batch size 不同而有差异
- Unsloth 为独立项目，非 Hugging Face 官方产品

Out of Scope Kept:
- 未写完整训练实践
- 未写分布式训练架构
- 未做与其他微调框架的优劣对比
