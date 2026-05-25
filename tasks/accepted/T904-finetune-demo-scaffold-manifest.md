# finetune-demo Scaffold Manifest

## Task ID: T904
## Title: finetune-demo Scaffold Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T804 repo layout、API contract、training config map、test plan、validation checklist，产出脚手架输入模板。

---

# finetune-demo Scaffold Manifest

## 概述

本文档定义 finetune-demo 脚手架的输入清单。

## 脚手架文件清单

| 序号 | 文件路径（蓝图） | 对应文件 | 说明 |
|------|----------------|----------|------|
| 1 | `finetune-demo/pyproject.toml` | `pyproject.toml` | 项目元数据和依赖 |
| 2 | `finetune-demo/.env.example` | `.env.example` | 环境变量模板 |
| 3 | `finetune-demo/Makefile` | `Makefile` | 构建和训练入口 |
| 4 | `finetune-demo/scripts/train.sh` | `scripts/train.sh` | 训练启动脚本 |
| 5 | `finetune-demo/tests/conftest.py` | `tests/conftest.py` | pytest fixture |
| 6 | `finetune-demo/tests/fixtures/` | `tests/fixtures/` | 测试数据 fixture |
| 7 | `finetune-demo/configs/lora_config_example.yaml` | `configs/` | 训练配置样例 |

## pyproject.toml 依赖组

基础依赖已在 `[project.dependencies]`，安装即包含核心运行时。

| 组名 | 依赖 | 用途 |
|------|------|------|
| `unsloth` | unsloth（GPU 加速） | 可选加速 |
| `test` | pytest, pytest-asyncio, pytest-cov, pytest-mock | 测试 |
| `dev` | ruff, mypy, pre-commit | 开发工具 |

## 关键 CLI 入口

```bash
# 安装（从 finetune-demo/ 目录执行）
pip install -e "."

# 安装带 Unsloth GPU 加速
pip install -e ".[unsloth]"

# 开发安装
pip install -e ".[test,dev]"

# 训练 LoRA
finetune-demo train --method lora --model Qwen/Qwen2.5-0.5B-Instruct --dataset data/train.jsonl

# 保存 adapter
finetune-demo save --checkpoint ./models/lora/checkpoint-500 --output ./models/lora/adapter

# 运行测试
pytest tests/ -v
```

## 目录结构（蓝图）

```
finetune-demo/
├── pyproject.toml
├── .env.example
├── Makefile
├── config.yaml
├── configs/
│   ├── lora_config_example.yaml
│   └── qlora_config_example.yaml
├── data/
│   └── example_dataset.jsonl
├── src/
│   └── finetune_demo/
│       ├── __init__.py
│       ├── main.py          # CLI 入口
│       ├── config.py        # 配置加载
│       ├── trainer/
│       │   ├── base.py
│       │   └── lora_trainer.py
│       ├── adapter/
│       │   ├── saver.py
│       │   └── loader.py
│       └── export/
│           └── adapter_exporter.py
├── tests/
│   ├── conftest.py
│   ├── fixtures/
│   │   └── sample_train.jsonl
│   └── test_trainer.py
└── scripts/
    └── train.sh
```

## 与 inference-service 的集成点

- 训练后的 adapter 通过 PEFT 加载到 base model
- adapter 路径配置在 inference-service 的 `INFERENCE_ADAPTER_DIR`
- 训练使用 HuggingFace base model，与 inference-service 部署的 model 保持一致

## 关键实现里程碑

| 里程碑 | 产出 | 验证 |
|--------|------|------|
| M1: CLI 可执行 | `finetune-demo train --help` | T804 validation checklist |
| M2: LoRA 可训练 | adapter 产物生成 | T804 validation checklist |
| M3: Adapter 可保存 | `adapter_config.json` + `.safetensors` | T804 validation checklist |
| M4: Adapter 可加载 | 加载后模型可推理 | T804 validation checklist |

---

Sources:
1. https://github.com/huggingface/peft — PEFT
2. https://github.com/huggingface/trl — TRL
3. https://github.com/unslothai/unsloth — Unsloth

Risk of Staleness:
- PEFT/TRL 版本更新可能改变 CLI 参数

Out of Scope Kept:
- 未写 DPO 训练
- 未写模型合并（merge）
