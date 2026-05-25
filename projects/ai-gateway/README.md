# ai-gateway

这是学习链路里的“平台治理层”入口。

它当前的价值不是做一个完整网关产品，而是帮助你理解：

- 请求进入平台后先经过什么
- 为什么要先鉴权再路由
- 为什么模型名和下游 target model 可能不一样
- 为什么 gateway 需要限流和独立 metrics
- 为什么 cache 命中状态需要被观察
- 为什么结构化事件能补足单次 header 和长期 metrics 的中间层

## 先看哪里

- [server.py](src/ai_gateway/server.py)
- [router.py](src/ai_gateway/router.py)
- [auth.py](src/ai_gateway/middleware/auth.py)
- [config.py](src/ai_gateway/config.py)

## 先跑什么

先确保 inference-service 已经启动，再执行：

```bash
cd projects/ai-gateway
PYTHONPATH=src ../../.venv/bin/python -m ai_gateway.main serve
```

## 你应该看到什么

- [http://localhost:8080/health](http://localhost:8080/health)
- [http://localhost:8080/metrics](http://localhost:8080/metrics)
- [http://localhost:8080/events](http://localhost:8080/events)
- [http://localhost:8080/v1/models](http://localhost:8080/v1/models)

`/events` 支持按 `event_type`、`request_id`、`requested_model` 和 `upstream_model` 过滤，例如：

```bash
curl -s 'http://localhost:8080/events?event_type=request_success&upstream_model=vllm-local'
curl -s 'http://localhost:8080/events/summary?event_type=request_success&upstream_model=vllm-local'
curl -s 'http://localhost:8080/events/failures'
curl -s 'http://localhost:8080/events/requests?requested_model=vllm-local&upstream_model=vllm-local'
curl -s 'http://localhost:8080/events/requests/req_demo_gateway_1'
```

现在 `/health` 里不再只是静态配置回显，它会对下游 inference 的 `/health` 做一次最小真实探测，所以你看到的 `upstream_services` 更接近 gateway 当前眼里的真实状态。只要有下游探测失败，gateway 顶层 `status` 也会收成 `degraded`。

`/v1/models` 会列出 gateway 对外暴露的模型名、target model、fallback 候选数量和 upstream health。它帮助你区分“调用方看到的模型目录”和“内部路由配置”。

你还可以主动试几种路径：

- 不带 token，应该是 `401`
- 带未知模型，应该是 `404`
- 请求太多，应该是 `429`
- 下游失败时，应该是 `502`

也可以试最小 streaming 透传：

```bash
curl -N http://localhost:8080/v1/chat/completions \
  -H 'Authorization: Bearer dev-gateway-key-1' \
  -H 'Content-Type: application/json' \
  -d '{"model":"vllm-local","messages":[{"role":"user","content":"Hello stream"}],"stream":true}'
```

这次你应该看到 gateway 原样把下游 `text/event-stream` 事件流继续向上转发。如果下游在首个 chunk 前 5xx 失败，gateway 会尝试配置里的 fallback；如果没有可用候选，或已经开始输出后才失败，gateway 会发出结构化 SSE `error` 事件并结束流。

默认 `configs/models.yaml` 里已经有一个教学用 fallback 链：`vllm-local -> vllm-backup`。两个候选当前都指向本地 inference-service，方便你先观察配置表达和候选顺序。

你还可以主动传一个 request id：

```bash
curl -i -s http://localhost:8080/v1/chat/completions \
  -H 'Authorization: Bearer dev-gateway-key-1' \
  -H 'X-Request-ID: req_demo_gateway_1' \
  -H 'Content-Type: application/json' \
  -d '{"model":"vllm-local","messages":[{"role":"user","content":"Hello request id"}]}'
```

现在 gateway 会把这个 `x-request-id` 保留下来，并继续向下游 inference 传递。

非流式响应还会带 `x-cache`：

- `BYPASS`：缓存未启用
- `MISS`：启用缓存但本次未命中
- `HIT`：直接由 gateway cache 返回

`/events` 会保留最近一批结构化事件，例如 `request_received`、`auth_failed`、`route_not_found`、`upstream_attempt`、`fallback_attempt`、`fallback_success`、`cache_hit`、`request_success`。它不是生产日志系统，但很适合学习一条请求在 gateway 内部发生了哪些关键动作，也支持按事件类型、请求 id、请求模型和上游模型过滤。`/events/summary` 则把最近事件聚合成 event/request/upstream counts，适合快速看整体分布。`/events/failures` 会聚合失败事件、状态码和失败上游模型。`/events/requests` 会列出最近请求 timeline 索引，`/events/requests/{request_id}` 会返回单请求 timeline，适合复盘一次请求的路由、fallback 和终止事件。

## 这段代码现在解决什么

- 最小鉴权
- 最小模型路由
- 最小模型列表
- 最小代理转发
- 最小限流
- 最小观测指标
- 最小结构化事件流
- 最小 streaming 透传
- 最小 request id 贯穿
- 最小 upstream 健康探测
- 普通请求和首 chunk 前 streaming 请求的 fallback
- 默认 fallback 配置示例
- streaming 失败时的结构化 SSE error 事件
- 默认关闭的非流式 TTL cache
- 非流式响应的 `x-cache` 可观察 header
- `/events` 最近事件查询、`/events/summary` 摘要、`/events/failures` 失败摘要、request timeline 索引和单请求 timeline

## 这段代码现在还没解决什么

- 没有更复杂的路由策略
- 没有真实租户/配额体系
- 没有生产级缓存和重试策略
- 没有生产级 tracing / structured logging 后端
- 还没有更复杂的 streaming 背压、取消、重试和观测
