# ai-gateway Task Pack Manifest v1

## Task ID: T1402
## Title: ai-gateway Codex Task Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# ai-gateway Task Pack Manifest

本文档索引 ai-gateway 的所有 Codex 实现任务卡。

## 任务卡清单

| Task ID | 任务名称 | 输入资产 | 目标文件 | 验证入口 |
|---|---|---|---|---|
| T1402-T01 | 包骨架 + 配置 | T1002 starter manifest | `pyproject.toml / config.py / models.yaml` | `import ai_gateway` |
| T1402-T02 | Health + Metrics 端点 | T1002 server.py blueprint + T1402-T01 | `server.py / main.py` | `/health`（含 upstream_services）+ `/metrics` 返回正确格式 |
| T1402-T03 | 鉴权中间件 | T1002 auth middleware blueprint + T1402-T01 | `middleware/auth.py` | 无 token → 401 |
| T1402-T04 | 路由 + 代理 | T1002 server.py blueprint + T1402-T03 | `router.py / server.py 修改` | 已知模型 → 200，未知 → 404 |

---

## 与 Slice 的对应关系

| Task ID | 对应 Slice |
|---|---|
| T1402-T01 | G1 |
| T1402-T02 | G4 |
| T1402-T03 | G2 |
| T1402-T04 | G3 |

---

## Cut Line

以下内容不进入当前 task pack：
- `/v1/completions`（后续扩展）
- `/v1/models`（后续扩展）
- 限流中间件 G5（后续扩展）
- 测试骨架 G6（后续扩展）

---

Sources:
- T1002: accepted starter manifest
- T1102: fixture assets
- T1302: accepted execution slice
- T302: accepted MVP design
- T812: accepted API contract
