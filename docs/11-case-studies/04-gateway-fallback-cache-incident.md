# Gateway Fallback 与缓存复盘案例

这个案例模拟一次平台层更微妙的故障：

> 用户没有看到 5xx，但回答来自 fallback 模型，且第二次请求命中了 cache。你要判断这是正常降级，还是掩盖了上游问题。

这类问题比单纯 `502` 更接近真实平台维护：请求表面成功，但质量、成本、延迟和来源都可能变了。

## 场景设定

你已经运行了：

- `inference-service`
- `ai-gateway`

并且 gateway 配置里有默认 fallback 模型。
你要回答：

- 请求是否真的走了 fallback
- fallback 发生在首个 chunk 之前还是之后
- 第二次请求是否命中了 cache
- cache 是否按 token 和请求体隔离
- 这次成功是否应该进入发布或运营复盘

## 第 1 步：发出带 request id 的请求

```bash
curl -i -s http://localhost:8080/v1/chat/completions \
  -H 'Authorization: Bearer dev-gateway-key-1' \
  -H 'X-Request-ID: req_case_fallback_1' \
  -H 'Content-Type: application/json' \
  -d '{"model":"vllm-local","messages":[{"role":"user","content":"explain fallback"}]}'
```

先看 header：

- `x-request-id`
- `x-upstream-model`
- `x-fallback-used`
- `x-cache`

如果 `x-fallback-used: true`，说明这次响应虽然成功，但并不是按原始首选 upstream 完成。
如果 `x-cache: HIT`，说明你看到的响应可能来自 gateway cache，而不是一次新的下游调用。

## 第 2 步：查 gateway request timeline

```bash
curl -s 'http://localhost:8080/events/requests/req_case_fallback_1'
```

重点看事件顺序：

```text
request_received
cache_miss
upstream_attempt
upstream_error
fallback_attempt
fallback_success
request_success
```

如果 timeline 里出现 `fallback_success`，但最终状态是 success，这通常是受控降级。
如果只有 `upstream_error` 和 `request_failed`，说明所有候选都失败。

## 第 3 步：判断 fallback 的工程含义

一次 fallback 不是自动坏事。它可能代表：

| 现象 | 可能解释 | 需要继续查什么 |
| --- | --- | --- |
| 单次 fallback，最终 success | 临时 upstream 抖动 | upstream health、失败摘要 |
| fallback 次数持续增加 | 首选模型或目标服务不稳定 | 最近部署、限流、连接超时 |
| fallback 后质量变差 | fallback 模型能力不一致 | eval、样本复盘、业务场景 |
| fallback 后成本升高 | fallback 目标更贵或更慢 | token usage、延迟、路由策略 |
| streaming 中途失败 | 首个 chunk 后无法安全切换 | streaming event 和客户端处理 |

学习项目里的 fallback 是为了展示边界。真实系统里还需要重试预算、超时策略、熔断、分级模型池和策略审计。

## 第 4 步：看失败摘要是否支持判断

```bash
curl -s 'http://localhost:8080/events/failures'
```

重点看：

- `failure_event_count`
- `failed_request_count`
- `failed_upstream_model_counts`
- `latest_failure_event`

如果失败摘要里首选 upstream 的错误持续出现，就不能只因为最终响应 200 就忽略。
平台层要同时关心“有没有成功返回”和“用什么代价成功返回”。

## 第 5 步：复现 cache 行为

用相同 token 和请求体再发一次：

```bash
curl -i -s http://localhost:8080/v1/chat/completions \
  -H 'Authorization: Bearer dev-gateway-key-1' \
  -H 'X-Request-ID: req_case_fallback_2' \
  -H 'Content-Type: application/json' \
  -d '{"model":"vllm-local","messages":[{"role":"user","content":"explain fallback"}]}'
```

如果 cache 开启且请求体一致，第二次可能出现：

```text
x-cache: HIT
```

再换一个 token：

```bash
curl -i -s http://localhost:8080/v1/chat/completions \
  -H 'Authorization: Bearer another-learning-token' \
  -H 'X-Request-ID: req_case_fallback_3' \
  -H 'Content-Type: application/json' \
  -d '{"model":"vllm-local","messages":[{"role":"user","content":"explain fallback"}]}'
```

期望它不会复用上一个 token 的 cache。
这对应 gateway cache 的一个重要边界：缓存必须按调用方和请求体隔离，不能只按 prompt 文本复用。

## 第 6 步：写平台复盘结论

可以用这个模板：

```text
现象：
- 用户请求返回 200，但 x-fallback-used 为 true

证据：
- request id:
- gateway timeline:
- failures summary:
- x-cache:
- x-upstream-model:

判断：
- 这是受控降级 / 非预期降级 / cache 掩盖问题

风险：
- 质量：
- 成本：
- 延迟：
- 可追溯：

下一步：
-
```

示例判断：

```text
这次不是用户侧失败，而是平台层受控降级。
短期可以接受，因为 fallback_success 和 request_success 都存在。
但不能直接忽略，因为 failed_upstream_model_counts 指向首选 upstream 持续失败。
下一步应该检查上游健康、最近配置变更和 eval 对 fallback 模型的覆盖。
```

## 生产系统还需要什么

当前学习项目能帮助你看懂 fallback/cache 的证据链，但生产系统还需要：

- fallback policy 审计记录
- 每个 fallback 原因的结构化分类
- per-tenant cache policy
- cache 命中后的质量和成本观测
- fallback 触发阈值和冷却时间
- streaming 中途失败的客户端语义
- fallback 模型与首选模型的 eval 对齐

## 这个案例应该带走什么

Gateway 成功返回不等于路径完全健康。
平台层复盘要同时看：

1. 是否成功返回
2. 是否使用 fallback
3. 是否命中 cache
4. 是否跨 token 隔离
5. upstream 是否持续失败
6. 质量、成本和延迟是否被改变

如果你能把这几件事讲清楚，就已经开始具备平台层工程判断力。
