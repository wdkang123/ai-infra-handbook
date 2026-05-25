# Root Makefile Blueprint v2

## Task ID: T1005
## Title: Root / Dev Workflow Starter File Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T905 scaffold（root-makefile blueprint v1），产出 v2 版本根目录 Makefile。

---

# Root Makefile Blueprint v2

## 概述

本文档定义仓库根目录的 `Makefile` v2 蓝图，提供跨项目统一开发入口。

## `Makefile` 模板

```makefile
# ============================================================
# ai-infra — Root Makefile
# 跨项目统一开发入口
# ============================================================

.PHONY: help
.PHONY: infra-install infra-test infra-serve infra-smoke infra-clean
.PHONY: \
	inference-install inference-serve inference-health inference-test \
	gateway-install gateway-serve gateway-health gateway-test \
	eval-install eval-run-mmlu eval-run-gsm8k \
	finetune-install finetune-train \
	all-serve all-stop

# ---------- Config ----------
# 共享配置
MODEL ?= Qwen/Qwen2.5-0.5B-Instruct
INFERENCE_PORT ?= 8000
GATEWAY_PORT ?= 8080
INFERENCE_BASE_URL ?= http://localhost:$(INFERENCE_PORT)/v1

# Color
RED  := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[1;33m
NC   := \033[0m

# ---------- Help ----------
help:; @grep -E '^[a-zA-Z_-]+:' Makefile | \
  grep -v '.pyc' | \
  sed 's/:;/  /' | \
  column -t -s: | \
  sed 's/^/\n/'

# ============================================================
# Cross-project infra targets
# ============================================================

infra-install: inference-install gateway-install eval-install finetune-install
	@echo -e "$(GREEN)[OK]${NC} All modules installed"

infra-test:
	@echo "Running inference-service tests..."
	@$(MAKE) -C inference-service test || true
	@echo "Running ai-gateway tests..."
	@$(MAKE) -C ai-gateway test || true
	@echo "Running eval-module tests..."
	@$(MAKE) -C eval-module test || true
	@echo "Running finetune-demo tests..."
	@$(MAKE) -C finetune-demo test || true

infra-serve: inference-serve gateway-serve
	@echo -e "$(GREEN)[OK]${NC} All services started"

infra-smoke:
	@echo "Running integration smoke tests..."
	@MODEL=$(MODEL) bash scripts/integration_smoke_test.sh

infra-clean:
	@echo "Cleaning all modules..."
	@$(MAKE) -C inference-service clean || true
	@$(MAKE) -C ai-gateway clean || true
	@$(MAKE) -C eval-module clean || true
	@$(MAKE) -C finetune-demo clean || true
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true

# ============================================================
# inference-service
# ============================================================

inference-install:
	@echo "Installing inference-service..."
	@$(MAKE) install -C inference-service

inference-serve:
	@echo "Starting inference-service on port $(INFERENCE_PORT)..."
	@$(MAKE) serve MODEL=$(MODEL) PORT=$(INFERENCE_PORT) -C inference-service &

inference-health:
	@echo "Checking inference-service health..."
	@curl -s http://localhost:$(INFERENCE_PORT)/health | python -m json.tool || \
		(echo -e "$(RED)[FAIL]${NC} inference-service not healthy" && exit 1)

inference-test:
	@$(MAKE) test -C inference-service

# ============================================================
# ai-gateway
# ============================================================

gateway-install:
	@echo "Installing ai-gateway..."
	@$(MAKE) install -C ai-gateway

gateway-serve:
	@echo "Starting ai-gateway on port $(GATEWAY_PORT)..."
	@$(MAKE) serve PORT=$(GATEWAY_PORT) -C ai-gateway &

gateway-health:
	@echo "Checking ai-gateway health..."
	@curl -s http://localhost:$(GATEWAY_PORT)/health | python -m json.tool || \
		(echo -e "$(RED)[FAIL]${NC} ai-gateway not healthy" && exit 1)

gateway-test:
	@$(MAKE) test -C ai-gateway

# ============================================================
# eval-module
# ============================================================

eval-install:
	@echo "Installing eval-module..."
	@$(MAKE) install -C eval-module

eval-run-mmlu:
	@echo "Running MMLU benchmark..."
	@$(MAKE) run-mmlu MODEL=$(MODEL) BACKEND_URL=$(INFERENCE_BASE_URL) -C eval-module

eval-run-gsm8k:
	@echo "Running GSM8K benchmark..."
	@$(MAKE) run-gsm8k MODEL=$(MODEL) BACKEND_URL=$(INFERENCE_BASE_URL) -C eval-module

# ============================================================
# finetune-demo
# ============================================================

finetune-install:
	@echo "Installing finetune-demo..."
	@$(MAKE) install -C finetune-demo

finetune-train:
	@echo "Training LoRA (see finetune-demo/Makefile for targets)..."
	@$(MAKE) help -C finetune-demo

# ============================================================
# All services
# ============================================================

all-serve: inference-serve
	@sleep 30 && inference-health && gateway-serve
	@echo -e "$(GREEN)[OK]${NC} All services running"
	@echo "  inference-service: http://localhost:$(INFERENCE_PORT)"
	@echo "  ai-gateway:        http://localhost:$(GATEWAY_PORT)"

all-stop:
	@echo "Stopping all services..."
	@pkill -f "inference-service" 2>/dev/null || true
	@pkill -f "ai-gateway" 2>/dev/null || true
	@echo "Done"
```

## 冒烟测试顺序

```bash
# 1. 启动所有服务
make all-serve

# 2. 等待就绪
sleep 35

# 3. 运行冒烟测试
make infra-smoke

# 4. 停止所有服务
make all-stop
```

---

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval
