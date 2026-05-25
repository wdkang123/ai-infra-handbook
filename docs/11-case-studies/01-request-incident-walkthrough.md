# 请求失败排查案例

这个案例模拟一次很常见的场景：

> 用户说请求失败了，只给你一个状态码和一个 request id。你要判断问题在哪里。

这不是生产事故手册，而是用当前学习项目训练排查思路。

## 场景设定

现象可能是：

- 调用 gateway 返回 `401`
- 调用 gateway 返回 `404`
- 调用 gateway 返回 `429`
- 调用 gateway 返回 `502`
- streaming 请求中途出现 error event

你的目标不是立刻改代码，而是先回答：

- 是调用方问题，还是平台层问题
- 是否命中了 gateway 的鉴权、限流、路由或 fallback
- inference-service 有没有收到请求
- 失败路径是否留下了足够证据

## 第 1 步：先拿到最外层证据

用 gateway 发一条带 request id 的请求：

```bash
curl -i -s http://localhost:8080/v1/chat/completions \
  -H 'Authorization: Bearer sk-test-key-1' \
  -H 'X-Request-ID: req_case_gateway_1' \
  -H 'Content-Type: application/json' \
  -d '{"model":"vllm-local","messages":[{"role":"user","content":"case study"}]}'
```

先看响应 header：

- `x-request-id`
- `x-upstream-model`
- `x-fallback-used`
- `x-cache`

如果 header 里没有你传入的 request id，说明链路追踪从入口就不稳定。  
如果有，就可以继续沿着这个 id 查事件。

## 第 2 步：判断是否是 gateway 入口错误

先故意触发鉴权失败：

```bash
curl -i -s http://localhost:8080/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"vllm-local","messages":[{"role":"user","content":"no auth"}]}'
```

再故意触发未知模型：

```bash
curl -i -s http://localhost:8080/v1/chat/completions \
  -H 'Authorization: Bearer sk-test-key-1' \
  -H 'Content-Type: application/json' \
  -d '{"model":"unknown-model","messages":[{"role":"user","content":"unknown"}]}'
```

这两类错误通常不需要查 inference-service：

| 状态码 | 更可能的层 | 说明 |
| --- | --- | --- |
| `401` | gateway 鉴权 | token 缺失或格式不对 |
| `404` | gateway 路由 | 外部模型名无法映射到内部目标 |
| `429` | gateway 限流 | 调用方超过平台预算 |
| `502` | gateway 到 upstream | 下游失败或所有 fallback 都失败 |

## 第 3 步：看 gateway 失败摘要

```bash
curl -s 'http://localhost:8080/events/failures'
```

重点看：

- `failure_event_count`
- `failed_request_count`
- `status_code_counts`
- `event_type_counts`
- `failed_upstream_model_counts`
- `latest_failure_event`

如果 `status_code_counts` 中 `401` 很高，先看调用方 token。  
如果 `502` 很高，再往 upstream 和 fallback 查。

这一步对应代码：

- `projects/ai-gateway/src/ai_gateway/server.py`
- `projects/ai-gateway/src/ai_gateway/runtime.py`

## 第 4 步：看 gateway request timeline

```bash
curl -s 'http://localhost:8080/events/requests/req_case_gateway_1'
```

你要判断 timeline 里有没有：

- `request_received`
- `cache_miss` 或 `cache_hit`
- `upstream_attempt`
- `fallback_attempt`
- `fallback_success`
- `request_success`
- `upstream_error`
- `request_failed`

如果 timeline 只有 `auth_failed`，说明请求没有真正进入下游。  
如果出现 `upstream_attempt` 但没有 `request_success`，再看下游。

## 第 5 步：看 inference-service 是否收到请求

如果 gateway 已经调用了 inference-service，可以继续查 inference 的 request timeline：

```bash
curl -s 'http://localhost:8000/events/requests/req_case_gateway_1'
```

重点看：

- `request_received`
- `engine_generate_start`
- `engine_stream_start`
- `request_success`
- `engine_error`

如果 gateway timeline 有 `upstream_attempt`，但 inference timeline 没有对应 request，说明问题可能在网络、配置或目标 URL。  
如果 inference timeline 有 `engine_error`，说明请求已经到执行层，问题更靠近模型服务或 engine adapter。

## 第 6 步：看 metrics 是否支持判断

gateway：

```bash
curl -s http://localhost:8080/metrics
```

inference：

```bash
curl -s http://localhost:8000/metrics
```

你不需要一开始读懂所有指标，先关注：

- gateway 有没有 fallback attempts / successes
- inference request 计数是否变化
- token 计数是否变化

metrics 的价值不是替代事件，而是帮你判断“这类现象是不是频繁发生”。

## 排查结论模板

```text
现象：gateway 返回 502

request id：req_case_gateway_1

gateway timeline：
- request_received
- upstream_attempt
- upstream_error
- fallback_attempt
- request_failed

inference timeline：
- 没有对应 request，或出现 engine_error

判断：
- 如果 inference 没有 request，更可能是 upstream 配置或网络问题
- 如果 inference 有 engine_error，更可能是执行层错误

下一步：
- 查 gateway upstream 配置
- 查 inference health
- 查 engine adapter 错误
```

## 这个案例应该带走什么

真正的排查不是从代码随机搜，而是按证据顺序走：

1. response header
2. request id
3. gateway failure summary
4. gateway timeline
5. inference timeline
6. metrics
7. 代码和测试

如果你能按这个顺序解释一次失败路径，说明你已经抓住 gateway 和 inference-service 的边界了。
