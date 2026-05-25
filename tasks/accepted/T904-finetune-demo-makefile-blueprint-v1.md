# finetune-demo Makefile Blueprint v1

## Task ID: T904
## Title: finetune-demo Scaffold Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T804 repo layout 和 validation checklist，产出 Makefile 模板。

---

# finetune-demo Makefile Blueprint v1

## 概述

本文档定义 finetune-demo 的 `Makefile` 模板。

## 模板全文

```makefile
# ============================================================
# finetune-demo — Makefile
# ============================================================

.PHONY: help install install-dev test test-cov lint
.PHONY: train-lora train-qlora save compare

# ---------- Config ----------
MODEL ?= Qwen/Qwen2.5-0.5B-Instruct
METHOD ?= lora
DATASET ?= ./data/example_dataset.jsonl
EPOCHS ?= 3
OUTPUT_DIR ?= ./models
ADAPTER_NAME ?= adapter
PYTHON := python3
PIP := pip

# ---------- Help ----------
help:; @grep -E '^[a-zA-Z_-]+:' Makefile | \
  grep -v '.pyc' | \
  sed 's/:;/  /' | \
  column -t -s: | \
  sed 's/^/\n/'

# ---------- Installation ----------
install:
	@echo "Installing finetune-demo..."
	$(PIP) install -e "."

install-dev:
	@echo "Installing finetune-demo with dev dependencies..."
	$(PIP) install -e ".[test,dev]"

install-unsloth:
	@echo "Installing finetune-demo with Unsloth..."
	$(PIP) install -e ".[core,unsloth]"

# ---------- Training ----------
train-lora:
	@echo "Training LoRA..."
	@mkdir -p $(OUTPUT_DIR)/lora
	finetune-demo train \
		--method lora \
		--model "$(MODEL)" \
		--dataset "$(DATASET)" \
		--epochs $(EPOCHS) \
		--output $(OUTPUT_DIR)/lora \
		--lora-r 16 \
		--lora-alpha 32 \
		--lora-target-modules q_proj,v_proj

train-qlora:
	@echo "Training QLoRA..."
	@mkdir -p $(OUTPUT_DIR)/qlora
	finetune-demo train \
		--method qlora \
		--model "$(MODEL)" \
		--dataset "$(DATASET)" \
		--epochs $(EPOCHS) \
		--output $(OUTPUT_DIR)/qlora \
		--lora-r 64 \
		--lora-alpha 16 \
		--lora-target-modules q_proj,v_proj,k_proj,o_proj \
		--load-in-4bit

# ---------- Adapter Management ----------
save:
	@echo "Saving adapter..."
	@ls $(OUTPUT_DIR)/$(METHOD) | grep checkpoint | tail -1 | while read ckpt; do \
		finetune-demo save \
			--checkpoint $(OUTPUT_DIR)/$(METHOD)/$$ckpt \
			--output $(OUTPUT_DIR)/$(METHOD)/$(ADAPTER_NAME); \
	done

save-checkpoint:
	@echo "Usage: make save CHECKPOINT=<path> OUTPUT=<path>"
	@echo "Example: make save CHECKPOINT=./models/lora/checkpoint-500 OUTPUT=./models/lora/adapter"
	@if [ -n "$(CHECKPOINT)" ]; then \
		finetune-demo save --checkpoint "$(CHECKPOINT)" --output "$(OUTPUT)"; \
	fi

list-checkpoints:
	@echo "Available checkpoints:"
	@find $(OUTPUT_DIR) -name "checkpoint-*" -type d 2>/dev/null | sort

# ---------- Compare ----------
compare:
	@echo "Comparing adapters..."
	@echo "Not implemented — use eval-module compare for benchmark results"

# ---------- Tests ----------
test:
	@echo "Running tests..."
	pytest tests/test_trainer.py tests/test_adapter.py -v

test-cov:
	@echo "Running tests with coverage..."
	pytest tests/ -v --cov=src/finetune_demo --cov-report=term-missing

# ---------- Lint ----------
lint:
	@echo "Running ruff..."
	ruff check src/

format:
	@echo "Formatting code..."
	ruff format src/
```

## 主要 Target 说明

| Target | 用途 |
|--------|------|
| `install` | 运行时安装 |
| `train-lora` | LoRA 训练 |
| `train-qlora` | QLoRA 训练 |
| `save-checkpoint` | 保存 adapter |
| `test` | 运行测试 |

## 常用工作流

```bash
# 1. 安装
make install-dev

# 2. 准备数据
cp /path/to/your/data.jsonl data/example_dataset.jsonl

# 3. 训练 LoRA
make train-lora MODEL=Qwen/Qwen2.5-0.5B-Instruct DATASET=data/example_dataset.jsonl EPOCHS=3

# 4. 查看 checkpoint
make list-checkpoints

# 5. 保存 adapter
make save-checkpoint CHECKPOINT=./models/lora/checkpoint-500 OUTPUT=./models/lora/adapter
```

---

Sources:
1. https://github.com/huggingface/peft — PEFT
2. https://github.com/huggingface/trl — TRL

Risk of Staleness:
- PEFT/TRL 命令参数可能变化

Out of Scope Kept:
- 未写模型合并（merge）make target
