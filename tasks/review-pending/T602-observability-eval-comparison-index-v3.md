Task ID: T602
Task Title: Observability / Evaluation Zero-Touch Pack
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
重点比较 Langfuse/Phoenix/Grafana-Prometheus/LM-Eval/HELM/BigCode Eval，不做营销式评分。

Result:

# Observability / Evaluation Comparison Index v3

## 定位比较

| 对象 | 定位 | 来源 |
|------|------|------|
| **Langfuse** | LLM 可观测性平台（tracing + metrics + prompt 管理） | https://langfuse.com/ |
| **Phoenix** | Arize 开源 LLM traces 分析工具 | https://github.com/Arize-AI/phoenix |
| **Grafana / Prometheus** | 指标存储与可视化标准组合 | https://grafana.com/ |
| **LM-Eval Harness** | 标准 benchmark 评测工具 | https://github.com/EleutherAI/lm-evaluation-harness |
| **Stanford HELM** | 综合评测框架，多场景覆盖 | https://crfm.stanford.edu/helm/ |
| **BigCode Eval** | 代码模型专用评测工具 | https://github.com/bigcode-project/bigcode-eval-harness |

## 所处层级比较

| 对象 | 所处层级 | 说明 | 来源 |
|------|---------|------|------|
| **Langfuse** | 平台层 | 端到端可观测性，数据存储和展示内置 | https://langfuse.com/ |
| **Phoenix** | 平台层 | traces 分析和 LLM-as-Judge | https://github.com/Arize-AI/phoenix |
| **Grafana / Prometheus** | 展示/存储层 | Prometheus 采集存储，Grafana 负责可视化 | https://grafana.com/ |
| **LM-Eval Harness** | 执行层 | 评测执行，不含数据存储 | https://github.com/EleutherAI/lm-evaluation-harness |
| **Stanford HELM** | 执行/展示层 | 评测执行 + 结果展示 | https://crfm.stanford.edu/helm/ |
| **BigCode Eval** | 执行层 | 代码评测执行 | https://github.com/bigcode-project/bigcode-eval-harness |

## 典型使用场景

| 对象 | 典型使用场景 | 来源 |
|------|-------------|------|
| **Langfuse** | LLM tracing + token 用量 + LLM-as-Judge | https://langfuse.com/docs/observability/overview |
| **Phoenix** | LLM trace 语义分析，prompt 调试 | https://docs.arize.com/phoenix/ |
| **Grafana / Prometheus** | 推理服务 QPS、延迟、GPU 利用率 | https://grafana.com/ |
| **LM-Eval Harness** | MMLU/GSM8K/HumanEval 等标准 benchmark | https://github.com/EleutherAI/lm-evaluation-harness |
| **Stanford HELM** | 学术研究，多场景综合评测 | https://crfm.stanford.edu/helm/ |
| **BigCode Eval** | 代码模型 HumanEval/MBPP Pass@K | https://github.com/bigcode-project/bigcode-eval-harness |

## 与本项目关系

| 对象 | 与 eval-module 关系 | 与 inference-service 关系 |
|------|------------------|----------------------|
| **Langfuse** | 评测结果上报 | tracing + token 用量 |
| **Phoenix** | 参考（trace 分析） | 参考 |
| **Grafana / Prometheus** | 评测资源监控 | metrics 可视化 |
| **LM-Eval Harness** | 主要评测执行工具 | 推理 backend |
| **Stanford HELM** | 参考架构 | 不直接相关 |
| **BigCode Eval** | 可选（代码模型） | 不直接相关 |

## MVP 适配性评估

| 对象 | MVP 适配性 | 说明 |
|------|-----------|------|
| **Langfuse** | 高 | 接入简单，LLM 原生支持 |
| **Phoenix** | 低 | 功能与 Langfuse 有重叠，非 MVP 必须 |
| **Grafana / Prometheus** | 中 | 指标可视化强，但需额外部署 |
| **LM-Eval Harness** | 高 | 主要评测工具，vLLM backend 支持好 |
| **Stanford HELM** | 低 | 偏学术，接入成本高 |
| **BigCode Eval** | 低（代码模型场景高） | 仅代码模型场景必须 |

## 工具组合建议（资料级）

```
可观测性组合：
Langfuse（tracing + token 用量）
    或
Prometheus + Grafana（metrics 可视化）
    或
Langfuse + Prometheus + Grafana（全量）

评测组合：
LM-Eval Harness（主要评测执行）← inference-service（vLLM/SGLang）
BigCode Eval（仅代码模型场景）
```

Sources:
1. https://langfuse.com/ — Langfuse
2. https://github.com/Arize-AI/phoenix — Phoenix
3. https://grafana.com/ — Grafana
4. https://prometheus.io/ — Prometheus
5. https://github.com/EleutherAI/lm-evaluation-harness — LM-Eval Harness
6. https://crfm.stanford.edu/helm/ — Stanford HELM
7. https://github.com/bigcode-project/bigcode-eval-harness — BigCode Eval

Risk of Staleness:
- Langfuse、lm-eval 版本更新快，API 以实际版本为准
- OTel 为 CNCF 标准，稳定性较高

Out of Scope Kept:
- 未写完整可观测性手册
- 未做厂商横评
- 未写日志存储相关
