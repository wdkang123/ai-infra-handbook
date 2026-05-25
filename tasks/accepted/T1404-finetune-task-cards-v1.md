# finetune-demo Task Cards v1

## Task ID: T1404
## Title: finetune-demo Codex Task Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# finetune-demo Task Cards

本文档定义每个任务卡的具体输入资产、目标文件、验收命令、完成信号和 cut line。

---

## T1404-T01: 包骨架 + CLI

**Task Name:** 包骨架 + CLI

**对应 Slice:** F1

**输入资产：**
- `T1004-finetune-starter-manifest.md`
- `T1004-finetune-main-py-blueprint-v1.md`

**目标文件：**
```
finetune-demo/
├── pyproject.toml
├── src/finetune_demo/
│   ├── __init__.py
│   ├── __version__.py
│   └── main.py
├── .env.example
```

**验收命令：**
```bash
cd finetune-demo
python -m finetune_demo.main --help
# 期望：显示 train / save 两个子命令
```

**完成信号：** Typer CLI 骨架可运行，`train` 和 `save` 子命令均可见

**Cut Line：** 不实现 config 加载、trainer、export

---

## T1404-T02: Config 加载

**Task Name:** Config 加载

**对应 Slice:** F2

**输入资产：**
- `T1004-finetune-config-schema-blueprint-v1.md`
- `T1404-T01/`

**目标文件：**
```
finetune-demo/src/finetune_demo/
└── config.py
```

**验收命令：**
```bash
cd finetune-demo
python -c "
from finetune_demo.config import load_config
cfg = load_config('configs/lora/lora_config_qwen_05b.yaml')
assert cfg.lora.r == 16
assert cfg.lora.lora_alpha == 32
assert cfg.method == 'lora'
print('LoRA config OK, method:', cfg.method)
"

python -c "
from finetune_demo.config import load_config
cfg = load_config('configs/qlora/qlora_config_qwen_05b.yaml')
assert cfg.qlora.load_in_4bit == True
assert cfg.qlora.bnb_4bit_quant_type == 'nf4'
assert cfg.method == 'qlora'
print('QLoRA config OK, method:', cfg.method)
"
```

**完成信号：** LoRA 和 QLoRA config 均正确解析，`load_config()` 返回 `TrainingConfig` Pydantic 对象

**Cut Line：** 不实现 trainer

---

## T1404-T03: Trainer 创建

**Task Name:** Trainer 创建

**对应 Slice:** F3

**输入资产：**
- `T1004-finetune-train-py-blueprint-v1.md`
- `T1404-T02/`

**目标文件：**
```
finetune-demo/src/finetune_demo/trainer/
├── __init__.py
├── base.py
└── lora_trainer.py
```

**验收命令：**
```bash
cd finetune-demo
python -c "
from finetune_demo.config import load_config
from finetune_demo.trainer.lora_trainer import LoRATrainer
cfg = load_config('configs/lora/lora_config_qwen_05b.yaml')
t = LoRATrainer(config=cfg)
print('LoRA trainer OK')
"

python -c "
from finetune_demo.config import load_config
from finetune_demo.trainer.lora_trainer import LoRATrainer
cfg = load_config('configs/qlora/qlora_config_qwen_05b.yaml')
t = LoRATrainer(config=cfg)
print('QLoRA trainer OK')
"
```

**完成信号：** LoRA 和 QLoRA trainer 均成功实例化

**Cut Line：** 不实现 `train()` 方法、不实现 export

---

## T1404-T04: CLI train 命令

**Task Name:** CLI train 命令

**对应 Slice:** F4

**输入资产：**
- `T1004-finetune-main-py-blueprint-v1.md`
- `T1404-T02/` + `T1404-T03/`

**目标文件：**
```
finetune-demo/src/finetune_demo/
└── main.py（修改）
```

**验收命令：**
```bash
cd finetune-demo
python -m finetune_demo.main train --help
# 期望：--method / --model / --dataset / --output / --epochs 等参数

# 快速验证（不需要真实 GPU）
python -m finetune_demo.main train \
  --method qlora \
  --model Qwen/Qwen2.5-0.5B-Instruct \
  --dataset ./data/train.jsonl \
  --output ./outputs/test_trial \
  --epochs 1
```

**完成信号：** CLI `train` 命令可执行，训练流程启动并生成输出目录

**Cut Line：** 不实现 adapter export（属于后续任务）

---

Sources:
- T1004: accepted starter manifest
- T1104: fixture assets
- T1304: accepted execution slice
- T304: accepted MVP design
