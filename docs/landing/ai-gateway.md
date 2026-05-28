# AI Gateway

> 本页解决：AI Gateway 为什么不是普通反向代理。
> 读完能做：理解 auth、routing、rate limit、fallback、cache、events 和 metrics 的平台边界。
> 关联代码：`projects/ai-gateway`、`projects/inference-service`。
> 验证命令：`curl -s http://localhost:8080/metrics`。

AI Gateway 是模型调用的策略边界。它不负责 GPU 推理，却负责让模型能力可控、可观测、可演进。

## Gateway 负责什么

| 能力 | 学习问题 |
| --- | --- |
| Auth | 谁能调用 |
| Routing | 外部模型名如何映射到内部 target |
| Rate limit | 调用方如何被限制 |
| Fallback | 主 upstream 失败时如何降级 |
| Cache | 重复请求是否可复用 |
| Events | 一次请求如何被复盘 |
| Metrics | 错误、fallback、cache 是否聚集 |

## 推荐路径

1. [AI Gateway Platform 总览](/03-ai-gateway-platform/00-overview)
2. [健康检查、Metrics、Request ID](/03-ai-gateway-platform/02-health-metrics-request-id)
3. [Gateway、Router、Fallback、Cache](/03-ai-gateway-platform/03-gateway-router-fallback-cache)
4. [Gateway 韧性 Lab](/07-hands-on-labs/02-gateway-resilience-lab)
5. [Gateway Fallback 与缓存复盘案例](/11-case-studies/04-gateway-fallback-cache-incident)

## 快速验证

```bash
curl -sD - -X POST http://localhost:8080/v1/chat/completions \
  -H 'Authorization: Bearer dev-gateway-key-1' \
  -H 'X-Request-ID: req_gateway_landing_1' \
  -H 'Content-Type: application/json' \
  -d '{"model":"vllm-local","messages":[{"role":"user","content":"gateway demo"}]}'
```

再查：

```bash
curl -s 'http://localhost:8080/events/requests/req_gateway_landing_1'
curl -s http://localhost:8080/metrics
```

## FAQ

### 为什么成功响应也要看 gateway 证据

因为 fallback 和 cache 可能让用户拿到 `200`，但主 upstream 实际不健康。

### Gateway 和 inference-service 都有 metrics，应该看哪个

Gateway metrics 看平台治理，inference metrics 看模型服务。不要混成一个层。

### 真实迁移先做什么

先保留外部模型名、request id、events、metrics 和 failure summary，再逐步增强 tenant、quota、fallback 和 audit。
