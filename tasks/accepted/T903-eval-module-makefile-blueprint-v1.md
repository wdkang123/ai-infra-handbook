# eval-module Makefile Blueprint v1

## Task ID: T903
## Title: eval-module Scaffold Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T803 repo layout 和 validation checklist，产出 Makefile 模板。

---

# eval-module Makefile Blueprint v1

## 概述

本文档定义 eval-module 的 `Makefile` 模板。

## 模板全文

```makefile
# ============================================================
# eval-module — Makefile
# ============================================================

.PHONY: help install install-dev test test-cov lint
.PHONY: run-mmlu run-gsm8k compare

# ---------- Config ----------
MODEL ?= Qwen/Qwen2.5-0.5B-Instruct
BACKEND_URL ?= http://localhost:8000/v1
NUM_FEWSHOT ?= 5
LIMIT ?=  # empty = full benchmark
RESULTS_DIR ?= ./results
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
	@echo "Installing eval-module..."
	$(PIP) install -e "."

install-dev:
	@echo "Installing eval-module with dev dependencies..."
	$(PIP) install -e ".[test,dev]"

# ---------- Benchmarks ----------
run-mmlu:
	@echo "Running MMLU benchmark..."
	@mkdir -p $(RESULTS_DIR)
	eval-module run \
		--task mmlu \
		--model "$(MODEL)" \
		--backend-url "$(BACKEND_URL)" \
		--num-fewshot $(NUM_FEWSHOT) \
		$(if $(LIMIT),--limit $(LIMIT),) \
		--output $(RESULTS_DIR)/mmlu_$(shell date +%Y%m%d_%H%M%S).json

run-gsm8k:
	@echo "Running GSM8K benchmark..."
	@mkdir -p $(RESULTS_DIR)
	eval-module run \
		--task gsm8k \
		--model "$(MODEL)" \
		--backend-url "$(BACKEND_URL)" \
		--num-fewshot $(NUM_FEWSHOT) \
		$(if $(LIMIT),--limit $(LIMIT),) \
		--output $(RESULTS_DIR)/gsm8k_$(shell date +%Y%m%d_%H%M%S).json

run-all:
	@echo "Running MMLU + GSM8K..."
	$(MAKE) run-mmlu
	$(MAKE) run-gsm8k

# ---------- Compare ----------
compare:
	@echo "Comparing results..."
	@ls $(RESULTS_DIR)/*.json | head -2 | xargs \
		eval-module compare --baseline $$1 --candidate $$2 || \
		echo "Usage: make compare BASELINE=<file> CANDIDATE=<file>"

compare-baseline:
	$(eval BASELINE := $(or $(BASELINE),$(firstword $(wildcard $(RESULTS_DIR)/mmlu_*.json))))
	$(eval CANDIDATE := $(or $(CANDIDATE),$(lastword $(wildcard $(RESULTS_DIR)/mmlu_*.json))))
	@echo "Baseline: $(BASELINE)"
	@echo "Candidate: $(CANDIDATE)"
	eval-module compare \
		--baseline "$(BASELINE)" \
		--candidate "$(CANDIDATE)"

# ---------- Tests ----------
test:
	@echo "Running tests..."
	pytest tests/test_runner.py tests/test_evaluator.py -v

test-cov:
	@echo "Running tests with coverage..."
	pytest tests/ -v --cov=src/eval_module --cov-report=term-missing

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
| `run-mmlu` | 运行 MMLU benchmark |
| `run-gsm8k` | 运行 GSM8K benchmark |
| `compare` | 对比两次评测结果 |
| `test` | 运行单元测试 |
| `test-cov` | 带覆盖率测试 |

## 常用命令

```bash
# 1. 安装
make install-dev

# 2. 快速验证（少量样本）
make run-mmlu LIMIT=10 NUM_FEWSHOT=5

# 3. 完整 MMLU
make run-mmlu

# 4. 完整 GSM8K
make run-gsm8k

# 5. 对比结果
make compare BASELINE=results/mmlu_baseline.json CANDIDATE=results/mmlu_finetuned.json
```

---

Sources:
1. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval

Risk of Staleness:
- lm-eval CLI 参数可能变化

Out of Scope Kept:
- 未写自动化评测报告生成
