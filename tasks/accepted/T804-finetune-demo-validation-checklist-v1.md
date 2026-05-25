# finetune-demo Validation Checklist v1

## Task ID: T804
## Task Title: finetune-demo Execution Prep Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T304 MVP 设计，准备 finetune-demo 实施前包。

---

# finetune-demo Validation Checklist v1

## 概述

本文档定义 finetune-demo 的验收清单，供 Codex 执行后快速验证。

---

## 验收清单总览

| 类别 | 检查项数 | 必须项 |
|------|---------|-------|
| LoRA 训练 | 5 | 5 |
| QLoRA 训练 | 4 | 4 |
| Adapter 保存 | 3 | 3 |
| Adapter 加载 | 2 | 2 |
| 产物验证 | 3 | 3 |
| **合计** | **17** | **17** |

---

## LoRA 训练验收

- [ ] `finetune-demo train --method lora` 可执行
- [ ] 训练日志显示 Loss 下降
- [ ] adapter 产物目录创建
- [ ] `adapter_config.json` 存在
- [ ] `adapter_model.safetensors` 存在

---

## QLoRA 训练验收

- [ ] `finetune-demo train --method qlora` 可执行
- [ ] 4-bit 量化生效（显存占用降低）
- [ ] QLoRA adapter 产物创建
- [ ] 与 LoRA 产物结构一致

---

## Adapter 保存验收

- [ ] `save_adapter()` 方法存在
- [ ] `adapter_config.json` 格式正确
- [ ] `adapter_model.safetensors` 权重非空

---

## Adapter 加载验收

- [ ] `load_adapter()` 方法存在
- [ ] 加载后模型可推理

---

## 产物验证验收

- [ ] `adapter_config.json` 包含 `r`, `lora_alpha`, `target_modules`
- [ ] 训练 metrics 文件存在
- [ ] Checkpoint 目录结构正确

---

## 快速验证命令

### LoRA 训练验证

```bash
# 1. 安装依赖
pip install peft transformers torch

# 2. 准备小数据集
cat > /tmp/test_data.jsonl << 'EOF'
{"instruction": "Hello", "input": "", "output": "Hi there!"}
{"instruction": "What is 2+2?", "input": "", "output": "4"}
EOF

# 3. 运行 LoRA 训练
finetune-demo train \
    --model Qwen/Qwen2.5-0.5B-Instruct \
    --method lora \
    --dataset /tmp/test_data.jsonl \
    --epochs 1 \
    --output /tmp/lora_output

# 4. 检查产物
ls -la /tmp/lora_output/
cat /tmp/lora_output/adapter_config.json
```

### QLoRA 训练验证

```bash
# 1. 安装依赖
pip install peft transformers torch bitsandbytes

# 2. 运行 QLoRA 训练
finetune-demo train \
    --model Qwen/Qwen2.5-0.5B-Instruct \
    --method qlora \
    --dataset /tmp/test_data.jsonl \
    --epochs 1 \
    --output /tmp/qlora_output

# 3. 检查产物
ls -la /tmp/qlora_output/
```

### Adapter 加载验证

```bash
# 使用 PEFT 加载 adapter
python << 'EOF'
from peft import PeftModel, AutoModelForCausalLM
from transformers import AutoTokenizer

model_name = "Qwen/Qwen2.5-0.5B-Instruct"
adapter_path = "/tmp/lora_output"

tokenizer = AutoTokenizer.from_pretrained(model_name)
base_model = AutoModelForCausalLM.from_pretrained(model_name)
model = PeftModel.from_pretrained(base_model, adapter_path)

print("Base model loaded")
print(f"LoRA modules: {list(model.peft_config.keys())}")
print("Adapter loaded successfully!")
EOF
```

---

Sources:
1. https://github.com/huggingface/peft — PEFT
2. https://github.com/huggingface/trl — TRL
3. https://github.com/unslothai/unsloth — Unsloth

Risk of Staleness:
- 验证命令可能因版本更新变化

Out of Scope Kept:
- 未写自动化验收脚本
