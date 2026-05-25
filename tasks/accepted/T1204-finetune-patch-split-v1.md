# finetune-demo Patch Split v1

## Task ID: T1204
## Title: finetune-demo Implementation Map Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# finetune-demo Patch Split Proposal

本文档定义 finetune-demo 的分批实现顺序。

## Patch 批次概览

| Patch | 名称 | 目标文件 | 验证方式 |
|---|---|---|---|
| P0 | 骨架 | `pyproject.toml / src/finetune_demo/__init__.py` | `from src.finetune_demo import main` |
| P1 | 配置加载 | `src/finetune_demo/config.py / configs/*.yaml` | `FinetuneConfig.from_yaml(...)` |
| P2 | Trainer 核心 | `trainer/base.py / trainer/lora_trainer.py` | `LoRATrainer.train()` mock（不真实调GPU） |
| P3 | Adapter 持久化 | `adapter/saver.py / adapter/loader.py` | adapter save/load roundtrip |
| P4 | 模型导出 | `export/adapter_exporter.py` | adapter merge 成功 |
| P5 | CLI 入口 | `src/finetune_demo/main.py` | `python -m finetune_demo.main train --help` |
| P6 | 测试骨架 | `tests/conftest.py / test_trainer.py` | `pytest tests/` |

---

## Patch 0: 骨架

**文件：**
- `pyproject.toml`
- `src/finetune_demo/__init__.py`
- `src/finetune_demo/__version__.py`

**验证：**
```bash
cd finetune-demo
python -c "from src.finetune_demo import main; print('OK')"
```

---

## Patch 1: 配置加载

**文件：**
- `src/finetune_demo/config.py`
- `configs/lora/lora_config_qwen_05b.yaml`
- `configs/qlora/qlora_config_qwen_05b.yaml`

**验证：**
```bash
cd finetune-demo
python -c "
from src.finetune_demo.config import FinetuneConfig
cfg = FinetuneConfig.from_yaml('configs/lora/lora_config_qwen_05b.yaml')
print(cfg.lora_r, cfg.lora_alpha)
# 期望：16 32
"
```

---

## Patch 2: LoRA Trainer（假训练）

**文件：**
- `src/finetune_demo/trainer/__init__.py`
- `src/finetune_demo/trainer/base.py`
- `src/finetune_demo/trainer/lora_trainer.py`（mock 版本，不调真实 GPU）

**验证：**
```bash
python -c "
from finetune_demo.trainer.lora_trainer import LoRATrainer
trainer = LoRATrainer(config_path='configs/qlora/qlora_config_qwen_05b.yaml')
# 不调用 trainer.train()，只验证对象创建
print('mock trainer created')
"
```

---

## Patch 3: LoRA Trainer（真实训练）

**文件：**
- `src/finetune_demo/trainer/lora_trainer.py`（真实版）
- `src/finetune_demo/main.py`（修改：调用真实 trainer）

**实现要点：**
```python
from trl import SFTTrainer
from peft import LoraConfig, get_peft_model

trainer = SFTTrainer(
    model=base_model,
    train_dataset=train_dataset,
    dataset_text_field="text",
    max_seq_length=512,
    args=TrainingArguments(
        output_dir="./outputs/qlora_qwen_05b",
        num_train_epochs=3,
        per_device_train_batch_size=4,
        learning_rate=2e-4,
        save_steps=100,
    )
)
trainer.train()
```

**验证：**
```bash
cd finetune-demo
python -m finetune_demo.main train \
  --method qlora \
  --config configs/qlora/qlora_config_qwen_05b.yaml \
  --data data/samples/conversation_sample_01.jsonl \
  --output ./outputs/qlora_qwen_05b
# 期望：outputs/qlora_qwen_05b/checkpoint-XXX/ 存在
```

**对应 fixture：** T1104 `T1104-finetune-training-log-samples-v1.md`

---

## Patch 4: Adapter 持久化 + 模型导出

**文件：**
- `src/finetune_demo/adapter/__init__.py`
- `src/finetune_demo/adapter/saver.py`
- `src/finetune_demo/adapter/loader.py`
- `src/finetune_demo/export/__init__.py`
- `src/finetune_demo/export/adapter_exporter.py`

**验证：**
```bash
python -c "
from src.finetune_demo.export.adapter_exporter import export_adapter
export_adapter(
    base_model='Qwen2.5-0.5B-Instruct',
    adapter_path='./outputs/qlora_qwen_05b/checkpoint-300',
    output_path='./outputs/merged_qwen_05b'
)
# 期望：outputs/merged_qwen_05b/ 存在
"
```

---

## Patch 5: CLI 入口

**文件：**
- `src/finetune_demo/main.py`

**验证：**
```bash
python -m finetune_demo.main --help
# 期望：usage: finetune_demo.main [-h] {train,merge,eval} ...

python -m finetune_demo.main train --help
# 期望：--config, --data, --output

python -m finetune_demo.main merge --help
# 期望：--base-model, --adapter, --output
```

---

## Patch 6: 测试骨架

**文件：**
- `tests/__init__.py`
- `tests/conftest.py`
- `tests/test_trainer.py`

**验证：**
```bash
pytest tests/ -v
# 期望：test_trainer.py 全部通过
```

---

## Patch 依赖关系图

```
P0 (骨架)
  │
  ├── P1 (配置加载)          ← 依赖 P0
  │
  ├── P2 (Trainer 核心)      ← 依赖 P1
  │       │
  │       └── P3 (Adapter)   ← 依赖 P2
  │               │
  │               └── P4 (模型导出) ← 依赖 P3
  │
  └── P5 (CLI)               ← 依赖 P2+P3+P4
          │
          └── P6 (测试)       ← 依赖 P5
```

**注意：** P2（Trainer 真实训练）需要真实 GPU。P0/P1/P5/P6 可在 CPU 上完成。

---

Sources:
- T304: finetune-demo MVP design
- T703: finetune training map v3
- T1104: finetune fixture manifest

Risk of Staleness:
- trl SFTTrainer API stable; PEFT adapter format stable
