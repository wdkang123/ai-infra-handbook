# finetune-demo First Codex Batch v1

## Task ID: T1304
## Title: finetune-demo Execution Slice Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# finetune-demo First Codex Batch

本文档定义适合第一轮真实 Codex 编码的文件批次。

## 建议批次

**第一批（当前批次）：F1 + F2**

理由：
- 无 GPU 依赖
- CLI 骨架和 Config 可并行开发
- 是后续所有 slice 的基础

**第二批：F3（Trainer 创建）**

理由：核心模块，依赖 F2 的 config。

**第三批：F6（测试骨架）**

理由：依赖 F3 的 trainer 实现。

**第四批：F4（CLI train 命令）**

理由：依赖 F2 + F3 完成后。

**第五批：F5（Adapter Export）**

理由：依赖 F3 的 trainer + checkpoint，独立的 export 逻辑。

---

## 第一批文件清单（F1 + F2）

### F1 产出

| 文件 | 说明 | 蓝本 |
|---|---|---|
| `src/finetune_demo/__init__.py` | 包声明 | T1004 |
| `src/finetune_demo/__version__.py` | 版本常量 | T1004 |
| `src/finetune_demo/main.py` | Typer CLI 入口，`train` / `save` 子命令 | T1004 |
| `pyproject.toml` | 项目元数据 | T1004 |
| `.env.example` | 环境变量模板 | T1004 |

### F2 产出

| 文件 | 说明 | 蓝本 |
|---|---|---|
| `src/finetune_demo/config.py` | `load_config()` Pydantic schema + YAML 加载 | T1004 |

---

## 第一批 Handoff Note for Codex

1. **CLI 结构：** `main.py` 使用 Typer，两个子命令：`train`、`save`
2. **命令口径：** `python -m finetune_demo.main train --method lora --model Qwen/Qwen2.5-0.5B-Instruct --dataset ./data/train.jsonl --output ./models`
3. **Config 格式：** LoRA 和 QLoRA config 均用 YAML，`load_config()` 返回 Pydantic schema 对象
4. **trainer 位置：** `src/finetune_demo/trainer/lora_trainer.py`，不是 `train.py`
5. **adapter export：** `src/finetune_demo/export/adapter_exporter.py`，使用 `export_adapter()` 函数
6. **不写 `dataset.py`：** 数据集加载不作为独立模块

---

Sources:
- T1004: accepted starter manifest
- T304: accepted MVP design
- T1204: accepted implementation map
