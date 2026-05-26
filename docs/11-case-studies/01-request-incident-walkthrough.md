# 请求失败排查案例

这个案例模拟一次很常见的场景：

> 用户说请求失败了，只给你一个状态码和一个 request id。你要判断问题在哪里。

这不是生产事故手册，而是用当前学习项目训练排查思路。

一个好的请求失败复盘，不是从代码里随机搜索，也不是看到状态码就下结论。它应该像一条证据链：先确认入口发生了什么，再确认 gateway 是否接收、是否路由、是否调用下游，最后确认 inference-service 是否真的执行。

这个案例训练的就是这种顺序感。

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

## 先形成排查假设

拿到 request id 后，可以先把问题分成四类：

| 假设 | 典型状态 | 最先看的证据 |
| --- | --- | --- |
| 调用方输入错误 | `401`、请求体校验失败 | response body、gateway events |
| gateway 路由失败 | `404` | 模型名、route_not_found event |
| 平台治理触发 | `429`、cache/fallback 异常 | gateway metrics、events/failures |
| 下游或执行层失败 | `502`、SSE error | upstream_attempt、inference timeline |

先分类的价值是减少无效排查。比如 `401` 通常不需要先看 inference；`502` 则不能只停在 gateway response body。

## 第 1 步：先拿到最外层证据

用 gateway 发一条带 request id 的请求：

```bash
curl -i -s http://localhost:8080/v1/chat/completions \
  -H 'Authorization: Bearer dev-gateway-key-1' \
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

记录方式：

```text
request id：
HTTP status：
x-upstream-model：
x-fallback-used：
x-cache：
响应 body 摘要：
第一判断：
```

这一步不要急着解释根因，只做事实记录。

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
  -H 'Authorization: Bearer dev-gateway-key-1' \
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

入口错误的关键判断是：请求有没有必要进入下游。对于 `401` 和 `404`，gateway 拦截是正确行为。你要复盘的是“为什么入口条件不满足”，不是“下游为什么失败”。

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

失败摘要适合回答“这是不是个别现象”。如果同类状态码持续升高，它就不再只是一个用户请求失败，而可能是配置变更、上游健康或调用方迁移造成的系统性问题。

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

timeline 里最值得关注的是事件顺序。相同事件出现在不同顺序里，含义可能完全不同：

- `auth_failed` 出现在最前面：入口鉴权问题。
- `cache_hit` 后直接 `request_success`：下游可能没有被调用。
- `upstream_attempt` 后 `fallback_success`：主 upstream 失败但降级成功。
- `upstream_attempt` 后 `request_failed`：所有候选失败或不可恢复错误。
- streaming 中出现 `error` event：客户端已经进入事件流语义，不能只按普通 `502` 理解。

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

这里最重要的是不要混淆两类失败：

| 现象 | 更可能的原因 |
| --- | --- |
| gateway 有 upstream_attempt，inference 没有 request | upstream URL、网络、端口、服务未启动 |
| inference 有 request_received，但没有 request_success | inference 内部或 engine adapter |
| inference 有 request_success，但 gateway 返回失败 | gateway 解析、转发、streaming 处理 |
| 两边都有 success，但用户仍说失败 | 客户端解析、cache/fallback 语义、业务质量 |

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

## 第 7 步：回到测试确认契约

排查完现象后，建议回到测试文件确认系统契约：

- `projects/ai-gateway/tests/test_proxy.py`
- `projects/inference-service/tests/test_api.py`

重点找：

- `401` 是否应该返回固定错误形状。
- 未知模型是否应该是 `404`。
- upstream failure 是否应该映射为 `502`。
- streaming error 是否应该用 SSE error event。
- request id 是否应该透传。

测试能帮你区分“系统按设计工作”和“系统发生回退”。很多时候用户看到失败，不代表代码错了；也可能是系统正确拒绝了不合法请求。

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

更完整的模板：

```text
我排除的可能性：
- 调用方鉴权：
- 模型路由：
- gateway 到 upstream：
- inference engine：
- cache / fallback：

仍然不确定：

需要补充的证据：

是否需要改代码：

是否需要改文档或报错信息：
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

## 生产系统会更复杂在哪里

当前学习项目把证据集中在 header、events 和 metrics 里。真实生产系统还会涉及：

- 分布式 tracing。
- 结构化日志检索。
- 多区域或多 upstream 的健康状态。
- 客户端重试和超时。
- per-tenant 限流和预算。
- 安全审计和异常访问检测。
- 告警、值班和 incident timeline。

但学习阶段先掌握这里的顺序就够了：入口证据、gateway timeline、inference timeline、metrics、测试契约。顺序稳了，以后接更复杂的观测系统也不会迷路。
