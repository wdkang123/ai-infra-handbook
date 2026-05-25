# ai-gateway Middleware Map v1

## Task ID: T802
## Task Title: ai-gateway Execution Prep Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T302 MVP 设计，准备 ai-gateway 实施前包。

---

# ai-gateway Middleware Map v1

## 概述

本文档定义 ai-gateway 的中间件组件及执行顺序。

---

## 中间件执行顺序

```
请求进入
    ↓
1. Logging Middleware（请求日志）
    ↓
2. Auth Middleware（鉴权）
    ↓
3. Rate Limit Middleware（限流）
    ↓
4. Metrics Middleware（计量）
    ↓
    ↓
5. 路由到下游
    ↓
6. Metrics Middleware（响应后）
    ↓
7. 响应返回
```

---

## 1. Logging Middleware

### 功能

- 记录请求开始时间、结束时间
- 记录请求方法、路径、model 参数
- 记录响应状态码
- 记录下游耗时

### 实现位置

`middleware/logging.py`

### 日志格式

```json
{
  "timestamp": "2026-04-03T12:00:00Z",
  "request_id": "req-xxx",
  "method": "POST",
  "path": "/v1/chat/completions",
  "model": "vllm-local",
  "status_code": 200,
  "duration_ms": 150,
  "upstream_duration_ms": 120
}
```

---

## 2. Auth Middleware

### 功能

- 验证 `Authorization` header
- 支持 `Bearer <api_key>` 格式
- API Key 存储在 config 或环境变量

### 实现位置

`middleware/auth.py`

### 配置项

| 配置项 | 说明 |
|--------|------|
| `auth.enabled` | 是否启用鉴权 |
| `auth.type` | `api_key`（MVP） |
| `auth.api_keys` | 有效 API Key 列表 |

### 错误响应

```json
{
  "error": {
    "message": "Invalid API key",
    "type": "authentication_error",
    "code": 401
  }
}
```

---

## 3. Rate Limit Middleware

### 功能

- 按 model 限流
- 支持 RPM（Requests Per Minute）
- 支持令牌桶或滑动窗口算法

### 实现位置

`middleware/rate_limit.py`

### 配置项

| 配置项 | 说明 |
|--------|------|
| `rate_limit.enabled` | 是否启用限流 |
| `rate_limit.default_rpm` | 默认 RPM |
| `rate_limit.per_model_rpm` | per-model RPM |

### 算法选择

| 算法 | 优点 | 缺点 | MVP 选择 |
|------|------|------|---------|
| 令牌桶 | 允许突发 | 实现复杂 | 备选 |
| 滑动窗口 | 实现简单 | 边界突发 | **推荐** |
| 固定窗口 | 最简单 | 边界突发严重 | 初始 |

### 错误响应

```json
{
  "error": {
    "message": "Rate limit exceeded",
    "type": "rate_limit_error",
    "code": 429
  }
}
```

### 响应头

```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1712140800
```

---

## 4. Metrics Middleware

### 功能

- 统计每个 model 的请求数
- 统计请求延迟直方图
- 统计 token 用量（prompt_tokens + completion_tokens）

### 实现位置

`middleware/metrics.py`

### 指标定义

| 指标名 | 类型 | 标签 | 说明 |
|--------|------|------|------|
| `ai_gateway_requests_total` | Counter | model, status | 总请求数 |
| `ai_gateway_request_duration_seconds` | Histogram | model | 请求延迟 |
| `ai_gateway_tokens_total` | Counter | model | 总 token 数 |
| `ai_gateway_tokens_prompt` | Counter | model | prompt token 数 |
| `ai_gateway_tokens_completion` | Counter | model | completion token 数 |

### Token 计量方式

```python
# 从下游响应中提取 usage
usage = response.json().get("usage", {})
prompt_tokens = usage.get("prompt_tokens", 0)
completion_tokens = usage.get("completion_tokens", 0)
```

---

## 5. Router（中间件之后）

### 功能

- 根据 `model` 参数匹配下游 URL
- 处理下游不可用时的 fallback

### 实现位置

`router.py`

### 路由匹配逻辑

```python
def route(model: str) -> str:
    if model in model_registry:
        return model_registry[model].base_url
    raise ModelNotFoundError(model)

def route_with_fallback(model: str) -> str:
    primary = route(model)
    if is_healthy(primary):
        return primary
    # fallback 逻辑
```

---

## Middleware 配置模板

```yaml
middleware:
  logging:
    enabled: true
    level: "INFO"

  auth:
    enabled: true
    type: "api_key"
    api_keys:
      - "dev-gateway-key-1"
      - "dev-gateway-key-2"

  rate_limit:
    enabled: true
    algorithm: "sliding_window"
    default_rpm: 60
    per_model_rpm:
      "openai-gpt4": 30
      "vllm-local": 120

  metrics:
    enabled: true
    track_tokens: true
```

---

Sources:
1. https://github.com/Portkey-AI/gateway — Portkey Gateway
2. https://github.com/BerriAI/litellm — LiteLLM
3. https://github.com/APIParkLab/APIPark — APIPark

Risk of Staleness:
- 开源 gateway 中间件实现可能有变化

Out of Scope Kept:
- 未写 JWT 鉴权
- 未写多租户隔离
- 未写成本计量
