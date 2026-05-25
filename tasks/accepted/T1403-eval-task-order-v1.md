# eval-module Task Order v1

## Task ID: T1403
## Title: eval-module Codex Task Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# eval-module Task Order

本文档定义 eval-module 的任务执行顺序。

## 执行顺序

```
T1403-T01 (包骨架 + CLI)
  │
  ├── T1403-T02 (Result Store)              ← 并行，依赖 T01
  │
  └── T1403-T03 (LmEvalRunner)              ← 并行，依赖 T01
          │
          └── T1403-T04 (CLI 完整化)         ← 依赖 T02 + T03
```

---

## 顺序说明

| 路径 | 说明 |
|---|---|
| T02 并行 T03 | Result store 和 Runner 是独立模块，均依赖 T01 的 CLI 骨架 |
| T04 依赖 T02 + T03 | CLI 的 `run` 命令调用 runner，`compare` 命令调用 result store |

---

Sources:
- T1303: accepted execution slice order
