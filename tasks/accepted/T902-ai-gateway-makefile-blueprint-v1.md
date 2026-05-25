# ai-gateway Makefile Blueprint v1

## Task ID: T902
## Title: ai-gateway Scaffold Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T802 repo layout 和 validation checklist，产出 Makefile 模板。

---

# ai-gateway Makefile Blueprint v1

## 概述

本文档定义 ai-gateway 的 `Makefile` 模板。

## 模板全文

```makefile
# ============================================================
# ai-gateway — Makefile
# ============================================================

.PHONY: help install install-dev run test test-cov lint
.PHONY: serve serve-dev health curl-chat curl-metrics
.PHONY: clean

# ---------- Config ----------
PORT ?= 8080
METRICS_PORT ?= 9091
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
	@echo "Installing ai-gateway..."
	$(PIP) install -e "."

install-dev:
	@echo "Installing ai-gateway with dev dependencies..."
	$(PIP) install -e ".[test,dev]"

# ---------- Run ----------
serve:
	@echo "Starting ai-gateway on port $(PORT)..."
	ai-gateway serve --port $(PORT) --metrics-port $(METRICS_PORT)

serve-dev:
	@echo "Starting ai-gateway in dev mode..."
	$(PYTHON) -m uvicorn \
		ai_gateway.server:app \
		--host 0.0.0.0 \
		--port $(PORT) \
		--reload \
		--log-level debug

# ---------- Health & Smoke ----------
health:
	@echo "Checking health..."
	@curl -s http://localhost:$(PORT)/health | $(PYTHON) -m json.tool || \
		(echo "Gateway not ready on port $(PORT)" && exit 1)

curl-chat:
	@echo "Testing /v1/chat/completions via gateway..."
	@curl -s -X POST http://localhost:$(PORT)/v1/chat/completions \
		-H "Content-Type: application/json" \
		-H "Authorization: Bearer dev-gateway-key-1" \
		-d '{"model":"vllm-local","messages":[{"role":"user","content":"Hello"}]}' | \
		$(PYTHON) -m json.tool

curl-chat-no-auth:
	@echo "Testing without auth (expected 401)..."
	@curl -s -X POST http://localhost:$(PORT)/v1/chat/completions \
		-H "Content-Type: application/json" \
		-d '{"model":"vllm-local","messages":[{"role":"user","content":"Hello"}]}'

curl-metrics:
	@echo "Fetching /metrics..."
	@curl -s http://localhost:$(PORT)/metrics | head -20

# ---------- Tests ----------
test:
	@echo "Running unit tests..."
	pytest tests/test_router.py tests/test_middleware.py -v

test-integration:
	@echo "Running integration tests..."
	pytest tests/test_integration.py -v

test-cov:
	@echo "Running tests with coverage..."
	pytest tests/ -v --cov=src/ai_gateway --cov-report=term-missing

# ---------- Lint & Type ----------
lint:
	@echo "Running ruff..."
	ruff check src/

format:
	@echo "Formatting code..."
	ruff format src/

# ---------- Clean ----------
clean:
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
```

## 主要 Target 说明

| Target | 用途 |
|--------|------|
| `install` | 运行时安装 |
| `serve` | 生产启动 |
| `serve-dev` | 开发热重载 |
| `health` | 健康检查 |
| `curl-chat` | 基本代理测试（含 auth） |
| `curl-chat-no-auth` | 无 auth 测试（预期 401） |
| `test` | 单元测试 |
| `test-cov` | 带覆盖率测试 |

## 典型开发工作流

```bash
# 1. 启动 inference-service（如未启动）
# make serve -C ../inference-service &

# 2. 安装 gateway
make install-dev

# 3. 启动 gateway
make serve-dev PORT=8080 &

# 4. 验证
sleep 5 && make health

# 5. 测试代理
make curl-chat
```

---

Sources:
1. https://github.com/Portkey-AI/gateway — Portkey Gateway

Risk of Staleness:
- Gateway middleware 行为可能随版本变化

Out of Scope Kept:
- 未写 docker-compose（多服务编排）
