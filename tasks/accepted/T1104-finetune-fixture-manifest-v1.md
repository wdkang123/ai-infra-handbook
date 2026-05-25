# finetune-demo Fixture Manifest v1

## Task ID: T1104
## Title: finetune-demo Fixture Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# finetune-demo Fixture Manifest

本文档是 `finetune-demo` 全部 fixture 资产的索引清单，对应真实路径 `finetune-demo/data/samples/`、`finetune-demo/configs/`、`finetune-demo/outputs/`。

## Fixture 文件清单

### JSONL Dataset Fixtures

| 文件路径 | 场景 | 样本数 |
|---|---|---|
| `data/samples/conversation_sample_01.jsonl` | 通用对话（数学 tutor） | 5 条 |
| `data/samples/code_generation_sample_01.jsonl` | Python 代码生成 | 5 条 |
| `data/samples/alpaca_format_sample_01.jsonl` | Alpaca 格式指令 | 5 条 |
| `data/samples/roleplay_sample_01.jsonl` | 角色扮演对话 | 3 条 |
| `data/samples/multiturn_sample_01.jsonl` | 多轮对话 | 3 条 |

### LoRA / QLoRA Config Fixtures

| 文件路径 | 场景 | 精度 |
|---|---|---|
| `configs/lora/lora_config_qwen_05b.yaml` | LoRA FP16 | FP16 |
| `configs/qlora/qlora_config_qwen_05b.yaml` | QLoRA NF4 | NF4/BF16 |

### Training Log Fixtures

| 文件路径 | 场景 |
|---|---|
| `outputs/logs/trainer_state_qwen_05b_3epoch.json` | 3 epoch 训练状态 |
| `outputs/logs/train_log_qwen_05b_3epoch.txt` | 训练文本日志 |

### Adapter Artifact Fixtures

| 文件路径 | 场景 |
|---|---|
| `outputs/qlora_qwen_05b/checkpoint-300/adapter_config.json` | PEFT adapter config |
| `outputs/qlora_qwen_05b/checkpoint-300/`（目录结构说明） | adapter 产物结构 |
| `outputs/merged_qwen_05b/`（目录结构说明） | 合并后模型目录 |

---

## 与 Starter Blueprint 对齐（T1004 finetune-demo）

| Blueprint 要点 | Fixture 对应 |
|---|---|
| LoRA / QLoRA 两种训练模式 | `configs/lora/` / `configs/qlora/` |
| JSONL 数据格式 | `data/samples/*.jsonl` |
| PEFT adapter 产物 | `outputs/*/adapter_config.json` |
| Training log (epoch/step/loss) | `outputs/logs/trainer_state_*.json` |

---

## 训练数据预处理流程

```
data/raw/                     ← 原始数据（用户提供）
    ↓ preprocess.py           ← 数据清洗 / 格式化
data/samples/*.jsonl          ← 预处理后的训练样本
    ↓ train.py + lora_config ← 训练
outputs/qlora_qwen_05b/checkpoint-XXX/
    ↓ merge_peft_adapter.py  ← 合并 adapter
outputs/merged_qwen_05b/      ← 可直接加载的合并模型
```

---

Sources:
1. https://github.com/artidoro/qlora
2. https://github.com/huggingface/peft
3. https://docs.unsloth.org/

Risk of Staleness:
- PEFT/LoRA format and adapter structure stable
