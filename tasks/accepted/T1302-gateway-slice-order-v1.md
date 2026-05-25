# ai-gateway Slice Order v1

## Task ID: T1302
## Title: ai-gateway Execution Slice Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# ai-gateway Execution Slice Order

本文档定义 ai-gateway 的 slice 执行顺序与依赖关系。

## Slice 执行顺序

```
G1 (包骨架 + 配置)
  │
  ├── G2 (鉴权中间件)              ← 独立开发，依赖 G1 的 config
  │       │
  │       └── G3 (路由 + 代理)     ← 依赖 G2 auth + G1 config
  │
  ├── G4 (Health + Metrics)         ← 与 G2/G3 并行，依赖 G1
  │
  └── G5 (限流中间件)               ← 与 G2/G3/G4 并行，依赖 G1
          │
          └── G6 (测试骨架)         ← 依赖 G3 完成后
```

---

## 关键依赖说明

| 依赖路径 | 说明 |
|---|---|
| G2 依赖 G1 | G1 的 config.py 定义配置结构，G2 的 `verify_bearer_token()` 需要 api_keys |
| G3 依赖 G2 | G3 的 router 需要 G2 的 auth 通过后才能路由 |
| G4 并行 G1 | `/health` 和 `/metrics` 端点与 auth/router 解耦 |
| G5 并行 G2 | 限流中间件独立于 auth 逻辑 |
| G6 依赖 G3 | 测试需要真实路由逻辑完成 |

---

## 与 inference-service 依赖

| Slice | 对 inference-service 的依赖 |
|---|---|
| G1 | 无 |
| G2 | 无 |
| G3 | **需要 inference-service 运行**才能端到端验证 |
| G4 | 无 |
| G5 | 无（可用 mock 测试） |
| G6 | 需要 mock downstream |

---

Sources:
- T1002: accepted starter manifest
- T1202: accepted implementation map
- T812: accepted API contract
