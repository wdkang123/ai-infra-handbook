# ai-gateway Starter File Manifest

## Task ID: T1002
## Title: ai-gateway Starter File Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T902 scaffold blueprints（T902 pyproject / run-script / test-fixture / curl catalog），产出 ai-gateway 源码蓝图文件。

---

# ai-gateway Starter File Manifest

## 概述

本文档索引 ai-gateway 的所有 starter file 蓝图，供 Codex 实施时参照。

## 蓝图文件清单

| 序号 | 文件路径（蓝图） | 对应真实文件 | 说明 |
|------|----------------|-------------|------|
| 1 | `T1002-ai-gateway-main-py-blueprint-v1.md` | `src/ai_gateway/main.py` | CLI 入口（Typer） |
| 2 | `T1002-ai-gateway-server-py-blueprint-v1.md` | `src/ai_gateway/server.py` | FastAPI 服务 |
| 3 | `T1002-ai-gateway-config-py-blueprint-v1.md` | `src/ai_gateway/config.py` | 配置加载 |
| 4 | `T1002-ai-gateway-auth-middleware-blueprint-v1.md` | `src/ai_gateway/middleware/auth.py` | 鉴权中间件 |
| 5 | `T1002-ai-gateway-conftest-py-blueprint-v1.md` | `tests/conftest.py` | pytest fixtures |
| 6 | `T1002-ai-gateway-test-proxy-py-blueprint-v1.md` | `tests/test_proxy.py` | 代理/路由测试 |
| 7 | (from T902 scaffold) | `scripts/serve.sh` | 启动脚本（沿用 T902 run-script blueprint） |

## 源码目录结构（蓝图）

```
ai-gateway/
├── src/
│   └── ai_gateway/
│       ├── __init__.py
│       ├── main.py          # CLI 入口（Typer）
│       ├── server.py        # FastAPI 服务
│       ├── config.py        # 配置加载
│       ├── router.py       # 下游路由
│       ├── middleware/
│       │   ├── __init__.py
│       │   ├── auth.py     # API Key 鉴权
│       │   └── rate_limit.py # 限流
│       └── models.py       # Pydantic models
├── tests/
│   ├── conftest.py
│   ├── fixtures/
│   │   ├── chat_request_valid.json
│   │   └── chat_request_no_auth.json
│   └── test_proxy.py
├── scripts/
│   └── serve.sh
├── pyproject.toml
├── .env.example
└── config.yaml
```

## MVP 必须功能

| 功能 | 说明 |
|------|------|
| 路由 | 代理 /v1/chat/completions 到下游 inference-service |
| 鉴权 | Bearer token 验证 |
| 限流 | sliding_window RPM 限制 |
| 观测 | /health, /metrics |

## 与 inference-service 集成

- ai-gateway 作为上游，代理请求到 `http://localhost:8000/v1`
- 路由模型名称映射（gateway `vllm-local` → `http://localhost:8000/v1`）

---

Sources:
1. https://github.com/Portkey-AI/gateway — Portkey Gateway
2. https://github.com/laurentS/slowapi — Slowapi

Risk of Staleness:
- 中间件实现细节可能因库版本变化

Out of Scope Kept:
- 未写多租户隔离
- 未写成本计算
