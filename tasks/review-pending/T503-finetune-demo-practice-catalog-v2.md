Task ID: T503
Task Title: Finetuning Long-Run Pack v2
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
在 v1 基础上补全从单机到多组件的 finetuning 最小实践路径。

Result:

# Finetune Demo Practice Catalog v2

## 概述

本文档在 v1 基础上补充更完整的 finetuning 实践路径，覆盖 LoRA/QLoRA 的最小实践、多组件协同训练、以及与评测和可观测性的联动。

---

## 单机单步骤实践（低门槛）

---

### F01：安装 PEFT 库并加载 LoRA 配置

**目标**：验证 PEFT 库可用，了解 LoRA 配置参数。

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
```

来源：https://github.com/huggingface/peft

---

### F02：使用 trl 进行单机 SFT 微调

**目标**：在单机上跑通 SFT 最小流程。

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

### F03：使用 Unsloth 加速 LoRA 训练

**目标**：验证 Unsloth 可用，确认加速效果。

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

## 单机多步骤实践

---

### F04：QLoRA 4-bit 量化微调完整流程

**目标**：在消费级 GPU 上完成 QLoRA 微调全流程。

```python
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import prepare_model_for_kbit_training, LoraConfig, get_peft_model

# 4-bit 量化配置
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype="float16"
)

# 加载量化模型
model = AutoModelForCausalLM.from_pretrained(
    "your-model",
    quantization_config=bnb_config,
    device_map="auto"
)
model = prepare_model_for_kbit_training(model)

# 配置 LoRA
lora_config = LoraConfig(r=64, lora_alpha=16, target_modules=["q_proj", "v_proj"])
model = get_peft_model(model, lora_config)

# 开始训练
trainer.train()
```

来源：https://arxiv.org/abs/2305.14314

---

### F05：使用 DPO 进行偏好优化

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

### F06：保存和加载 LoRA 适配器

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

## 多组件协同实践

---

### F07：finetune + eval-module 评测串联

**目标**：微调后自动运行 benchmark 评测，验证效果。

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
# 微调后自动评测
finetuned_model = load_adapted_model("./lora_adapter")
eval_results = run_benchmark(finetuned_model, tasks=["mmlu", "gsm8k"])
save_eval_results(eval_results, "finetune_eval_results.json")
```

来源：https://github.com/EleutherAI/lm-evaluation-harness

---

### F08：finetune + Langfuse 上报训练 metrics

**目标**：训练过程的 metrics（loss、learning_rate）上报 Langfuse。

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

### F09：finetune + Prometheus 监控训练资源

**目标**：训练过程 GPU 利用率、显存上报 Prometheus。

```bash
# 在训练脚本中启动 metrics 端点
# 使用 pytorchfinetuner 或自定义 hook 暴露 /metrics

# Prometheus 抓取配置
# prometheus.yml:
#   scrape_configs:
#     - job_name: 'finetune'
#       static_configs:
#         - targets: ['localhost:8000']
```

来源：https://prometheus.io/

---

### F10：多实验 LoRA 参数对比

**目标**：对比不同 LoRA rank/alpha 配置的效果差异。

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

# 汇总对比
for r in results:
    print(f"r={r['config']['r']}, alpha={r['config']['lora_alpha']}: mmlu={r['mmlu']:.4f}")
```

来源：https://github.com/huggingface/peft

---

## 实践分类总览

| 实践 | 分类 | 门槛 | 组件数 |
|------|------|------|-------|
| F01 PEFT + LoRA 配置 | 单机单步骤 | 低 | 1 |
| F02 trl SFT 微调 | 单机单步骤 | 中 | 1 |
| F03 Unsloth 加速 | 单机单步骤 | 中 | 1 |
| F04 QLoRA 量化微调 | 单机多步骤 | 中 | 1 |
| F05 DPO 偏好优化 | 单机多步骤 | 高 | 1 |
| F06 Adapter 保存/加载/合并 | 单机多步骤 | 低 | 1 |
| F07 finetune + eval 串联 | 多组件 | 中 | 2 |
| F08 finetune + Langfuse | 多组件 | 中 | 2 |
| F09 finetune + Prometheus | 多组件 | 中 | 2 |
| F10 LoRA 参数对比实验 | 多组件 | 中 | 2 |

Sources:
1. https://github.com/huggingface/peft — PEFT
2. https://github.com/huggingface/trl — TRL
3. https://github.com/unslothai/unsloth — Unsloth
4. https://arxiv.org/abs/2305.14314 — QLoRA
5. https://arxiv.org/abs/2305.18290 — DPO
6. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval
7. https://langfuse.com/docs/observability/overview — Langfuse
8. https://prometheus.io/ — Prometheus

Risk of Staleness:
- PEFT/TRL/Unsloth 版本更新可能影响 API 兼容性
- QLoRA 量化配置可能随库版本变化

Out of Scope Kept:
- 未写完整 RLHF 训练流程
- 未写数据准备详细步骤
- 未写分布式训练配置
