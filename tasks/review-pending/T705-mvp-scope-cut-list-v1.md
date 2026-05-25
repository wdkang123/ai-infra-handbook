# MVP Scope Cut List v1

## Task ID: T705
## Task Title: Execution Decomposition Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
把后续实施拆成若干工作流，便于 Codex 继续分发。

---

# MVP Scope Cut List v1

## 概述

本文档明确 MVP 阶段必须完成和可选裁剪的任务，便于控制范围。

---

## MVP 范围定义

**MVP 目标**：完成基础推理 + 评测 + 微调串联，最小可用闭环。

**不追求**：
- 生产级高可用
- 完整可观测性
- DPO/强化学习等高级微调

---

## MVP 必须（Must Have）

### 基础设施（4/4）
| 任务 ID | 任务 | 原因 |
|---------|------|------|
| T0-01 | 项目仓库骨架 | 其他所有任务的基础 |
| T0-02 | CI 基础 | 代码质量保障 |
| T0-03 | README 初版 | 文档是 MVP 一部分 |
| T0-04 | 任务看板 | 任务跟踪必须 |

### 推理核心（7/7）
| 任务 ID | 任务 | 原因 |
|---------|------|------|
| T1-01 | inference-service MVP 设计 | 架构设计先行 |
| T1-02 | vLLM 集成 | 推理引擎就绪 |
| T1-03 | OpenAI 兼容 API | 标准化接口 |
| T1-04 | 模型加载 | 核心功能 |
| T1-05 | /health 健康检查 | 可用性保障 |
| T1-06 | /metrics 端点 | 基础监控 |
| T1-07 | 模型版本管理 | 迭代基础 |

### Gateway（5/5）
| 任务 ID | 任务 | 原因 |
|---------|------|------|
| T1-08 | ai-gateway MVP 设计 | 架构设计先行 |
| T1-09 | 路由逻辑 | 核心功能 |
| T1-10 | 鉴权中间件 | 安全性必须 |
| T1-11 | 限流中间件 | 稳定性必须 |
| T1-12 | 端到端串联 | 验证全链路 |

### 评测能力（6/6）
| 任务 ID | 任务 | 原因 |
|---------|------|------|
| T3-01 | eval-module MVP 设计 | 架构设计先行 |
| T3-02 | lm-eval 集成 | 核心依赖 |
| T3-03 | MMLU benchmark | 评测基准 |
| T3-04 | GSM8K benchmark | 评测基准 |
| T3-05 | 结果 JSON 持久化 | 结果可追溯 |
| T3-06 | 历史结果对比 | 迭代对比 |

### 微调能力（4/7）
| 任务 ID | 任务 | 原因 |
|---------|------|------|
| T4-01 | MVP 设计文档 | 架构设计先行 |
| T4-02 | PEFT/LoRA 集成 | 核心微调方法 |
| T4-05 | adapter 保存/加载 | 训练产物管理 |
| T4-06 | 训练+评测串联 | 验证微调效果 |

---

## MVP 可选（Nice to Have）

### 微调能力（3/7）
| 任务 ID | 任务 | 裁剪原因 |
|---------|------|---------|
| T4-03 | QLoRA 集成 | MVP 可用标准 LoRA |
| T4-04 | SFTTrainer 集成 | 后续引入 |
| T4-07 | Unsloth 加速 | 硬件依赖 |

### 可观测性（0/5）
| 任务 ID | 任务 | 裁剪原因 |
|---------|------|---------|
| T2-02 | Prometheus 部署 | MVP 只需 metrics 端点 |
| T2-03 | Grafana dashboard | 后续引入 |
| T2-04 | Langfuse SDK 埋点 | trace 后续引入 |
| T2-05 | gateway tracing | token 计量后续引入 |

---

## MVP 范围统计

| 类别 | 必须 | 可选 | MVP 必须比例 |
|------|------|------|------------|
| 基础设施 | 4 | 0 | 100% |
| 推理核心 | 7 | 0 | 100% |
| Gateway | 5 | 0 | 100% |
| 评测能力 | 6 | 0 | 100% |
| 微调能力 | 4 | 3 | 57% |
| 可观测性 | 0 | 5 | 0% |
| **合计** | **26** | **8** | **76%** |

---

## MVP 后续阶段（Post-MVP）

### Phase 2+：可观测性增强
- Prometheus/Grafana 部署
- Langfuse 全链路 tracing
- 日志采集

### Phase 3+：评测增强
- 更多 benchmark 引入
- LLM-as-Judge
- 评测结果上报 Langfuse

### Phase 4+：微调增强
- QLoRA 引入
- DPO 训练
- Unsloth 加速

---

## 裁剪决策记录

| 决策 | 理由 | 后续影响 |
|------|------|---------|
| 不引入 Prometheus/Grafana | MVP 阶段 metrics 端点足够 | 后续需补充部署 |
| 不引入 Langfuse tracing | MVP 只需验证核心链路 | 后续需补充埋点 |
| 标准 LoRA 优先于 QLoRA | 简化实现路径 | 显存不足时升级 QLoRA |
| 不引入 SFTTrainer | 基础 LoRA 足够验证 | SFT 需求时引入 |

---

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval
3. https://github.com/huggingface/peft — PEFT

Risk of Staleness:
- MVP 范围可能因业务需求调整

Out of Scope Kept:
- 未写具体排期
- 未写资源需求
