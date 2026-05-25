Task ID: T194
Task Title: 产出 Observability 章节初稿
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 T162 observability/evaluation 资料包，产出 Observability 章节初稿，使用完整 10 节结构，聚焦 tracing/logging/metrics/token usage。

Result:

# LLM Observability

## 1. 这是什么

LLM Observability（可观测性）关注推理过程中的运行时数据，帮助理解"系统做了什么、什么时候、耗时多久"。核心是 traces（调用链）、metrics（指标）、logs（日志）。

**与 Evaluation 的边界**：Observability 关注"系统行为"，Evaluation 关注"输出质量"。Observability 高点后需要 Evaluation 向下钻取质量。两者互补，不等同。

## 2. 为什么重要

在 AI Infra 推理服务中，可观测性是运维和迭代的基础：

1. **延迟定位**：通过 tracing 找到 TTFT/ITL 的具体瓶颈在哪个环节
2. **成本分析**：通过 token 用量统计了解各模型、各用户的消耗分布
3. **故障排查**：通过错误日志和 span 还原请求完整路径
4. **SLO 监控**：通过 P99 latency、错误率等指标建立服务等级目标

## 3. 核心原理

### Tracing（调用链追踪）
为每个请求生成唯一 trace ID，在各环节（Gateway → Router → 推理引擎 → Token 生成）记录 span。单次请求的完整调用链包含：prompt、response、token 数、延迟、环节耗时。

来源：https://opentelemetry.io/docs/concepts/observability-primer/#distributed-traces

### Metrics（指标聚合）
聚合指标关注整体表现：
- **QPS**：每秒请求数
- **P99 Latency**：99% 请求的最大延迟
- **Token 用量**：每分钟 token 数（TPM）
- **GPU Util**：GPU 利用率

来源：https://langfuse.com/docs/observability/overview

### Logging（日志）
原始请求/响应对，用于回溯和调试。生产环境通常只存储脱敏后的 prompt/response。

来源：https://github.com/Arize-AI/phoenix

### Token Usage（Token 用量）
记录每次请求消耗的 input/output token 数，是成本核算和 rate limiting 的基础。

来源：https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/

## 4. 常见方案 / 组件

| 工具 | 定位 | 官方入口 |
|------|------|---------|
| **Langfuse** | LLM 可观测性平台，tracing + metrics + prompt 管理 | https://langfuse.com/ |
| **TensorZero** | 开源 LLMOps 平台，统一 gateway + observability + evaluation | https://github.com/tensorzero/tensorzero |
| **Agenta** | 开源 LLMOps，prompt playground + evaluation + observability | https://github.com/agenta-ai/agenta |
| **Phoenix** | Arize 开源可观测性库，支持 LLM traces | https://github.com/Arize-AI/phoenix |
| **OpenTelemetry** | CNCF 标准，traces/metrics 规范和 SDK | https://opentelemetry.io/ |
| **Grafana + Prometheus** | 指标可视化，常与 Triton IS 等集成 | https://grafana.com/ |

来源：https://langfuse.com/docs/observability/overview
来源：https://github.com/Arize-AI/phoenix

## 5. 关键指标

| 指标 | 全称 | 说明 | 来源 |
|------|------|------|------|
| **TTFT** | Time To First Token | 首个 token 产出时间，反映 prefill 效率 | 各推理引擎 |
| **ITL** | Inter-Token Latency | 相邻 token 产出间隔，反映 decode 效率 | 各推理引擎 |
| **E2E Latency** | End-to-End Latency | 请求到响应的完整延迟 | Gateway/Tracer |
| **TPM** | Tokens Per Minute | 每分钟 token 消耗 | 用量统计 |
| **RPS** | Requests Per Second | 每秒请求数 | Metrics |
| **P99 Latency** | 99th Percentile Latency | 99% 请求的最大延迟 | Metrics |

来源：https://docs.vllm.ai/
来源：https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/

## 6. 常见误区

1. **"Tracing 等于 Metrics"**：Tracing 关注单个请求的完整路径，Metrics 关注聚合数值；需要两者结合才能完整理解系统
2. **"Observability 等于 Evaluation"**：Observability 描述系统行为（做了什么），Evaluation 评估输出质量（做得好不好）
3. **"有了 metrics 就不需要 tracing"**：Metrics 高点需要 tracing 向下钻取才能定位具体原因

## 7. 与项目关系

在 AI Infra 学习路径中，可观测性是连接各模块的横向能力：

- inference-service 提供 Prometheus metrics 端点，是可观测性的数据源之一
- ai-gateway 记录请求日志和 token 用量，是用量统计的主要来源
- eval-module 在推理请求上叠加评测，是 Observability → Evaluation 协作的典型场景

## 8. 最小实践任务

**目标**：使用 Langfuse 采集 vLLM 请求的 traces 和 metrics，验证可观测性数据正常上报。

```bash
# 1. 安装 Langfuse（SDK + self-hosted 或 cloud）
pip install langfuse

# 2. 启动 Langfuse（本地开发模式参考官方文档）
# https://langfuse.com/docs/observability/quick-start

# 3. 集成到 vLLM 请求（Python SDK 示例）
from langfuse import Langfuse
langfuse = Langfuse()

def call_llm(prompt):
    with langfuse.span(name="llm_call") as span:
        span.input = prompt
        response = call_vllm(prompt)  # 实际 vLLM 调用
        span.output = response
        return response

# 4. 查看 Langfuse dashboard
# 访问 http://localhost:3000 查看 traces
```

来源：https://langfuse.com/docs/observability/overview

## 9. 输出物

- Langfuse 服务运行中（本地或云端）
- vLLM 请求的 traces 和 metrics 上报到 Langfuse
- 可在 dashboard 查看 TTFT、ITL、token 用量等指标

## 10. 延伸阅读

1. https://langfuse.com/docs/observability/overview — Langfuse 可观测性文档
2. https://github.com/tensorzero/tensorzero — TensorZero 主仓库
3. https://github.com/Arize-AI/phoenix — Phoenix 主仓库
4. https://opentelemetry.io/ — OpenTelemetry 官网
5. https://github.com/EleutherAI/lm-evaluation-harness — LM-Eval Harness（evaluation 工具）
6. https://crfm.stanford.edu/helm/ — Stanford HELM（evaluation 平台）

Sources:
1. https://langfuse.com/docs/observability/overview — Langfuse 可观测性文档
2. https://github.com/tensorzero/tensorzero — TensorZero
3. https://github.com/Arize-AI/phoenix — Phoenix
4. https://opentelemetry.io/ — OpenTelemetry
5. https://github.com/EleutherAI/lm-evaluation-harness — LM-Eval Harness
6. https://crfm.stanford.edu/helm/ — Stanford HELM

Risk of Staleness:
- Langfuse、TensorZero 等工具更新频繁，具体 SDK API 以实际安装版本为准
- OpenTelemetry 为 CNCF 标准，稳定性较高

Out of Scope Kept:
- 未写完整 evaluation 章节
- 未做厂商横评
- 未写数据治理相关

Need Codex Review On:
- 最小实践是否需要完全基于开源工具，而非 Langfuse cloud
