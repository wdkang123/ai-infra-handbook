# finetune-demo Import Map v1

## Task ID: T1204
## Title: finetune-demo Implementation Map Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# finetune-demo Import Dependency Map

本文档定义 `finetune-demo` 内部模块的导入依赖关系。

## Import Map

```
src/finetune_demo/
│
├── __init__.py
├── __version__.py             # 纯常量，无依赖
│
├── main.py                    # Typer CLI 入口
│   ├── import typer
│   ├── import yaml
│   ├── from .config import FinetuneConfig
│   ├── from .trainer.lora_trainer import LoRATrainer
│   ├── from .adapter.saver import save_adapter
│   └── from .export.adapter_exporter import export_adapter
│
├── config.py                  # Pydantic 配置 schema
│   └── from pydantic import BaseModel, Field
│
├── trainer/
│   ├── __init__.py
│   ├── base.py              # Base trainer 抽象
│   └── lora_trainer.py      # LoRA/QLoRA 训练封装
│       ├── import yaml
│       ├── from transformers import AutoTokenizer, AutoModelForCausalLM
│       ├── from peft import LoraConfig, get_peft_model
│       ├── from trl import SFTTrainer
│       └── from .config import FinetuneConfig
│
├── adapter/
│   ├── __init__.py
│   ├── saver.py             # Adapter 保存
│   │   └── from peft import PeftModel
│   └── loader.py            # Adapter 加载
│       └── from peft import PeftModel
│
└── export/
    ├── __init__.py
    └── adapter_exporter.py  # Adapter 合并导出
        └── from peft import PeftModel
```

## External Dependencies

| 模块 | 外部依赖 | 版本 |
|---|---|---|
| `main.py` | `typer` | ≥0.9 |
| `config.py` | `pydantic`, `pyyaml` | ≥2.0, ≥6.0 |
| `lora_trainer.py` | `transformers`, `peft`, `trl`, `bitsandbytes` | transformers≥4.36, peft≥0.7, trl≥0.7 |
| `adapter/saver.py` | `peft` | ≥0.7 |
| `export/adapter_exporter.py` | `peft`, `transformers` | 同上 |

## CLI 命令流

```
main.py (Typer app)
  │
  ├── train → LoRATrainer.train()
  │              ├── FinetuneConfig.from_yaml(config_path)
  │              ├── load_dataset(data_path)
  │              ├── AutoModelForCausalLM.from_pretrained()
  │              ├── get_peft_model(model, lora_config)
  │              ├── SFTTrainer(model, train_dataset, ...)
  │              └── trainer.train()
  │       → adapter saved via adapter/saver.py
  │
  └── save → export_adapter()
              ├── PeftModel.from_pretrained(base, adapter_path)
              └── .merge_and_unload()
       → merged model saved to output/merged/
```

## 与 eval-module 的边界

```
finetune_demo (train/merge)
    │
    └── outputs/qlora_qwen_05b/checkpoint-XXX/
              └── adapter_model.safetensors
                        ↓ （外部调用）
              eval_module (run --model <base> --adapter <path>)
                        ↓
              evaluation result JSON
```

---

Sources:
- T304: finetune-demo MVP directory design
- T703: finetune training map v3
- T1104: finetune fixture manifest

Risk of Staleness:
- PEFT/TRL import structure stable since v0.7
