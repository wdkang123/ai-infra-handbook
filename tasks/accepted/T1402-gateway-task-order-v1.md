# ai-gateway Task Order v1

## Task ID: T1402
## Title: ai-gateway Codex Task Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# ai-gateway Task Order

本文档定义 ai-gateway 的任务执行顺序。

## 执行顺序

```
T1402-T01 (包骨架 + 配置)
  │
  ├── T1402-T02 (Health + Metrics)              ← 与 T03/T04 并行，依赖 T01
  │
  ├── T1402-T03 (鉴权中间件)                    ← 依赖 T01
  │       │
  │       └── T1402-T04 (路由 + 代理)           ← 依赖 T01 + T03
  │
  └── T1402-T04 (路由 + 代理)                    ← 依赖 T01 + T03
```

---

## 顺序说明

| 路径 | 说明 |
|---|---|
| T02 并行 T03/T04 | `/health` 和 `/metrics` 端点与 auth/router 解耦 |
| T04 依赖 T03 | 路由需要 auth 通过后才能代理 |

---

Sources:
- T1302: accepted execution slice order
