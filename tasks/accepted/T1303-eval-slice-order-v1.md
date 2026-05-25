# eval-module Slice Order v1

## Task ID: T1303
## Title: eval-module Execution Slice Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# eval-module Execution Slice Order

本文档定义 eval-module 的 slice 执行顺序与依赖关系。

## Slice 执行顺序

```
E1 (包骨架 + CLI)
  │
  ├── E2 (Runner)                     ← 依赖 E1 的 main.py 和 typer
  │       │
  │       └── E6 (测试骨架)            ← 依赖 E2 的 runner
  │
  ├── E3 (Result Store)               ← 与 E2 并行，独立模块
  │       │
  │       └── E4 (Comparator)          ← 依赖 E3 的 result store
  │
  └── E5 (CLI 命令完整化)              ← 依赖 E2 + E3
```

---

## 关键依赖说明

| 依赖路径 | 说明 |
|---|---|
| E2 依赖 E1 | E2 的 runner 被 E1 的 typer CLI 调用 |
| E3 并行 E2 | Result store 是独立模块，不依赖 runner |
| E4 依赖 E3 | Comparator 需要 E3 的 result store |
| E5 依赖 E2 + E3 | CLI 的 `run` 命令调用 runner，`compare` 命令调用 result store |
| E6 依赖 E2 | 测试 runner 需要 E2 的 runner 实现 |

---

## 与 inference-service 依赖

| Slice | 对 inference-service 的依赖 |
|---|---|
| E1 | 无 |
| E2 | 需要 inference-service 运行才能端到端验证（但 P0 可用 mock） |
| E3 | 无 |
| E4 | 无 |
| E5 | 需要 inference-service 运行才能完整端到端验证 |
| E6 | 无（可用 mock） |

---

Sources:
- T1003: accepted starter manifest
- T1203: accepted implementation map
- T813: accepted validation checklist
