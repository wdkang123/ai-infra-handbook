# inference-service Slice Order v1

## Task ID: T1301
## Title: inference-service Execution Slice Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# inference-service Execution Slice Order

本文档定义 inference-service 的 slice 执行顺序与依赖关系。

## Slice 执行顺序

```
S1 (包骨架 + 配置)
  │
  └── S2 (FastAPI 骨架)
          │
          ├── S3 (vLLM Engine)              ← S2 的 /v1/chat/completions 用 mock
          │       │
          │       └── S4 (流式输出)         ← 依赖 S3 的 predict_stream
          │
          ├── S5 (Prometheus Metrics)       ← 与 S3/S4 并行，独立端点
          │
          └── S6 (测试骨架)                 ← 依赖 S2 骨架完整
```

---

## 关键依赖说明

| 依赖路径 | 说明 |
|---|---|
| S2 依赖 S1 | S1 提供 config.py，S2 的 server.py 需 import config |
| S3 依赖 S2 | S2 的 server.py 需要 S3 的 engine 实例注入 |
| S4 依赖 S3 | S4 依赖 S3 的 `predict_stream()` 方法实现 |
| S5 并行 S2 | `/metrics` 端点与 engine 无关，可独立开发 |
| S6 依赖 S2 | 测试需要 app fixture，依赖 S2 的 server.py |

---

## GPU 资源说明

| Slice | GPU 需求 | 说明 |
|---|---|---|
| S1 | 否 | 仅 Python 包，无外部依赖 |
| S2 | 否 | FastAPI mock 响应 |
| S3 | **是** | vLLM LLM 加载需要 GPU |
| S4 | 是 | 依赖 S3 的流式生成器 |
| S5 | 否 | Prometheus metrics 聚合 |
| S6 | 否 | pytest 测试可 mock engine |

**建议：** S1 → S2 → S5 → S6 可在 CPU 环境完成，S3/S4 需 GPU。

---

Sources:
- T1001: accepted starter manifest
- T1201: accepted implementation map
- T811: accepted API contract
