# finetune-demo File Order v1

## Task ID: T1204
## Title: finetune-demo Implementation Map Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# finetune-demo File Implementation Order

本文档定义 `finetune-demo/` 目录的编码实现顺序，基于 accepted `T304 / T703 / T1104` blueprints。

## 文件实现顺序

### Phase 0: 骨架

| Order | 文件路径 | 目的 | 依赖 |
|---|---|---|---|
| 0.1 | `pyproject.toml` | 项目元数据 + 依赖声明 | 无 |
| 0.2 | `src/finetune_demo/__init__.py` | 模块命名空间 | 无 |
| 0.3 | `src/finetune_demo/__version__.py` | `__version__` | 无 |
| 0.4 | `configs/` 目录结构 | task presets 目录 | 无 |
| 0.5 | `data/samples/` 目录结构 | JSONL 样本目录 | 无 |
| 0.6 | `outputs/` 目录结构 | 训练输出目录 | 无 |

### Phase 1: 配置加载

| Order | 文件路径 | 目的 | 依赖 |
|---|---|---|---|
| 1.1 | `src/finetune_demo/config.py` | Pydantic 配置 schema | Phase 0 |
| 1.2 | `configs/lora/lora_config_qwen_05b.yaml` | LoRA FP16 配置 | Phase 0 |
| 1.3 | `configs/qlora/qlora_config_qwen_05b.yaml` | QLoRA NF4 配置 | Phase 0 |

**实现要点：** `config.py` 加载 YAML，解析 `model_name_or_path`、`lora_r`、`lora_alpha`、`target_modules` 等字段。对齐 T1104 `lora_config_qwen_05b.yaml` 和 `qlora_config_qwen_05b.yaml`。

### Phase 2: Trainer 核心

| Order | 文件路径 | 目的 | 依赖 |
|---|---|---|---|
| 2.1 | `src/finetune_demo/trainer/__init__.py` | trainer 子包导出 | Phase 0 |
| 2.2 | `src/finetune_demo/trainer/base.py` | Base trainer 抽象 | Phase 1 |
| 2.3 | `src/finetune_demo/trainer/lora_trainer.py` | LoRA/QLoRA 训练逻辑 | Phase 1 |

**实现要点：** `lora_trainer.py` 封装 `trl.SFTTrainer` + `peft.LoraConfig`。支持 FP16 LoRA 和 NF4 QLoRA 两条路径。对齐 T304 `LoRA / QLoRA 路径` 和 T703 `v3 收紧`。

### Phase 3: Adapter 持久化

| Order | 文件路径 | 目的 | 依赖 |
|---|---|---|---|
| 3.1 | `src/finetune_demo/adapter/__init__.py` | adapter 子包 | Phase 2 |
| 3.2 | `src/finetune_demo/adapter/saver.py` | Adapter 保存 | Phase 2 |
| 3.3 | `src/finetune_demo/adapter/loader.py` | Adapter 加载 | Phase 2 |

**实现要点：** 对齐 T1104 `adapter artifact manifest`。`saver.py` 使用 `PeftModel.save_pretrained()`。

### Phase 4: 模型导出

| Order | 文件路径 | 目的 | 依赖 |
|---|---|---|---|
| 4.1 | `src/finetune_demo/export/__init__.py` | export 子包 | Phase 3 |
| 4.2 | `src/finetune_demo/export/adapter_exporter.py` | Adapter 导出与合并 | Phase 3 |

**实现要点：** `adapter_exporter.py` 使用 `PeftModel.merge_and_unload()` 合并 adapter 到 base model。对齐 T1104 `adapter artifact manifest`。

### Phase 5: CLI 入口

| Order | 文件路径 | 目的 | 依赖 |
|---|---|---|---|
| 5.1 | `src/finetune_demo/main.py` | Typer CLI（train / merge） | Phase 2 + 3 + 4 |

**实现要点：** 来自 accepted T1004 `T1004-finetune-main-py-blueprint-v1.md`。两个命令：
- `train`: 调用 `lora_trainer.py`
- `save`: 调用 `adapter/saver.py`

### Phase 6: 测试骨架

| Order | 文件路径 | 目的 | 依赖 |
|---|---|---|---|
| 6.1 | `tests/__init__.py` | 测试包 | 无 |
| 6.2 | `tests/conftest.py` | pytest fixtures | Phase 5 |
| 6.3 | `tests/test_trainer.py` | trainer 单元测试 | Phase 2 + 6.2 |

### Phase 7: 脚本

| Order | 文件路径 | 目的 | 依赖 |
|---|---|---|---|
| 7.1 | `scripts/train.sh` | 快速启动训练脚本 | Phase 5 |

---

## 目录结构

```
finetune-demo/
├── pyproject.toml                 ← Phase 0
├── src/
│   └── finetune_demo/
│       ├── __init__.py
│       ├── __version__.py
│       ├── main.py                ← Phase 5 (CLI)
│       ├── config.py              ← Phase 1
│       ├── trainer/
│       │   ├── __init__.py
│       │   ├── base.py           ← Phase 2
│       │   └── lora_trainer.py   ← Phase 2
│       ├── adapter/
│       │   ├── __init__.py
│       │   ├── saver.py          ← Phase 3
│       │   └── loader.py         ← Phase 3
│       └── export/
│           ├── __init__.py
│           └── adapter_exporter.py ← Phase 4
├── configs/
│   ├── lora/
│   │   └── lora_config_qwen_05b.yaml  ← Phase 1
│   └── qlora/
│       └── qlora_config_qwen_05b.yaml  ← Phase 1
├── data/
│   └── samples/
│       ├── conversation_sample_01.jsonl  ← T1104 fixture
│       ├── code_generation_sample_01.jsonl
│       ├── alpaca_format_sample_01.jsonl
│       ├── roleplay_sample_01.jsonl
│       └── multiturn_sample_01.jsonl
├── outputs/                       ← Phase 0
│   ├── logs/
│   └── qlora_qwen_05b/
│       └── checkpoint-XXX/
├── scripts/
│   └── train.sh                   ← Phase 7
└── tests/
    ├── __init__.py                ← Phase 6
    ├── conftest.py                ← Phase 6
    └── test_trainer.py            ← Phase 6
```

---

Sources:
- T304: finetune-demo MVP directory design
- T703: finetune training map v3 (LoRA/QLoRA/SFT/DPO paths)
- T1104: finetune fixture manifest (JSONL samples, LoRA/QLoRA configs, adapter artifacts)
- T1004: finetune starter file pack

Risk of Staleness:
- PEFT/TRL API stable; training map v3 aligns with current best practices
