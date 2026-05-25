# ai-gateway Scaffold Manifest

## Task ID: T902
## Title: ai-gateway Scaffold Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T802 repo layout、API contract（已收紧为 T812）、config surface、test plan、validation checklist，产出脚手架输入模板。

---

# ai-gateway Scaffold Manifest

## 概述

本文档定义 ai-gateway 脚手架的输入清单，包含所有待 Codex 实现的文件蓝图。

## 脚手架文件清单

| 序号 | 文件路径（蓝图） | 对应文件 | 说明 |
|------|----------------|----------|------|
| 1 | `ai-gateway/pyproject.toml` | `pyproject.toml` | 项目元数据和依赖 |
| 2 | `ai-gateway/.env.example` | `.env.example` | 环境变量模板 |
| 3 | `ai-gateway/Makefile` | `Makefile` | 构建和启动入口 |
| 4 | `ai-gateway/scripts/serve.sh` | `scripts/serve.sh` | 服务启动脚本 |
| 5 | `ai-gateway/tests/conftest.py` | `tests/conftest.py` | pytest fixture |
| 6 | `ai-gateway/tests/fixtures/` | `tests/fixtures/` | 测试请求 fixture |
| 7 | `ai-gateway/examples/curl_catalog.sh` | `examples/curl_catalog.sh` | curl 命令合集 |

## pyproject.toml 依赖组

基础依赖已在 `[project.dependencies]`，安装即包含核心运行时。

| 组名 | 依赖 | 用途 |
|------|------|------|
| `test` | pytest, pytest-asyncio, pytest-cov, httpx, pytest-mock | 测试 |
| `dev` | ruff, mypy, pre-commit | 开发工具 |

## 关键 CLI 入口

```bash
# 安装（从 ai-gateway/ 目录执行）
pip install -e "."

# 开发安装
pip install -e ".[test,dev]"

# 启动服务
ai-gateway serve --port 8080

# 运行测试
pytest tests/ -v
```

## 目录结构（蓝图）

```
ai-gateway/
├── pyproject.toml
├── .env.example
├── Makefile
├── config.yaml
├── src/
│   └── ai_gateway/
│       ├── __init__.py
│       ├── main.py          # CLI 入口
│       ├── server.py        # FastAPI app
│       ├── config.py        # 配置加载
│       ├── proxy.py         # 代理核心
│       ├── router.py        # 路由策略
│       ├── middleware/
│       │   ├── auth.py
│       │   ├── rate_limit.py
│       │   ├── metrics.py
│       │   └── logging.py
│       └── api/
│           └── chat.py
├── tests/
│   ├── conftest.py
│   ├── fixtures/
│   │   └── chat_request.json
│   └── test_router.py
├── examples/
│   └── curl_catalog.sh
└── scripts/
    └── serve.sh
```

## 服务端口约定

| 端口 | 用途 | 环境变量 |
|------|------|---------|
| `8080` | HTTP Gateway | `GATEWAY_PORT` |
| `9091` | Prometheus metrics | `METRICS_PORT` |

## 与 inference-service 的集成点

- `models[].base_url` 指向 `http://localhost:8000/v1`
- Gateway 透传 `/v1/chat/completions` 到 inference-service
- Gateway 不处理推理逻辑，只做路由/鉴权/限流

## 关键实现里程碑

| 里程碑 | 产出 | 验证 |
|--------|------|------|
| M1: 服务可启动 | Uvicorn 进程在 8080 监听 | `curl localhost:8080/health` |
| M2: 基本代理 | 请求透传到 inference-service | `examples/curl_catalog.sh` |
| M3: 鉴权 | 无 token 返回 401 | T802 validation checklist |
| M4: 限流 | 超出 RPM 返回 429 | T802 validation checklist |
| M5: Metrics | Prometheus 格式 metrics | T802 validation checklist |

---

Sources:
1. https://github.com/Portkey-AI/gateway — Portkey Gateway
2. https://github.com/BerriAI/litellm — LiteLLM
3. https://fastapi.tiangolo.com/ — FastAPI

Risk of Staleness:
- LiteLLM/Portkey 版本更新可能改变 middleware 用法

Out of Scope Kept:
- 未写多租户路由
- 未写成本感知路由
- 未写 K8s 部署
