# Root Integration Slice Order v1

## Task ID: T1305
## Title: Root Integration Execution Slice Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# Root Integration Execution Slice Order

本文档定义根级联调的 slice 执行顺序与依赖关系。

## Slice 执行顺序

```
R1 (Makefile 入口)
  │
  ├── R2 (本地开发顺序)              ← 依赖 R1
  │       │
  │       └── R3 (冒烟测试)          ← 依赖 R1 + 子项目 S2 + G2
  │               │
  │               └── R4 (跨项目 handoff) ← 依赖 R3
  │
  └── R3 (冒烟测试)                  ← 依赖 R1 + 子项目 S2 + G2
          │
          └── R4 (跨项目 handoff)      ← 依赖 R3
```

---

## 关键依赖说明

| 依赖路径 | 说明 |
|---|---|
| R2 依赖 R1 | `scripts/local_dev_sequence.sh` 内部调用 `make help` 等 |
| R3 依赖 R1 | `make infra-smoke` 需要 R1 的 Makefile 目标 |
| R3 依赖子项目 S2 | inference-service 需要 S2 完成才能 `/health` 和 `/v1/chat/completions` |
| R3 依赖子项目 G2 | ai-gateway 需要 G2 完成才能 `/health` 和鉴权 |
| R4 依赖 R3 | cross-project handoff 验证需要 smoke test 通过 |

---

## 服务依赖关系

```
inference-service (port 8000)
  ↑
  │ HTTP /v1/chat/completions
  │
ai-gateway (port 8080)
  ↑
  │ HTTP (eval-module CLI only, no server)
  │
eval-module (CLI only)
  ↓
  inference-service (for backend)

finetune-demo (CLI only, produces adapter)
  ↓
  inference-service (loads adapter for serving)
```

---

Sources:
- T1005: accepted root makefile blueprint
- T1205: accepted implementation map
- T805: cross-project integration prep pack
