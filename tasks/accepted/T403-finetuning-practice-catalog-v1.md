Task ID: T403
Task Title: Finetuning Long-Run Pack v1
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 T207/T198/T304，整理 6 个最小实践入口（LoRA basic、QLoRA basic、PEFT basic、TRL SFT、DPO entry、Unsloth entry）。

Result:

# Finetuning Practice Catalog v1

## 概述

本目录整理 6 个低门槛 finetuning 最小实践，每个实践均可独立完成，帮助开发者从零到第一个微调产物。

---

### F01：LoRA basic — 使用 PEFT 配置 LoRA

**目标**：使用 Hugging Face PEFT 配置 LoRA，验证 LoRA 权重可正常保存。

```bash
pip install peft transformers
```

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig, get_peft_model

model_name = "Qwen/Qwen2.5-0.5B-Instruct"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

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
model.save_pretrained("./lora-checkpoint")
```

来源：https://github.com/huggingface/peft

---

### F02：QLoRA basic — 4-bit 量化 LoRA

**目标**：验证 QLoRA 配置正确，模型以 4-bit 加载。

```bash
pip install peft transformers bitsandbytes
```

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype="float16"
)
model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2.5-0.5B-Instruct",
    quantization_config=quantization_config
)
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct")

lora_config = LoraConfig(r=8, lora_alpha=16, target_modules=["q_proj", "k_proj", "v_proj", "o_proj"])
model = get_peft_model(model, lora_config)
```

来源：https://github.com/huggingface/peft
来源：https://arxiv.org/abs/2305.14314

---

### F03：PEFT basic — 使用 PEFT 加载和推理

**目标**：验证微调后的 LoRA adapter 可正确加载到模型并参与推理。

```python
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

base_model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct")
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct")

# 加载 LoRA adapter
model = PeftModel.from_pretrained(base_model, "./lora-checkpoint")
model.generate(**tokenizer("Hello world", return_tensors="pt"))
```

来源：https://github.com/huggingface/peft

---

### F04：TRL SFT — 使用 SFTTrainer 做监督微调

**目标**：使用 TRL 的 SFTTrainer 完成一个完整 SFT 训练流程。

```bash
pip install trl datasets
```

```python
from trl import SFTTrainer
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments

model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct")
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct")

training_args = TrainingArguments(
    output_dir="./sft-output",
    num_train_epochs=3,
    per_device_train_batch_size=2,
    learning_rate=2e-4,
)
trainer = SFTTrainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    tokenizer=tokenizer,
)
trainer.train()
```

来源：https://github.com/huggingface/trl

---

### F05：DPO entry — 使用 DPOTrainer 做偏好优化

**目标**：验证 DPO 训练配置正确。

```python
from trl import DPOTrainer
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments

model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct")
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct")

training_args = TrainingArguments(
    output_dir="./dpo-output",
    num_train_epochs=1,
    per_device_train_batch_size=2,
)
trainer = DPOTrainer(
    model=model,
    args=training_args,
    train_dataset=dpo_dataset,  # 包含 chosen/rejected 的数据集
    tokenizer=tokenizer,
)
trainer.train()
```

来源：https://github.com/huggingface/trl

---

### F06：Unsloth entry — 使用 Unsloth 加速 LoRA

**目标**：使用 Unsloth 加载模型并验证 LoRA 配置。

```bash
pip install unsloth
```

```python
from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="Qwen/Qwen2.5-0.5B-Instruct",
    max_seq_length=2048,
    dtype=None,
    load_in_4bit=True,
)

model = FastLanguageModel.get_peft_model(
    model,
    r=16,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
)
# 使用标准 PEFT API 继续训练
```

来源：https://github.com/unslothai/unsloth

---

## 实践分类

| 实践 | 分类 | 工具 | 门槛 |
|------|------|------|------|
| F01 LoRA basic | 方法验证 | PEFT + Transformers | 低（pip + Python） |
| F02 QLoRA basic | 方法验证 | PEFT + bitsandbytes | 低 |
| F03 PEFT inference | 推理验证 | PEFT | 低 |
| F04 TRL SFT | 完整训练 | TRL | 中（需要数据集） |
| F05 DPO entry | 偏好训练 | TRL | 中（需要偏好数据） |
| F06 Unsloth entry | 加速验证 | Unsloth | 低（pip） |

Sources:
1. https://github.com/huggingface/peft — PEFT
2. https://github.com/huggingface/trl — TRL
3. https://github.com/unslothai/unsloth — Unsloth
4. https://arxiv.org/abs/2106.09685 — LoRA 论文
5. https://arxiv.org/abs/2305.14314 — QLoRA 论文

Risk of Staleness:
- PEFT/TRL 版本更新快，具体 API 以实际安装版本为准
- Unsloth 更新频繁，加速效果以实际测试为准

Out of Scope Kept:
- 未写数据集准备教程
- 未写完整训练参数调优
- 未写模型部署相关
