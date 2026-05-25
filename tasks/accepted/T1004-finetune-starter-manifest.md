# finetune-demo Starter File Manifest

## Task ID: T1004
## Title: finetune-demo Starter File Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T904 scaffold blueprints（T904 pyproject / run-script / test-fixture / sample-config），产出 finetune-demo 源码蓝图文件。

---

# finetune-demo Starter File Manifest

## 概述

本文档索引 finetune-demo 的所有 starter file 蓝图，供 Codex 实施时参照。

## 蓝图文件清单

| 序号 | 文件路径（蓝图） | 对应真实文件 | 说明 |
|------|----------------|-------------|------|
| 1 | `T1004-finetune-main-py-blueprint-v1.md` | `src/finetune_demo/main.py` | Typer CLI 入口 |
| 2 | `T1004-finetune-train-py-blueprint-v1.md` | `src/finetune_demo/trainer/lora_trainer.py` | LoRA/QLoRA 训练器 |
| 3 | `T1004-finetune-config-schema-blueprint-v1.md` | `src/finetune_demo/config.py` | Pydantic 配置 schema |
| 4 | `T1004-finetune-conftest-py-blueprint-v1.md` | `tests/conftest.py` | pytest fixtures |
| 5 | `T1004-finetune-test-train-py-blueprint-v1.md` | `tests/test_trainer.py` | 训练器单元测试 |
| 6 | `T1004-finetune-train-sh-blueprint-v2.md` | `scripts/train.sh` | 训练启动脚本（v2） |
| 7 | (沿用 T904 scaffold) | `configs/lora_config_example.yaml` | LoRA 配置样例（沿用 T904 sample-config） |

## 源码目录结构（蓝图）

```
finetune-demo/
├── src/
│   └── finetune_demo/
│       ├── __init__.py
│       ├── main.py              # Typer CLI
│       ├── config.py            # Pydantic config schema
│       ├── trainer/
│       │   ├── __init__.py
│       │   ├── base.py          # Base trainer 抽象
│       │   └── lora_trainer.py  # LoRA/QLoRA trainer
│       ├── adapter/
│       │   ├── __init__.py
│       │   ├── saver.py         # Adapter 保存
│       │   └── loader.py        # Adapter 加载
│       └── export/
│           └── adapter_exporter.py
├── tests/
│   ├── conftest.py
│   ├── fixtures/
│   │   └── sample_train.jsonl
│   └── test_trainer.py
├── scripts/
│   └── train.sh
├── configs/
│   ├── lora_config_example.yaml
│   └── qlora_config_example.yaml
├── data/
│   └── example_dataset.jsonl
├── pyproject.toml
└── .env.example
```

## MVP CLI 命令

| 命令 | 说明 |
|------|------|
| `finetune-demo train --method lora --model Qwen/Qwen2.5-0.5B-Instruct --dataset ./data/train.jsonl` | LoRA 训练 |
| `finetune-demo save --checkpoint ./models/lora/checkpoint-500 --output ./models/lora/adapter` | 保存 adapter |

## 与 inference-service 集成

- 训练使用 HuggingFace base model，与 inference-service 部署的 model 保持一致
- adapter 可通过 PEFT 加载到 inference-service 的 vLLM 进行推理

---

Sources:
1. https://github.com/huggingface/peft — PEFT
2. https://github.com/huggingface/trl — TRL

Risk of Staleness:
- PEFT/TRL API 在 0.10+ / 0.8+ 相对稳定
