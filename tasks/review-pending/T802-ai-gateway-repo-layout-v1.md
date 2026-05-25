# ai-gateway Repo Layout v1

## Task ID: T802
## Task Title: ai-gateway Execution Prep Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T302 MVP 设计，准备 ai-gateway 实施前包。

---

# ai-gateway Repo Layout v1

## 概述

本文档定义 ai-gateway 模块的完整目录结构，对应 MVP 实施需求。

---

## 顶层结构

```
ai-gateway/
├── README.md
├── pyproject.toml
├── config.yaml
├── .env.example
├── src/
│   └── ai_gateway/
│       ├── __init__.py
│       ├── main.py
│       ├── proxy.py
│       ├── router.py
│       ├── config.py
│       ├── middleware/
│       │   ├── __init__.py
│       │   ├── auth.py
│       │   ├── rate_limit.py
│       │   ├── metrics.py
│       │   └── logging.py
│       ├── models/
│       │   ├── __init__.py
│       │   └── model_registry.py
│       └── api/
│           ├── __init__.py
│           ├── chat.py
│           ├── completions.py
│           └── models.py
├── tests/
│   ├── __init__.py
│   ├── test_router.py
│   ├── test_middleware.py
│   └── test_integration.py
├── examples/
│   └── quickstart.py
└── scripts/
    └── serve.sh
```

---

## 目录说明

### `src/ai_gateway/`

| 文件 | 说明 |
|------|------|
| `__init__.py` | 包初始化 |
| `main.py` | CLI 入口，`ai-gateway` 命令定义 |
| `proxy.py` | HTTP 代理核心，请求转发 |
| `router.py` | 路由策略，根据 model 路由到下游 |
| `config.py` | 配置加载（YAML + 环境变量） |
| `middleware/` | 中间件目录 |
| `models/` | 下游模型配置管理 |
| `api/` | 代理 API 路由 |

### `middleware/`

| 文件 | 说明 |
|------|------|
| `auth.py` | API 密钥验证 |
| `rate_limit.py` | 限流（令牌桶/滑动窗口） |
| `metrics.py` | 请求计量（token 计数） |
| `logging.py` | 请求日志 |

### `api/`

| 文件 | 说明 |
|------|------|
| `chat.py` | `POST /v1/chat/completions` 代理 |
| `completions.py` | `POST /v1/completions` 代理 |
| `models.py` | `GET /v1/models` 代理 |

### `tests/`

| 文件 | 说明 |
|------|------|
| `test_router.py` | 路由逻辑单元测试 |
| `test_middleware.py` | 中间件单元测试 |
| `test_integration.py` | 端到端集成测试 |

---

## 关键文件内容概要

### `pyproject.toml`

```toml
[project]
name = "ai-gateway"
version = "0.1.0"
requires-python = ">=3.10"

dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.30.0",
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
    "pyyaml>=6.0",
    "httpx>=0.27.0",
    "prometheus-client>=0.20.0",
    "python-jose[cryptography]>=3.3.0",
    "slowapi>=0.1.9",
]
```

### `config.yaml`

```yaml
server:
  host: "0.0.0.0"
  port: 8080
  timeout: 300

models:
  - name: "vllm-local"
    base_url: "http://localhost:8000/v1"
    api_key: ""  # 本地无需 key
  - name: "openai-gpt4"
    base_url: "https://api.openai.com/v1"
    api_key: "${OPENAI_API_KEY}"

auth:
  enabled: true
  type: "api_key"  # api_key | jwt

rate_limit:
  enabled: true
  default_rpm: 60
  per_model_rpm:
    "openai-gpt4": 30
    "vllm-local": 120

metrics:
  enabled: true
  port: 9090
```

### `.env.example`

```bash
# Gateway 配置
GATEWAY_HOST=0.0.0.0
GATEWAY_PORT=8080

# 外部 API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Auth 配置
AUTH_ENABLED=true
AUTH_TYPE=api_key

# Rate Limit 配置
RATE_LIMIT_ENABLED=true
DEFAULT_RPM=60
```

---

## 与 MVP 设计（T302）的差异

| 维度 | T302 MVP | T802（本版） |
|------|---------|-------------|
| Middleware 分离 | 提到有 middleware | 独立 `middleware/` 目录 |
| Config 分离 | 提到有 config | 独立 `config.yaml` |
| 环境变量 | 未提 | 独立 `.env.example` |
| 测试 | 未提 | 新增 `tests/` |
| Scripts | 未提 | 新增 `scripts/serve.sh` |

---

Sources:
1. https://github.com/Portkey-AI/gateway — Portkey Gateway
2. https://github.com/BerriAI/litellm — LiteLLM

Risk of Staleness:
- 目录结构可能随项目规模调整

Out of Scope Kept:
- 未写 Dockerfile
- 未写 docker-compose
