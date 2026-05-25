# ai-gateway .env.example Blueprint v1

## Task ID: T902
## Title: ai-gateway Scaffold Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T802 config surface，产出 .env.example 模板。

---

# ai-gateway .env.example Blueprint v1

## 概述

本文档定义 ai-gateway 的 `.env.example` 模板。

## 模板全文

```bash
# ============================================================
# ai-gateway — .env.example
# ============================================================

# ---------- Server ----------
GATEWAY_HOST=0.0.0.0
GATEWAY_PORT=8080
GATEWAY_TIMEOUT=300
GATEWAY_WORKERS=1

# ---------- Models / Routing ----------
# 下游模型配置（YAML config.yaml 中定义，env 可覆盖 base_url）
# INFERENCE_BASE_URL=http://localhost:8000/v1

# ---------- Auth ----------
# 是否启用 API Key 鉴权
AUTH_ENABLED=true
AUTH_TYPE=api_key  # api_key | jwt

# 有效 API Keys（逗号分隔，或在 config.yaml 中列表定义）
# API_KEYS=dev-gateway-key-1,dev-gateway-key-2

# JWT 密钥（如果 AUTH_TYPE=jwt）
# JWT_SECRET=your-secret-key-here
# JWT_ALGORITHM=HS256

# ---------- Rate Limit ----------
# 是否启用限流
RATE_LIMIT_ENABLED=true
RATE_LIMIT_ALGORITHM=sliding_window  # sliding_window | fixed_window | token_bucket
DEFAULT_RPM=60
# Per-model RPM 覆盖（在 config.yaml 中定义

# ---------- Metrics ----------
METRICS_ENABLED=true
METRICS_PORT=9091

# ---------- Logging ----------
LOGGING_ENABLED=true
LOGGING_LEVEL=INFO  # DEBUG | INFO | WARNING | ERROR

# ---------- External API Keys ----------
OPENAI_API_KEY=replace-with-openai-api-key
ANTHROPIC_API_KEY=replace-with-anthropic-api-key
```

## 字段优先级

```
CLI 参数 > 环境变量 > .env 文件 > config.yaml > 默认值
```

## 最小必须字段（MVP）

```bash
# MVP 最简配置：
AUTH_ENABLED=true
# API keys 在 config.yaml 中定义（更安全）
```

## 生产环境建议

| 字段 | 开发环境 | 生产环境 |
|------|---------|---------|
| `AUTH_ENABLED` | false（方便调试） | true |
| `LOGGING_LEVEL` | DEBUG | INFO |
| `GATEWAY_WORKERS` | 1 | >=2 |

---

Sources:
1. https://github.com/Portkey-AI/gateway — Portkey Gateway
2. https://github.com/laurentS/slowapi — Slowapi

Risk of Staleness:
- Slowapi 版本更新可能改变环境变量用法

Out of Scope Kept:
- 未写多租户 API Key 隔离
- 未写 Key 轮换机制
