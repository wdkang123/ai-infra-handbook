# inference-service

这是整个学习链路里最靠底层的一段：模型服务本体。

它现在不是完整推理框架，而是一套“足够你理解服务边界”的最小骨架，重点是让你看清楚：

- 服务如何暴露 `/health`
- 服务如何暴露 `/metrics`
- 服务如何暴露 `/events`
- 服务如何暴露 `/v1/models`
- OpenAI 风格的 `/v1/chat/completions` 最小需要什么
- 正常返回、流式返回和错误返回应该长什么样
- 一次请求结束后，服务侧能沉淀哪些运行态指标
- prompt token 和 completion token 为什么应该分开观察

## 先看哪里

- [main.py](src/inference_service/main.py)
- [server.py](src/inference_service/server.py)
- [engines.py](src/inference_service/engines.py)
- [runtime.py](src/inference_service/runtime.py)
- [config.py](src/inference_service/config.py)

## 先跑什么

```bash
cd projects/inference-service
PYTHONPATH=src ../../.venv/bin/python -m inference_service.main serve
```

默认是 `mock` engine。接入 OpenAI-compatible 后端时可以这样启动：

```bash
PYTHONPATH=src ../../.venv/bin/python -m inference_service.main serve \
  --engine openai-compatible \
  --engine-base-url http://localhost:9000/v1
```

## 你应该看到什么

- [http://localhost:8000/health](http://localhost:8000/health)
- [http://localhost:8000/metrics](http://localhost:8000/metrics)
- [http://localhost:8000/events](http://localhost:8000/events)
- [http://localhost:8000/v1/models](http://localhost:8000/v1/models)

`/events` 支持 `event_type`、`request_id` 和 `requested_model` 查询参数，例如：

```bash
curl -s 'http://localhost:8000/events?event_type=request_success&requested_model=Qwen/Qwen2.5-0.5B-Instruct'
curl -s 'http://localhost:8000/events/summary?event_type=request_success&requested_model=Qwen/Qwen2.5-0.5B-Instruct'
curl -s 'http://localhost:8000/events/requests?requested_model=Qwen/Qwen2.5-0.5B-Instruct'
curl -s 'http://localhost:8000/events/requests/req_demo_direct_1'
```

再发一条请求：

```bash
curl -s http://localhost:8000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"Qwen/Qwen2.5-0.5B-Instruct","messages":[{"role":"user","content":"Hi"}]}'
```

然后再看一次 `/metrics`，你会发现请求数、prompt token 数和 completion token 数已经变化了。当前 mock engine 使用轻量估算，不等于真实 tokenizer，但能先把 usage 边界表达清楚。

你也可以主动试一条错误路径：

```bash
curl -i -s http://localhost:8000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"unknown-model","messages":[{"role":"user","content":"Hi"}]}'
```

现在这层的错误也会按统一 `error` 结构返回。

你也可以试一条最小流式请求：

```bash
curl -N http://localhost:8000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"Qwen/Qwen2.5-0.5B-Instruct","messages":[{"role":"user","content":"Hi stream"}],"stream":true}'
```

这次你会看到的是 `text/event-stream` 风格输出，而不是一次性 JSON。

如果你想观察跨服务追踪最小长什么样，也可以自己传一个 request id：

```bash
curl -i -s http://localhost:8000/v1/chat/completions \
  -H 'X-Request-ID: req_demo_direct_1' \
  -H 'Content-Type: application/json' \
  -d '{"model":"Qwen/Qwen2.5-0.5B-Instruct","messages":[{"role":"user","content":"Hi"}]}'
```

你会在响应头里看到同一个 `x-request-id`。

## 这段代码现在解决什么

- 帮你理解推理服务最小 API 轮廓
- 帮你理解最小模型发现接口
- 帮你理解最近请求事件流
- 帮你理解请求计数和 token 计数这类运行态指标
- 帮你理解 prompt / completion token usage 的边界
- 帮你理解最小错误口径应该如何统一
- 帮你理解最小 streaming 事件流长什么样
- 帮你理解 request id 这类跨请求追踪信息应该放在哪里
- 给上层 gateway 和 eval 提供一个稳定下游
- 给真实 OpenAI-compatible 后端预留 adapter 边界

## 这段代码现在还没解决什么

- 没管理真实 vLLM / SGLang 进程生命周期
- 没有真实 tokenizer / batching / scheduling
- 还不是生产级错误处理
- 上层 gateway 虽然已经能做最小 streaming 透传，但还没做更复杂的背压、取消和重试
