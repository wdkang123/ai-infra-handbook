# finetune-demo Slice Order v1

## Task ID: T1304
## Title: finetune-demo Execution Slice Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# finetune-demo Execution Slice Order

本文档定义 finetune-demo 的 slice 执行顺序与依赖关系。

## Slice 执行顺序

```
F1 (包骨架 + CLI)
  │
  └── F2 (Config 加载)                  ← 依赖 F1 的 main.py
          │
          └── F3 (Trainer 创建)           ← 依赖 F2 的 config 加载
                  │
                  ├── F6 (测试骨架)        ← 依赖 F3 的 trainer
                  │
                  ├── F4 (CLI train 命令) ← 依赖 F2 + F3
                  │       │
                  │       └── F5 (Adapter Export) ← 与 F4 并行，依赖 F3
                  │
                  └── F5 (Adapter Export) ← 依赖 F3 的 trainer
```

---

## 关键依赖说明

| 依赖路径 | 说明 |
|---|---|
| F2 依赖 F1 | F1 的 main.py 需要 F2 的 config |
| F3 依赖 F2 | LoRATrainer 初始化需要 config |
| F4 依赖 F2 + F3 | CLI `train` 命令调用 trainer 和 config |
| F5 依赖 F3 | Export 使用 trainer 产生的 checkpoint |
| F6 依赖 F3 | 测试 trainer 需要 F3 的实现 |

---

## GPU 资源说明

| Slice | GPU 需求 | 说明 |
|---|---|---|
| F1 | 否 | 仅 CLI 骨架 |
| F2 | 否 | 纯配置解析 |
| F3 | **是** | LoRA/QLoRA trainer 需要 GPU |
| F4 | 是 | 依赖 F3 |
| F5 | **是**（可能） | export 可能需要加载 base model |
| F6 | 否（可用 mock） | 测试可 mock trainer |

---

Sources:
- T1004: accepted starter manifest
- T1204: accepted implementation map
- T304: accepted MVP design
