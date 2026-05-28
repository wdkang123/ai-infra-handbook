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

## Lab 记录表

建议边跑边记录。
Serving lab 的重点不是请求成功，而是每个请求能不能留下可追踪证据。

| 请求 | request id | status | response 证据 | metrics 变化 | events/timeline | 备注 |
| --- | --- | --- | --- | --- | --- | --- |
| 普通 JSON | `req_lab_serving_json_1` |  | `choices`、`usage`、header |  |  |  |
| Streaming | `req_lab_serving_stream_1` |  | `data: ...`、`[DONE]` |  |  |  |
| Unknown model | `req_lab_serving_bad_model_1` |  | 统一 error |  |  |  |
| Empty messages | `req_lab_serving_empty_messages_1` |  | validation error |  |  |  |

跑完后，至少挑一条成功请求和一条失败请求，说明它们分别留下了哪些证据。

## 本 Lab 的最终交付物

完成后不要只留下终端输出。
建议产出一段短复盘：

```text
我证明了 inference-service 能处理普通请求和 streaming 请求。
成功请求的 request id 是：
我从 response 里看到：
我从 metrics 里看到：
我从 events timeline 里看到：
我制造的失败是：
这个失败属于：
我认为 serving 层不应该负责：
```

这段复盘的重点是把“调用成功”升级成“我知道服务暴露了哪些证据”。

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

一个好的解释应该像这样：

```text
这条普通请求返回了 200，并且响应 header 里的 x-request-id 等于我传入的 req_lab_serving_json_1。
metrics 中成功请求数和 token 计数发生变化，说明服务不仅返回了 body，也把请求计入运行指标。
events/requests/{id} 能查到 timeline，说明后续可以按 request id 复盘这次调用。
```

不要只写“接口正常”。
接口正常只是事实的一部分，指标和事件才让它变成可维护服务。

到这里，你应该能看到一组“前后变化”：

| 观察对象 | 请求前 | 请求后 |
| --- | --- | --- |
| `/metrics` request counter | 初始值 | 至少增加一次成功请求 |
| prompt token counter | 初始值 | 随输入文本增加 |
| completion token counter | 初始值 | 随 mock 输出增加 |
| `/events/requests/{id}` | 不存在或为空 | 能看到 request timeline |

如果响应成功但 metrics 或 events 没变化，要优先怀疑观测链路，而不是只看 API 返回体。

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

如果你要写复盘，建议明确写出：

```text
streaming 不是更快的普通响应，而是同一个生成请求的事件流传输方式。
我看到每个 chunk 以 data: 开头，最后通过 [DONE] 收尾。
这意味着服务在输出过程中已经把部分结果交给客户端，因此错误处理和普通 JSON 响应不同。
```

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

## 常见卡点

| 现象 | 可能原因 | 先检查 |
| --- | --- | --- |
| `/health` 正常但 completion 失败 | 模型名不在服务注册表里 | `/v1/models` 和请求体里的 `model` |
| 没有看到 `x-request-id` | 请求 header 没传，或响应头没有回传 | `curl -i` 是否打印 header |
| streaming 没有逐段输出 | curl 没用 `-N` 或终端缓冲 | 命令是否使用 `curl -N` |
| metrics 没变化 | 请求没有真正进入目标服务，或看的是旧输出 | 重新读取 `/metrics` 并记录前后值 |
| timeline 查不到 | request id 写错或请求失败路径没记录 | `/events/summary` 和具体 request id |
| 422 和 404 分不清 | 一个是请求校验失败，一个是业务对象不存在 | 对比 empty messages 和 unknown model |

这些卡点都适合写进复盘。
你真正要练的是：看到一个现象后，知道该找哪个证据，而不是直接猜原因。

## 常见错误结论

### “请求返回 200，所以服务可观测性没问题”

不够。
还要确认 metrics 和 events 是否同步记录了这次请求。

### “streaming 有输出，所以错误处理也没问题”

不一定。
streaming 的中途错误和普通 JSON 错误语义不同，需要单独测试。

### “usage 数字就是生产级 token 计费”

当前项目是学习型实现，usage 主要帮助你理解 prompt/completion 两条成本线。
真实后端接入后，还要确认 tokenizer 和 usage 来源。

### “404 和 422 都是请求失败，区别不重要”

区别很重要。
`404` 更像业务对象不存在，`422` 更像请求结构不合法。
错误语义清楚，调用方才知道该改模型名还是改请求体。

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
