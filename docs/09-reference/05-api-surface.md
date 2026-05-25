# API Surface 速查

这页把两个 HTTP 服务的公开接口集中到一起。

它不是完整 OpenAPI 文档，而是学习时用来快速定位：

- 哪个接口属于哪一层
- 用什么参数过滤
- 结果应该看哪些字段
- 对应代码和测试在哪里

## inference-service

inference-service 是执行层。它回答“模型服务本体是否健康、能提供哪些模型、请求如何被处理”。

| 方法 | 路径 | 用途 | 重点字段 |
| --- | --- | --- | --- |
| `GET` | `/health` | 服务健康状态 | `status`、`engine`、`model` |
| `GET` | `/v1/models` | 当前可服务模型 | `data[].id`、`metadata.engine` |
| `POST` | `/v1/chat/completions` | 普通或 streaming chat completion | `choices`、`usage`、`x-request-id` |
| `GET` | `/metrics` | Prometheus 风格指标 | request counters、token counters |
| `GET` | `/events` | 最近结构化事件 | `events`、`filters`、`limit` |
| `GET` | `/events/summary` | 事件聚合摘要 | `event_type_counts`、`requested_model_counts` |
| `GET` | `/events/requests` | request timeline 索引 | `matched_request_count`、`request_ids` |
| `GET` | `/events/requests/{request_id}` | 单 request timeline | `timeline` |

### 常用查询

```bash
curl -s http://localhost:8000/health
curl -s http://localhost:8000/v1/models
curl -s 'http://localhost:8000/events?event_type=request_success'
curl -s 'http://localhost:8000/events/summary?requested_model=Qwen/Qwen2.5-0.5B-Instruct'
curl -s 'http://localhost:8000/events/requests?requested_model=Qwen/Qwen2.5-0.5B-Instruct'
curl -s 'http://localhost:8000/events/requests/req_demo_direct_1'
```

### 代码入口

- `projects/inference-service/src/inference_service/server.py`
- `projects/inference-service/src/inference_service/runtime.py`
- `projects/inference-service/src/inference_service/engines.py`
- `projects/inference-service/tests/test_api.py`

## ai-gateway

ai-gateway 是治理层。它回答“请求如何被鉴权、路由、限流、缓存、fallback 和观测”。

| 方法 | 路径 | 用途 | 重点字段 |
| --- | --- | --- | --- |
| `GET` | `/health` | gateway 与 upstream 健康状态 | `status`、`upstream_services` |
| `GET` | `/v1/models` | 平台模型列表 | `metadata.target_model`、`metadata.fallback_count`、`metadata.upstream_health` |
| `POST` | `/v1/chat/completions` | 鉴权后代理到下游模型服务 | `x-request-id`、`x-upstream-model`、`x-fallback-used`、`x-cache` |
| `GET` | `/metrics` | gateway 指标 | fallback、cache、upstream failure counters |
| `GET` | `/events` | 最近结构化事件 | `events`、`filters`、`limit` |
| `GET` | `/events/summary` | 事件聚合摘要 | `event_type_counts`、`upstream_model_counts` |
| `GET` | `/events/failures` | 失败摘要 | `status_code_counts`、`failed_upstream_model_counts` |
| `GET` | `/events/requests` | request timeline 索引 | `matched_request_count`、`event_types`、`upstream_models` |
| `GET` | `/events/requests/{request_id}` | 单 request timeline | `timeline` |

### 常用查询

```bash
curl -s http://localhost:8080/health
curl -s http://localhost:8080/v1/models
curl -s 'http://localhost:8080/events?event_type=request_success&upstream_model=vllm-local'
curl -s 'http://localhost:8080/events/summary?requested_model=vllm-local'
curl -s 'http://localhost:8080/events/failures'
curl -s 'http://localhost:8080/events/requests?requested_model=vllm-local&upstream_model=vllm-local'
curl -s 'http://localhost:8080/events/requests/req_demo_gateway_1'
```

### 代码入口

- `projects/ai-gateway/src/ai_gateway/server.py`
- `projects/ai-gateway/src/ai_gateway/router.py`
- `projects/ai-gateway/src/ai_gateway/runtime.py`
- `projects/ai-gateway/src/ai_gateway/middleware/auth.py`
- `projects/ai-gateway/tests/test_proxy.py`

## 错误语义

| 状态码 | 更可能的系统层 | 典型原因 |
| --- | --- | --- |
| `401` | gateway 鉴权 | 缺少 Bearer token、token 格式错误 |
| `404` | gateway 路由或 inference 模型校验 | 外部模型名不存在、请求模型不等于服务模型 |
| `422` | inference 请求校验 | `messages` 为空 |
| `429` | gateway 限流 | 调用方超过最小限流预算 |
| `502` | gateway 到 upstream 或 inference engine | 下游失败、所有 fallback 失败、engine adapter 报错 |

## 调试顺序

建议按这个顺序排查：

1. 看 response status 和 headers
2. 用 `x-request-id` 查 gateway timeline
3. 用同一个 request id 查 inference timeline
4. 看 gateway `/events/failures`
5. 看 `/metrics` 判断是否是单点还是趋势
6. 回到对应代码和测试

对应案例：[请求失败排查案例](/11-case-studies/01-request-incident-walkthrough)。
