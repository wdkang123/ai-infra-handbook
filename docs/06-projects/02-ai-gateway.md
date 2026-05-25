# ai-gateway

这是整条学习链里的平台治理层。

它的重点不是做一个完整网关产品，而是让你直观看懂：

- 请求为什么要先鉴权
- 模型路由是怎么接在平台层上的
- 为什么 gateway 自己不生成内容
- streaming 为什么可以由下游产生、再由 gateway 继续透传
- `x-request-id` 和 `/health` 为什么是跨服务理解系统状态的重要入口
- 为什么 `/events` 能补足单次 header 和长期 metrics 之间的观察空白

更进一步说，`ai-gateway` 这一页最想帮你建立的，不是“怎么写一个代理”，而是：

- 平台层为什么值得单独存在
- 平台层和模型服务层到底该怎么分
- 为什么很多治理能力应该先落在入口，而不是落在模型执行层

## 先看哪些代码

- `projects/ai-gateway/src/ai_gateway/server.py`
- `projects/ai-gateway/src/ai_gateway/router.py`
- `projects/ai-gateway/src/ai_gateway/middleware/auth.py`
- `projects/ai-gateway/src/ai_gateway/config.py`

如果你是第一次回看代码，最推荐顺序是：

1. 先看 `server.py`，建立“入口长什么样”的感觉
2. 再看 `auth.py`，理解为什么平台层先做鉴权
3. 再看 `router.py`，理解外部模型名是怎么被映射到内部目标的

现在 `router.py` 里还保留了一层 fallback 候选逻辑：主下游返回 5xx 时，gateway 可以按 `configs/models.yaml` 里的 `fallbacks` 继续尝试备用模型。普通请求会直接换备用模型重试，并通过 `x-upstream-model` 和 `x-fallback-used` 告诉你最终命中了哪个下游、是否发生过 fallback；streaming 请求只会在尚未向客户端发出第一个 chunk 前 fallback，避免半条主流和半条备用流混在一起。如果所有候选都失败，或已经开始输出后下游失败，gateway 会在 SSE 中发出结构化 `error` 事件并结束流。

默认 `configs/models.yaml` 已经配置了一个教学用 fallback 示例：`vllm-local` 的备用候选是 `vllm-backup`。两者当前都指向本地 inference-service，目的是让你能先看懂 fallback 链怎么表达，而不是假装已经有真实多集群。

`runtime.py` 里也有一层默认关闭的非流式 TTL cache。它按 token 和请求体生成缓存键，已经覆盖了 TTL 过期和不同 token 之间的隔离，适合学习 gateway 为什么会有独立缓存层，但当前还不是生产级缓存系统。

非流式响应现在会带 `x-cache` header：`BYPASS` 表示没有启用缓存，`MISS` 表示查过缓存但需要访问下游，`HIT` 表示直接由 gateway 缓存返回。这个 header 不是业务结果的一部分，但很适合用来学习缓存是否真的参与了请求路径。

`/metrics` 里也会暴露 fallback attempts 和 fallback successes。它们和 `x-upstream-model` / `x-fallback-used` 是互补的：header 帮你观察单次请求，metrics 帮你观察一段时间内 fallback 是否频繁发生。

`/events` 会保留最近一批结构化事件，例如 `request_received`、`auth_failed`、`route_not_found`、`upstream_attempt`、`fallback_attempt`、`fallback_success`、`cache_hit`、`cache_miss`、`request_success`。它不是生产日志系统，但很适合学习“一条请求在 gateway 内部经历了哪些关键动作”。它也支持按 `event_type`、`request_id`、`requested_model` 和 `upstream_model` 过滤。`/events/failures` 则会把失败相关事件聚合成 `status_code_counts`、`failed_upstream_model_counts` 和 failed request 计数，适合先判断最近失败大概来自鉴权、路由、限流还是下游。

## 先跑什么

先确保 inference-service 已经启动，再执行：

```bash
cd /path/to/ai-infra/projects/ai-gateway
PYTHONPATH=src ../../.venv/bin/python -m ai_gateway.main serve
```

如果你想最快确认自己已经站在正确观察面上，可以按这个顺序试：

1. 先开 `/health`
2. 再打一条正常代理请求
3. 再打 `401`
4. 再打 `404`
5. 再试 `stream=true`
6. 最后再带上 `X-Request-ID`

## 你应该观察什么

- `http://localhost:8080/health`
- `http://localhost:8080/metrics`
- `http://localhost:8080/events`
- `http://localhost:8080/v1/models`

模型列表：

```bash
curl -s http://localhost:8080/v1/models
```

这里会看到外部模型名、target model、fallback 列表和 upstream health。它不是完整模型目录系统，但能让你观察“平台层暴露给调用方的模型”和“下游真实执行目标”之间的关系。

普通代理：

```bash
curl -s http://localhost:8080/v1/chat/completions \
  -H 'Authorization: Bearer sk-test-key-1' \
  -H 'Content-Type: application/json' \
  -d '{"model":"vllm-local","messages":[{"role":"user","content":"Hello gateway"}]}'
```

最小 streaming 透传：

```bash
curl -N http://localhost:8080/v1/chat/completions \
  -H 'Authorization: Bearer sk-test-key-1' \
  -H 'Content-Type: application/json' \
  -d '{"model":"vllm-local","messages":[{"role":"user","content":"Hello stream"}],"stream":true}'
```

带 request id：

```bash
curl -i -s http://localhost:8080/v1/chat/completions \
  -H 'Authorization: Bearer sk-test-key-1' \
  -H 'X-Request-ID: req_demo_gateway_1' \
  -H 'Content-Type: application/json' \
  -d '{"model":"vllm-local","messages":[{"role":"user","content":"Hello request id"}]}'
```

查看最近 gateway 事件：

```bash
curl -s 'http://localhost:8080/events?limit=20'
curl -s 'http://localhost:8080/events?event_type=request_success&upstream_model=vllm-local'
curl -s 'http://localhost:8080/events/summary?event_type=request_success&upstream_model=vllm-local'
curl -s 'http://localhost:8080/events/failures'
curl -s 'http://localhost:8080/events/requests?requested_model=vllm-local&upstream_model=vllm-local'
curl -s 'http://localhost:8080/events/requests/req_demo_gateway_1'
```

除了结果本身，这里最值得刻意观察的是：

1. 为什么外部 `model` 名和下游执行目标不是必须同名
2. 为什么 `/health` 里会包含 `upstream_services`
3. 为什么 `/v1/models` 是模型发现入口，不是生成入口
4. 为什么 `x-request-id` 这种 header 对业务无感，却对排障很关键
5. 为什么 `x-cache` 能让 cache hit / miss / bypass 变成可观察行为
6. 为什么 `x-upstream-model` 和 fallback metrics 能把“静默重试”变成可复盘行为
7. 为什么 `/events` 比 header 更完整、比 metrics 更贴近单条请求
8. 为什么 `/events/summary` 能快速回答最近事件类型、请求模型和上游模型的分布
9. 为什么 `/events/failures` 适合先看失败类型、状态码和失败上游分布
10. 为什么 `/events/requests` 和 `/events/requests/{request_id}` 适合把最近请求索引、单次路由、fallback 和成功路径串成 timeline

## 这部分当前已经做到什么

- 最小鉴权
- 最小模型路由
- 最小 `/v1/models` 模型列表
- 最小代理转发
- 最小 streaming 透传
- 最小 `x-request-id` 贯穿
- 最小 upstream 健康探测
- 普通请求和首 chunk 前 streaming 请求的最小 fallback
- `configs/models.yaml` 中的默认 fallback 示例
- fallback attempts/successes metrics
- 非流式 fallback 的 `x-upstream-model` 与 `x-fallback-used`
- streaming 失败时的结构化 SSE error 事件
- `/events` 最近结构化事件查询和按事件/请求/模型过滤
- `/events/summary` 最近结构化事件摘要
- `/events/failures` 失败事件摘要
- `/events/requests` 请求 timeline 索引和 `/events/requests/{request_id}` 单请求 timeline
- 默认关闭的非流式 TTL cache
- cache 的 TTL 过期与 token 隔离测试
- 非流式响应的 `x-cache: BYPASS / MISS / HIT`
- `401 / 404 / 429 / 502` 路径

这意味着它已经不只是“转发成功”，而是已经具备了平台层最关键的第一批系统行为。

## 这部分当前还没做到什么

- 更复杂的路由策略
- 多租户 / 配额体系
- 更完整的缓存 / 重试策略
- 更完整的 streaming 背压、取消和重试
- 生产级 tracing / structured logging 后端

## 最适合的继续学习顺序

如果你已经把这页跑过一轮，下一步最适合接着读：

1. [平台层与模型服务层边界](/03-ai-gateway-platform/05-platform-vs-model-service)
2. [外部模型名与内部目标映射](/03-ai-gateway-platform/06-model-name-to-target-mapping)
3. [从 Demo Gateway 到真实平台](/03-ai-gateway-platform/07-from-demo-gateway-to-real-platform)

这样你就不会只把 `ai-gateway` 理解成一段代理代码，而会开始把它看成平台层骨架。
