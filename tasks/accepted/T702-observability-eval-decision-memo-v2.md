Task ID: T702
Task Title: Observability / Evaluation Deep-Research Pack
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
围绕默认 observability 起步组合、eval-module 边界、哪些内容不该进入 MVP，做资料级收紧。

Result:

# Observability / Evaluation Decision Memo v2

## 概述

本文档在 v1 基础上进一步收紧 observability 和 evaluation 的关键决策点，给出资料级输入，帮助 Codex 做最终判断。

---

## 决策点一：默认 observability 起步组合（收紧）

### 推荐组合（v2 收紧）

| 阶段 | 推荐组合 | 收紧理由 |
|------|---------|---------|
| **MVP 快速验证** | Langfuse SDK | 接入最简单，LLM 原生 |
| **研发阶段** | Langfuse + vLLM /metrics | tracing + token 用量 + 基础 metrics |
| **生产准备** | Langfuse + Prometheus + Grafana | 全量可观测性 |

### 不推荐的起步组合（v2 收紧）

- **纯 OTel**：接入成本高，概念模型复杂，MVP 阶段是 overkill
- **纯 Grafana-Prometheus**：缺少 LLM 专用 tracing，metrics 能力不完整
- **纯 Phoenix**：功能与 Langfuse 有重叠，接入后需要维护两套

### 资料级建议（v2 收紧）

| 场景 | 推荐起步组合 |
|------|------------|
| MVP 快速验证 | Langfuse SDK |
| 需要 metrics 可视化 | Langfuse + Prometheus + Grafana |
| 长期架构 | OTel 作为采集标准，Langfuse/Prometheus 作为后端 |

来源：https://langfuse.com/docs/observability/overview
来源：https://opentelemetry.io/

---

## 决策点二：evaluation 与 benchmark 职责分工（收紧）

### 分工框架（v2 收紧）

| 组件 | 职责 | 核心能力 |
|------|------|---------|
| **eval-module** | 评测任务管理、结果记录、版本对比 | 评测编排、结果持久化 |
| **lm-eval** | 具体 benchmark 执行（vLLM/SGLang backend） | MMLU/GSM8K/HumanEval 等数据集执行 |
| **benchmark** | 标准测试题，产出量化分数 | 分数本身（不负责执行） |

### 分工说明（v2 收紧）

- **eval-module** 是评测任务管理层，不直接跑 benchmark
- **lm-eval** 是评测执行层，负责在具体数据集上运行模型
- **eval-module** 通过调用 **lm-eval** 的 Python API 完成评测

```
eval-module（任务管理）
    ↓ 调用
lm-eval（评测执行）← inference-service（vLLM/SGLang）
    ↓
评测结果 → eval-module 持久化
```

来源：https://github.com/EleutherAI/lm-evaluation-harness

---

## 决策点三：eval-module MVP 边界（收紧）

### MVP 必须包含（v2 收紧）

| 功能 | 说明 |
|------|------|
| **评测任务执行** | 调用 lm-eval 运行 benchmark |
| **结果持久化** | 评测结果保存为 JSON |
| **HeuristicEval** | 基于规则的评测（准确率、BLEU、Pass@K） |
| **基础接口** | `evaluate(dataset, model)` 接口 |

### MVP 不包含（v2 收紧）

| 功能 | 收紧原因 |
|------|---------|
| **LLM-as-Judge** | 需要外部 Judge 模型（GPT-4），增加复杂度和成本 |
| **评测结果上报 Langfuse** | MVP 简化，评测结果存本地 JSON 即可 |
| **评测结果对比 dashboard** | MVP 阶段手动对比 JSON 即可满足 |
| **自定义数据集管理** | MVP 使用 lm-eval 内置数据集 |
| **多 benchmark 自动调度** | MVP 手动指定即可 |

### 资料级建议（v2 收紧）

- MVP 阶段 eval-module 做"评测执行 + 结果存储"即可
- LLM-as-Judge 和 Langfuse 上报作为后续迭代项

来源：https://github.com/EleutherAI/lm-evaluation-harness

---

## 决策点四：Langfuse self-hosted vs 云端（新增）

### 选型对比

| 维度 | Self-hosted | Cloud |
|------|-------------|-------|
| **数据控制** | 完全自主 | 部分在第三方 |
| **运维复杂度** | 高（需维护 DB/存储） | 低（托管服务） |
| **成本** | 基础设施成本 | 订阅费用 |
| **适用** | 数据敏感场景 | 快速启动 |

### 资料级建议

| 场景 | 推荐 |
|------|------|
| MVP 快速验证 | Langfuse Cloud（无需运维） |
| 数据敏感 / 合规要求 | Self-hosted |
| 长期生产 | Self-hosted（自建或云端私有部署） |

来源：https://langfuse.com/docs/

---

## 总结：资料级建议（v2 收紧，不下结论）

| 决策点 | 建议方向 | 收紧程度 |
|--------|---------|---------|
| observability 起步组合 | MVP 用 Langfuse SDK | 明确 |
| Langfuse 部署方式 | MVP 用 Cloud，后续按需 | 明确 |
| eval vs benchmark 分工 | eval-module 管流程，lm-eval 管执行 | 明确 |
| eval-module MVP 边界 | 评测执行 + 结果 JSON，暂不上报 | 明确 |

---

## 需要 Codex 最终判断

1. **Langfuse Cloud 是否在 MVP 必须**？还是 self-hosted 可接受？
2. **Prometheus + Grafana 是否在 MVP 引入**？
3. **LLM-as-Judge 是否在 MVP 包含**？
4. **eval-module 结果是否上报 Langfuse**？

Sources:
1. https://langfuse.com/docs/observability/overview — Langfuse
2. https://opentelemetry.io/ — OpenTelemetry
3. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval
4. https://grafana.com/ — Grafana
5. https://prometheus.io/ — Prometheus

Risk of Staleness:
- Langfuse SDK 更新快，具体 API 以实际版本为准
- 各推理引擎 metrics 格式可能随版本变化

Out of Scope Kept:
- 未写代码实现
- 未写完整监控告警配置
- 未写评测结果数据库持久化
