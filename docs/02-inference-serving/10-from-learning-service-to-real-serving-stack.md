# 从学习型服务到真实 Serving Stack

当前仓库里的 `inference-service` 是学习型服务。
它不是生产级 vLLM，也不是完整推理平台，但它并不“假”。

它的价值在于：用最小复杂度表达真实 serving stack 最重要的边界。

读到这里，读者自然会问：

- 如果我想接真实 vLLM/SGLang，下一步怎么走？
- 当前接口哪些要保留？
- 哪些 mock 细节可以替换？
- 替换后怎么确认没有把系统变成黑箱？

这页就是回答这个迁移问题。

## 当前学习型服务已经解决了什么

当前 `inference-service` 已经表达了 serving 系统的几个关键外壳：

| 能力 | 当前表达 |
| --- | --- |
| 服务健康 | `GET /health` |
| 模型发现 | `GET /v1/models` |
| Chat API | `POST /v1/chat/completions` |
| Streaming | SSE 风格 chunk |
| Metrics | `GET /metrics` |
| Structured events | `GET /events`、`GET /events/requests/{request_id}` |
| Request trace key | `x-request-id` |
| Token usage | `usage.prompt_tokens`、`usage.completion_tokens` |
| Engine adapter | mock 与 OpenAI-compatible engine 边界 |

这些东西不是装饰。
它们是后续接真实后端时最应该保住的边界。

## 它故意没有做满什么

学习型服务还没有完整实现：

- 真实 tokenizer 和 chat template
- 真实 GPU scheduler
- continuous batching
- prefix caching 指标
- KV Cache 内存管理
- cancellation / timeout / backpressure
- 多模型动态加载
- 完整 latency histogram
- 生产级 tracing 和日志保留策略

这不是缺陷，而是学习节奏控制。
如果一开始就把这些全部接满，读者会先被运行环境和硬件细节挡住，反而看不清服务边界。

## 迁移的核心原则

一句话：

> 保住外壳和观测，逐步替换内部执行。

也就是：

- API 不要先乱。
- request id 不要丢。
- metrics 不要退化。
- events 不要消失。
- mock 路径仍然可用。
- 新后端的错误必须进入结构化错误和 timeline。

如果接入真实框架后，用户更难排查、更难跑通、更难回退，那不是升级。

## 推荐迁移顺序

### 第一步：保留 mock engine

公开学习项目必须让没有 GPU、没有模型权重、没有本地 serving runtime 的读者也能跑通。

所以真实后端接入后，mock engine 仍然应该可用：

```bash
cd projects/inference-service
PYTHONPATH=src ../../.venv/bin/python -m inference_service.main serve --engine mock
```

mock 的价值不是模拟真实质量，而是提供稳定学习路径和测试基线。

### 第二步：接 OpenAI-compatible 后端

先不要急着把 vLLM/SGLang 的所有内部指标都塞进项目。
更稳的第一步是通过 OpenAI-compatible API 接入。

示例：

```bash
cd projects/inference-service
PYTHONPATH=src ../../.venv/bin/python -m inference_service.main serve \
  --engine openai-compatible \
  --engine-base-url http://localhost:8001/v1 \
  --engine-api-key local-engine-key \
  --model Qwen/Qwen2.5-0.5B-Instruct
```

这一阶段只确认：

- 普通请求能返回。
- streaming 能返回。
- 上游 4xx/5xx 能被映射。
- `x-request-id` 能透传或保留。
- `/metrics` 和 `/events` 仍然能解释请求。

### 第三步：明确 tokenizer / usage 语义

真实后端接入后，token usage 语义会变得更重要。

你要明确：

- usage 是否直接来自上游？
- 上游没有 usage 时是否本地估算？
- 本地估算使用哪个 tokenizer？
- streaming 场景是否有最终 usage？
- prompt/completion token 是否仍然分开？
- metrics 里的 token counters 是否和响应 usage 对齐？

不要让 `usage` 字段只是“看起来存在”。
如果语义不清楚，eval、cost、quota 和 release decision 都会被影响。

### 第四步：扩展真实错误路径

真实后端会带来 mock 没有的错误：

| 错误 | 应该怎么处理 |
| --- | --- |
| 上游连接失败 | 结构化 502，写入 events |
| 上游超时 | 结构化 timeout error，metrics 计数 |
| 上游 404 | 保留模型名错误语义 |
| 上游 429 | 不要和 gateway 自己的 rate limit 混淆 |
| streaming 中途断开 | SSE error event + timeline |
| 畸形 JSON | 结构化 bad gateway |
| usage 缺失 | 明确 fallback 估算或标记 unknown |

这些都应该能通过 request id 复盘。

### 第五步：再接 runtime-specific 指标

等基础边界稳定后，再考虑引入更真实的 vLLM/SGLang 指标：

- queue time
- prefill time
- decode time
- tokens/sec
- KV Cache usage
- batch size
- running / waiting requests
- prefix cache hit rate

这些指标很有价值，但不要在 API 边界还没稳定时就把复杂度拉满。

## 哪些接口迁移时优先不要动

这些接口是学习站和 gateway 的依赖面：

```text
GET  /health
GET  /v1/models
GET  /metrics
GET  /events
GET  /events/summary
GET  /events/requests
GET  /events/requests/{request_id}
POST /v1/chat/completions
```

这些字段也尽量保持：

```text
x-request-id
usage.prompt_tokens
usage.completion_tokens
usage.total_tokens
```

如果必须改，文档、API surface、case study、smoke 和 gateway 都要同步。

## 一个具体迁移场景

假设你要把当前 mock engine 替换为本地 vLLM。

建议不要直接把 gateway 改到 vLLM 地址。
更稳的做法是：

```text
client
  -> ai-gateway
  -> inference-service
  -> OpenAI-compatible vLLM backend
```

这样 `inference-service` 仍然承担学习站里的执行层边界：

- 统一错误格式
- 保留 request timeline
- 对齐 usage
- 暴露服务级 metrics
- 支持 mock 回退学习路径

等这层稳定后，再决定 gateway 是否直接支持多个 OpenAI-compatible upstream。

## 当前仓库相关文件

重点看：

```text
projects/inference-service/src/inference_service/server.py
projects/inference-service/src/inference_service/engines.py
projects/inference-service/src/inference_service/runtime.py
projects/inference-service/src/inference_service/config.py
projects/inference-service/tests/test_api.py
```

其中：

- `server.py` 表达 API 外壳。
- `engines.py` 表达 engine adapter 边界。
- `runtime.py` 表达 metrics/events。
- tests 表达迁移时不能破坏的行为。

## 不建议一开始做什么

### 不建议一口气接完整 GPU 资源管理

GPU 资源管理重要，但它会立刻引入部署、并发、显存、驱动和多卡复杂度。
学习项目更适合先接 OpenAI-compatible 后端。

### 不建议马上做多模型动态加载

多模型动态加载会把配置、状态、健康检查和资源隔离全部复杂化。
先把单后端迁移走稳。

### 不建议让真实后端绕过现有 observability

如果接入后只能看到“返回了文本”，而看不到 events、metrics 和 request timeline，那学习价值会下降。

### 不建议破坏 mock 路径

mock 是公开项目的低门槛入口。
它应该一直能跑。

## 验收清单

迁移后至少确认：

- [ ] mock engine 仍然可用
- [ ] OpenAI-compatible engine 普通请求可用
- [ ] OpenAI-compatible engine streaming 可用
- [ ] 上游错误会变成结构化错误
- [ ] streaming 错误会以 SSE error event 结束
- [ ] `x-request-id` 仍然贯穿
- [ ] `/metrics` 仍然能看到 request/token 变化
- [ ] `/events/requests/{request_id}` 仍然能复盘单次请求
- [ ] `PYTHON=.venv/bin/python make inference-test` 通过
- [ ] `PYTHON=.venv/bin/python make infra-smoke` 通过

## 文档同步点

如果真的接入新后端，需要同步更新：

- [inference-service](/06-projects/01-inference-service)
- [API Surface 速查](/09-reference/05-api-surface)
- [CLI Surface 速查](/09-reference/06-cli-surface)
- [验证矩阵](/09-reference/07-validation-matrix)
- [Serving / Gateway 输出证据](/13-output-gallery/01-serving-gateway-evidence)
- [请求失败排查案例](/11-case-studies/01-request-incident-walkthrough)

## 常见误区

### “接上真实 vLLM，这一层就完成了”

不够。
真实 serving 还要保错误、观测、usage、streaming 和回退路径。

### “学习型服务和真实系统是两套东西”

不准确。
学习型服务是结构预演，真实系统是在这些边界上替换内部实现。

### “真实后端自己有 metrics，本服务就不用 metrics”

不对。
后端 metrics 很重要，但服务层仍然要暴露和请求路径相关的指标与事件。

### “迁移时可以先删 mock”

不建议。
公开学习项目需要一个低门槛、可测试、可复现的默认路径。

## 学完应该能回答

读完这一页后，你应该能回答：

1. 当前 `inference-service` 哪些边界迁移时最应该保留？
2. 为什么先接 OpenAI-compatible 后端比一开始深入 runtime 内部更稳？
3. 真实后端接入后，usage 和 streaming 错误为什么要重新明确语义？
4. 为什么 mock engine 仍然有公开学习价值？
5. 一次 serving backend 迁移应该跑哪些验收命令？

## 继续阅读

- [Serving 后端迁移](/12-production-migration/01-serving-backend-migration)
- [vLLM 与 SGLang](/02-inference-serving/01-vllm-sglang)
- [Streaming、Batching、Metrics](/02-inference-serving/09-streaming-batching-metrics)
- [验证矩阵](/09-reference/07-validation-matrix)
