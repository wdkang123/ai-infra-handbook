# finetune-demo Slice Contracts v1

## Task ID: T1304
## Title: finetune-demo Execution Slice Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# finetune-demo Slice Contracts

本文档定义每个 slice 的具体目标、入口、验收命令、前置条件和完成信号。

---

## F1: 包骨架 + CLI

**目标文件：**
- `pyproject.toml`
- `src/finetune_demo/__init__.py`
- `src/finetune_demo/__version__.py`
- `src/finetune_demo/main.py`
- `.env.example`

**入口：** `python -m finetune_demo.main --help`

**验收命令：**
```bash
cd finetune-demo
python -m finetune_demo.main --help
# 期望：显示 train / save 两个子命令

python -m finetune_demo.main train --help
# 期望：显示 --method / --model / --dataset / --output / --epochs 等参数

python -m finetune_demo.main save --help
# 期望：显示 --checkpoint / --output 等参数
```

**前置条件：** 无

**完成信号：** Typer CLI 骨架可运行，`train` 和 `save` 子命令均可见

**Cut Line：** 不实现 config 加载、trainer、export

---

## F2: Config 加载

**目标文件：**
- `src/finetune_demo/config.py`

**入口：** 直接 import 或 F1/F4 调用

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

**前置条件：** F1 完成

**完成信号：** LoRA 和 QLoRA config 均正确解析

**Cut Line：** 不实现 trainer

---

## F3: Trainer 创建

**目标文件：**
- `src/finetune_demo/trainer/__init__.py`
- `src/finetune_demo/trainer/base.py`
- `src/finetune_demo/trainer/lora_trainer.py`

**入口：** 直接 import

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

**前置条件：** F2 完成

**完成信号：** LoRA 和 QLoRA trainer 均成功实例化

**Cut Line：** 不实现 train() 方法、不实现 export

---

## F4: CLI train 命令

**目标文件：**
- `src/finetune_demo/main.py`（修改）

**入口：** `python -m finetune_demo.main train`

**验收命令：**
```bash
cd finetune-demo
# 3 步假训练（不需要真实 GPU 数据）
python -m finetune_demo.main train \
  --method qlora \
  --model Qwen/Qwen2.5-0.5B-Instruct \
  --dataset ./data/train.jsonl \
  --output ./outputs/test_trial \
  --epochs 1

# 输出目录存在
ls outputs/test_trial/
# 期望：输出目录存在，训练过程已启动并写出产物
```

**前置条件：** F2 + F3 完成

**完成信号：** 训练执行，输出目录生成

**Cut Line：** 不实现 adapter export

---

## F5: Adapter Export

**目标文件：**
- `src/finetune_demo/export/__init__.py`
- `src/finetune_demo/export/adapter_exporter.py`

**入口：** `python -m finetune_demo.main save` 或直接 import

**验收命令：**
```bash
cd finetune-demo
python -c "
from finetune_demo.export.adapter_exporter import export_adapter
from pathlib import Path

base = 'Qwen2.5-0.5B-Instruct'
adapter = 'outputs/test_trial/checkpoint-3'
output = 'outputs/merged_test'

export_adapter(base, adapter, output)

merged = Path(output)
assert merged.exists(), f'merged model not found: {merged}'
print('Export OK:', merged)
"

ls outputs/merged_test/adapter_config.json
# 期望：adapter_config.json 存在
```

**前置条件：** F3 完成

**完成信号：** adapter export 成功，`adapter_config.json` 存在

**Cut Line：** 不实现 adapter 加载到 inference-service

---

## F6: 测试骨架

**目标文件：**
- `tests/__init__.py`
- `tests/conftest.py`
- `tests/test_trainer.py`

**入口：** `pytest tests/ -v`

**验收命令：**
```bash
cd finetune-demo
pytest tests/ -v
# 期望：所有测试通过
```

**前置条件：** F3 完成

**完成信号：** pytest 全部通过

**Cut Line：** 不写集成测试

---

Sources:
- T1004: accepted starter manifest
- T1104: fixture assets
- T304: accepted MVP design
- T1204: accepted implementation map
