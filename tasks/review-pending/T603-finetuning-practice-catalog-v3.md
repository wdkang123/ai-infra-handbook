Task ID: T603
Task Title: Finetuning / Training Zero-Touch Pack
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
整理8到10个从最小训练验证到偏工程化训练路径的实践。

Result:

# Finetuning Practice Catalog v3

## 概述

本文档整理从最小训练验证到工程化训练路径的实践，覆盖 LoRA/QLoRA 的最小实践、TRL 使用、与评测联动等场景。

---

## 最小训练验证实践

---

### F01：PEFT + LoRA 最小配置

**目标**：验证 PEFT 库和 LoRA 配置可用。

```bash
pip install peft
```

```python
from peft import LoraConfig, get_peft_model

lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(base_model, lora_config)
model.print_trainable_parameters()
```

来源：https://github.com/huggingface/peft

---

### F02：trl SFTTrainer 单机 SFT

**目标**：使用 trl 的 SFTTrainer 完成监督微调。

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

### F03：Unsloth 加速 LoRA 训练

**目标**：验证 Unsloth 可用并确认加速效果。

```bash
pip install unsloth
```

```python
from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/llama-2-7b",
    max_seq_length=2048,
    dtype=None,
    load_in_4bit=True
)

model = FastLanguageModel.get_peft_model(
    model,
    r=16,
    target_modules=["q_proj", "v_proj"],
    lora_alpha=32
)
```

来源：https://github.com/unslothai/unsloth

---

## 量化训练实践

---

### F04：QLoRA 4-bit 量化微调

**目标**：在消费级 GPU 上完成 QLoRA 全流程。

```python
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import prepare_model_for_kbit_training, LoraConfig, get_peft_model

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype="float16"
)

model = AutoModelForCausalLM.from_pretrained(
    "your-model",
    quantization_config=bnb_config,
    device_map="auto"
)
model = prepare_model_for_kbit_training(model)

lora_config = LoraConfig(r=64, lora_alpha=16, target_modules=["q_proj", "v_proj"])
model = get_peft_model(model, lora_config)
trainer.train()
```

来源：https://arxiv.org/abs/2305.14314

---

### F05：bitsandbytes 8-bit 量化加载

**目标**：使用 8-bit 量化减少显存。

```python
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(
    load_in_8bit=True,
    llm_int8_threshold=6.0
)

model = AutoModelForCausalLM.from_pretrained(
    "your-model",
    quantization_config=bnb_config,
    device_map="auto"
)
```

来源：https://github.com/TimDettmers/bitsandbytes

---

## 偏好优化实践

---

### F06：DPO 偏好优化

**目标**：验证 DPO 训练流程（需要偏好数据集）。

```python
from trl import DPOTrainer
from transformers import TrainingArguments

dpo_trainer = DPOTrainer(
    model=model,
    ref_model=ref_model,
    train_dataset=preference_dataset,  # 需包含 chosen/rejected
    args=TrainingArguments(
        output_dir="./dpo_output",
        num_train_epochs=3,
        per_device_train_batch_size=2,
        learning_rate=1e-5,
    )
)
dpo_trainer.train()
```

来源：https://arxiv.org/abs/2305.18290

---

## 适配器管理实践

---

### F07：LoRA 适配器保存/加载/合并

**目标**：了解适配器的保存、加载和合并。

```python
# 保存
model.save_pretrained("./lora_adapter")

# 加载
from peft import PeftModel
model = PeftModel.from_pretrained(base_model, "./lora_adapter")

# 合并（推理时不再需要适配器）
merged_model = model.merge_and_unload()
merged_model.save_pretrained("./merged_model")
```

来源：https://github.com/huggingface/peft

---

### F08：多 LoRA 配置对比实验

**目标**：对比不同 rank/alpha 配置的效果差异。

```python
configs = [
    {"r": 8, "lora_alpha": 16},
    {"r": 16, "lora_alpha": 32},
    {"r": 64, "lora_alpha": 128},
]

results = []
for cfg in configs:
    model = get_peft_model(base_model, LoraConfig(**cfg, target_modules=["q_proj", "v_proj"]))
    trainer = SFTTrainer(...)
    trainer.train()
    eval_result = run_benchmark(model, tasks=["mmlu"])
    results.append({"config": cfg, "mmlu": eval_result["mmlu"]})
```

来源：https://github.com/huggingface/peft

---

## 与其他模块联动实践

---

### F09：finetune 后 benchmark 评测验证

**目标**：微调后自动运行 benchmark 验证效果。

```
finetune 模型
    ↓ 保存 adapter
eval-module
    ↓ 加载 adapter + base model
运行 MMLU/GSM8K benchmark
    ↓
评测结果 JSON
```

```python
finetuned_model = load_adapted_model("./lora_adapter")
eval_results = run_benchmark(finetuned_model, tasks=["mmlu", "gsm8k"])
save_eval_results(eval_results, "finetune_eval_results.json")
```

来源：https://github.com/EleutherAI/lm-evaluation-harness

---

### F10：训练 metrics 上报 Langfuse

**目标**：训练过程 metrics 上报 Langfuse。

```python
from langfuse import Langfuse
langfuse = Langfuse()

class LangfuseCallback:
    def on_log(self, logs):
        langfuse.log(
            name="finetune_metrics",
            metadata={
                "step": logs["step"],
                "loss": logs["loss"],
                "learning_rate": logs["learning_rate"]
            }
        )
```

来源：https://langfuse.com/docs/observability/overview

---

## 实践分类总览

| 实践 | 分类 | 门槛 | 组件数 |
|------|------|------|-------|
| F01 PEFT + LoRA 配置 | 最小验证 | 低 | 1 |
| F02 SFTTrainer SFT | 最小验证 | 中 | 1 |
| F03 Unsloth 加速 | 最小验证 | 中 | 1 |
| F04 QLoRA 量化 | 量化训练 | 中 | 1 |
| F05 8-bit 量化加载 | 量化训练 | 低 | 1 |
| F06 DPO 偏好优化 | 偏好优化 | 高 | 1 |
| F07 适配器管理 | 适配器管理 | 低 | 1 |
| F08 LoRA 参数对比 | 适配器管理 | 中 | 1 |
| F09 finetune + eval 联动 | 模块联动 | 中 | 2 |
| F10 Langfuse metrics 上报 | 模块联动 | 中 | 2 |

Sources:
1. https://github.com/huggingface/peft — PEFT
2. https://github.com/huggingface/trl — TRL
3. https://github.com/unslothai/unsloth — Unsloth
4. https://arxiv.org/abs/2305.14314 — QLoRA
5. https://arxiv.org/abs/2305.18290 — DPO
6. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval
7. https://langfuse.com/docs/observability/overview — Langfuse
8. https://github.com/TimDettmers/bitsandbytes — bitsandbytes

Risk of Staleness:
- PEFT/TRL/Unsloth 版本更新可能影响 API 兼容性
- QLoRA 量化配置可能随库版本变化

Out of Scope Kept:
- 未写完整 RLHF 训练流程
- 未写数据准备详细步骤
- 未写分布式训练配置
