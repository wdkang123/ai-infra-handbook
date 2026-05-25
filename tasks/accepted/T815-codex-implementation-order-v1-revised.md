# Codex Implementation Order v1 (Revised)

## Task ID: T815
## Task Title: Codex Implementation Order Tighten
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T805-review.md，去掉按周节奏和每日节奏，改成纯任务序列/阶段序列。

---

# Codex Implementation Order v1 (Revised)

## 概述

本文档定义 Codex 执行 MVP 任务的推荐顺序，明确先做什么、后做什么。

---

## 推荐实现顺序

### 阶段 1：基础设施

**目标**：建立项目骨架，CI 就绪。

| 顺序 | 任务 ID | 任务 | 产出 |
|------|---------|------|------|
| 1 | T0-01 | 项目仓库骨架 | 目录结构 |
| 2 | T0-02 | CI 基础 | lint/test 可运行 |
| 3 | T0-03 | README 初版 | 文档结构 |
| 4 | T0-04 | 任务看板 | TASKBOARD.md |

**Codex 行动**：按顺序创建目录、配置 CI，写 README。

---

### 阶段 2：inference-service

**目标**：推理服务可独立运行。

| 顺序 | 任务 ID | 任务 | 产出 |
|------|---------|------|------|
| 1 | T1-01 | MVP 设计文档 | 架构设计 |
| 2 | T1-02 | vLLM 集成 | 服务可启动 |
| 3 | T1-05 | /health 健康检查 | 健康端点 |
| 4 | T1-06 | /metrics 端点 | Prometheus metrics |
| 5 | T1-03 | OpenAI 兼容 API | /v1/chat/completions |
| 6 | T1-04 | 模型加载 | base + adapter |
| 7 | T1-07 | 模型版本管理 | 版本切换 |

**验证**：参考 T801-validation-checklist

---

### 阶段 3：ai-gateway

**目标**：Gateway 可代理请求到 inference-service。

| 顺序 | 任务 ID | 任务 | 产出 |
|------|---------|------|------|
| 1 | T1-08 | MVP 设计文档 | 架构设计 |
| 2 | T1-09 | 路由逻辑 | 路由到正确后端 |
| 3 | T1-10 | 鉴权中间件 | Token 验证 |
| 4 | T1-11 | 限流中间件 | QPS 控制 |
| 5 | T1-12 | 端到端串联 | 全链路可跑 |

**验证**：参考 T802-validation-checklist

---

### 阶段 4：eval-module

**目标**：评测任务可运行，结果可对比。

| 顺序 | 任务 ID | 任务 | 产出 |
|------|---------|------|------|
| 1 | T3-01 | MVP 设计文档 | 架构设计 |
| 2 | T3-02 | lm-eval 集成 | lm-eval 可运行 |
| 3 | T3-03 | MMLU benchmark | 分数正常返回 |
| 4 | T3-04 | GSM8K benchmark | 分数正常返回 |
| 5 | T3-05 | 结果 JSON 持久化 | 文件保存 |
| 6 | T3-06 | 历史结果对比 | 两个结果可对比 |

**验证**：参考 T803-validation-checklist

---

### 阶段 5：finetune-demo

**目标**：微调可训练，产物可部署。

| 顺序 | 任务 ID | 任务 | 产出 |
|------|---------|------|------|
| 1 | T4-01 | MVP 设计文档 | 架构设计 |
| 2 | T4-02 | PEFT/LoRA 集成 | LoRA adapter 可训练 |
| 3 | T4-05 | adapter 保存/加载 | 持久化可用 |
| 4 | T4-06 | 训练+评测串联 | 微调后 benchmark 可跑 |

**验证**：参考 T804-validation-checklist

---

## 关键路径（最短 MVP）

```
T0-01 → T0-02 → T0-03 → T0-04 →
T1-01 → T1-02 → T1-05 → T1-06 → T1-03 →
T1-08 → T1-09 → T1-10 → T1-11 → T1-12 →
T3-01 → T3-02 → T3-03 → T3-04 → T3-05 →
T4-01 → T4-02 → T4-05 → T4-06
```

---

## 可选任务（不阻塞 MVP）

| 任务 ID | 任务 | 说明 |
|---------|------|------|
| T2-02 | Prometheus 部署 | metrics 存储 |
| T2-03 | Grafana dashboard | 可视化 |
| T2-04 | Langfuse SDK 埋点 | trace 上报 |
| T2-05 | gateway tracing | token 计量 |
| T4-03 | QLoRA 集成 | 4-bit 量化 |
| T4-04 | SFTTrainer 集成 | SFT 训练 |
| T4-07 | Unsloth 加速 | GPU 加速 |

---

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval
3. https://github.com/huggingface/peft — PEFT

Risk of Staleness:
- 实现顺序可能因实际情况调整

Out of Scope Kept:
- 未写详细排期
- 未写人员分工
