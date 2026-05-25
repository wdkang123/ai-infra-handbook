# inference-service Makefile Blueprint v1

## Task ID: T901
## Title: inference-service Scaffold Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T801 repo layout 和 T801 validation checklist，产出 Makefile 模板。

---

# inference-service Makefile Blueprint v1

## 概述

本文档定义 inference-service 的 `Makefile` 模板，提供标准化开发入口。

## 模板全文

```makefile
# ============================================================
# inference-service — Makefile
# ============================================================

.PHONY: help install install-dev run test test-cov lint
.PHONY: serve serve-dev health curl-chat curl-stream curl-metrics
.PHONY: clean docker-build docker-run docker-stop

# ---------- Config ----------
MODEL ?= Qwen/Qwen2.5-0.5B-Instruct
PORT ?= 8000
METRICS_PORT ?= 9090
ENGINE ?= vllm
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
	@echo "Installing inference-service..."
	$(PIP) install -e "."

install-dev:
	@echo "Installing inference-service with dev dependencies..."
	$(PIP) install -e ".[test,dev]"

# ---------- Run ----------
serve:
	@echo "Starting inference-service (engine=$(ENGINE), model=$(MODEL))..."
	inference-service serve \
		--engine $(ENGINE) \
		--model "$(MODEL)" \
		--port $(PORT) \
		--metrics-port $(METRICS_PORT)

serve-dev:
	@echo "Starting inference-service in dev mode..."
	$(PYTHON) -m uvicorn \
		inference_service.server:app \
		--host 0.0.0.0 \
		--port $(PORT) \
		--reload \
		--log-level debug

# ---------- Health & Smoke ----------
health:
	@echo "Checking health..."
	@curl -s http://localhost:$(PORT)/health | $(PYTHON) -m json.tool || \
		(echo "Service not ready on port $(PORT)" && exit 1)

curl-chat:
	@echo "Testing /v1/chat/completions..."
	@curl -s -X POST http://localhost:$(PORT)/v1/chat/completions \
		-H "Content-Type: application/json" \
		-d '{"model":"$(MODEL)","messages":[{"role":"user","content":"What is 2+2?"}]}' | \
		$(PYTHON) -m json.tool

curl-stream:
	@echo "Testing streaming /v1/chat/completions..."
	@curl -s -X POST http://localhost:$(PORT)/v1/chat/completions \
		-H "Content-Type: application/json" \
		-d '{"model":"$(MODEL)","messages":[{"role":"user","content":"Count to 3"}],"stream":true}'

curl-metrics:
	@echo "Fetching /metrics..."
	@curl -s http://localhost:$(PORT)/metrics | head -20

# ---------- Tests ----------
test:
	@echo "Running unit tests..."
	pytest tests/test_engine.py tests/test_config.py -v

test-api:
	@echo "Running API tests..."
	pytest tests/test_api.py -v

test-integration:
	@echo "Running integration tests..."
	pytest tests/test_integration.py -v

test-cov:
	@echo "Running tests with coverage..."
	pytest tests/ -v --cov=src/inference_service --cov-report=term-missing

# ---------- Lint & Type ----------
lint:
	@echo "Running ruff..."
	ruff check src/

typecheck:
	@echo "Running mypy..."
	mypy src/

format:
	@echo "Formatting code..."
	ruff format src/ tests/

# ---------- Clean ----------
clean:
	@echo "Cleaning..."
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

# ---------- Docker ----------
docker-build:
	@echo "Building Docker image..."
	docker build -t inference-service:latest .

docker-run:
	@echo "Running Docker container..."
	docker run -d \
		--gpus all \
		-p $(PORT):$(PORT) \
		-p $(METRICS_PORT):$(METRICS_PORT) \
		--shm-size=10g \
		-e INFERENCE_MODEL_PATH="$(MODEL)" \
		-e INFERENCE_ENGINE_TYPE=$(ENGINE) \
		inference-service:latest

docker-stop:
	@echo "Stopping container..."
	docker stop $$(docker ps -q --filter ancestor=inference-service:latest) 2>/dev/null || true
```

## 主要 Target 说明

| Target | 用途 | 关键命令 |
|--------|------|---------|
| `install` | 运行时安装 | `pip install -e .` |
| `install-dev` | 开发安装 | `pip install -e ".[test,dev]"` |
| `serve` | 生产启动 | `inference-service serve` |
| `serve-dev` | 开发热重载 | `uvicorn --reload` |
| `health` | 健康检查 | `curl /health` |
| `curl-chat` | 基本推理测试 | `curl /v1/chat/completions` |
| `curl-stream` | 流式推理测试 | `curl ... stream=true` |
| `curl-metrics` | metrics 检查 | `curl /metrics` |
| `test` | 单元测试 | `pytest tests/test_engine.py` |
| `test-cov` | 带覆盖率测试 | `pytest --cov` |
| `lint` | 代码检查 | `ruff check` |
| `format` | 代码格式化 | `ruff format` |
| `docker-run` | Docker 启动 | `docker run -d --gpus all` |

## 常用开发工作流

```bash
# 1. 首次安装
make install-dev

# 2. 启动服务（后台）
make serve MODEL=Qwen/Qwen2.5-0.5B-Instruct PORT=8000 &

# 3. 等待启动后验证
sleep 30 && make health

# 4. 运行测试
make test

# 5. 清理
make clean
```

---

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://github.com/astral-sh/ruff — Ruff

Risk of Staleness:
- vLLM docker 镜像标签可能变化

Out of Scope Kept:
- 未写 docker-compose（多服务编排）
- 未写 K8s 部署
