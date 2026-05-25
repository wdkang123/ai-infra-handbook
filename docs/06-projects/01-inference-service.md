# inference-service

这是整条学习链里最底层的部分，也就是“模型服务本体”。

你在这里最该学到的不是大而全的推理框架，而是最小服务边界：

- `/health` 是什么
- `/metrics` 是什么
- `/events` 为什么能解释最近请求路径
- `/v1/models` 为什么是最小模型发现接口
- `/v1/chat/completions` 最小长什么样
- 为什么同一个接口既可以一次性 JSON 返回，也可以做最小流式返回
- token usage 为什么应该区分 prompt 和 completion
- `x-request-id` 为什么值得保留下来

换句话说，`inference-service` 这一页最重要的，不是让你觉得“它已经是完整推理系统”，而是让你先把最小 serving 结构看明白。

只要这层结构清楚了，后面无论你是接真实 vLLM、SGLang，还是继续让别的大模型帮你细化实现，都会容易很多。

## 先看哪些代码

- `projects/inference-service/src/inference_service/main.py`
- `projects/inference-service/src/inference_service/server.py`
- `projects/inference-service/src/inference_service/engines.py`
- `projects/inference-service/src/inference_service/runtime.py`
- `projects/inference-service/src/inference_service/config.py`

## 先跑什么

```bash
cd /path/to/ai-infra/projects/inference-service
PYTHONPATH=src ../../.venv/bin/python -m inference_service.main serve
```

默认启动的是 `mock` engine。如果你已经有一个 OpenAI-compatible 的本地 vLLM/SGLang 服务，可以把这层切到 HTTP adapter：

```bash
PYTHONPATH=src ../../.venv/bin/python -m inference_service.main serve \
  --engine openai-compatible \
  --engine-base-url http://localhost:9000/v1
```

也可以在 `config.yaml` 里设置 `engine.type`、`engine.base_url` 和 `engine.api_key`。这条路径的目标不是让当前仓库立刻承担真实推理，而是把 API 层和执行层的边界先留正确。

当 OpenAI-compatible 上游返回 HTTP 错误、网络错误或畸形响应时，adapter 会把它转换成结构化的 engine error；非流式请求会返回 `502 bad_gateway_error`，这样调用方能区分“模型服务上游失败”和“本服务内部崩溃”。如果是 streaming 请求，服务会在 SSE 中发出结构化 `error` 事件再结束流，避免客户端只看到连接硬断。

如果你想把第一次观察做得更完整，建议按这个顺序：

1. 先看 `/health`
2. 再看 `/metrics`
3. 再打一条普通请求
4. 再打一条 `stream=true`
5. 最后再带一条 `X-Request-ID`

## 你应该观察什么

- `http://localhost:8000/health`
- `http://localhost:8000/metrics`
- `http://localhost:8000/events`
- `http://localhost:8000/v1/models`

模型列表：

```bash
curl -s http://localhost:8000/v1/models
```

最近请求事件：

```bash
curl -s 'http://localhost:8000/events?limit=20'
curl -s 'http://localhost:8000/events?event_type=request_success&requested_model=Qwen/Qwen2.5-0.5B-Instruct'
curl -s 'http://localhost:8000/events/summary?event_type=request_success&requested_model=Qwen/Qwen2.5-0.5B-Instruct'
curl -s 'http://localhost:8000/events/requests?requested_model=Qwen/Qwen2.5-0.5B-Instruct'
curl -s 'http://localhost:8000/events/requests/req_demo_direct_1'
```

`/events` 支持按 `event_type`、`request_id` 和 `requested_model` 过滤。`/events/summary` 会把过滤后的事件汇总成 `event_type_counts`、`requested_model_counts` 和 `engine_counts`。`/events/requests` 会列出最近请求 timeline 索引，`/events/requests/{request_id}` 则会把单条请求的事件串成 timeline，包含 `event_types`、`duration_seconds` 和终止事件。它适合在 metrics 之外复盘“刚刚这批请求整体走到了哪一步，以及某一条请求具体经历了什么”。

普通请求：

```bash
curl -s http://localhost:8000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"Qwen/Qwen2.5-0.5B-Instruct","messages":[{"role":"user","content":"Hi"}]}'
```

最小 streaming：

```bash
curl -N http://localhost:8000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"Qwen/Qwen2.5-0.5B-Instruct","messages":[{"role":"user","content":"Hi stream"}],"stream":true}'
```

带 request id：

```bash
curl -i -s http://localhost:8000/v1/chat/completions \
  -H 'X-Request-ID: req_demo_direct_1' \
  -H 'Content-Type: application/json' \
  -d '{"model":"Qwen/Qwen2.5-0.5B-Instruct","messages":[{"role":"user","content":"Hi"}]}'
```

这里最值得刻意观察的，不只是“返回成功了”，而是：

1. 为什么这层暴露的是最小服务接口，而不是平台治理逻辑
2. 为什么 streaming 和非 streaming 共享同一个主入口
3. 为什么 request id 这种 header 对业务结果无感，却对后面跨服务排障很重要
4. 为什么 `/events` 能让最近请求的 engine start / success / error 变得可复盘
5. 为什么 `/metrics` 的存在，会让这层从“能跑”提升到“可观察”

现在 mock engine 会用一个轻量 tokenizer 估算 prompt / completion token，而不是固定写死 token 数。  
它不等于真实模型 tokenizer，但能让你先看到这条边界：prompt token 代表输入处理成本，completion token 代表生成成本，二者应该分开观察。

## 这部分当前已经做到什么

- 最小服务骨架
- 动态 `health / metrics`
- 最小 `/events` 请求事件流、`/events/summary` 事件摘要、request timeline 索引和单请求 timeline
- 最小 `/v1/models` 模型列表
- 最小 chat completion
- 最小 SSE streaming
- 最小 `x-request-id`
- 可替换的 engine adapter 边界
- OpenAI-compatible HTTP adapter
- OpenAI-compatible 上游错误到 `502` 的结构化映射
- streaming 失败时的结构化 SSE error 事件
- mock engine 的 prompt / completion token 估算

也就是说，这层已经不只是一个 mock 接口，而是一个很合格的学习型 serving 骨架。

## 这部分当前还没做到什么

- 生产级 vLLM / SGLang 生命周期管理
- 真实 tokenizer / batching / scheduling
- 更完整的 streaming 取消逻辑和背压处理
- 生产级 tracing / logging

## 最适合的继续学习顺序

如果你已经把这页跑过一轮，下一步最推荐接着读：

1. [从请求到首个 Token](/01-llm-fundamentals/04-from-request-to-first-token)
2. [Streaming、Batching、Metrics](/02-inference-serving/09-streaming-batching-metrics)
3. [从学习型服务到真实 Serving Stack](/02-inference-serving/10-from-learning-service-to-real-serving-stack)

这样你会更容易从“会用这个服务”进入“看得懂它以后会怎么继续长”。
