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

## 前置知识

建议先读：

- [从请求到首个 Token](/01-llm-fundamentals/04-from-request-to-first-token)
- [Streaming、Batching、Metrics](/02-inference-serving/09-streaming-batching-metrics)
- [inference-service 项目页](/06-projects/01-inference-service)

## 代码入口

重点看这些文件：

- `projects/inference-service/src/inference_service/server.py`
- `projects/inference-service/src/inference_service/engines.py`
- `projects/inference-service/src/inference_service/runtime.py`
- `projects/inference-service/tests/test_api.py`

## 操作步骤

### 1. 启动服务

```bash
cd /path/to/ai-infra/projects/inference-service
PYTHONPATH=src ../../.venv/bin/python -m inference_service.main serve
```

打开：

- `http://localhost:8000/health`
- `http://localhost:8000/metrics`

先记录 `/metrics` 里的请求数和 token 数。

### 2. 发送普通请求

```bash
curl -s http://localhost:8000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -H 'X-Request-ID: req_lab_serving_json_1' \
  -d '{"model":"Qwen/Qwen2.5-0.5B-Instruct","messages":[{"role":"user","content":"Hello serving lab"}]}'
```

观察：

- 返回体里的 `choices`
- 返回 header 里的 `x-request-id`
- `/metrics` 里的请求计数变化
- `usage.prompt_tokens` 与 `usage.completion_tokens` 如何随输入和输出变化

### 3. 发送 streaming 请求

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

### 4. 主动制造错误

```bash
curl -i -s http://localhost:8000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"unknown-model","messages":[{"role":"user","content":"bad model"}]}'
```

观察：

- 状态码是 `404`
- 返回体是统一 `error` 结构
- failed metrics 会增加

## 关键观察点

### 观察点 1：服务层不做平台治理

`inference-service` 不负责 Bearer token 鉴权，也不负责外部模型名到内部目标的复杂映射。

这是刻意的分层：

- serving 层关注执行
- gateway 层关注治理

### 观察点 2：普通响应和 streaming 共用入口

同一个 `/v1/chat/completions` 可以根据 `stream` 字段进入不同响应路径。

这说明 streaming 不是另一个业务接口，而是同一个生成请求的不同传输形态。

### 观察点 3：metrics 让服务从“能跑”变成“能观察”

如果没有 `/metrics`，你只能知道请求成功或失败。  
有了 metrics，你开始能回答：

- 一共处理了多少请求
- 失败了多少
- 当前是否还有 running request
- prompt token 与 completion token 是否分别变化

## 扩展任务

任选一个完成：

1. 给 `InferenceMetrics` 增加一个新的计数，比如 streaming 请求总数。
2. 对比短 prompt 和长 prompt，解释 mock token 估算为什么只是学习用近似。
3. 给 `OpenAICompatibleEngine` 的 malformed response 路径增加更具体的测试。

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
