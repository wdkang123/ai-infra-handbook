# LoRA / PEFT

## 1. 这是什么

LoRA（Low-Rank Adaptation）和 PEFT（Parameter-Efficient Fine-Tuning）是 LLM 参数高效微调的核心技术，用于在有限计算资源下对预训练模型做任务适配或领域适应。

- **LoRA**：在预训练模型权重矩阵旁添加低秩分解矩阵（A、B），只训练这两个小矩阵而非全量参数
- **QLoRA**：LoRA + 4-bit 量化，进一步降低显存占用
- **PEFT**：Hugging Face 维护的统一框架，封装 LoRA、QLoRA、Prefix Tuning、Prompt Tuning 等多种方法

## 2. 为什么重要

在 AI Infra 微调实践中，全参数微调成本高昂：

1. **显存节省**：LoRA 将可训练参数从数十亿降低到几百万，显存需求大幅减少
2. **成本降低**：QLoRA 使得单卡 24GB GPU 微调 65B 模型成为可能
3. **快速迭代**：小数据集场景下 LoRA 收敛快，适合快速实验
4. **模块化管理**：不同任务 LoRA 权重可独立存储和切换

## 3. 核心原理

### LoRA 原理
在预训练模型权重矩阵 W 旁，添加低秩分解矩阵 A 和 B。前向传播时 h = Wx + BAx，其中 BA 为低秩矩阵。只训练 A、B，全量 W 冻结。

- 原始论文：https://arxiv.org/abs/2106.09685
- 官方仓库：https://github.com/microsoft/LoRA

### QLoRA 原理
在 LoRA 基础上引入 4-bit 量化（NF4 数据类型），结合双重量化（Double Quantization）和分页优化，进一步降低显存。

- 原始论文：https://arxiv.org/abs/2305.14314
- 官方仓库：https://github.com/artidoro/qlora

### PEFT 框架
Hugging Face PEFT 库统一封装了 LoRA、QLoRA 及其他 PEFT 方法，提供简洁 API。

- 官方仓库：https://github.com/huggingface/peft

### 三者关系
```
LoRA：底层微调方法（添加低秩矩阵）
  ↓
QLoRA：LoRA + 4-bit 量化（显存极致优化）
  ↓
PEFT：统一框架（封装 LoRA、QLoRA 及其他方法）
```

## 4. 常见方案 / 组件

| 工具 | 定位 | 官方入口 |
|------|------|---------|
| **Hugging Face PEFT** | 主流 PEFT 框架，支持 LoRA/QLoRA 等 | https://github.com/huggingface/peft |
| **Hugging Face TRL** | SFT/DPO/PPO 训练框架，含 LoRA 集成 | https://github.com/huggingface/trl |
| **Unsloth** | LoRA/QLoRA 微调加速层（2x 速度、50% 显存） | https://github.com/unslothai/unsloth |
| **LoRA 官方仓库** | 微软 LoRA 原始实现 | https://github.com/microsoft/LoRA |
| **QLoRA 官方仓库** | QLoRA 原始实现 | https://github.com/artidoro/qlora |

来源：https://github.com/huggingface/peft
来源：https://github.com/huggingface/trl

## 5. 关键指标

| 指标 | 全称 | 说明 | 来源 |
|------|------|------|------|
| **Trainable Params** | 可训练参数量 | LoRA 添加的小矩阵参数量 | https://arxiv.org/abs/2106.09685 |
| **Rank (r)** | LoRA 秩 | 低秩矩阵的秩值，影响容量与参数量 | https://arxiv.org/abs/2106.09685 |
| **Target Modules** | 目标模块 | LoRA 应用到的模型层（如 q_proj, v_proj） | https://github.com/huggingface/peft |
| **Quantization Bits** | 量化位数 | QLoRA 的量化精度（通常 4-bit NF4） | https://arxiv.org/abs/2305.14314 |

## 6. 常见误区

1. **"LoRA 和 QLoRA 是两个独立技术"**：QLoRA 是在 LoRA 基础上增加量化，是 LoRA 的进阶形式
2. **"PEFT 就是 LoRA"**：PEFT 是封装多种方法的框架，LoRA 只是其中一种
3. **"LoRA 训练效果不如全参数微调"**：在特定任务（指令遵循、领域适配）上，LoRA 可达到接近全参数微调的效果，且效率更高
4. **"Unsloth 是独立训练平台"**：Unsloth 是 PEFT 接口下的加速内核，不是完整训练平台

## 7. 与项目关系

在 AI Infra 学习路径中，LoRA/PEFT 是模型微调的核心技术：

- finetune-demo 模块参考 LoRA/QLoRA 的微调路径设计
- Unsloth 在 PEFT 接口下加速训练，但不属于 PEFT 本身
- TRL（Transformers Reinforcement Learning）提供 SFT/DPO/PPO 的完整训练流程

## 8. 最小实践任务

**目标**：使用 Hugging Face PEFT 对本地 vLLM 推理服务的基础模型做 LoRA 微调，验证 LoRA 权重可正常训练和加载。

```bash
# 1. 安装 PEFT 和 transformers
pip install peft transformers

# 2. 加载基础模型和 tokenizer
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, LoraConfig
from peft import get_peft_model

model_name = "Qwen/Qwen2.5-0.5B-Instruct"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# 3. 配置 LoRA
lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
# 输出：trainable params: 1,888,320 || all params: 314,773,632 || trainable%: 0.5998

# 4. 保存 LoRA 权重
model.save_pretrained("./lora-checkpoint")

# 5. 加载微调后的 LoRA 权重到推理模型
# 在 vLLM 中通过 --lora-config 参数加载
```

来源：https://github.com/huggingface/peft
来源：https://arxiv.org/abs/2106.09685

## 9. 输出物

- PEFT 和 transformers 安装完成
- LoRA 配置可训练参数输出（r=8 时约 0.6% 可训练）
- LoRA 权重保存到本地目录

## 10. 延伸阅读

1. https://arxiv.org/abs/2106.09685 — LoRA 原始论文
2. https://arxiv.org/abs/2305.14314 — QLoRA 原始论文
3. https://github.com/huggingface/peft — Hugging Face PEFT 主仓库
4. https://github.com/huggingface/trl — Hugging Face TRL 主仓库
5. https://github.com/unslothai/unsloth — Unsloth（微调加速层）
6. https://github.com/microsoft/LoRA — LoRA 官方仓库
7. https://github.com/artidoro/qlora — QLoRA 官方仓库

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
- 未写完整训练实践
- 未写多节点训练方案
- 未做微调框架排名
