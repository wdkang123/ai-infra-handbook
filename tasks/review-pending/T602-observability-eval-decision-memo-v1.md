Task ID: T602
Task Title: Observability / Evaluation Zero-Touch Pack
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
围绕默认 observability 起步组合、evaluation 与 benchmark 职责分工、eval-module MVP 边界给出资料级输入。

Result:

# Observability / Evaluation Decision Memo v1

## 概述

本文档围绕 observability 和 evaluation 的关键决策点，给出资料级输入，帮助 Codex 做最终判断。

---

## 决策点一：默认 observability 起步组合

### 推荐组合（资料级）

| 阶段 | 推荐组合 | 理由 |
|------|---------|------|
| **MVP 快速验证** | Langfuse SDK | 接入简单，LLM 原生，pip install 即可 |
| **研发阶段** | Langfuse + vLLM /metrics | tracing + token 用量 + 基础 metrics |
| **生产准备** | Langfuse + Prometheus + Grafana | 全量可观测性 |

### 不推荐的起步组合

- **纯 OTel**：接入成本高，概念模型复杂，MVP 阶段是 overkill
- **纯 Grafana-Prometheus**：缺少 LLM 专用 tracing，metrics 能力不完整
- **纯 Phoenix**：功能与 Langfuse 有重叠，接入后需要维护两套

### 资料级建议

| 场景 | 推荐起步组合 |
|------|------------|
| MVP 快速验证 | Langfuse SDK |
| 需要 metrics 可视化 | Langfuse + Prometheus + Grafana |
| 长期架构 | OTel 作为采集标准，Langfuse/Prometheus 作为后端 |

来源：https://langfuse.com/docs/observability/overview
来源：https://opentelemetry.io/

---

## 决策点二：evaluation 与 benchmark 在项目里的职责分工

### 分工框架

| 组件 | 职责 | 核心能力 |
|------|------|---------|
| **eval-module** | 评测任务管理、结果记录、版本对比 | 评测编排、结果持久化、HeuristicEval / LLM-as-Judge |
| **lm-eval** | 具体 benchmark 执行（vLLM/SGLang backend） | MMLU/GSM8K/HumanEval 等数据集执行 |
| **benchmark** | 标准测试题，产出量化分数 | 分数本身（不负责执行） |

### 分工说明

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

### 资料级建议

- eval-module 与 lm-eval 是调用关系，不是替代关系
- eval-module 负责评测流程管理，lm-eval 负责具体执行

来源：https://github.com/EleutherAI/lm-evaluation-harness
来源：https://langfuse.com/docs/observability/overview

---

## 决策点三：eval-module MVP 边界

### MVP 必须包含

| 功能 | 说明 |
|------|------|
| **评测任务执行** | 调用 lm-eval 运行 benchmark |
| **结果持久化** | 评测结果保存为 JSON |
| **HeuristicEval** | 基于规则的评测（准确率、BLEU、Pass@K） |
| **基础接口** | `evaluate(dataset, model)` 接口 |

### MVP 不包含

| 功能 | 原因 |
|------|------|
| **LLM-as-Judge** | 需要外部 Judge 模型（GPT-4），增加复杂度和成本 |
| **评测结果上报 Langfuse** | MVP 简化，评测结果存本地 JSON 即可 |
| **评测结果对比 dashboard** | MVP 阶段手动对比 JSON 即可满足 |
| **自定义数据集管理** | MVP 使用 lm-eval 内置数据集 |

### 资料级建议

- MVP 阶段 eval-module 做"评测执行 + 结果存储"即可
- LLM-as-Judge 和 Langfuse 上报作为后续迭代项

来源：https://github.com/EleutherAI/lm-evaluation-harness

---

## 总结：资料级建议（不下结论）

| 决策点 | 建议方向 | 关键依据 |
|--------|---------|---------|
| observability 起步组合 | MVP 用 Langfuse，后续加 Prometheus | Langfuse 简单，metrics 需要 Grafana |
| eval vs benchmark 分工 | eval-module 管流程，lm-eval 管执行 | 分层明确，职责清晰 |
| eval-module MVP 边界 | 评测执行 + 结果 JSON，暂不上报 | 减少初期复杂度 |

---

## 需要 Codex 最终判断

1. **Langfuse self-hosted 是否在 MVP 必须**？还是云端即可？
2. **Prometheus + Grafana 是否在 MVP 引入**？
3. **LLM-as-Judge 是否在 MVP 包含**？

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
