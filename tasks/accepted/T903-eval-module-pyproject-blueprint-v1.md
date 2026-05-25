# eval-module pyproject Blueprint v1

## Task ID: T903
## Title: eval-module Scaffold Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T803 repo layout 和 config surface，产出 pyproject.toml 模板。

---

# eval-module pyproject Blueprint v1

## 概述

本文档定义 eval-module 的 `pyproject.toml` 模板。

## 模板全文

```toml
# pyproject.toml — eval-module
[project]
name = "eval-module"
version = "0.1.0"
description = "Benchmark evaluation module using lm-eval-harness"
requires-python = ">=3.10"
license = { text = "Apache-2.0" }
authors = [
    { name = "MiniMax", email = "infra@minimax.io" }
]
readme = "README.md"

dependencies = [
    # FastAPI (optional HTTP API)
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.30.0",

    # Config
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
    "pyyaml>=6.0",

    # HTTP client (for backend calls)
    "httpx>=0.27.0",

    # Evaluation
    "lm-eval>=0.4.0",

    # Result persistence
    "jsonpickle>=3.0.0",

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
eval-module = "eval_module.main:app"

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
addopts = "-v --cov=src/eval_module --cov-report=term-missing"

[tool.coverage.run]
source = ["src/eval_module"]
branch = true

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "raise NotImplementedError",
]
```

## lm-eval 安装说明

lm-eval 安装较慢，建议单独安装：

```bash
# 推荐：带 vLLM backend
pip install "lm-eval>=0.4.0"

# 或从源码
pip install git+https://github.com/EleutherAI/lm-evaluation-harness.git
```

## 依赖版本说明

| 依赖 | 最低版本 | 理由 |
|------|---------|------|
| `lm-eval` | >=0.4.0 | OpenAI compatible API 支持 |
| `typer` | >=0.12.0 | CLI 框架 |
| `jsonpickle` | >=3.0.0 | 结果序列化 |

---

Sources:
1. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval
2. https://github.com/astral-sh/ruff — Ruff

Risk of Staleness:
- lm-eval 版本更新可能改变 API 和 CLI 参数

Out of Scope Kept:
- 未写 HELM runner 支持
