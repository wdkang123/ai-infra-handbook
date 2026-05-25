# ai-gateway Slice Manifest v1

## Task ID: T1302
## Title: ai-gateway Execution Slice Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# ai-gateway Execution Slice Manifest

本文档索引 ai-gateway 的所有 execution slices，供 Codex 编码时参照。

## Slice 总览

| Slice ID | 名称 | 目标文件 | 验证入口 | 前置条件 |
|---|---|---|---|---|
| G1 | 包骨架 + 配置 | `pyproject.toml / config.py / models.yaml` | `import ai_gateway` | 无 |
| G2 | 鉴权中间件 | `middleware/auth.py` | 无 token → 401，有 token → 通过 | G1 |
| G3 | 路由 + 代理 | `router.py / server.py` | 未知模型 → 404，已知模型 → 200 | G2 + G1 |
| G4 | Health + Metrics | `server.py` | `/health` + `/metrics` 返回正确格式 | G1 |
| G5 | 限流中间件 | `middleware/rate_limit.py` | 超出 60/min → 429 | G2 |
| G6 | 测试骨架 | `tests/conftest.py / tests/test_proxy.py` | `pytest tests/` | G3 |

---

## Slice 覆盖范围

| 主线 | 覆盖 Slice |
|---|---|
| 配置层 | G1 |
| 鉴权 | G2 |
| 路由 + 代理 | G3 |
| Health + Metrics | G4 |
| 限流 | G5 |
| 测试 | G6 |

---

## Cut Line

以下内容不进入当前 slice 集合：
- `/v1/completions`（后续扩展）
- `/v1/models`（后续扩展）
- 成本感知路由
- Semantic Cache
- 多租户认证

---

Sources:
- T1002: accepted starter manifest
- T1102: fixture assets
- T302: accepted MVP design
- T812: accepted API contract
- T1202: accepted implementation map

Risk of Staleness:
- auth/routing 逻辑相对稳定，API 契约以 T812 为准
