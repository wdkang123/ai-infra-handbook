# finetune-demo Artifact Flow v1

## Task ID: T804
## Task Title: finetune-demo Execution Prep Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T304 MVP 设计，准备 finetune-demo 实施前包。

---

# finetune-demo Artifact Flow v1

## 概述

本文档定义 finetune-demo 的训练产物在模块间的流转路径。

---

## 产物总览

| 产物 | 类型 | 用途 | 下游模块 |
|------|------|------|---------|
| Adapter 权重 | safetensors | 微调产物 | inference-service |
| Adapter Config | JSON | PEFT 配置 | inference-service |
| 训练 Metrics | JSON | 训练过程记录 | Langfuse（可选） |
| Checkpoint | 目录 | 中间保存点 | — |

---

## 产物流转图

```
finetune-demo
    │
    ├── 训练
    │     │
    │     ├── 1. base model（HuggingFace）
    │     │         ↓
    │     ├── 2. LoRA/QLoRA adapter
    │     │         ↓
    │     └── 3. adapter 产物
    │               ├── adapter_config.json
    │               ├── adapter_model.safetensors
    │               └── training_metrics.json
    │
    └── 部署交接
              ↓
        inference-service
              │
              ├── 加载 base model
              ├── 加载 adapter
              └── 提供推理 API
```

---

## Adapter 产物结构

```
./models/
└── qlora/
    └── checkpoint-500/
        ├── adapter_config.json      # PEFT 配置
        ├── adapter_model.safetensors  # adapter 权重
        ├── optimizer.pt             # 优化器状态（可选）
        ├── scheduler.pt             # 学习率调度器（可选）
        └── trainer_state.json       # 训练状态
```

### adapter_config.json 示例

```json
{
  "auto_mapping": null,
  "base_model_name_or_path": "Qwen/Qwen2.5-0.5B-Instruct",
  "bias": "none",
  "fan_in_fan_out": false,
  "inference_mode": true,
  "init_lora_weights": true,
  "layers_pattern": null,
  "layers_to_transform": null,
  "lora_alpha": 32,
  "lora_dropout": 0.05,
  "r": 16,
  "rank_null_space": null,
  "rank_per_layer": null,
  "restore_cell_weights": null,
  "target_modules": ["q_proj", "v_proj"],
  "task_type": "CAUSAL_LM"
}
```

---

## 与 inference-service 的交接

### 交接点

```
finetune-demo                              inference-service
     │                                           │
     ├── adapter 产物目录 ──────────────────────→ │
     │      │                                    ├── 加载 base model
     │      │                                    ├── 加载 adapter_config.json
     │      │                                    └── 启动推理服务
     │                                           │
     └── 交接完成                                 └── 提供推理 API
```

### inference-service 加载 adapter

```bash
# 方式一：vLLM 命令行
vllm serve Qwen/Qwen2.5-0.5B-Instruct \
    --lora ./models/qlora/checkpoint-500 \
    --port 8000

# 方式二：代码加载
from peft import PeftModel
base_model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct")
model = PeftModel.from_pretrained(base_model, "./models/qlora/checkpoint-500")
```

来源：https://docs.vllm.ai/

---

## 与 eval-module 的联动

### 评测流程

```
finetune-demo
    │
    ├── 训练 adapter
    │
    └── 交接 ──────────────────────────────────→ inference-service
                                               │
                                               ├── 加载 adapter
                                               │
eval-module ←───────────────────────────────────┘
     │
     ├── 运行 benchmark
     │
     └── 输出评测结果
```

---

## 产物版本管理

### 建议目录结构

```
./models/
├── qlora-7b-run-001/
│   ├── checkpoint-100/
│   ├── checkpoint-500/
│   ├── checkpoint-1000/
│   └── final/
│       ├── adapter_config.json
│       └── adapter_model.safetensors
├── qlora-7b-run-002/
│   └── ...
└── lora-7b-run-001/
    └── ...
```

---

## 产物存储策略

| 产物 | 存储位置 | 持久化 | 建议 |
|------|---------|--------|------|
| Final adapter | `./models/` | 是 | Git LFS 或外部存储 |
| Checkpoints | `./models/` | 可选 | 中间 checkpoint 不必全部保留 |
| Training metrics | `./results/` | 是 | JSON 文件 |

---

Sources:
1. https://github.com/huggingface/peft — PEFT
2. https://docs.vllm.ai/ — vLLM

Risk of Staleness:
- adapter 格式可能随 PEFT 版本变化

Out of Scope Kept:
- 未写产物版本管理系统
