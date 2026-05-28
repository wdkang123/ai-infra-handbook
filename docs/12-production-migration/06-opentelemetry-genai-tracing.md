# OpenTelemetry GenAI Tracing 设计

> 本页解决：如何把当前 request id / events / metrics 迁移到 OpenTelemetry GenAI tracing 思路。
> 读完能做：设计一张版本化字段映射表，并知道哪些字段不能直接写死。
> 关联代码：`projects/inference-service`、`projects/ai-gateway`、`scripts/integration_smoke_test.sh`。
> 验证命令：`PYTHON=.venv/bin/python make infra-smoke`。

OpenTelemetry GenAI tracing 的目标不是替代当前 events，而是把当前学习项目的结构化证据逐步对齐到更通用的可观测标准。迁移时应该先做设计和字段映射，再引入 SDK。

重要提醒：GenAI semantic conventions 可能仍处在 Development 或持续演进状态。项目里不要把字段名当成永远稳定的事实，应该记录 spec 版本、验证日期和映射来源。

## 当前证据模型

当前项目已经有几类可观测证据：

| 证据 | 位置 | 作用 |
| --- | --- | --- |
| `x-request-id` | gateway / inference response header | 串联一次请求 |
| `/events` | gateway / inference | 结构化事件列表 |
| `/events/requests/{request_id}` | gateway / inference | 单次请求时间线 |
| `/metrics` | gateway / inference | 聚合趋势 |
| eval reports | eval-module | 质量证据 |
| manifests | finetune-demo | 训练资产证据 |

OpenTelemetry 的加入应该让这些证据更容易进入 traces / metrics / logs，而不是让学习者失去当前直观入口。

## Span 设计

建议最小 span 结构：

```text
gateway.request
  -> gateway.auth
  -> gateway.route
  -> gateway.cache_lookup
  -> gateway.upstream_call
      -> inference.request
          -> inference.model_call
```

如果未来支持 tool call，可以扩展：

```text
inference.model_call
  -> genai.tool_call
```

## 字段映射

| 学习项目字段 | OTel 方向 | 说明 |
| --- | --- | --- |
| `request_id` | trace attribute / log correlation id | 保留当前 header，也写入 span attribute |
| `requested_model` | GenAI request model attribute | 对外模型名 |
| `upstream_model` | GenAI response / backend model attribute | 内部真实模型名 |
| `backend` | service / deployment attribute | `mock`、`vllm`、`sglang` |
| `prompt_tokens` | token usage attribute / metric | 优先使用真实 backend usage |
| `completion_tokens` | token usage attribute / metric | 和 eval 成本分析相关 |
| `duration_ms` | span duration / latency metric | 区分 gateway latency 和 model latency |
| `status_code` | span status / http attribute | HTTP 结果 |
| `error_type` | exception / error attribute | 保留学习项目稳定错误语义 |
| `fallback_used` | gateway span attribute | 平台治理信号 |
| `cache_status` | gateway span attribute | `hit` / `miss` / `bypass` |
| `tool_name` | tool call span attribute | 未来 tool call 路径 |

## Request id

当前 `x-request-id` 继续作为学习项目的主键。

迁移后建议：

- gateway 收到请求时生成或接受 `x-request-id`
- gateway span 写入 `request_id`
- gateway 调 inference 时继续传递 `x-request-id`
- inference span 写入同一个 `request_id`
- events 和 trace 都能按 request id 反查

这样即使读者还没有 tracing backend，也能用现有 `/events/requests/{request_id}` 学习。

## Model span

`inference.model_call` 是核心 span。它应该覆盖：

- 模型名
- backend type
- streaming / non-streaming
- token usage
- latency
- error
- finish reason

不要把 gateway 的平台延迟和模型执行延迟混成一个 span。gateway 可以包含 route、cache、fallback；model span 应尽量描述真实模型调用。

## Token usage

token usage 要区分来源：

| 来源 | 可用性 | 处理 |
| --- | --- | --- |
| mock estimate | 学习路径可用，但不代表真实 tokenization | 标记 `usage_source=mock_estimate` |
| vLLM usage | 更接近真实请求 | 标记 `usage_source=backend` |
| gateway cache hit | 可能没有真实上游调用 | 单独记录 cache status |
| streaming | usage 可能在最后 chunk 或最终汇总出现 | adapter 负责汇总 |

eval release decision 不应该混用不可比的 usage 来源。

## Latency

至少分三类：

- gateway total latency
- upstream call latency
- model generation latency

如果后续接 vLLM，真实 runtime 还可能暴露 scheduler / queue / prefill / decode 相关指标。OpenTelemetry span 可以先承载端到端时间，Prometheus metrics 再承载更细 runtime 指标。

## Error

错误映射要保留稳定语义：

| 场景 | 建议错误语义 |
| --- | --- |
| auth missing | `auth_error` |
| unknown model | `model_not_found` |
| upstream timeout | `upstream_timeout` |
| upstream connection error | `upstream_connection_error` |
| backend returned 5xx | `upstream_error` |
| stream interrupted | `stream_interrupted` |
| eval regression | 不作为 request error，进入 release gate |

span status 可以是错误，但 events 仍要保留，因为 events 更适合学习者阅读。

## Tool call

当前项目还没有完整 tool call 执行链。设计上先预留：

- `tool_call_id`
- `tool_name`
- `tool_arguments_size`
- `tool_duration_ms`
- `tool_error_type`
- `model_request_id`

不要在没有真实 tool runtime 的情况下伪造复杂 trace。可以先在迁移路线中说明，等 gateway / agent layer 扩展后再落地。

## 版本化映射

建议新增一张维护表：

| 字段 | 当前项目字段 | OTel GenAI 字段 | Spec 状态 | 验证日期 |
| --- | --- | --- | --- | --- |
| request id | `request_id` | 待确认 | Development / Stable 以官方为准 | 2026-05-28 |
| model | `requested_model` | 待确认 | Development / Stable 以官方为准 | 2026-05-28 |
| token usage | `usage.prompt_tokens` | 待确认 | Development / Stable 以官方为准 | 2026-05-28 |

这张表进入代码前必须查官方文档。不要只凭博客或二手资料写死字段名。

## 最小实施顺序

1. 先在文档中固定 span 结构和字段映射。
2. 给 events 增加 `trace_id` / `span_id` 可选字段，但默认可为空。
3. 选择 OpenTelemetry SDK 并加最小 tracing exporter。
4. 保持 `/events` 和 `/metrics` 不变。
5. 扩展 smoke：验证 request id 仍能贯穿。
6. 扩展 evidence packet：记录 trace config 和 sample trace pointer。

## 外部参考

- [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/)
- [OpenTelemetry semantic conventions](https://opentelemetry.io/docs/specs/semconv/)
