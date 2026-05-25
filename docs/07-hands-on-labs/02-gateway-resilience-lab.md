# Gateway 韧性 Lab

## 学习目标

这个 lab 训练你理解“平台治理层”如何把请求失败变成可理解的系统行为。

完成后你应该能说清楚：

- 为什么 gateway 要先鉴权再路由
- `401 / 404 / 429 / 502` 分别属于哪类问题
- fallback 为什么只适合某些失败路径
- streaming fallback 为什么只能发生在首个 chunk 前
- cache 为什么要按 token 隔离
- `x-cache` 为什么能帮助观察缓存路径
- `x-upstream-model` / `x-fallback-used` 和 fallback metrics 如何解释一次 fallback
- `/events` 如何把请求、cache、fallback 和成功路径串成最近事件流

## 前置知识

建议先读：

- [鉴权、路由、限流](/03-ai-gateway-platform/01-auth-routing-rate-limit)
- [Gateway、Router、Fallback、Cache](/03-ai-gateway-platform/03-gateway-router-fallback-cache)
- [Streaming、错误路径、Upstream Health](/03-ai-gateway-platform/04-streaming-errors-upstream-health)
- [ai-gateway 项目页](/06-projects/02-ai-gateway)

## 代码入口

重点看这些文件：

- `projects/ai-gateway/src/ai_gateway/server.py`
- `projects/ai-gateway/src/ai_gateway/router.py`
- `projects/ai-gateway/src/ai_gateway/runtime.py`
- `projects/ai-gateway/src/ai_gateway/middleware/auth.py`
- `projects/ai-gateway/tests/test_proxy.py`

## 操作步骤

### 1. 启动 inference 和 gateway

先启动 inference：

```bash
cd /path/to/ai-infra/projects/inference-service
PYTHONPATH=src ../../.venv/bin/python -m inference_service.main serve
```

再启动 gateway：

```bash
cd /path/to/ai-infra/projects/ai-gateway
PYTHONPATH=src ../../.venv/bin/python -m ai_gateway.main serve
```

打开：

- `http://localhost:8080/health`
- `http://localhost:8080/metrics`
- `http://localhost:8080/events`

### 2. 验证正常代理

```bash
curl -s http://localhost:8080/v1/chat/completions \
  -H 'Authorization: Bearer sk-test-key-1' \
  -H 'Content-Type: application/json' \
  -H 'X-Request-ID: req_lab_gateway_ok_1' \
  -d '{"model":"vllm-local","messages":[{"role":"user","content":"Hello gateway lab"}]}'
```

观察：

- gateway 返回 `x-request-id`
- gateway 返回 `x-cache: BYPASS`
- gateway 返回 `x-upstream-model: vllm-local`
- gateway 返回 `x-fallback-used: false`
- 返回内容来自下游 inference
- gateway metrics 的 successful requests 增加
- `/events` 里能看到 `request_received`、`upstream_attempt`、`request_success`

### 3. 验证三个入口错误

不带 token：

```bash
curl -i -s http://localhost:8080/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"vllm-local","messages":[{"role":"user","content":"no token"}]}'
```

未知模型：

```bash
curl -i -s http://localhost:8080/v1/chat/completions \
  -H 'Authorization: Bearer sk-test-key-1' \
  -H 'Content-Type: application/json' \
  -d '{"model":"unknown-model","messages":[{"role":"user","content":"unknown"}]}'
```

连续请求触发限流：

```bash
for i in 1 2 3; do
  curl -i -s http://localhost:8080/v1/chat/completions \
    -H 'Authorization: Bearer sk-test-key-1' \
    -H 'Content-Type: application/json' \
    -d '{"model":"vllm-local","messages":[{"role":"user","content":"rate limit"}]}'
done
```

观察：

- `401` 是身份问题
- `404` 是路由问题
- `429` 是平台主动保护下游

### 4. 验证 streaming

```bash
curl -N http://localhost:8080/v1/chat/completions \
  -H 'Authorization: Bearer sk-test-key-1' \
  -H 'Content-Type: application/json' \
  -d '{"model":"vllm-local","messages":[{"role":"user","content":"stream through gateway"}],"stream":true}'
```

观察：

- gateway 不生成 chunk，只透传下游事件流
- 正常流最后有 `[DONE]`

## 关键观察点

### 观察点 1：gateway 的失败不是一种失败

不同错误对应不同系统层：

| 状态码 | 含义 | 所属层 |
| --- | --- | --- |
| `401` | token 不合法 | 入口身份 |
| `404` | 模型名无法路由 | 路由 |
| `429` | 超过配额 | 治理 |
| `502` | 下游不可用 | 依赖 |

把这些错误统一成结构化返回，是平台层价值的一部分。

### 观察点 2：fallback 不是万能重试

普通请求还没返回时，可以切备用模型。  
streaming 请求如果已经发出 chunk，就不应该再切备用模型。

原因很简单：客户端已经收到一部分主模型输出，再拼上备用模型输出，会让结果语义混乱。

当前 `configs/models.yaml` 已经有一个教学用 fallback 链：

```text
vllm-local -> vllm-backup
```

它们默认都指向本地 inference-service，目的是让你先学会读配置和观察候选顺序。

当 fallback 发生时，普通响应会通过 `x-upstream-model` 告诉你最终使用了哪个候选，通过 `x-fallback-used` 告诉你这次请求是否切过备用模型。`/metrics` 里的 `ai_gateway_fallback_attempts_total` 和 `ai_gateway_fallback_successes_total` 则适合观察一段时间内 fallback 是否变多。

如果你想复盘请求的内部路径，再看 `/events`。它会把 `upstream_attempt`、`fallback_attempt`、`fallback_success`、`request_success` 这些关键动作按时间记录下来，也可以用 `event_type`、`request_id` 或 `upstream_model` 过滤，比只看最终响应 header 更完整。`/events/summary` 适合快速看最近成功、fallback、cache 等事件大概分布，`/events/failures` 适合专门看失败类型、状态码和失败上游模型。`/events/requests` 适合先看最近请求 timeline 索引，`/events/requests/{request_id}` 适合把一次请求的事件类型、上游候选和总耗时串成 timeline。

### 观察点 3：cache 必须考虑隔离

非流式 response cache 当前按 token 和请求体生成 key。  
这表达了一个非常重要的平台直觉：

同样的 prompt，在不同 token 或租户下，不应该默认共享响应。

响应里的 `x-cache` 可以帮助你区分：

- `BYPASS`：缓存未启用
- `MISS`：查过缓存，但需要访问下游
- `HIT`：直接命中 gateway 缓存

## 扩展任务

任选一个完成：

1. 给 gateway metrics 增加 `streaming_requests_total`。
2. 给 cache 加一个测试，验证超过 `max_entries` 后最旧条目会被淘汰，并观察 `x-cache`。
3. 修改 `models.yaml` 中的 fallback 顺序，然后说明 gateway 会按什么候选顺序尝试，并观察 `x-upstream-model` 是否变化。

## 验收标准

完成这个 lab 后，至少要能通过：

```bash
PYTHON=.venv/bin/python make infra-check
PYTHON=.venv/bin/python make infra-smoke
```

你还应该能回答：

- 为什么 gateway 不自己生成内容
- 为什么 fallback 不能在 streaming 中途随便切
- 为什么 cache key 里需要 token
- `x-cache: BYPASS / MISS / HIT` 分别代表什么
- `x-upstream-model` 和 `x-fallback-used` 分别回答什么问题
- 为什么 `/health` 要包含 upstream 状态
