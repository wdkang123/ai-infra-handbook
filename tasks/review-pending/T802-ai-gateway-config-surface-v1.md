# ai-gateway Config Surface v1

## Task ID: T802
## Task Title: ai-gateway Execution Prep Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T302 MVP 设计，准备 ai-gateway 实施前包。

---

# ai-gateway Config Surface v1

## 概述

本文档定义 ai-gateway 的配置项清单，对应 `config.yaml` 和环境变量。

---

## 配置项总览

| 配置类 | 配置项数 | MVP 必须 |
|--------|---------|---------|
| Server | 4 | 4 |
| Models | 3 | 3 |
| Auth | 3 | 2 |
| Rate Limit | 4 | 3 |
| Metrics | 2 | 2 |
| Logging | 2 | 2 |
| **合计** | **18** | **16** |

---

## Server 配置

| 配置项 | 环境变量 | 默认值 | 说明 | MVP 必须 |
|--------|---------|-------|------|---------|
| `server.host` | `GATEWAY_HOST` | `0.0.0.0` | 服务监听地址 | 是 |
| `server.port` | `GATEWAY_PORT` | `8080` | 服务监听端口 | 是 |
| `server.timeout` | `GATEWAY_TIMEOUT` | `300` | 请求超时（秒） | 是 |
| `server.workers` | `GATEWAY_WORKERS` | `1` | Uvicorn 工作进程数 | 是 |

---

## Models 配置

| 配置项 | 环境变量 | 默认值 | 说明 | MVP 必须 |
|--------|---------|-------|------|---------|
| `models[].name` | — | — | 模型名称（路由 key） | 是 |
| `models[].base_url` | — | — | 下游 API base URL | 是 |
| `models[].api_key` | — | — | 下游 API Key（如需要） | 否 |

### 配置示例

```yaml
models:
  - name: "vllm-local"
    base_url: "http://localhost:8000/v1"
    api_key: ""  # 本地无需 key
  - name: "openai-gpt4"
    base_url: "https://api.openai.com/v1"
    api_key: "${OPENAI_API_KEY}"
```

---

## Auth 配置

| 配置项 | 环境变量 | 默认值 | 说明 | MVP 必须 |
|--------|---------|-------|------|---------|
| `auth.enabled` | `AUTH_ENABLED` | `true` | 是否启用鉴权 | 是 |
| `auth.type` | `AUTH_TYPE` | `api_key` | 鉴权类型（api_key/jwt） | 否（MVP api_key） |
| `auth.api_keys` | — | `[]` | 有效 API Key 列表 | 是 |

---

## Rate Limit 配置

| 配置项 | 环境变量 | 默认值 | 说明 | MVP 必须 |
|--------|---------|-------|------|---------|
| `rate_limit.enabled` | `RATE_LIMIT_ENABLED` | `true` | 是否启用限流 | 是 |
| `rate_limit.algorithm` | `RATE_LIMIT_ALGORITHM` | `sliding_window` | 限流算法 | 否 |
| `rate_limit.default_rpm` | `DEFAULT_RPM` | `60` | 默认 RPM | 是 |
| `rate_limit.per_model_rpm` | — | `{}` | per-model RPM 覆盖 | 否 |

### 配置示例

```yaml
rate_limit:
  enabled: true
  algorithm: "sliding_window"
  default_rpm: 60
  per_model_rpm:
    "openai-gpt4": 30
    "vllm-local": 120
```

---

## Metrics 配置

| 配置项 | 环境变量 | 默认值 | 说明 | MVP 必须 |
|--------|---------|-------|------|---------|
| `metrics.enabled` | `METRICS_ENABLED` | `true` | 是否启用 metrics | 是 |
| `metrics.port` | `METRICS_PORT` | `9090` | Metrics 端口 | 是 |

---

## Logging 配置

| 配置项 | 环境变量 | 默认值 | 说明 | MVP 必须 |
|--------|---------|-------|------|---------|
| `logging.enabled` | `LOGGING_ENABLED` | `true` | 是否启用日志 | 是 |
| `logging.level` | `LOGGING_LEVEL` | `INFO` | 日志级别 | 是 |

---

## 配置加载优先级

```
CLI 参数 > 环境变量 > config.yaml > 默认值
```

---

## config.yaml 示例

```yaml
server:
  host: "0.0.0.0"
  port: 8080
  timeout: 300
  workers: 1

models:
  - name: "vllm-local"
    base_url: "http://localhost:8000/v1"
    api_key: ""
  - name: "openai-gpt4"
    base_url: "https://api.openai.com/v1"
    api_key: "${OPENAI_API_KEY}"

auth:
  enabled: true
  type: "api_key"
  api_keys:
    - "sk-test-key-1"
    - "sk-test-key-2"

rate_limit:
  enabled: true
  algorithm: "sliding_window"
  default_rpm: 60
  per_model_rpm:
    "openai-gpt4": 30
    "vllm-local": 120

metrics:
  enabled: true
  port: 9090

logging:
  enabled: true
  level: "INFO"
```

---

Sources:
1. https://github.com/Portkey-AI/gateway — Portkey Gateway
2. https://github.com/BerriAI/litellm — LiteLLM

Risk of Staleness:
- 开源 gateway 配置项可能随版本变化

Out of Scope Kept:
- 未写多租户配置
- 未写成本配置
