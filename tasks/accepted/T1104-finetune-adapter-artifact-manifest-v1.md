# finetune-demo Adapter Artifact Manifest v1

## Task ID: T1104
## Title: finetune-demo Fixture Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# finetune-demo Adapter Artifact Manifest

本文档定义 PEFT LoRA / QLoRA adapter 产物的清单，对应真实文件 `finetune-demo/outputs/`。

## Adapter 类型

| Adapter 类型 | 精度 | 量化 | 产物大小（Qwen2.5-0.5B） |
|---|---|---|---|
| `lora_qwen_05b` | FP16 | 无 | ~50 MB |
| `qlora_qwen_05b` | BF16 | NF4 | ~30 MB |

---

## Adapter 产物清单

### checkpoint-XXX/ 目录结构

**对应文件：** `finetune-demo/outputs/qlora_qwen_05b/checkpoint-300/`

```
checkpoint-300/
├── adapter_config.json       # PEFT adapter 配置
├── adapter_model.safetensors # LoRA adapter 权重（NF4 量化）
├── README.md                 # Adapter 使用说明
└── tokenizer.json            # Tokenizer 配置（PEFT 不改 tokenizer）
```

---

### adapter_config.json（LoRA）

**对应文件：** `finetune-demo/outputs/qlora_qwen_05b/checkpoint-300/adapter_config.json`

```json
{
  "auto_mapping": null,
  "base_model_name_or_path": "Qwen/Qwen2.5-0.5B-Instruct",
  "bias": "none",
  "fan_in_fan_out": false,
  "inference_mode": true,
  "init_lora_weights": true,
  "layers_pattern": null,
  "layers_to_transform": null,
  "lora_alpha": 64,
  "lora_dropout": 0.1,
  "modules_to_save": null,
  "peft_type": "LORA",
  "r": 64,
  "revision": null,
  "target_modules": [
    "q_proj",
    "k_proj",
    "v_proj",
    "o_proj",
    "gate_proj",
    "up_proj",
    "down_proj"
  ],
  "task_type": "CAUSAL_LM"
}
```

---

### adapter_config.json（QLoRA 扩展字段）

当 `load_in_4bit: true` 时，adapter_config.json 额外包含：

```json
{
  "bnb_4bit_compute_dtype": "bfloat16",
  "bnb_4bit_quant_type": "nf4",
  "bnb_4bit_use_double_quant": true,
  "load_in_4bit": true
}
```

---

## 如何加载 Adapter

### 方法 1: PEFT + Transformers

```python
from peft import PeftModel, AutoPeftModelForCausalLM
from transformers import AutoTokenizer, AutoModelForCausalLM

base_model = AutoPeftModelForCausalLM.from_pretrained(
    "Qwen/Qwen2.5-0.5B-Instruct",
    quantization_config={"load_in_4bit": True},  # for QLoRA
    device_map="auto"
)

model = PeftModel.from_pretrained(base_model, "./outputs/qlora_qwen_05b/checkpoint-300")
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct")

# 合并 adapter 到 base model（可选）
merged_model = model.merge_and_unload()
```

---

### 方法 2: 直接合并输出

```python
from peft import PeftModel, AutoPeftModelForCausalLM
from transformers import AutoTokenizer

model = AutoPeftModelForCausalLM.from_pretrained(
    "Qwen/Qwen2.5-0.5B-Instruct",
    "outputs/qlora_qwen_05b/checkpoint-300",
    quantization_config={"load_in_4bit": True},
    device_map="auto"
)
merged_model = model.merge_and_unload()
merged_model.save_pretrained("./outputs/merged_qwen_05b")
tokenizer.save_pretrained("./outputs/merged_qwen_05b")
```

合并后的目录：
```
outputs/merged_qwen_05b/
├── config.json
├── generation_config.json
├── model.safetensors
├── tokenizer.json
├── tokenizer_config.json
└── merges.txt
```

---

## Adapter 产物与验收 Checklist

| 检查项 | 对应文件 | 说明 |
|---|---|---|
| `adapter_config.json` 存在 | `checkpoint-XXX/adapter_config.json` | PEFT config |
| `r` 参数正确 | `adapter_config.json.r` | LoRA rank |
| `target_modules` 完整 | `adapter_config.json.target_modules` | 包含全部 7 个模块 |
| `adapter_model.safetensors` 存在 | `checkpoint-XXX/adapter_model.safetensors` | LoRA 权重 |
| tokenizer 未被修改 | `checkpoint-XXX/tokenizer.json` | PEFT 不改 tokenizer |
| 可加载 | 加载测试 | `PeftModel.from_pretrained()` |

---

Sources:
1. https://github.com/huggingface/peft — PEFT adapter format
2. https://github.com/artidoro/qlora — QLoRA adapter
3. https://docs.unsloth.org/ — Unsloth adapter format

Risk of Staleness:
- PEFT adapter format is stable across versions
