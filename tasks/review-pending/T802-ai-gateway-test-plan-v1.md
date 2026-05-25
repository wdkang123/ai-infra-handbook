# ai-gateway Test Plan v1

## Task ID: T802
## Task Title: ai-gateway Execution Prep Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T302 MVP 设计，准备 ai-gateway 实施前包。

---

# ai-gateway Test Plan v1

## 概述

本文档定义 ai-gateway 的测试计划，覆盖单元测试、集成测试、端到端测试。

---

## 测试分层

| 测试类型 | 覆盖范围 | Mock 程度 |
|---------|---------|----------|
| 单元测试 | Router、Auth、Rate Limit | 完全 Mock 下游 |
| 集成测试 | API 端点、中间件链 | Mock 部分下游 |
| 端到端测试 | Gateway + inference-service | 无 Mock |

---

## 单元测试

### Router

| 测试用例 | 输入 | 预期输出 |
|---------|------|---------|
| `test_route_valid_model` | `"vllm-local"` | `"http://localhost:8000/v1"` |
| `test_route_invalid_model` | `"unknown-model"` | 抛出 `ModelNotFoundError` |
| `test_route_fallback_healthy` | `"vllm-local"` | 返回主 URL |
| `test_route_fallback_unhealthy` | `"vllm-local"` | 返回 fallback URL |

### Auth Middleware

| 测试用例 | 输入 | 预期输出 |
|---------|------|---------|
| `test_auth_valid_key` | 有效 Bearer token | 通过，调用下游 |
| `test_auth_invalid_key` | 无效 token | 返回 401 |
| `test_auth_missing_header` | 无 Authorization header | 返回 401 |
| `test_auth_disabled` | auth disabled | 直接调用下游 |

### Rate Limit Middleware

| 测试用例 | 输入 | 预期输出 |
|---------|------|---------|
| `test_rate_limit_within_limit` | 第 1-60 个请求 | 通过 |
| `test_rate_limit_exceeded` | 第 61 个请求 | 返回 429 |
| `test_rate_limit_per_model` | 某 model 超出 RPM | 返回 429 |
| `test_rate_limit_disabled` | rate_limit disabled | 直接调用下游 |

### Metrics Middleware

| 测试用例 | 输入 | 预期输出 |
|---------|------|---------|
| `test_metrics_increment` | 1 个请求 | `requests_total` +1 |
| `test_metrics_track_tokens` | 带 usage 的响应 | `tokens_total` 正确累加 |
| `test_metrics_histogram` | 1 个请求 | `duration_seconds` 记录 |

---

## 集成测试

### API 端点测试

#### `POST /v1/chat/completions`

| 测试用例 | 输入 | Mock 方式 | 预期输出 |
|---------|------|----------|---------|
| `test_proxy_chat_success` | 有效请求 | Mock httpx | 200 + 透传响应 |
| `test_proxy_chat_with_auth` | 有效 token | Mock httpx | 200 + 透传响应 |
| `test_proxy_chat_no_auth` | 无 token | — | 401 |
| `test_proxy_chat_rate_limit` | 超 RPM | — | 429 |
| `test_proxy_chat_downstream_error` | 下游 500 | Mock httpx | 502 |

#### `GET /health`

| 测试用例 | 输入 | 预期输出 |
|---------|------|---------|
| `test_health_healthy` | Gateway 正常 | `{"status": "healthy"}` |

---

## 端到端测试

### 基本代理测试

```bash
# 1. 启动 inference-service（已在 T801 定义）
# inference-service serve --engine vllm --model Qwen/Qwen2.5-0.5B-Instruct &

# 2. 启动 gateway
ai-gateway serve --port 8080 &

# 3. 等待服务就绪
sleep 10

# 4. 健康检查
curl http://localhost:8080/health

# 5. 通过 gateway 请求
curl -s -X POST http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-test-key-1" \
  -d '{"model":"vllm-local","messages":[{"role":"user","content":"Hello"}]}'
```

### 预期输出

| 步骤 | 预期结果 |
|------|---------|
| 健康检查 | `{"status": "healthy"}` |
| 代理请求 | 与直接调用 inference-service 相同响应 |
| Auth 拒绝 | 无 token 请求返回 401 |
| Rate limit | 超出 RPM 返回 429 |

---

## 测试工具建议

| 工具 | 用途 | 安装 |
|------|------|------|
| `pytest` | 测试框架 | `pip install pytest pytest-asyncio` |
| `pytest-asyncio` | 异步测试 | `pip install pytest-asyncio` |
| `pytest-cov` | 覆盖率 | `pip install pytest-cov` |
| `httpx` | HTTP 客户端 | `pip install httpx` |
| `pytest-mock` | Mock 工具 | `pip install pytest-mock` |

---

## 测试覆盖率目标

| 模块 | 目标覆盖率 |
|------|----------|
| `router.py` | 95% |
| `middleware/auth.py` | 90% |
| `middleware/rate_limit.py` | 90% |
| `middleware/metrics.py` | 85% |
| `api/` | 85% |
| **总体** | **85%** |

---

Sources:
1. https://github.com/Portkey-AI/gateway — Portkey Gateway
2. https://github.com/BerriAI/litellm — LiteLLM
3. https://pytest.org/ — pytest

Risk of Staleness:
- 测试命令可能因框架版本变化

Out of Scope Kept:
- 未写压力测试
- 未写混沌测试
