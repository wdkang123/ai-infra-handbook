# Root Integration Codex Task Order v1

## Task ID: T1405
## Title: Root Integration Codex Task Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# Root Integration Codex Task Order

本文档定义根级联调任务的执行顺序。

## 执行顺序

```
T1405-R1 (Makefile 入口)
  │
  └── T1405-R2 (本地开发顺序)              ← 依赖 R1
          │
          └── T1405-R3 (冒烟测试)              ← 依赖 R1 + 子项目 S2 + G3
                  │
                  └── T1405-R4 (跨项目 handoff)  ← 依赖 R3
```

---

## 顺序说明

| 路径 | 说明 |
|---|---|
| R2 依赖 R1 + 子项目 S2 + G3 | `scripts/local_dev_sequence.sh` 需要 Makefile 目标和已可用的 inference / gateway 基础服务 |
| R3 依赖 R1 | `make infra-smoke` 需要 R1 的 Makefile 目标 |
| R3 依赖子项目 S2 | inference-service 需要 S2 完成才能 `/health` 和 `/v1/chat/completions` |
| R3 依赖子项目 G3 | ai-gateway 需要 G3 完成才能 `/health` 和路由/代理 |
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
- T1305: accepted root slice order
- T1005: accepted root makefile blueprint v2
