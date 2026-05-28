# Prometheus Metrics 对照表

> 本页解决：当前项目 metrics、真实 vLLM metrics 和学习者观察目标如何对应。
> 读完能做：知道看 gateway、inference 和真实 backend 指标时分别应该问什么问题。
> 关联代码：`projects/inference-service`、`projects/ai-gateway`、`scripts/integration_smoke_test.sh`。
> 验证命令：`curl -s http://localhost:8080/metrics`。

Metrics 的价值不是“页面上有很多数字”，而是帮助你回答：请求有没有进来、上游有没有失败、fallback 有没有被隐藏、token usage 是否异常、真实 runtime 是否出现资源瓶颈。

## 当前项目 metrics

| 层 | 示例指标 | 学习问题 |
| --- | --- | --- |
| gateway | `ai_gateway_requests_total` | 入口请求是否增长 |
| gateway | `ai_gateway_fallback_attempts_total` | 是否发生 fallback |
| gateway | `ai_gateway_cache_hits_total` | cache 是否命中 |
| gateway | `ai_gateway_upstream_errors_total` | 上游错误是否聚集 |
| inference | `vllm_num_requests_total` | 模型服务收到多少请求 |
| inference | `vllm_prompt_tokens_total` | prompt token 估算或真实 usage |
| inference | `vllm_completion_tokens_total` | completion token 估算或真实 usage |

当前 inference 的部分指标使用 vLLM 风格命名，是为了提前训练读者的真实 serving 观察习惯；默认实现仍然是学习型 mock。

## vLLM metrics 对齐思路

接入真实 vLLM 后，指标会分成三层：

| 层 | 谁暴露 | 作用 |
| --- | --- | --- |
| Gateway metrics | `ai-gateway` | 平台治理：auth、routing、fallback、cache、upstream health |
| Adapter metrics | `inference-service` | adapter 行为：请求、错误、timeout、usage 映射 |
| Runtime metrics | vLLM server | 真实执行：scheduler、token、KV cache、queue、latency |

不要用 vLLM runtime metrics 替代 gateway metrics。两者回答的问题不同。

## 学习者应该观察什么

### 1. 请求是否真的经过 gateway

命令：

```bash
curl -s http://localhost:8080/metrics
```

重点看：

```text
ai_gateway_requests_total
```

如果 gateway 没增长，但 inference 增长，说明你可能绕过了 gateway。

### 2. fallback 是否发生

重点看：

```text
ai_gateway_fallback_attempts_total
```

再配合：

```bash
curl -s 'http://localhost:8080/events/failures'
curl -s 'http://localhost:8080/events/requests/{request_id}'
```

成功响应不代表主路径健康。fallback 是平台风险信号。

### 3. token usage 是否变化

命令：

```bash
curl -s http://localhost:8000/metrics
```

重点看：

```text
vllm_prompt_tokens_total
vllm_completion_tokens_total
```

如果候选版本质量略升但 completion tokens 大幅增加，release decision 不能只看分数。

### 4. timeout 是否集中

当前学习项目通过 events 和 failure summary 更容易观察 timeout：

```bash
curl -s 'http://localhost:8080/events/failures'
```

真实迁移后，metrics 应能补充：

- upstream timeout count
- upstream latency bucket
- request error count
- retry / fallback count

### 5. vLLM runtime 是否拥塞

真实 vLLM 接入后，学习者应该观察：

- 请求队列是否变长
- token throughput 是否下降
- KV cache 是否接近瓶颈
- prefill / decode latency 是否异常
- running / waiting requests 是否堆积

这些属于 runtime 层，不应该和 gateway 策略层混在一起。

## 对照表

| 问题 | 当前指标 / 证据 | vLLM 迁移后补充 | 读者结论 |
| --- | --- | --- | --- |
| 请求到了哪里 | gateway requests、inference requests、request id events | vLLM request metrics | 判断是否绕过 gateway |
| 模型是否返回 | inference success events、token metrics | completion / token metrics | 判断 backend 是否执行 |
| 是否 fallback | gateway fallback metrics、headers、events | upstream error metrics | 判断成功响应是否降级 |
| 是否 timeout | failure summary、request timeline | latency bucket、timeout counter | 判断瓶颈在平台还是 runtime |
| 成本是否变化 | prompt / completion token metrics | backend usage metrics | 判断发布是否带来成本风险 |
| 质量是否变好 | eval compare report | 不由 metrics 直接证明 | 需要 eval + observability 一起判断 |

## 最小 PromQL 风格示例

这些示例是学习口径，不要求当前项目已经接入 Prometheus：

```text
rate(ai_gateway_requests_total[5m])
rate(ai_gateway_fallback_attempts_total[5m])
rate(ai_gateway_upstream_errors_total[5m])
rate(vllm_prompt_tokens_total[5m])
rate(vllm_completion_tokens_total[5m])
```

如果接入真实 runtime，还可以继续扩展：

```text
histogram_quantile(0.95, rate(vllm_request_latency_seconds_bucket[5m]))
```

具体指标名必须以目标 vLLM 版本实际暴露为准。

## 指标不能证明什么

Metrics 不能单独证明：

- 回答质量更好
- 发布一定安全
- fallback 结果和主模型等价
- cache 命中的内容一定仍然正确
- 微调产物 lineage 一定一致

这些必须结合 eval report、events、manifest 和 evidence packet。

## 推荐下一步

- 想理解请求证据：读 [Serving 与 Gateway 输出证据](/13-output-gallery/01-serving-gateway-evidence)。
- 想理解发布判断：读 [Eval regression gate 示例](/04-evaluation-observability/09-eval-regression-gate-example)。
- 想接真实 backend：读 [vLLM Adapter 设计](/12-production-migration/05-vllm-adapter-design)。
