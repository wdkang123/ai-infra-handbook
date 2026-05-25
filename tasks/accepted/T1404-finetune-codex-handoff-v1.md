# finetune-demo Codex Handoff v1

## Task ID: T1404
## Title: finetune-demo Codex Task Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# finetune-demo Codex Handoff

本文档是可直接复制给 Codex 的任务卡 handoff 文本。

---

## T1404-T01: 包骨架 + CLI

**任务：** 为 `finetune-demo/` 创建 Typer CLI 骨架。

**main.py 要求：**
- 使用 Typer，两个子命令：`train`、`save`
- `train` 命令参数：`--method`、`--model`、`--dataset`、`--output`、`--epochs`、`--per-device-batch-size`、`--learning-rate`、`--lora-r`、`--lora-alpha`、`--load-in-4bit`、`--config`
- `save` 命令参数：`--checkpoint`、`--output`

**CLI 命令格式：**
```bash
finetune-demo train --method lora --model Qwen/Qwen2.5-0.5B-Instruct --dataset ./data/train.jsonl
finetune-demo save --checkpoint ./models/lora/checkpoint-500 --output ./models/lora/adapter
```

**禁止事项：** 不得在 T01 实现真实 trainer/config 调用

---

## T1404-T02: Config 加载

**任务：** 实现 `config.py`。

**关键类：`TrainingConfig`（Pydantic BaseSettings）**
- 子配置：`model.ModelConfig`、`lora.LoRAConfig`、`qlora.QLoRAConfig`、`data.DataConfig`
- `load_config(config_path) -> TrainingConfig` — 从 YAML 加载
- `load_config_from_cli(**kwargs) -> TrainingConfig` — 从 CLI 参数构建

**LoRAConfig 属性：**
```python
lora.r: int = 16
lora.lora_alpha: int = 32
lora.lora_dropout: float = 0.05
lora.target_modules: list[str] = ["q_proj", "v_proj"]
```

**QLoRAConfig 属性：**
```python
qlora.load_in_4bit: bool = True
qlora.bnb_4bit_quant_type: str = "nf4"
```

**注意：** `load_config()` 返回 `TrainingConfig` 对象，不是 dict。访问字段用 `cfg.lora.r`，不是 `cfg['lora_r']`。

**禁止事项：** 不实现 trainer

---

## T1404-T03: Trainer 创建

**任务：** 实现 `trainer/lora_trainer.py`。

**关键类：`LoRATrainer`**
- `__init__(config: TrainingConfig | dict[str, Any])` — 接收 config 对象
- 内部使用 `TrainingConfig(**config)` 将 dict 转为 config 对象
- `validate()` — 验证参数合法性

**LoRATrainer 初始化示例：**
```python
from finetune_demo.config import load_config
from finetune_demo.trainer.lora_trainer import LoRATrainer

cfg = load_config('configs/qlora/qlora_config_qwen_05b.yaml')
trainer = LoRATrainer(config=cfg)
```

**注意：** 不要写 `LoRATrainer('configs/...')` 直接传路径字符串。正确做法是先 `load_config()` 再传 config 对象。

**禁止事项：** 不实现 `train()` 方法、不实现 export

---

## T1404-T04: CLI train 命令

**任务：** 将 T02 和 T03 接入 `main.py` 的 `train` 子命令。

**train 子命令接入：**
- 从 CLI 参数构建 config（优先使用 YAML config 文件）
- 调用 `LoRATrainer(config=cfg)`
- 调用 `trainer.train()`（placeholder）

**注意：** CLI 参数 `--max-steps` 不是有效参数。有效参数包括：`--epochs`、`--per-device-batch-size`、`--learning-rate`、`--lora-r` 等（见 T1004-finetune-main-py-blueprint-v1.md）。

**禁止事项：**
- 不得实现 `--max-steps`（该参数不存在）
- 不得实现 adapter export（属于后续任务）

---

Sources:
- T1004: accepted starter manifest
- T304: accepted MVP design
- T1304: accepted execution slice
