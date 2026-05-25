# finetune-demo Task Pack Manifest v1

## Task ID: T1404
## Title: finetune-demo Codex Task Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# finetune-demo Task Pack Manifest

本文档索引 finetune-demo 的所有 Codex 实现任务卡。

## 任务卡清单

| Task ID | 任务名称 | 输入资产 | 目标文件 | 验证入口 |
|---|---|---|---|---|
| T1404-T01 | 包骨架 + CLI | T1004 starter manifest | `main.py / pyproject.toml` | `python -m finetune_demo.main --help` |
| T1404-T02 | Config 加载 | T1004 config schema blueprint + T1404-T01 | `config.py` | `load_config()` 返回 TrainingConfig |
| T1404-T03 | Trainer 创建 | T1004 train blueprint + T1404-T02 | `trainer/lora_trainer.py` | `LoRATrainer(config=cfg)` 成功 |
| T1404-T04 | CLI train 命令 | T1004 main.py blueprint + T1404-T02 + T1404-T03 | `main.py`（修改） | `python -m finetune_demo.main train` 执行 |

---

## 与 Slice 的对应关系

| Task ID | 对应 Slice |
|---|---|
| T1404-T01 | F1 |
| T1404-T02 | F2 |
| T1404-T03 | F3 |
| T1404-T04 | F4 |

---

## Cut Line

以下内容不进入当前 task pack：
- Adapter Export（F5）
- 测试骨架（F6）
- Unsloth 加速
- DPO / SFT

---

Sources:
- T1004: accepted starter manifest
- T1104: fixture assets
- T1304: accepted execution slice
- T304: accepted MVP design
- T703: finetuning training map
