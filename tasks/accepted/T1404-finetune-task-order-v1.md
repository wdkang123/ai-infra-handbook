# finetune-demo Task Order v1

## Task ID: T1404
## Title: finetune-demo Codex Task Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# finetune-demo Task Order

本文档定义 finetune-demo 的任务执行顺序。

## 执行顺序

```
T1404-T01 (包骨架 + CLI)
  │
  └── T1404-T02 (Config 加载)                  ← 依赖 T01
          │
          └── T1404-T03 (Trainer 创建)            ← 依赖 T02
                  │
                  └── T1404-T04 (CLI train 命令) ← 依赖 T02 + T03
```

---

## 顺序说明

| 路径 | 说明 |
|---|---|
| T02 依赖 T01 | `main.py` 需要 import `config.py` |
| T03 依赖 T02 | `LoRATrainer` 需要 `TrainingConfig` 对象 |
| T04 依赖 T02 + T03 | CLI `train` 命令调用 trainer 和 config |

---

Sources:
- T1304: accepted execution slice order
