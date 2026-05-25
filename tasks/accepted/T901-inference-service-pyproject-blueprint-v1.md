# inference-service pyproject Blueprint v1

## Task ID: T901
## Title: inference-service Scaffold Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T801 repo layout 和 config surface，产出 pyproject.toml 模板。

---

# inference-service pyproject Blueprint v1

## 概述

本文档定义 inference-service 的 `pyproject.toml` 模板，接近可复制状态。

## 模板全文

```toml
# pyproject.toml — inference-service
[project]
name = "inference-service"
version = "0.1.0"
description = "OpenAI-compatible inference service powered by vLLM"
requires-python = ">=3.10"
license = { text = "Apache-2.0" }
authors = [
    { name = "MiniMax", email = "infra@minimax.io" }
]
readme = "README.md"

dependencies = [
    # FastAPI and server
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.30.0",

    # vLLM engine
    "vllm>=0.6.0",

    # Observability
    "prometheus-client>=0.20.0",

    # Config and validation
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
    "pyyaml>=6.0",

    # HTTP client
    "httpx>=0.27.0",

    # CLI
    "typer>=0.12.0",
    "rich>=13.0.0",
]

[project.optional-dependencies]
# SGLang engine support
sglang = [
    "sglang>=0.1.0",
]

# Triton IS engine support
triton = [
    "tritonclient[all]>=3.0.0",
]

# Test dependencies
test = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
    "pytest-cov>=4.1.0",
    "pytest-mock>=3.12.0",
    "httpx>=0.27.0",
]

# Development dependencies
dev = [
    "ruff>=0.4.0",
    "mypy>=1.9.0",
    "pre-commit>=3.6.0",
    "typer[all]>=0.12.0",  # for CLI testing
    "shellingham>=0.4.0",   # for static analysis
]

[project.scripts]
inference-service = "inference_service.main:app"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 100
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "UP", "B", "C4", "DTZ", "T10", "ISC"]
ignore = ["E501"]  # line too long handled by formatter

[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_ignores = true
disallow_untyped_defs = false

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
addopts = "-v --cov=src/inference_service --cov-report=term-missing"
filterwarnings = [
    "ignore::DeprecationWarning",
]

[tool.coverage.run]
source = ["src/inference_service"]
branch = true

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "raise NotImplementedError",
]
```

## 依赖版本说明

| 依赖 | 最低版本 | 理由 |
|------|---------|------|
| `fastapi` | >=0.115.0 | Pydantic v2 支持 |
| `uvicorn` | >=0.30.0 | HTTP/2 和 asyncio 改进 |
| `vllm` | >=0.6.0 | OpenAI 兼容 API 成熟 |
| `pydantic` | >=2.0.0 | Pydantic v2，性能更好 |
| `typer` | >=0.12.0 | CLI 框架 |
| `ruff` | >=0.4.0 | 快速 linting |

## 可选依赖组使用场景

基础依赖已在 `[project.dependencies]`，直接安装即包含全部核心依赖，无需 extra。

| 场景 | 安装命令（从各模块目录执行） |
|------|---------|
| 基础安装 | `pip install -e "."` |
| + SGLang | `pip install -e ".[sglang]"` |
| + Triton | `pip install -e ".[triton]"` |
| 开发 | `pip install -e ".[test,dev]"` |

---

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://fastapi.tiangolo.com/ — FastAPI
3. https://pydantic.dev/ — Pydantic v2
4. https://github.com/astral-sh/ruff — Ruff

Risk of Staleness:
- 依赖版本可能随 vLLM/FastAPI 更新需要调整

Out of Scope Kept:
- 未写多模型并发支持
- 未写 GPU 资源调度
