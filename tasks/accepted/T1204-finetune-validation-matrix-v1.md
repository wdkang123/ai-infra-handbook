# finetune-demo Validation Matrix v1

## Task ID: T1204
## Title: finetune-demo Implementation Map Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# finetune-demo Validation Matrix

本文档定义 finetune-demo 各 patch 的验收测试矩阵。

## Validation Matrix

| ID | 命令 | 场景 | 预期结果 | 验证命令 | 依赖 Patch |
|---|---|---|---|---|---|
| F01 | `load_config` | LoRA config 加载 | 返回正确字段 | `python -c "from finetune_demo.config import load_config; c = load_config('configs/lora/lora_config_qwen_05b.yaml'); print(c['lora_r'])"` | P0 |
| F02 | `load_config` | QLoRA config 加载 | 返回正确字段 | `python -c "from finetune_demo.config import load_config; c = load_config('configs/qlora/qlora_config_qwen_05b.yaml'); print(c['quantization']['load_in_4bit'])"` | P0 |
| F03 | `LoRATrainer` | LoRA Trainer 创建 | 对象创建成功 | `python -c "from finetune_demo.trainer.lora_trainer import LoRATrainer; t = LoRATrainer('configs/lora/lora_config_qwen_05b.yaml'); print('OK')"` | P2 |
| F04 | `LoRATrainer` | QLoRA Trainer 创建 | 对象创建成功 | `python -c "from finetune_demo.trainer.lora_trainer import LoRATrainer; t = LoRATrainer('configs/qlora/qlora_config_qwen_05b.yaml'); print('OK')"` | P2 |
| F05 | `main.py train` | 假训练（3步） | loss 输出 | `python -m finetune_demo.main train --config configs/qlora/qlora_config_qwen_05b.yaml --output ./outputs/test_trial --max-steps 3` | P3 |
| F06 | `main.py train` | checkpoint 保存 | checkpoint 目录存在 | `ls outputs/test_trial/checkpoint-3/` | P3 |
| F07 | `main.py save` | adapter 导出 | merged 目录存在 | `python -c "from finetune_demo.export.adapter_exporter import export_adapter; export_adapter('Qwen2.5-0.5B-Instruct', 'outputs/test_trial/checkpoint-3', 'outputs/merged_test'); print('OK')"` | P4 |
| F08 | `main.py train --help` | CLI train 帮助 | 输出正确参数 | `python -m finetune_demo.main train --help` | P5 |
| F09 | `main.py save --help` | CLI save 帮助 | 输出正确参数 | `python -m finetune_demo.main save --help` | P5 |

---

## F01-F02: Config Loading Verification

```bash
# F01: LoRA config
python -c "
from finetune_demo.config import load_config
cfg = load_config('configs/lora/lora_config_qwen_05b.yaml')
assert cfg['lora_r'] == 16
assert cfg['lora_alpha'] == 32
assert cfg['target_modules'] == ['q_proj', 'v_proj']
print('LoRA config OK:', cfg)
"

# F02: QLoRA config
python -c "
from finetune_demo.config import load_config
cfg = load_config('configs/qlora/qlora_config_qwen_05b.yaml')
assert cfg['quantization']['load_in_4bit'] == True
assert cfg['quantization']['bnb_4bit_quant_type'] == 'nf4'
print('QLoRA config OK:', cfg)
"
```

**对应 fixture：** T1104 `T1104-finetune-lora-config-samples-v1.md`

---

## F03-F04: Trainer Creation Verification

```bash
# F03: LoRA trainer
python -c "
from finetune_demo.trainer.lora_trainer import LoRATrainer
t = LoRATrainer('configs/lora/lora_config_qwen_05b.yaml')
print('LoRA trainer OK')
"

# F04: QLoRA trainer
python -c "
from finetune_demo.trainer.lora_trainer import LoRATrainer
t = LoRATrainer('configs/qlora/qlora_config_qwen_05b.yaml')
print('QLoRA trainer OK')
"
```

**对应 fixture：** T1104 `T1104-finetune-jsonl-dataset-samples-v1.md`

---

## F05-F06: Training Verification

```bash
# F05: 3-step trial run
python -m finetune_demo.main train \
  --config configs/qlora/qlora_config_qwen_05b.yaml \
  --output ./outputs/test_trial \
  --max-steps 3

# F06: checkpoint exists
python -c "
from pathlib import Path
ckpt = Path('outputs/test_trial/checkpoint-3')
assert ckpt.exists(), f'checkpoint not found: {ckpt}'
print('Checkpoint OK:', ckpt)
"
```

**对应 fixture：** T1104 `T1104-finetune-training-log-samples-v1.md`

---

## F07: Adapter Export Verification

```bash
# F07: export adapter
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

# 检查 adapter_config.json 存在
ls outputs/merged_test/adapter_config.json
```

**对应 fixture：** T1104 `T1104-finetune-adapter-artifact-manifest-v1.md`

---

Sources:
- T304: finetune-demo MVP design
- T703: finetune training map v3
- T1104: finetune fixture manifest, lora config samples, adapter artifact manifest

Risk of Staleness:
- CLI and config format are project-internal; PEFT adapter format stable
