# Serving 后端迁移

这一页说明如何把 `inference-service` 从学习型 mock engine，逐步迁移到更真实的 OpenAI-compatible serving 后端。

这里不绑定某个具体后端版本。你可以把真实后端理解成：

- 本地 vLLM
- 本地 SGLang
- 远程 OpenAI-compatible 推理服务
- 公司内部统一模型服务

迁移目标不是“立刻变成生产平台”，而是让真实后端进入当前已有的服务边界，并继续可测试、可观察、可回退。

## 当前最应该保留的边界

当前 `inference-service` 已经保留了几个迁移时最重要的接口：

```text
POST /v1/chat/completions
GET  /v1/models
GET  /health
GET  /metrics
GET  /events
GET  /events/summary
GET  /events/requests
GET  /events/requests/{request_id}
```

这些接口服务于不同角色：

| 接口 | 谁会依赖 |
| --- | --- |
| `/v1/chat/completions` | gateway、eval、调用方 |
| `/v1/models` | gateway、学习者、模型发现 |
| `/health` | gateway health probe、部署检查 |
| `/metrics` | 运行态观察、公开证据 |
| `/events` | 请求复盘、case study |
| `/events/requests/{request_id}` | 单请求 timeline |

迁移真实后端时，优先不要动这些外壳。

## 第一阶段：保持 mock 路径可用

真实后端接入不应该破坏默认学习路径。

保留：

```bash
cd projects/inference-service
PYTHONPATH=src ../../.venv/bin/python -m inference_service.main serve --engine mock
```

原因很简单：

- 公开读者不一定有 GPU。
- 公开读者不一定有模型权重。
- CI 不应该依赖本地大模型服务。
- 文档里的第一次实操需要低门槛。
- mock 是测试错误路径和接口外壳的稳定基线。

所以 mock 不是临时残留，而是学习项目的可回退路径。

## 第二阶段：接 OpenAI-compatible 后端

先通过已有 adapter 接入真实后端：

```bash
cd projects/inference-service
PYTHONPATH=src ../../.venv/bin/python -m inference_service.main serve \
  --engine openai-compatible \
  --engine-base-url http://localhost:8001/v1 \
  --engine-api-key local-engine-key \
  --model Qwen/Qwen2.5-0.5B-Instruct
```

这一阶段重点验证：

- 普通请求能返回。
- streaming 能返回。
- request id 能保留。
- 上游 4xx/5xx 能映射成结构化错误。
- 上游 streaming error 能变成 SSE error event。
- `/metrics` 仍然更新。
- `/events/requests/{request_id}` 仍然可复盘。

先不要急着接所有 runtime-specific 指标。
先把基础路径走稳。

## 第三阶段：明确 Usage 和 Token 语义

真实后端接入后，usage 语义必须明确。

你需要决定：

| 问题 | 需要明确 |
| --- | --- |
| 上游返回 usage | 是否直接采用 |
| 上游不返回 usage | 是否估算，估算方式是什么 |
| streaming usage | 是否在最后 chunk 返回，或由本地累积 |
| tokenizer | 使用上游 tokenizer 还是本地 tokenizer |
| metrics | token counters 是否和响应 usage 对齐 |
| eval | sample summary 是否能解释 token usage |

如果 usage 不可信，后续会影响：

- cost
- quota
- performance analysis
- eval comparison
- release decision

所以 token usage 不是小字段。

## 第四阶段：扩展错误路径

真实后端带来的最大变化，往往不是“回答更真实”，而是错误路径更多。

需要覆盖：

| 错误路径 | 预期行为 |
| --- | --- |
| 上游连接失败 | 返回结构化 502，events 记录 engine error |
| 上游超时 | 返回 timeout / bad gateway，metrics 记录失败 |
| 上游 404 | 保留模型不存在语义 |
| 上游 429 | 不要和 gateway 自身 rate limit 混淆 |
| 上游 500 | 映射为结构化上游错误 |
| streaming 中途断开 | SSE error event + `[DONE]` |
| 上游 JSON 畸形 | 结构化 bad gateway |
| usage 缺失 | 明确估算或 unknown |

这些路径都应该有测试。
否则迁移只验证了 happy path。

## 第五阶段：补真实运行时指标

当基础路径稳定后，再逐步引入 runtime-specific 指标：

- queue time
- prefill time
- decode time
- TTFT
- ITL
- tokens/sec
- running / waiting requests
- batch size
- KV Cache usage
- prefix cache hit rate
- timeout count
- cancellation count

这些指标很有价值，但要分层暴露。
不要把下游后端的原始指标直接混成当前服务自己的指标。

一个稳妥做法是：

- 保留当前服务级 metrics。
- 新增 backend metrics 或 backend metadata。
- 在 events 中记录 upstream/backend 字段。
- 在 output gallery 里解释哪些字段来自服务层，哪些来自后端。

## 第六阶段：接 Gateway 联调

Serving 后端迁移不能只在 inference-service 内部看。

还要确认 gateway 路径：

```text
client
  -> ai-gateway
  -> inference-service
  -> real backend
```

重点验证：

- gateway `/health` 能反映 inference health。
- gateway `x-request-id` 能传到 inference。
- gateway events 和 inference events 能用同一 request id 串起来。
- gateway fallback 不会掩盖 inference 侧错误。
- gateway `/metrics` 和 inference `/metrics` 各自语义清楚。

这一步能避免“直接打 inference 成功，但平台入口不稳”。

## 当前仓库相关文件

重点文件：

```text
projects/inference-service/src/inference_service/server.py
projects/inference-service/src/inference_service/engines.py
projects/inference-service/src/inference_service/runtime.py
projects/inference-service/src/inference_service/config.py
projects/inference-service/tests/test_api.py
scripts/integration_smoke_test.sh
```

迁移时最常改：

- `engines.py`：新增或调整 backend adapter。
- `server.py`：保持 API 外壳和错误映射。
- `runtime.py`：扩展 metrics/events。
- tests：覆盖真实后端新增错误路径。
- smoke：覆盖 gateway/inference 联调。

## 不建议一开始做什么

不建议第一步就做：

- 多模型动态加载
- 完整 batching scheduler
- Kubernetes 部署
- GPU 多卡资源管理
- tokenizer/chat template/cache 全量一次接满
- 大规模性能压测

这些都重要，但应在边界稳定后逐步推进。

## 验收清单

迁移 PR 至少确认：

- [ ] mock engine 仍然可用
- [ ] OpenAI-compatible engine 普通请求可用
- [ ] OpenAI-compatible engine streaming 可用
- [ ] 上游错误会变成结构化错误
- [ ] 上游 streaming 错误会变成 SSE error event
- [ ] `x-request-id` 仍然贯穿
- [ ] `/metrics` 仍然能看到 request/token 变化
- [ ] `/events/requests/{request_id}` 仍然能复盘单次请求
- [ ] `PYTHON=.venv/bin/python make inference-test` 通过
- [ ] `PYTHON=.venv/bin/python make infra-smoke` 通过

## 应该更新的文档

如果真的接入了新后端，需要同步更新：

- [inference-service](/06-projects/01-inference-service)
- [API Surface 速查](/09-reference/05-api-surface)
- [CLI Surface 速查](/09-reference/06-cli-surface)
- [验证矩阵](/09-reference/07-validation-matrix)
- [请求失败排查案例](/11-case-studies/01-request-incident-walkthrough)
- [Serving / Gateway 输出证据](/13-output-gallery/01-serving-gateway-evidence)

## 常见误区

### “真实后端接入后，mock 就可以删掉”

不建议。
mock 是学习路径、CI 路径和低门槛复现路径。

### “只要 OpenAI-compatible API 能返回就完成迁移”

不够。
还要保留 usage、streaming error、metrics、events 和 gateway 联调。

### “后端自带 metrics，所以服务层不用管”

不对。
后端 metrics 和服务层 request timeline 解决的问题不同。

### “迁移后接口可以顺手重构”

要谨慎。
接口是学习站、gateway、eval 和 docs 的共同依赖面。

## 学完应该能回答

读完这一页后，你应该能回答：

1. Serving 后端迁移时哪些接口最应该保持稳定？
2. 为什么 mock engine 仍然应该保留？
3. OpenAI-compatible 后端接入后，usage 和 streaming 错误为什么要重新定义？
4. 真实后端会新增哪些错误路径？
5. 为什么迁移后必须通过 gateway 联调验证？

## 继续阅读

- [从学习型服务到真实 Serving Stack](/02-inference-serving/10-from-learning-service-to-real-serving-stack)
- [服务选型与取舍](/02-inference-serving/03-serving-tradeoffs)
- [Gateway 平台化加固](/12-production-migration/02-gateway-platform-hardening)
- [验证矩阵](/09-reference/07-validation-matrix)
