# Serving 可观测性 Lab

## 学习目标

这个 lab 训练你理解“模型服务本体”最小应该暴露什么。

完成后你应该能说清楚：

- 一次 chat completion 请求如何进入服务
- 普通响应和 streaming 响应有什么差别
- `/metrics` 为什么不是装饰品
- prompt / completion token 为什么要分开观察
- `x-request-id` 为什么要保留
- engine adapter 失败为什么要映射成结构化错误
- `/events` 和 request timeline 如何帮助复盘

这不是一个“调用接口成功”的 lab，而是一个“用证据解释服务行为”的 lab。

## 前置知识

建议先读：

- [从请求到首个 Token](/01-llm-fundamentals/04-from-request-to-first-token)
- [Streaming、Batching、Metrics](/02-inference-serving/09-streaming-batching-metrics)
- [inference-service 项目页](/06-projects/01-inference-service)
- [API Surface 速查](/09-reference/05-api-surface)

## 代码入口

重点看这些文件：

- `projects/inference-service/src/inference_service/server.py`
- `projects/inference-service/src/inference_service/engines.py`
- `projects/inference-service/src/inference_service/runtime.py`
- `projects/inference-service/tests/test_api.py`

如果你只想先跑 lab，可以暂时不读完所有代码；但跑完后建议回到这些文件，把输出和实现连起来。

## 操作步骤

### 1. 启动服务

```bash
cd /path/to/ai-infra/projects/inference-service
PYTHONPATH=src ../../.venv/bin/python -m inference_service.main serve
```

打开：

- `http://localhost:8000/health`
- `http://localhost:8000/v1/models`
- `http://localhost:8000/metrics`

先记录 `/metrics` 里的请求数和 token 数。

你要确认：

- 服务是否 healthy
- 模型名是否符合预期
- 初始 request counters 是多少
- prompt / completion token counters 是否存在

### 2. 发送普通请求

```bash
curl -i -s http://localhost:8000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -H 'X-Request-ID: req_lab_serving_json_1' \
  -d '{"model":"Qwen/Qwen2.5-0.5B-Instruct","messages":[{"role":"user","content":"Hello serving lab"}]}'
```

观察：

- HTTP status
- 返回体里的 `choices`
- 返回体里的 `usage`
- 返回 header 里的 `x-request-id`
- `/metrics` 里的请求计数变化
- `usage.prompt_tokens` 与 `usage.completion_tokens` 如何随输入和输出变化

记录：

```text
request id:
status:
prompt tokens:
completion tokens:
metrics changed:
```

### 3. 查看事件

普通请求后查看：

```bash
curl -s 'http://localhost:8000/events?event_type=request_success'
curl -s 'http://localhost:8000/events/summary'
curl -s 'http://localhost:8000/events/requests/req_lab_serving_json_1'
```

观察：

- request id 是否能查到
- timeline 里是否有 request started / success
- summary 是否统计了模型或事件类型

这一步的意义是让你看到：响应返回只是结果之一，事件才是后续复盘的证据。

### 4. 发送 streaming 请求

```bash
curl -N http://localhost:8000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -H 'X-Request-ID: req_lab_serving_stream_1' \
  -d '{"model":"Qwen/Qwen2.5-0.5B-Instruct","messages":[{"role":"user","content":"Hello stream lab"}],"stream":true}'
```

观察：

- 每个事件都是 `data: ...`
- 最后有 `data: [DONE]`
- streaming 请求也会影响 metrics
- timeline 能否查到这次 request

再查：

```bash
curl -s 'http://localhost:8000/events/requests/req_lab_serving_stream_1'
```

重点解释：streaming 和普通响应共用同一个入口，但输出形态和错误语义不同。

### 5. 主动制造错误

```bash
curl -i -s http://localhost:8000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -H 'X-Request-ID: req_lab_serving_bad_model_1' \
  -d '{"model":"unknown-model","messages":[{"role":"user","content":"bad model"}]}'
```

观察：

- 状态码是 `404`
- 返回体是统一 `error` 结构
- failed metrics 会增加
- `/events` 中是否出现失败事件

再查：

```bash
curl -s 'http://localhost:8000/events/requests/req_lab_serving_bad_model_1'
```

你应该能说明：错误请求同样应该留下可复盘证据。

### 6. 主动制造校验错误

```bash
curl -i -s http://localhost:8000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -H 'X-Request-ID: req_lab_serving_empty_messages_1' \
  -d '{"model":"Qwen/Qwen2.5-0.5B-Instruct","messages":[]}'
```

观察：

- status 是否为 `422`
- 错误是否来自请求校验
- 这和 unknown model 的 `404` 有什么区别

## 关键观察点

### 服务层不做平台治理

`inference-service` 不负责 Bearer token 鉴权，也不负责外部模型名到内部目标的复杂映射。

这是刻意的分层：

- serving 层关注执行
- gateway 层关注治理

如果你在 serving 层加了大量平台策略，后面 gateway 的边界会变模糊。

### 普通响应和 streaming 共用入口

同一个 `/v1/chat/completions` 可以根据 `stream` 字段进入不同响应路径。

这说明 streaming 不是另一个业务接口，而是同一个生成请求的不同传输形态。

### Metrics 让服务从能跑变成能观察

如果没有 `/metrics`，你只能知道请求成功或失败。

有了 metrics，你开始能回答：

- 一共处理了多少请求
- 失败了多少
- 当前是否还有 running request
- prompt token 与 completion token 是否分别变化
- streaming 请求是否被计入

### Events 让服务从能观察变成能复盘

Metrics 看趋势，events 看具体事件。

当某个 request id 出问题时，你需要 timeline 这样的结构来回答：

- 它有没有进入服务
- 什么时候开始
- 什么时候失败
- 请求模型是什么
- 最终 status 是什么

## 扩展任务

任选一个完成：

1. 给 `InferenceMetrics` 增加一个新的计数，比如 streaming 请求总数。
2. 对比短 prompt 和长 prompt，解释 mock token 估算为什么只是学习用近似。
3. 给 `OpenAICompatibleEngine` 的 malformed response 路径增加更具体的测试。
4. 给 `/events/summary` 增加一个更适合 lab 观察的字段。
5. 给 lab 增加一个 request timeline 截图或 markdown 复盘模板。

每个扩展任务都要说明：

- 改哪些文件
- 新增或修改哪些测试
- 跑哪些验证命令
- 文档是否需要同步更新

## 验收标准

完成这个 lab 后，至少要能通过：

```bash
PYTHON=.venv/bin/python make infra-check
```

你还应该能回答：

- `inference-service` 为什么不做鉴权
- prompt token 和 completion token 为什么是两条不同成本线
- streaming 错误为什么不能完全等同普通 JSON 错误
- `x-request-id` 为什么对服务本身无业务意义，但对系统排障重要
- `/metrics` 和 `/events` 分别解决什么问题
- request timeline 如何帮助复盘一次失败

## Lab 复盘模板

完成后写下：

```text
我调用的请求：
我看到的 request id：
我观察到的 metrics 变化：
我查到的 events：
我制造的错误：
我对 serving 层边界的理解：
我下一步想改进的观测点：
```

这份复盘可以放进 [学习者工作簿](/14-workshop-kit/02-learner-workbook)。
