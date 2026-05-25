Task ID: T316
Task Title: 产出 observability / evaluation comparison-index v2
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 T205/T310/T313，产出 observability/evaluation comparison-index v2，比较 OpenTelemetry、Langfuse、Phoenix、LM-Eval Harness、Stanford HELM 五个对象。

Result:

# Observability / Evaluation Comparison Index v2

## 比较对象

- OpenTelemetry
- Langfuse
- Phoenix
- LM-Eval Harness
- Stanford HELM

## 定位比较

| 对象 | 定位 | 来源 |
|------|------|------|
| **OpenTelemetry** | CNCF 标准，提供 traces/metrics 数据采集的规范和 SDK | https://opentelemetry.io/ |
| **Langfuse** | LLM 可观测性平台，支持 tracing、metrics、prompt 管理和 LLM-as-Judge | https://langfuse.com/ |
| **Phoenix** | Arize 开源可观测性库，专注 LLM traces 和 LLM-as-Judge | https://github.com/Arize-AI/phoenix |
| **LM-Eval Harness** | 标准 benchmark 评测工具，执行模型能力评测并输出量化分数 | https://github.com/EleutherAI/lm-evaluation-harness |
| **Stanford HELM** | 全面评测框架，执行评测并提供结果展示，覆盖多场景 | https://crfm.stanford.edu/helm/ |

## 所处层级比较

| 对象 | 所处层级 | 说明 | 来源 |
|------|---------|------|------|
| **OpenTelemetry** | 规范/采集层 | 标准化数据采集接口，数据流向可配置 | https://opentelemetry.io/ |
| **Langfuse** | 平台层 | 端到端可观测性平台，数据存储和展示均内置 | https://langfuse.com/ |
| **Phoenix** | 平台层 | traces 分析和 LLM-as-Judge 平台 | https://github.com/Arize-AI/phoenix |
| **LM-Eval Harness** | 框架层 | 执行 benchmark 评测的工具，输出原始分数 | https://github.com/EleutherAI/lm-evaluation-harness |
| **Stanford HELM** | 框架 + 展示层 | 评测框架兼结果展示，多场景覆盖 | https://crfm.stanford.edu/helm/ |

层级关系：
```
规范/采集层：OpenTelemetry（数据采集标准）
    ↓
平台层：Langfuse / Phoenix（observability 平台）
    ↓
框架层：LM-Eval Harness / Stanford HELM（evaluation 框架）
```

## 典型使用场景

| 对象 | 典型使用场景 | 来源 |
|------|-------------|------|
| **OpenTelemetry** | 需要统一采集 traces/metrics 并接入多种后端存储 | https://opentelemetry.io/ |
| **Langfuse** | LLM 应用需要 tracing + metrics + prompt 版本管理的完整可观测性 | https://langfuse.com/ |
| **Phoenix** | 需要 LLM 专用 traces 分析和 LLM-as-Judge 能力 | https://github.com/Arize-AI/phoenix |
| **LM-Eval Harness** | 在标准数据集（MMLU、GSM8K 等）上评测模型能力 | https://github.com/EleutherAI/lm-evaluation-harness |
| **Stanford HELM** | 全面评测模型在多场景下的综合表现 | https://crfm.stanford.edu/helm/ |

## 与本项目关系

| 对象 | 与本项目关系 | 来源 |
|------|------------|------|
| **OpenTelemetry** | inference-service 可通过 OTel SDK 采集运行时数据 | https://opentelemetry.io/ |
| **Langfuse** | eval-module 的评测结果可上报 Langfuse 做可观测性关联 | https://langfuse.com/ |
| **Phoenix** | 作为 traces 分析工具的参考，inference-service 可对接 | https://github.com/Arize-AI/phoenix |
| **LM-Eval Harness** | eval-module 评测工具的首选 | https://github.com/EleutherAI/lm-evaluation-harness |
| **Stanford HELM** | 作为全面评测框架参考，了解评测维度设计 | https://crfm.stanford.edu/helm/ |

Sources:
1. https://opentelemetry.io/ — OpenTelemetry 官网
2. https://langfuse.com/ — Langfuse 官网
3. https://github.com/Arize-AI/phoenix — Phoenix 主仓库
4. https://github.com/EleutherAI/lm-evaluation-harness — LM-Eval Harness 主仓库
5. https://crfm.stanford.edu/helm/ — Stanford HELM 官网

Risk of Staleness:
- Langfuse、TensorZero、Agenta 更新频繁，具体 API 以实际安装版本为准
- OpenTelemetry 为 CNCF 标准，稳定性较高
- LM-Eval Harness 版本更新可能影响 benchmark 兼容性

Out of Scope Kept:
- 未写完整手册
- 未做排名式结论
- 未写分布式训练相关

Need Codex Review On:
- inference-service 和 eval-module 中实际使用的可观测性和评测工具选型（以实际实现为准）
