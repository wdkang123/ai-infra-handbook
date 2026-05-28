# LLM Observability

> 本页解决：LLM 系统怎么从“接口能返回”升级到“请求可解释”。
> 读完能做：用 request id、events、metrics 和未来 tracing 设计排查一次模型调用。
> 关联代码：`projects/ai-gateway`、`projects/inference-service`、`scripts/integration_smoke_test.sh`。
> 验证命令：`PYTHON=.venv/bin/python make infra-smoke`。

LLM Observability 不只是 dashboard。对学习者来说，它首先是一条证据链：

```text
request id -> headers -> events timeline -> metrics -> failure summary -> evidence packet
```

## 先看哪三个入口

| 入口 | 用途 |
| --- | --- |
| `/events/requests/{request_id}` | 复盘单次请求 |
| `/events/summary` | 看某类事件是否聚集 |
| `/metrics` | 看服务或平台趋势 |

## 推荐路径

1. [Tracing、Metrics、Logs](/04-evaluation-observability/03-observability-traces-metrics-logs)
2. [Serving 与 Gateway 输出证据](/13-output-gallery/01-serving-gateway-evidence)
3. [Prometheus Metrics 对照表](/12-production-migration/07-prometheus-metrics-map)
4. [OpenTelemetry GenAI Tracing 设计](/12-production-migration/06-opentelemetry-genai-tracing)
5. [失败案例手册](/11-case-studies/06-failure-case-playbook)

## 快速验证

```bash
curl -s 'http://localhost:8080/events/requests/req_smoke_gateway_1'
curl -s 'http://localhost:8080/events/failures'
curl -s http://localhost:8080/metrics
curl -s http://localhost:8000/metrics
```

## FAQ

### events 和 traces 是一回事吗

不是。当前项目用 events 训练可读证据，未来可以把它映射到 OpenTelemetry traces。

### metrics 能证明回答质量好吗

不能。metrics 证明运行状态，质量要看 eval report 和 sample analysis。

### 为什么要强调 request id

没有 request id，gateway、inference、eval 和 evidence 很难串成一次可复盘故事。
