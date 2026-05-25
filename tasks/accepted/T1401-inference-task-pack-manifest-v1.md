# inference-service Task Pack Manifest v1

## Task ID: T1401
## Title: inference-service Codex Task Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# inference-service Task Pack Manifest

本文档索引 inference-service 的所有 Codex 实现任务卡，供 Codex 执行时参照。

## 任务卡清单

| Task ID | 任务名称 | 输入资产 | 目标文件 | 验证入口 |
|---|---|---|---|---|
| T1401-T01 | 包骨架 + 配置 | T1001 starter manifest | `pyproject.toml / config.py / config.yaml / config.local.yaml / config.smoke.yaml` | `import inference_service` |
| T1401-T02 | FastAPI 骨架 | T1001 server.py blueprint + T1401-T01 | `server.py / main.py` | `curl localhost:8000/health` |

---

## 与 Slice 的对应关系

| Task ID | 对应 Slice |
|---|---|
| T1401-T01 | S1 |
| T1401-T02 | S2 |

---

## Cut Line

以下内容不进入当前 task pack：
- `/v1/completions`（后续扩展）
- `/v1/models`（后续扩展）
- vLLM Engine 集成（S3）
- 流式输出（S4）
- Prometheus Metrics（S5）
- 测试骨架（S6）

---

Sources:
- T1001: accepted starter manifest
- T1101: fixture assets
- T1301: accepted execution slice
- T301: accepted MVP design
- T811: accepted API contract
