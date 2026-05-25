# finetune-demo Slice Manifest v1

## Task ID: T1304
## Title: finetune-demo Execution Slice Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# finetune-demo Execution Slice Manifest

本文档索引 finetune-demo 的所有 execution slices，供 Codex 编码时参照。

## Slice 总览

| Slice ID | 名称 | 目标文件 | 验证入口 | 前置条件 |
|---|---|---|---|---|
| F1 | 包骨架 + CLI | `main.py / pyproject.toml` | `python -m finetune_demo.main train --help` | 无 |
| F2 | Config 加载 | `config.py` | `load_config()` 返回正确字段 | F1 |
| F3 | Trainer 创建 | `trainer/lora_trainer.py / trainer/base.py` | `LoRATrainer` 实例化成功 | F2 |
| F4 | CLI train 命令 | `main.py`（修改） | `python -m finetune_demo.main train` 执行 | F2 + F3 |
| F5 | Adapter Export | `export/adapter_exporter.py` | `export_adapter()` 产出目录 | F3 |
| F6 | 测试骨架 | `tests/conftest.py / tests/test_trainer.py` | `pytest tests/` | F3 |

---

## Slice 覆盖范围

| 主线 | 覆盖 Slice |
|---|---|
| CLI 入口 | F1, F4 |
| Config | F2 |
| Trainer | F3, F6 |
| Adapter Export | F5 |
| CLI 完整化 | F4 |

---

## Cut Line

以下内容不进入当前 slice 集合：
- Unsloth 加速训练
- DPO / SFT 训练器
- 多节点分布式训练
- 全参数微调

---

Sources:
- T1004: accepted starter manifest
- T1104: fixture assets
- T304: accepted MVP design
- T703: finetuning training map
- T1204: accepted implementation map

Risk of Staleness:
- PEFT/TRL API 在 0.10+ / 0.8+ 相对稳定
