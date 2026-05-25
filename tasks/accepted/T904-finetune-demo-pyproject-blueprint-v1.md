# finetune-demo pyproject Blueprint v1

## Task ID: T904
## Title: finetune-demo Scaffold Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T804 repo layout 和 training config map，产出 pyproject.toml 模板。

---

# finetune-demo pyproject Blueprint v1

## 概述

本文档定义 finetune-demo 的 `pyproject.toml` 模板。

## 模板全文

```toml
# pyproject.toml — finetune-demo
[project]
name = "finetune-demo"
version = "0.1.0"
description = "Fine-tuning demo with LoRA/QLoRA using PEFT and TRL"
requires-python = ">=3.10"
license = { text = "Apache-2.0" }
authors = [
    { name = "MiniMax", email = "infra@minimax.io" }
]
readme = "README.md"

dependencies = [
    # Transformers
    "transformers>=4.40.0",
    "tokenizers>=0.15.0",
    "datasets>=2.14.0",
    "accelerate>=0.28.0",

    # PEFT (LoRA/QLoRA)
    "peft>=0.10.0",

    # TRL (SFTTrainer, DPOTrainer)
    "trl>=0.8.0",

    # BitsAndBytes (QLoRA 4-bit)
    "bitsandbytes>=0.43.0",

    # PyTorch (GPU training)
    "torch>=2.0.0",
    "torchvision>=0.15.0",  # optional

    # Config
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
    "pyyaml>=6.0",

    # CLI
    "typer>=0.12.0",
    "rich>=13.0.0",

    # Logging
    "tensorboard>=2.15.0",
    "wandb>=0.16.0",  # optional
]

[project.optional-dependencies]
# Unsloth GPU acceleration
unsloth = [
    "unsloth @ git+https://github.com/unslothai/unsloth.git",
]

# Test dependencies
test = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
    "pytest-cov>=4.1.0",
    "pytest-mock>=3.12.0",
]

# Development dependencies
dev = [
    "ruff>=0.4.0",
    "mypy>=1.9.0",
    "pre-commit>=3.6.0",
    "bitsandbytes>=0.43.0",  # for type stubs
]

[project.scripts]
finetune-demo = "finetune_demo.main:app"

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
[[tool.mypy.overrides]]
module = "bitsandbytes.*"
ignore_missing_imports = true
[[tool.mypy.overrides]]
module = "unsloth.*"
ignore_missing_imports = true

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
addopts = "-v --cov=src/finetune_demo --cov-report=term-missing"

[tool.coverage.run]
source = ["src/finetune_demo"]
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
| `transformers` | >=4.40.0 | Qwen2.5 系列支持 |
| `peft` | >=0.10.0 | LoRA/QLoRA 支持 |
| `trl` | >=0.8.0 | SFTTrainer 支持 |
| `bitsandbytes` | >=0.43.0 | 4-bit 量化支持 |
| `accelerate` | >=0.28.0 | 分布式训练支持 |
| `torch` | >=2.0.0 | CUDA 12+ 支持 |

## Unsloth 加速说明

基础依赖已在 `[project.dependencies]`。Unsloth 是单独的可选依赖：

```bash
# 安装（从 finetune-demo/ 目录执行）
pip install -e "."

# 安装带 Unsloth GPU 加速（可获得 2x 训练加速）
pip install -e ".[unsloth]"
```

---

Sources:
1. https://github.com/huggingface/peft — PEFT
2. https://github.com/huggingface/trl — TRL
3. https://github.com/unslothai/unsloth — Unsloth
4. https://github.com/astral-sh/ruff — Ruff

Risk of Staleness:
- PEFT/TRL 版本更新可能改变 API

Out of Scope Kept:
- 未写多节点分布式训练
- 未写 DeepSpeed 配置
