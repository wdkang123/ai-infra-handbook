Task ID: T603
Task Title: Finetuning / Training Zero-Touch Pack
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
给 finetune-demo 提供更完整的训练路径说明，资料级输入，不是实现设计。

Result:

# Finetune Demo Training Map v2

## 概述

本文档说明 finetune-demo 的可能训练路径，基于 T304 MVP 结果和最新实践积累，给出资料级输入。

---

## 训练路径总览

```
finetune-demo
    ├── LoRA 路径（主要）
    │     ├── QLoRA（低显存，MVP 默认）
    │     └── LoRA（标准显存）
    │
    ├── SFT 路径
    │     └── trl SFTTrainer
    │
    ├── DPO 路径（后续迭代）
    │     └── trl DPOTrainer
    │
    └── Unsloth 加速（可选）
          └── FastLanguageModel
```

---

## LoRA / QLoRA 路径

### QLoRA（低显存场景，MVP 默认）

适用条件：
- GPU 显存 < 20GB
- 快速验证
- 消费级 GPU

```python
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype="float16"
)

model = AutoModelForCausalLM.from_pretrained(
    "your-model",
    quantization_config=bnb_config
)
model = get_peft_model(model, LoraConfig(r=64, lora_alpha=16))
```

来源：https://arxiv.org/abs/2305.14314

### LoRA（标准显存场景）

适用条件：
- GPU 显存 >= 20GB
- 追求更好效果
- 不需要量化

```python
from peft import LoraConfig, get_peft_model

lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    task_type="CAUSAL_LM"
)
model = get_peft_model(base_model, lora_config)
```

来源：https://arxiv.org/abs/2106.09685

---

## SFT 路径

### trl SFTTrainer

适用场景：需要在标注数据上直接训练模型。

```python
from trl import SFTTrainer
from transformers import TrainingArguments

trainer = SFTTrainer(
    model=base_model,
    train_dataset=train_dataset,
    dataset_text_field="text",
    max_seq_length=512,
    args=TrainingArguments(
        output_dir="./output",
        num_train_epochs=3,
        per_device_train_batch_size=4,
        learning_rate=2e-4,
    )
)
trainer.train()
```

来源：https://github.com/huggingface/trl

---

## DPO 路径（后续迭代）

### 何时进入 DPO

- 有高质量偏好数据集
- 需要比 SFT 更精细的效果优化
- 愿意投入数据标注成本

### DPO 基本流程

```python
from trl import DPOTrainer

dpo_trainer = DPOTrainer(
    model=model,
    ref_model=ref_model,
    train_dataset=preference_dataset,
    args=TrainingArguments(output_dir="./dpo_output", num_train_epochs=3)
)
dpo_trainer.train()
```

来源：https://arxiv.org/abs/2305.18290

---

## Unsloth 加速路径（可选）

### 何时使用 Unsloth

- 有 Ampere/Hopper GPU
- 追求训练加速
- 不需要 DPO

```python
from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/llama-2-7b",
    load_in_4bit=True
)
model = FastLanguageModel.get_peft_model(model, r=16)
```

来源：https://github.com/unslothai/unsloth

---

## 训练后验证路径

### 与 eval-module 联动

```
finetune 模型（adapter）
    ↓
eval-module 加载（base model + adapter）
    ↓
运行 benchmark（MMLU / GSM8K / HumanEval）
    ↓
评测结果 JSON
```

```python
# 加载微调后模型
finetuned_model = load_adapted_model("./lora_adapter")

# 运行评测
eval_results = run_benchmark(finetuned_model, tasks=["mmlu", "gsm8k"])

# 对比基线
baseline_results = load_baseline_results("./baseline_eval.json")
for task in eval_results:
    diff = eval_results[task] - baseline_results[task]
    print(f"{task}: {diff:+.4f}")
```

来源：https://github.com/EleutherAI/lm-evaluation-harness

---

## 训练路径选择决策树

```
输入：GPU 显存
    │
    ├── < 10GB
    │     → QLoRA（4-bit）+ Unsloth（如 GPU 兼容）
    │
    ├── 10GB - 20GB
    │     → QLoRA 或 LoRA（视模型大小而定）
    │
    └── >= 20GB
          → LoRA（全参数或量化可选）

输入：是否需要 DPO
    │
    ├── 否
    │     → SFT（trl SFTTrainer）
    │
    └── 是
          → DPO（需要偏好数据集）
```

---

## 与其他模块的协作

| 模块 | 协作方式 |
|------|---------|
| inference-service | 训练后的 adapter 可加载到 inference-service 做推理 |
| eval-module | 训练后用 benchmark 验证效果 |
| Langfuse | 训练 metrics 上报（可选） |
| Prometheus | 训练资源监控（可选） |

来源：https://langfuse.com/docs/observability/overview
来源：https://prometheus.io/

Sources:
1. https://arxiv.org/abs/2106.09685 — LoRA
2. https://arxiv.org/abs/2305.14314 — QLoRA
3. https://arxiv.org/abs/2305.18290 — DPO
4. https://github.com/huggingface/peft — PEFT
5. https://github.com/huggingface/trl — TRL
6. https://github.com/unslothai/unsloth — Unsloth
7. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval

Risk of Staleness:
- LoRA/QLoRA 超参数最佳实践可能随新研究更新
- PEFT/TRL API 可能随版本变化

Out of Scope Kept:
- 未写代码实现
- 未写数据准备详细步骤
- 未写分布式训练配置
