Task ID: T162
Task Title: 搜集 observability/evaluation 官方资料与核心链接
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
搜集 LLM observability / tracing / evaluation 在 AI Infra 中的资料包，包含术语边界、代表性实现、官方入口、核心能力、优先阅读链接。

Result:

## 一、术语边界说明

**Observability（可观测性）** 和 **Evaluation（评测）** 是 LLM 系统两个不同维度：

### Observability（可观测性）
关注推理过程中的**运行时数据**，核心是 traces（调用链）、metrics（指标）、logs（日志）。目标是回答"系统做了什么、什么时候、耗时多久"。

- **Tracing**：单次请求的完整调用链，包含 prompt、response、token 数、延迟
- **Metrics**：聚合指标，如 QPS、P99 latency、token 用量、错误率
- **Feedback**：用户对模型输出的反馈（ thumbs up/down、评分）
- **Prompt/Response 存储**：原始输入输出对，用于回溯和再分析

### Evaluation（评测）
关注模型输出的**质量评估**，目标是回答"模型回答得好不好"。

- **Heuristic Evals**：基于规则的评测（Rouge、BLEU、准确率）
- **LLM-as-Judge**：用强模型评估弱模型输出
- **Benchmark Evals**：在标准数据集（MMLU、GSM8K 等）上测模型能力
- **Replay/回放**：用真实流量重放，验证新版本模型质量

**边界**：Observability 关注"系统行为"，Evaluation 关注"输出质量"。两者互补，observability 高点后需要 evaluation 向下钻取质量。

## 二、代表性开源/产品实现

### Observability
| 实现 | 官方入口 |
|------|---------|
| **Langfuse** | https://langfuse.com/ |
| **TensorZero** | https://github.com/tensorzero/tensorzero |
| **Agenta**（含 evaluation） | https://github.com/agenta-ai/agenta |
| **Phoenix（ Arize）** | https://github.com/Arize-AI/phoenix |
| **OpenTelemetry** | https://opentelemetry.io/ |
| **Grafana + Loki** | https://grafana.com/ |

### Evaluation
| 实现 | 官方入口 |
|------|---------|
| **EleutherAI LM-Eval Harness** | https://github.com/EleutherAI/lm-evaluation-harness |
| **BigCode Evaluation Harness** | https://github.com/bigcode-project/bigcode-eval-harness |
| **Stanford HELM** | https://crfm.stanford.edu/helm/ |
| **LMSYS Chatbot Arena** | https://chat.lmsys.org/ |

## 三、官方主页 / GitHub / 文档

1. **Langfuse**：https://langfuse.com/ — LLM 可观测性平台，支持 tracing、metrics、prompt 版本管理
2. **TensorZero**：https://github.com/tensorzero/tensorzero — 开源 LLMOps 平台，统一 gateway + observability + evaluation
3. **Agenta**：https://github.com/agenta-ai/agenta — 开源 LLMOps，prompt playground + evaluation + observability
4. **Phoenix**：https://github.com/Arize-AI/phoenix — Arize 开源可观测性库，支持 LLM traces
5. **LM-Eval Harness**：https://github.com/EleutherAI/lm-evaluation-harness — 标准 benchmark 评测工具
6. **OpenTelemetry**：https://opentelemetry.io/ — 行业标准 traces/metrics 规范，CNCF 项目

## 四、核心能力对比

| 工具 | Tracing | Metrics | Evals | Prompt管理 | LLM-as-Judge |
|------|---------|---------|-------|-----------|-------------|
| Langfuse | 是 | 是 | 是 | 是 | 是 |
| TensorZero | 是 | 是 | 是 | 是 | 是 |
| Agenta | 是 | 是 | 是 | 是 | 是 |
| Phoenix | 是 | 是 | 部分 | 否 | 是 |
| LM-Eval Harness | 否 | 否 | 是 | 否 | 外部接入 |

## 五、精确优先阅读链接（7 个）

1. **Langfuse 官方文档**：https://langfuse.com/docs/observability/overview
2. **TensorZero GitHub**：https://github.com/tensorzero/tensorzero
3. **Agenta GitHub**：https://github.com/agenta-ai/agenta
4. **Phoenix GitHub**：https://github.com/Arize-AI/phoenix
5. **LM-Eval Harness GitHub**：https://github.com/EleutherAI/lm-evaluation-harness
6. **OpenTelemetry 官方**：https://opentelemetry.io/
7. **Stanford HELM**：https://crfm.stanford.edu/helm/

Sources:
1. https://langfuse.com/docs/observability/overview — Langfuse 可观测性文档
2. https://github.com/tensorzero/tensorzero — TensorZero 主仓库
3. https://github.com/agenta-ai/agenta — Agenta 主仓库
4. https://github.com/Arize-AI/phoenix — Phoenix 主仓库
5. https://github.com/EleutherAI/lm-evaluation-harness — LM-Eval 主仓库
6. https://opentelemetry.io/ — OpenTelemetry 官网
7. https://crfm.stanford.edu/helm/ — Stanford HELM 官网

Risk of Staleness:
- Langfuse、TensorZero、Agenta 均为活跃项目，功能迭代快
- LM-Eval Harness 版本更新影响 benchmark 兼容性
- OpenTelemetry 为 CNCF 标准，稳定性较高

Out of Scope Kept:
- 未写完整章节
- 未做评测排名
- 未写训练相关
