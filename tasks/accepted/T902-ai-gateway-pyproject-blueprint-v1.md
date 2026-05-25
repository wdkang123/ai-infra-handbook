# ai-gateway pyproject Blueprint v1

## Task ID: T902
## Title: ai-gateway Scaffold Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T802 repo layout 和 config surface，产出 pyproject.toml 模板。

---

# ai-gateway pyproject Blueprint v1

## 概述

本文档定义 ai-gateway 的 `pyproject.toml` 模板。

## 模板全文

```toml
# pyproject.toml — ai-gateway
[project]
name = "ai-gateway"
version = "0.1.0"
description = "AI Gateway: proxy, auth, rate-limit, and observability layer"
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

    # Config and validation
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
    "pyyaml>=6.0",

    # HTTP client (for proxying)
    "httpx>=0.27.0",

    # Observability
    "prometheus-client>=0.20.0",

    # Auth
    "python-jose[cryptography]>=3.3.0",
    "passlib[bcrypt]>=1.7.4",

    # Rate limiting
    "slowapi>=0.1.9",

    # CLI
    "typer>=0.12.0",
    "rich>=13.0.0",
]

[project.optional-dependencies]
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
]

[project.scripts]
ai-gateway = "ai_gateway.main:app"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 100
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "UP", "B", "C4", "DTZ", "T10", "ISC"]
ignore = ["E501"]

[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_ignores = true
disallow_untyped_defs = false

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
addopts = "-v --cov=src/ai_gateway --cov-report=term-missing"
filterwarnings = ["ignore::DeprecationWarning"]

[tool.coverage.run]
source = ["src/ai_gateway"]
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
| `slowapi` | >=0.1.9 | 限流中间件 |
| `python-jose` | >=3.3.0 | JWT token 验证 |
| `httpx` | >=0.27.0 | 异步 HTTP 客户端 |

## 中间件选择说明

| 组件 | 方案 | 备选 |
|------|------|------|
| 限流 | `slowapi`（基于 limits） | 手写令牌桶 |
| 认证 | `python-jose` | `PyJWT` |
| 代理 | `httpx.AsyncClient` | `aiohttp` |

---

Sources:
1. https://github.com/Portkey-AI/gateway — Portkey Gateway
2. https://github.com/BerriAI/litellm — LiteLLM
3. https://github.com/laurentS/lslowapi — Slowapi
4. https://github.com/astral-sh/ruff — Ruff

Risk of Staleness:
- LiteLLM/Slowapi 版本更新可能改变 API

Out of Scope Kept:
- 未写多租户隔离
- 未写成本计算
