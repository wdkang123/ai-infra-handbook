# MVP Sequencing Board v1

## Task ID: T805
## Task Title: Cross-Project Integration Prep Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T715 任务拆解，准备 MVP 实施排序板。

---

# MVP Sequencing Board v1

## 概述

本文档定义 MVP 阶段四个模块的实施排序，考虑模块间依赖关系。

---

## MVP 实施排序

| 顺序 | 模块 | 任务 | 依赖 |
|------|------|------|------|
| 1 | 基础设施 | T0-01 ~ T0-04 | — |
| 2 | inference-service | T1-01 ~ T1-07 | T0-01 |
| 3 | ai-gateway | T1-08 ~ T1-12 | T1-01, T1-07 |
| 4 | eval-module | T3-01 ~ T3-06 | T1-07 |
| 5 | finetune-demo | T4-01 ~ T4-06 | T3-03 |

---

## 详细排序

### 阶段 1：基础设施

```
T0-01 → T0-02 → T0-03 → T0-04
```

| 任务 | 内容 |
|------|------|
| T0-01 | 项目仓库骨架 |
| T0-02 | CI 基础 |
| T0-03 | README 初版 |
| T0-04 | 任务看板 |

---

### 阶段 2：推理核心

```
T1-01 → T1-02 → T1-05 → T1-06 → T1-03 → T1-04 → T1-07
```

| 任务 | 内容 | 前置 |
|------|------|------|
| T1-01 | inference-service MVP 设计 | — |
| T1-02 | vLLM 集成 | T1-01 |
| T1-05 | /health 健康检查 | T1-02 |
| T1-06 | /metrics 端点 | T1-02 |
| T1-03 | OpenAI 兼容 API | T1-06 |
| T1-04 | 模型加载 | T1-03 |
| T1-07 | 模型版本管理 | T1-04 |

---

### 阶段 3：Gateway

```
T1-08 → T1-09 → T1-10 → T1-11 → T1-12
                ↓
            T1-01（已完成）
```

| 任务 | 内容 | 前置 |
|------|------|------|
| T1-08 | ai-gateway MVP 设计 | — |
| T1-09 | 路由逻辑 | T1-08 |
| T1-10 | 鉴权中间件 | T1-08 |
| T1-11 | 限流中间件 | T1-08 |
| T1-12 | gateway → inference 串联 | T1-09, T1-10, T1-03 |

---

### 阶段 4：评测能力

```
T3-01 → T3-02 → T3-03 → T3-04 → T3-05 → T3-06
```

| 任务 | 内容 | 前置 |
|------|------|------|
| T3-01 | eval-module MVP 设计 | — |
| T3-02 | lm-eval 集成 | T3-01 |
| T3-03 | MMLU benchmark | T3-02 |
| T3-04 | GSM8K benchmark | T3-02 |
| T3-05 | 结果 JSON 持久化 | T3-03 |
| T3-06 | 历史结果对比 | T3-05 |

---

### 阶段 5：微调能力

```
T4-01 → T4-02 → T4-05 → T4-06
              ↓
          T3-03（已完成）
```

| 任务 | 内容 | 前置 |
|------|------|------|
| T4-01 | finetune-demo MVP 设计 | — |
| T4-02 | PEFT/LoRA 集成 | T4-01 |
| T4-05 | adapter 保存/加载 | T4-02 |
| T4-06 | 训练+评测串联 | T4-05, T3-03 |

---

## 可并行任务

| 并行组 | 任务 | 说明 |
|--------|------|------|
| A | T1-02, T4-01 | inference 和 finetune 设计可并行 |
| B | T1-08, T3-01 | gateway 和 eval 设计可并行 |
| C | T3-03, T3-04 | MMLU 和 GSM8K 可并行 |

---

## MVP 完成检查点

| 检查点 | 验证 |
|--------|------|
| 推理可跑 | T1-03, T1-04, T1-05, T1-06 完成 |
| Gateway 就绪 | T1-12 完成 |
| 评测可跑 | T3-03, T3-04 完成 |
| 微调可跑 | T4-02, T4-05 完成 |
| 串联验证 | T4-06 完成 |

---

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval

Risk of Staleness:
- 排序可能因实际执行情况调整

Out of Scope Kept:
- 未写详细排期
- 未写人员分工
