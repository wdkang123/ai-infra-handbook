# SGLang 迁移对比

> 本页解决：SGLang 适合作为什么迁移目标，以及它和 vLLM 在教学上的差异。
> 读完能做：判断 SGLang 应该作为 serving 对比、结构化生成实验还是 agentic workload 迁移入口。
> 关联代码：`projects/inference-service`、`projects/ai-gateway`、`docs/02-inference-serving/05-sglang.md`。
> 验证命令：`PYTHON=.venv/bin/python make docs-quality`。

SGLang 暂时不要求完整实现。它在当前项目里的价值，是作为 vLLM 之外的真实 serving 迁移对比目标，让读者理解不同 runtime 在教学和工程边界上的差异。

## 它适合作为什么迁移目标

SGLang 可以作为三类目标：

| 目标 | 适合原因 | 当前阶段 |
| --- | --- | --- |
| OpenAI-compatible serving 对比 | 和当前 `/v1/chat/completions` 契约相近 | 先做设计 |
| 结构化生成 / constrained decoding 教学 | 适合解释生成控制和应用层需求 | 后续 lab |
| agentic workload / tool-use 路线 | 适合引出更复杂的执行图和 tracing | 后续迁移 |

当前不建议一上来把 SGLang 接成默认 backend。默认路径仍应是 mock，vLLM / SGLang 都作为可选真实路径。

## 和 vLLM 在教学上的差异

| 维度 | vLLM | SGLang |
| --- | --- | --- |
| 首要教学价值 | 高吞吐 serving、OpenAI-compatible server、runtime metrics | 结构化生成、程序化控制、agentic / multi-step workload |
| 读者第一感知 | “真实模型服务怎么替换 mock” | “复杂生成流程怎么表达和观测” |
| 最小迁移点 | adapter、model list、metrics、streaming | adapter、结构化请求、tool/span 设计 |
| 推荐章节 | serving backend migration、Prometheus metrics | tracing、tool call、structured output lab |
| 风险 | GPU / 模型门槛、指标版本漂移 | 概念更复杂，容易超出新手 quickstart |

所以教学顺序建议：

1. 先用 mock 跑通系统。
2. 再用 vLLM 理解真实 serving backend。
3. 再用 SGLang 引出结构化生成和更复杂 tracing。

## 暂不完整实现的原因

当前项目进入“公开增长态”时，优先级是：

- Quickstart 清楚
- 文档站可传播
- 首批 issue 可贡献
- vLLM / OTel / metrics / eval gate 的迁移锚点明确

如果此时同时完整接 vLLM 和 SGLang，读者可能还没跑通基础链路，就被环境和工具差异淹没。

更稳的做法是先补：

- SGLang 对比页
- SGLang lab 入口
- OpenAI-compatible contract 对照
- tracing / tool call 预留设计

## 最小 lab 入口

未来 SGLang lab 可以这样设计：

### 目标

用 SGLang 作为可选 backend，验证 `/v1/chat/completions`、`/v1/models`、streaming、request id 和 metrics / events 是否仍然可解释。

### 步骤

1. 启动 SGLang OpenAI-compatible server。
2. 设置 `INFERENCE_BACKEND=sglang` 和 `UPSTREAM_BASE_URL`。
3. 通过 gateway 发送带 `X-Request-ID` 的请求。
4. 查看 gateway events、inference events 和 backend metrics。
5. 对比 vLLM adapter 文档中的字段。

### 验收

- mock 默认路径不受影响
- gateway 仍然只暴露稳定外部模型名
- request id 能贯穿 gateway / inference / backend
- evidence packet 能记录 backend type
- 失败时能区分 model not found、upstream timeout、stream interruption

## 与 OpenTelemetry 的关系

SGLang 迁移更适合和 tracing 一起设计，因为它常常涉及更复杂的生成流程。

未来可以把 span 拆成：

```text
gateway.request
  -> inference.request
      -> sglang.program
          -> sglang.model_call
          -> genai.tool_call
```

但在没有真实实现前，不要为了好看伪造 trace。先在设计页里明确字段和边界。

## 推荐后续 issue

- 设计 SGLang OpenAI-compatible backend 配置样例
- 增加 SGLang 和 vLLM 的 request / response 字段对照
- 增加 structured output lab
- 增加 tool call tracing 设计
- 增加 SGLang 失败案例：结构化输出不符合 schema

## 外部参考

- [SGLang documentation](https://docs.sglang.ai/)
- [vLLM Adapter 设计](/12-production-migration/05-vllm-adapter-design)
- [OpenTelemetry GenAI Tracing 设计](/12-production-migration/06-opentelemetry-genai-tracing)
