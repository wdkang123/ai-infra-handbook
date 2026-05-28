# vLLM Adapter 设计

> 本页解决：如何把当前学习型 inference-service 逐步接到 vLLM，而不破坏现有学习契约。
> 读完能做：说清 mock backend 和 vLLM backend 的切换边界、接口保留项和验证命令。
> 关联代码：`projects/inference-service`、`projects/ai-gateway`、`scripts/integration_smoke_test.sh`。
> 验证命令：`PYTHON=.venv/bin/python make infra-smoke`。

vLLM adapter 的目标不是立刻把项目变成生产 serving 平台，而是把“真实模型服务后端”作为一个可选迁移路径接进来。默认路径仍然应该保留 mock backend，让没有 GPU 的读者也能完成学习。

## 为什么接 vLLM

vLLM 适合作为第一阶段真实 serving 迁移目标，原因是：

- 它提供 OpenAI-compatible server，和当前 `/v1/chat/completions`、`/v1/models` 学习契约接近。
- 它暴露 metrics，有助于把当前 Prometheus-style 指标映射到真实 runtime。
- 它让读者看到 mock engine 之外的真实 token generation、batching、KV cache、streaming 和模型列表。
- 它可以先作为 upstream backend 接入，而不是推倒现有 gateway / eval / evidence 结构。

这里的重点是“adapter”，不是“替换全部系统”。当前项目最有价值的部分是接口、观测、评测和证据链；vLLM 只是 serving 执行层的真实化候选。

## 必须保留的接口

迁移时优先保留这些外部契约：

| 当前契约 | 为什么不能轻易变 |
| --- | --- |
| `/v1/chat/completions` | gateway、eval 和 Quickstart 都依赖这个入口 |
| `/v1/models` | gateway model mapping 和读者验证依赖模型列表 |
| `/health` | smoke、Pages 文档和排障路径依赖健康检查 |
| `/metrics` | 输出证据库、Prometheus 对照表和观测 lab 依赖指标 |
| `/events` | 学习项目需要结构化事件解释请求发生了什么 |
| `x-request-id` | request id 是跨 gateway / inference 复盘主键 |
| `stream=true` | streaming 是 LLM serving 的核心行为 |
| OpenAI-compatible response shape | 上游工具和 eval runner 更容易复用 |

如果真实 vLLM 的返回字段和当前 mock 字段不同，adapter 应该做最小映射，而不是让调用方到处分支。

## Backend 切换方式

建议保留一个明确配置：

```text
INFERENCE_BACKEND=mock
INFERENCE_BACKEND=openai-compatible
INFERENCE_BACKEND=vllm
```

最小配置表：

| 配置 | 示例 | 用途 |
| --- | --- | --- |
| `INFERENCE_BACKEND` | `mock` / `vllm` | 选择内部执行路径 |
| `UPSTREAM_BASE_URL` | `http://localhost:8001/v1` | vLLM OpenAI-compatible endpoint |
| `UPSTREAM_METRICS_URL` | `http://localhost:8001/metrics` | 真实 runtime metrics |
| `MODEL` | `Qwen/Qwen2.5-0.5B-Instruct` | 当前对外模型或默认模型 |
| `UPSTREAM_TIMEOUT_SECONDS` | `30` | 上游超时边界 |

切换原则：

- 默认仍是 `mock`，保证新手 clone 后可跑。
- `vllm` 作为可选路径，文档要写明 GPU / 模型下载 / 端口要求。
- gateway 对外模型名不直接等于 vLLM 内部模型名，仍通过 mapping 进入。
- eval 不直接依赖 vLLM，只依赖 inference-service 或 gateway 的 OpenAI-compatible endpoint。

## `/v1/chat/completions` 对齐

当前学习项目需要保留：

- `model`
- `messages`
- `stream`
- `usage`
- `id`
- `choices`
- error mapping
- request id propagation

adapter 要处理的差异：

| 差异 | 处理方式 |
| --- | --- |
| vLLM 返回字段更丰富 | 保留原始字段，同时确保当前必要字段存在 |
| usage 字段来自真实 tokenization | 优先使用 vLLM usage，不再用 mock 估算 |
| streaming chunk 格式差异 | 转成当前 gateway 能透传和 smoke 能识别的 SSE |
| 上游错误不同 | 映射到稳定 error type 和 status code |
| timeout / cancellation | 写入 events，暴露到 failure summary |

## `/v1/models` 对齐

当前 `/v1/models` 对 gateway 很重要，因为它决定可路由模型。

建议 adapter 规则：

1. 从 vLLM `/v1/models` 获取真实模型列表。
2. 允许本地配置为模型加上 public alias。
3. gateway 继续只认识外部模型名，例如 `vllm-local`。
4. evidence packet 记录 public model、upstream model 和 backend type。

最小字段：

| 字段 | 来源 |
| --- | --- |
| `id` | 对外可见模型名或 alias |
| `object` | OpenAI-compatible model object |
| `owned_by` | 可以是 `local` / `vllm` |
| `upstream_model` | vLLM 内部模型名 |
| `backend` | `mock` / `vllm` |

## `/metrics` 对齐

真实 vLLM metrics 不应该直接替代当前学习指标，而应该并存：

| 指标层 | 作用 |
| --- | --- |
| inference-service adapter metrics | 当前服务视角：请求数、错误、usage、adapter timeout |
| vLLM runtime metrics | 真实执行视角：scheduler、KV cache、tokens、requests、latency |
| gateway metrics | 平台视角：auth、routing、fallback、cache、upstream health |

迁移初期可以先让 inference-service `/metrics` 暴露当前学习指标，同时在文档里说明如何查看 vLLM 原生 `/metrics`。后续再选择是否聚合。

## Events 如何记录

adapter 应新增或保留这些事件：

| event | 说明 |
| --- | --- |
| `request_received` | inference-service 收到请求 |
| `upstream_request_started` | adapter 开始请求 vLLM |
| `upstream_request_succeeded` | vLLM 返回成功 |
| `upstream_request_failed` | vLLM 返回错误或连接失败 |
| `request_success` | 最终返回给调用方成功 |
| `request_error` | 最终返回给调用方失败 |

每个事件至少保留：

- `request_id`
- `requested_model`
- `upstream_model`
- `backend`
- `duration_ms`
- `status_code`
- `error_type`

## 最小实施顺序

1. 抽象当前 mock engine 的 backend interface。
2. 增加 OpenAI-compatible upstream client。
3. 在 `INFERENCE_BACKEND=vllm` 时调用 vLLM。
4. 保留 mock 为默认。
5. 扩展 smoke：mock 路径必须继续通过，vLLM 路径可作为可选 job。
6. 扩展 evidence packet：记录 backend type 和 upstream metrics pointer。
7. 更新 Quickstart：普通用户仍用 mock，进阶用户看 vLLM lab。

## 验收标准

| 验收项 | 命令 |
| --- | --- |
| mock 默认路径仍可跑 | `PYTHON=.venv/bin/python make infra-smoke` |
| 文档链接有效 | `PYTHON=.venv/bin/python make docs-quality` |
| adapter 代码不破坏单测 | `PYTHON=.venv/bin/python make infra-check` |
| vLLM 可选路径可手动验证 | `INFERENCE_BACKEND=vllm PYTHON=.venv/bin/python make inference-serve` |

## 风险

- GPU / 模型下载会显著提高本地门槛。
- vLLM metrics 名称会随版本演进，文档必须写目标版本。
- 真实 token usage 可能和 mock 估算差异很大，eval / release brief 不应混用不可比数据。
- timeout、stream interruption、model not found 要先写失败案例，再扩大功能。

## 外部参考

- [vLLM documentation](https://docs.vllm.ai/)
- [vLLM OpenAI-compatible server](https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html)
