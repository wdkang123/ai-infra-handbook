# Serving 后端迁移

这一页说明如何把 `inference-service` 从学习型 mock engine，逐步迁移到更真实的 OpenAI-compatible serving 后端。

这里不绑定某个具体后端版本。你可以把后端理解成：

- 本地 vLLM
- 本地 SGLang
- 其他 OpenAI-compatible 推理服务

## 当前边界

当前 `inference-service` 已经保留了几个迁移时最重要的边界：

- `POST /v1/chat/completions`
- `GET /v1/models`
- `GET /health`
- `GET /metrics`
- `GET /events`
- `GET /events/requests/{request_id}`
- OpenAI-compatible engine adapter
- streaming error event

迁移时优先不要动这些外壳。

## 迁移顺序

### 第一步：保持 mock 路径可用

真实后端接入不应该破坏默认学习路径。

保留：

```bash
PYTHONPATH=src ../../.venv/bin/python -m inference_service.main serve --engine mock
```

原因很简单：公开学习项目必须让没有 GPU、没有本地模型服务的人也能跑通。

### 第二步：接 OpenAI-compatible 后端

使用现有 adapter：

```bash
PYTHONPATH=src ../../.venv/bin/python -m inference_service.main serve \
  --engine openai-compatible \
  --engine-base-url http://localhost:8001/v1 \
  --engine-api-key local-engine-key \
  --model Qwen/Qwen2.5-0.5B-Instruct
```

这一步先验证三件事：

- 普通请求能返回
- streaming 能返回
- 上游错误能被映射成结构化 `502` 或 SSE error event

### 第三步：补真实 usage 和 tokenizer 边界

当前 mock token usage 是学习型估算。  
真实后端接入后，应优先明确：

- usage 是否来自上游
- 上游没返回 usage 时是否估算
- prompt token 和 completion token 是否分开
- streaming 场景是否有最终 usage

不要让 usage 字段“看起来存在”，但语义不清楚。

### 第四步：扩展观测

真实后端会新增更多失败路径：

- 上游超时
- 连接失败
- 上游 4xx / 5xx
- streaming 中途断开
- 上游返回畸形 JSON

这些都应该进入：

- `/events`
- `/events/summary`
- `/events/requests/{request_id}`
- `/metrics`

## 不建议一开始做什么

不建议第一步就做：

- 多模型动态加载
- 完整 batching scheduler
- 复杂 GPU 资源管理
- Kubernetes 部署
- 真实 tokenizer、chat template、cache 全量一次接满

这些都重要，但它们会把学习主线冲散。

## 验收清单

- [ ] mock engine 仍然可用
- [ ] OpenAI-compatible engine 普通请求可用
- [ ] OpenAI-compatible engine streaming 可用
- [ ] 上游错误会变成结构化错误
- [ ] `x-request-id` 仍然贯穿
- [ ] `/metrics` 仍然能看到 request/token 变化
- [ ] `/events/requests/{request_id}` 仍然能复盘单次请求
- [ ] `inference-test` 通过
- [ ] `infra-smoke` 通过

## 应该更新的文档

如果真的接入了新后端，需要同步更新：

- [inference-service](/06-projects/01-inference-service)
- [API Surface 速查](/09-reference/05-api-surface)
- [CLI Surface 速查](/09-reference/06-cli-surface)
- [请求失败排查案例](/11-case-studies/01-request-incident-walkthrough)

## 一句话结论

Serving 迁移的关键，不是“尽快接上真实框架”，而是让真实框架进入已有服务边界，并且仍然可观测、可测试、可回退。
