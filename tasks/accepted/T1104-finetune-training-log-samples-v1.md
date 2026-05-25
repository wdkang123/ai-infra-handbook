# finetune-demo Training Log Samples v1

## Task ID: T1104
## Title: finetune-demo Fixture Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# finetune-demo Training Log Samples

本文档定义 finetune-demo 训练过程的日志样本，对应真实文件 `finetune-demo/outputs/logs/`。**这是仓库样例约定，不是真实跑出的数据。**

## 日志结构

每个训练 run 生成：
- `trainer_state.json` — Trainer 状态（step / epoch / loss）
- `train_log.txt` — 实时训练日志
- `tensorboard/` — TensorBoard event files

---

## Trainer State Sample

**对应文件：** `finetune-demo/outputs/logs/trainer_state_qwen_05b_3epoch.json`

```json
{
  "epoch": 2.97,
  "global_step": 290,
  "max_steps": 300,
  "logging_steps": 10,
  "save_steps": 100,
  "total_flos": 1.23e17,
  "train_history": [
    {"step": 10, "loss": 2.341, "learning_rate": 2.97e-4, "epoch": 0.1},
    {"step": 20, "loss": 1.892, "learning_rate": 2.94e-4, "epoch": 0.2},
    {"step": 30, "loss": 1.654, "learning_rate": 2.91e-4, "epoch": 0.3},
    {"step": 40, "loss": 1.512, "learning_rate": 2.88e-4, "epoch": 0.4},
    {"step": 50, "loss": 1.398, "learning_rate": 2.85e-4, "epoch": 0.5},
    {"step": 60, "loss": 1.301, "learning_rate": 2.82e-4, "epoch": 0.6},
    {"step": 70, "loss": 1.234, "learning_rate": 2.79e-4, "epoch": 0.7},
    {"step": 80, "loss": 1.178, "learning_rate": 2.76e-4, "epoch": 0.8},
    {"step": 90, "loss": 1.132, "learning_rate": 2.73e-4, "epoch": 0.9},
    {"step": 100, "loss": 1.095, "learning_rate": 2.70e-4, "epoch": 1.0, "checkpoint": "saved"},
    {"step": 110, "loss": 1.061, "learning_rate": 2.67e-4, "epoch": 1.1},
    {"step": 120, "loss": 1.032, "learning_rate": 2.64e-4, "epoch": 1.2},
    {"step": 130, "loss": 1.007, "learning_rate": 2.61e-4, "epoch": 1.3},
    {"step": 140, "loss": 0.985, "learning_rate": 2.58e-4, "epoch": 1.4},
    {"step": 150, "loss": 0.967, "learning_rate": 2.55e-4, "epoch": 1.5},
    {"step": 160, "loss": 0.950, "learning_rate": 2.52e-4, "epoch": 1.6},
    {"step": 170, "loss": 0.936, "learning_rate": 2.49e-4, "epoch": 1.7},
    {"step": 180, "loss": 0.923, "learning_rate": 2.46e-4, "epoch": 1.8},
    {"step": 190, "loss": 0.912, "learning_rate": 2.43e-4, "epoch": 1.9},
    {"step": 200, "loss": 0.902, "learning_rate": 2.40e-4, "epoch": 2.0, "checkpoint": "saved"},
    {"step": 210, "loss": 0.893, "learning_rate": 2.37e-4, "epoch": 2.1},
    {"step": 220, "loss": 0.885, "learning_rate": 2.34e-4, "epoch": 2.2},
    {"step": 230, "loss": 0.878, "learning_rate": 2.31e-4, "epoch": 2.3},
    {"step": 240, "loss": 0.872, "learning_rate": 2.28e-4, "epoch": 2.4},
    {"step": 250, "loss": 0.867, "learning_rate": 2.25e-4, "epoch": 2.5},
    {"step": 260, "loss": 0.863, "learning_rate": 2.22e-4, "epoch": 2.6},
    {"step": 270, "loss": 0.859, "learning_rate": 2.19e-4, "epoch": 2.7},
    {"step": 280, "loss": 0.856, "learning_rate": 2.16e-4, "epoch": 2.8},
    {"step": 290, "loss": 0.853, "learning_rate": 2.13e-4, "epoch": 2.9},
    {"step": 300, "loss": 0.851, "learning_rate": 2.10e-4, "epoch": 3.0, "checkpoint": "saved"}
  ],
  "best_metric": 0.851,
  "best_model_checkpoint": "outputs/qlora_qwen_05b/checkpoint-300",
  "is_local_process_zero": true
}
```

---

## Training Log Output Sample（文本日志）

**对应文件：** `finetune-demo/outputs/logs/train_log_qwen_05b_3epoch.txt`

```
{"epoch": 0.1, "step": 10, "loss": 2.341, "lr": 2.97e-4, "msg": "Training..."}
{'loss': 2.341, 'learning_rate': 0.000297, 'epoch': 0.1}
{"epoch": 0.2, "step": 20, "loss": 1.892, "lr": 2.94e-4, "msg": "Training..."}
{'loss': 1.892, 'learning_rate': 0.000294, 'epoch': 0.2}
{"epoch": 0.3, "step": 30, "loss": 1.654, "lr": 2.91e-4, "msg": "Training..."}
{'loss': 1.654, 'learning_rate': 0.000291, 'epoch': 0.3}
...
{"level": "INFO", "step": 100, "msg": "Saving checkpoint", "checkpoint_path": "outputs/qlora_qwen_05b/checkpoint-100"}
{"level": "INFO", "step": 100, "msg": "checkpoint saved"}
{"level": "INFO", "step": 200, "msg": "Saving checkpoint", "checkpoint_path": "outputs/qlora_qwen_05b/checkpoint-200"}
{"level": "INFO", "step": 200, "msg": "checkpoint saved"}
...
{"level": "INFO", "step": 300, "msg": "Training completed", "total_steps": 300, "best_loss": 0.851}
{"level": "INFO", "step": 300, "msg": "Saving final model", "output_path": "outputs/qlora_qwen_05b/checkpoint-300"}
```

---

## 关键 checkpoint 节点

| Step | Epoch | Loss | 事件 |
|---|---|---|---|
| 100 | 1.0 | 1.095 | ✅ Checkpoint saved |
| 200 | 2.0 | 0.902 | ✅ Checkpoint saved |
| 300 | 3.0 | 0.851 | ✅ Final model saved |

---

## Loss Curve 趋势（仓库样例约定）

```
step 10:  ████████████████ 2.341
step 50:  ████████████░░░ 1.398
step 100: ██████████░░░░░ 1.095  ← checkpoint
step 150: █████████░░░░░░ 0.967
step 200: ████████░░░░░░░ 0.902  ← checkpoint
step 250: ████████░░░░░░░ 0.867
step 300: ████████░░░░░░░ 0.851  ← final
```

**预期趋势：** 前 100 step 下降最快，随后趋于平稳。

---

## 训练结束后目录结构

```
outputs/qlora_qwen_05b/
├── checkpoint-100/
│   ├── adapter_config.json   # PEFT adapter config
│   ├── adapter_model.safetensors  # LoRA weights
│   └── tokenizer.json
├── checkpoint-200/
│   └── ...
├── checkpoint-300/          # best / final
│   ├── adapter_config.json
│   ├── adapter_model.safetensors
│   └── tokenizer.json
├── trainer_state.json        # training history
└── train_log.txt            # raw training log
```

---

Sources:
1. https://github.com/huggingface/transformers — Trainer
2. https://github.com/artidoro/qlora — QLoRA paper

Risk of Staleness:
- HuggingFace Trainer log format is stable
