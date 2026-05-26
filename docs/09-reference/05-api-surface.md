# API Surface 速查

这页把两个 HTTP 服务的公开接口集中到一起。

它不是完整 OpenAPI 文档，而是学习时用来快速定位：

- 哪个接口属于哪一层
- 正常响应应该看哪些字段
- 错误响应更可能来自哪里
- 哪些 headers 可以帮助排障
- 对应代码和测试在哪里

如果你正在调试请求链路，这一页应该和 [常见排障手册](/09-reference/04-troubleshooting)、[示例输出与证据库](/13-output-gallery/00-overview) 一起看。

## API Surface 怎么读

不要把接口只看成 URL 列表。每个接口都应该回答 4 个问题：

1. 它属于哪一层？
2. 它证明系统的哪个能力存在？
3. 它失败时说明什么？
4. 它的输出能否进入复盘证据？

例如 `/health` 不只是“看服务活不活”。在 gateway 层，它还可以表达 upstream 是否健康；在 inference 层，它表达模型服务本体是否可用。

## inference-service

inference-service 是执行层。

它回答：

> 模型服务本体是否健康、能提供哪些模型、请求如何被处理、执行过程是否可观察？

### 接口列表

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

### 最小查询

```bash
curl -s http://localhost:8000/health
curl -s http://localhost:8000/v1/models
curl -s http://localhost:8000/metrics
```

这三条可以快速判断 inference-service 是否可用、模型名是否暴露、指标是否存在。

### Chat completion 查询

普通请求重点看：

- response id
- `choices`
- `usage`
- `x-request-id`
- status code

Streaming 请求重点看：

- chunk 是否持续产生
- error event 如何表达
- metrics 是否记录 streaming path
- request timeline 是否完整

### Events 查询

```bash
curl -s 'http://localhost:8000/events?event_type=request_success'
curl -s 'http://localhost:8000/events/summary?requested_model=Qwen/Qwen2.5-0.5B-Instruct'
curl -s 'http://localhost:8000/events/requests?requested_model=Qwen/Qwen2.5-0.5B-Instruct'
curl -s 'http://localhost:8000/events/requests/req_demo_direct_1'
```

Events 的学习价值是让你看到一次请求不仅有响应，还有可复盘的结构化轨迹。

### 代码入口

- `projects/inference-service/src/inference_service/server.py`
- `projects/inference-service/src/inference_service/runtime.py`
- `projects/inference-service/src/inference_service/engines.py`
- `projects/inference-service/tests/test_api.py`

### 常见判断

| 现象 | 更可能说明 |
| --- | --- |
| `/health` 失败 | 服务没启动或进程异常 |
| `/v1/models` 没有目标模型 | 模型配置或服务启动参数不符合预期 |
| chat completion 返回 `422` | 请求 schema 不满足要求，例如 messages 为空 |
| chat completion 返回 `502` | engine adapter 或 upstream 执行失败 |
| `/metrics` 没有请求变化 | 请求可能没有打到这个服务，或路径被 gateway 拦截 |
| timeline 为空 | request id 不一致，或事件没有被记录 |

## ai-gateway

ai-gateway 是治理层。

它回答：

> 请求如何被鉴权、路由、限流、缓存、fallback 和观测？

### 接口列表

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

### 最小查询

```bash
curl -s http://localhost:8080/health
curl -s http://localhost:8080/v1/models
curl -s http://localhost:8080/metrics
```

这三条可以快速判断 gateway 自己是否可用、它认识哪些模型、平台指标是否存在。

### Chat completion Headers

Gateway 请求最值得看 headers：

| Header | 含义 |
| --- | --- |
| `x-request-id` | 跨层排查的主线 |
| `x-upstream-model` | 最终命中的内部目标 |
| `x-fallback-used` | 是否发生 fallback |
| `x-cache` | response cache 是否命中 |

这些字段比响应文本更适合做系统复盘。

### Events 查询

```bash
curl -s 'http://localhost:8080/events?event_type=request_success&upstream_model=vllm-local'
curl -s 'http://localhost:8080/events/summary?requested_model=vllm-local'
curl -s 'http://localhost:8080/events/failures'
curl -s 'http://localhost:8080/events/requests?requested_model=vllm-local&upstream_model=vllm-local'
curl -s 'http://localhost:8080/events/requests/req_demo_gateway_1'
```

Gateway events 可以帮助你回答：

- 请求是否通过鉴权
- 路由到了哪个 upstream
- 是否发生 fallback
- cache 是否命中
- 失败 status 如何分布

### 代码入口

- `projects/ai-gateway/src/ai_gateway/server.py`
- `projects/ai-gateway/src/ai_gateway/router.py`
- `projects/ai-gateway/src/ai_gateway/runtime.py`
- `projects/ai-gateway/src/ai_gateway/middleware/auth.py`
- `projects/ai-gateway/tests/test_proxy.py`

### 常见判断

| 现象 | 更可能说明 |
| --- | --- |
| `401` | 缺少 Bearer token 或 token 格式错误 |
| `404` | 外部模型名不存在，或路由目标不匹配 |
| `429` | 调用方超过限流预算 |
| `502` | upstream failure、fallback failure 或下游不可达 |
| `x-cache: HIT` | response cache 命中 |
| `x-fallback-used: true` | 主路径失败后使用了备用目标 |
| `/events/failures` 增加 | 平台层记录了失败事件 |

## 错误语义

| 状态码 | 更可能的系统层 | 典型原因 | 下一步 |
| --- | --- | --- | --- |
| `401` | gateway 鉴权 | 缺少 Bearer token、token 格式错误 | 检查 Authorization header |
| `404` | gateway 路由或 inference 模型校验 | 外部模型名不存在、请求模型不等于服务模型 | 查 `/v1/models` 和 route config |
| `422` | inference 请求校验 | `messages` 为空或请求结构不合法 | 检查请求 body |
| `429` | gateway 限流 | 调用方超过最小限流预算 | 检查 token、rate limit 配置和 metrics |
| `502` | gateway 到 upstream 或 inference engine | 下游失败、所有 fallback 失败、engine adapter 报错 | 查 request timeline、failures、upstream health |

不要只根据状态码下结论。状态码是入口，timeline 和 events 才是证据。

## 调试顺序

建议按这个顺序排查：

1. 看 response status 和 headers。
2. 用 `x-request-id` 查 gateway timeline。
3. 用同一个 request id 查 inference timeline。
4. 看 gateway `/events/failures`。
5. 看 `/metrics` 判断是否是单点还是趋势。
6. 查 `/v1/models` 判断模型名映射是否正确。
7. 回到对应代码和测试。

对应案例：[请求失败排查案例](/11-case-studies/01-request-incident-walkthrough)。

## API 和学习模块的关系

| API 主题 | 对应学习页 |
| --- | --- |
| chat completion | [从请求到首个 Token](/01-llm-fundamentals/04-from-request-to-first-token) |
| streaming | [Streaming、Batching、Metrics](/02-inference-serving/09-streaming-batching-metrics) |
| gateway routing | [外部模型名与内部目标映射](/03-ai-gateway-platform/06-model-name-to-target-mapping) |
| fallback/cache | [Gateway、Router、Fallback、Cache](/03-ai-gateway-platform/03-gateway-router-fallback-cache) |
| request id / metrics | [健康检查、Metrics、Request ID](/03-ai-gateway-platform/02-health-metrics-request-id) |
| events / traces | [Tracing、Metrics、Logs](/04-evaluation-observability/03-observability-traces-metrics-logs) |

这张表能帮助你把接口从“怎么调”连接到“为什么这样设计”。

## 公开分享时怎么讲 API Surface

如果你要录视频或写文章，建议这样讲：

1. 先说明两个服务的层次不同。
2. 再展示 `/health` 和 `/v1/models`。
3. 调一次 gateway chat completion。
4. 解释 response headers。
5. 用 request id 查 timeline。
6. 展示一个失败路径。
7. 最后指向代码和测试。

这样读者看到的不只是接口列表，而是一条完整排障链路。
