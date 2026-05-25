# inference-service Task Order v1

## Task ID: T1401
## Title: inference-service Codex Task Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# inference-service Task Order

本文档定义 inference-service 的任务执行顺序。

## 执行顺序

```
T1401-T01 (包骨架 + 配置)
  │
  └── T1401-T02 (FastAPI 骨架)
```

---

## 顺序说明

| 路径 | 说明 |
|---|---|
| T1401-T01 → T1401-T02 | T01 提供 config.py，T02 的 server.py 需要 import config |

---

Sources:
- T1301: accepted execution slice order
