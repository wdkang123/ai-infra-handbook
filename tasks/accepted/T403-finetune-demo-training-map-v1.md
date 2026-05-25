Task ID: T403
Task Title: Finetuning Long-Run Pack v1
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 T304，说明 finetune-demo 的训练路径拆分和资料入口，不写实现结论。

Result:

# Finetune Demo Training Map v1

## 模块定位回顾

finetune-demo 是 AI Infra 项目中负责**模型微调演示**的模块，提供 LoRA/QLoRA 微调的最小可运行流程，产出可用于 inference-service 部署的 adapter 权重。

## 训练路径拆分

finetune-demo 支持多条训练路径，以下是主要路径的拆分和对应资料入口。

### 路径一：LoRA 基本路径

```
数据集准备
    ↓
PEFT LoRA 配置（r=8, target_modules）
    ↓
SFT 训练（SFTTrainer）
    ↓
adapter 权重导出
    ↓
inference-service 加载
```

**关键资料入口**：
- LoRA 原理：https://arxiv.org/abs/2106.09685
- PEFT LoRA API：https://github.com/huggingface/peft
- TRL SFTTrainer：https://github.com/huggingface/trl

### 路径二：QLoRA 量化路径

```
数据集准备
    ↓
4-bit 量化加载（BitsAndBytes）
    ↓
PEFT LoRA 配置
    ↓
SFT 训练
    ↓
adapter 权重导出
    ↓
inference-service 加载（支持量化）
```

**关键资料入口**：
- QLoRA 原理：https://arxiv.org/abs/2305.14314
- BitsAndBytes 量化：https://github.com/TimDettmers/bitsandbytes
- vLLM LoRA 加载：https://docs.vllm.ai/en/latest/models/lora.html

### 路径三：Unsloth 加速路径

```
数据集准备
    ↓
Unsloth 模型加载（4bit/bf16）
    ↓
PEFT LoRA 配置（接口不变）
    ↓
SFT 训练（PEFT API，底层 Unsloth kernel）
    ↓
adapter 权重导出
    ↓
inference-service 加载
```

**关键资料入口**：
- Unsloth 主仓库：https://github.com/unslothai/unsloth
- Unsloth Notebooks：https://github.com/unslothai/notebooks
- Unsloth 与 PEFT 关系：https://docs.unsloth.ai/

### 路径四：DPO 偏好优化路径

```
SFT 训练产物
    ↓
偏好数据集准备（chosen/rejected）
    ↓
DPOTrainer 训练
    ↓
adapter 权重导出
    ↓
inference-service 加载
```

**关键资料入口**：
- DPO 原理：https://github.com/huggingface/trl
- TRL DPOTrainer：https://github.com/huggingface/trl

## 与其他模块的交接边界

```
finetune-demo
    │ 训练
    ↓
微调产物（adapter 权重）
    │
    │ 部署
    ↓
inference-service
    │ 推理
    ↓
eval-module（评测微调后模型）
```

**交接点**：
- finetune-demo **导出** adapter 权重到指定目录
- inference-service **加载** adapter 权重并启动推理服务
- eval-module **评测** 部署后模型的质量

## 资料入口汇总

| 主题 | 资料入口 | 用途 |
|------|---------|------|
| LoRA 原理 | https://arxiv.org/abs/2106.09685 | 理解 LoRA 低秩分解机制 |
| QLoRA 原理 | https://arxiv.org/abs/2305.14314 | 理解 4-bit NF4 量化 |
| PEFT | https://github.com/huggingface/peft | LoRA/QLoRA 配置 API |
| TRL | https://github.com/huggingface/trl | SFT/DPO 训练器 |
| Unsloth | https://github.com/unslothai/unsloth | 训练加速 |
| Unsloth Notebooks | https://github.com/unslothai/notebooks | 快速入门示例 |
| vLLM LoRA 加载 | https://docs.vllm.ai/en/latest/models/lora.html | 部署 adapter 到 vLLM |

## 需要 Codex 判断的点

1. **MVP 默认训练路径**：LoRA 还是 QLoRA 作为默认训练路径？
2. **DPO 是否纳入 MVP**：DPO 训练需要偏好数据，是否属于 MVP 必须？
3. **Unsloth 加速是否可选**：作为可选优化还是 MVP 必须？
4. **adapter 权重导出格式**：safetensors 还是 ckpt？是否有特殊要求？

Sources:
1. https://arxiv.org/abs/2106.09685 — LoRA 原始论文
2. https://arxiv.org/abs/2305.14314 — QLoRA 原始论文
3. https://github.com/huggingface/peft — PEFT 主仓库
4. https://github.com/huggingface/trl — TRL 主仓库
5. https://github.com/unslothai/unsloth — Unsloth 主仓库
6. https://github.com/unslothai/notebooks — Unsloth Notebooks
7. https://docs.vllm.ai/en/latest/models/lora.html — vLLM LoRA 加载文档

Risk of Staleness:
- PEFT/TRL 版本更新快，具体 API 以实际安装版本为准
- Unsloth 更新频繁，加速效果以实际测试为准
- vLLM LoRA 加载方式可能随版本变化

Out of Scope Kept:
- 未写代码实现
- 未写最终训练架构结论
- 未写分布式训练方案
