Task ID: T604
Task Title: Cross-Project Systemization Pack
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
说明如果按最小可验证路径推进，先做什么、后做什么、哪些可以并行。

Result:

# Build Order Roadmap v1

## 概述

本文档给出阶段化推进路线，按最小可验证路径（MVP）优先的原则，整理先做什么、后做什么、哪些可以并行。

---

## 阶段划分

### 阶段 0：基础设施（前置）

| 任务 | 说明 | 依赖 |
|------|------|------|
| 代码仓库建立 | 项目骨架 | 无 |
| CI/CD 基础 | 基础流水线 | 无 |
| 文档基础 | README / docs 结构 | 无 |

---

### 阶段 1：推理核心（最早可验证）

**目标**：能够跑通推理请求，验证基本能力。

| 任务 | 说明 | 依赖 |
|------|------|------|
| inference-service 骨架 | vLLM/SGLang 集成 | 无 |
| vLLM 部署验证 | 单机推理可跑通 | inference-service 骨架 |
| ai-gateway 骨架 | 路由 / 鉴权 / 限流 | inference-service 骨架 |
| gateway → inference 串联 | 端到端推理请求 | gateway + inference |

**可并行**：
- inference-service 和 ai-gateway 可以并行开发，通过接口 Mock 联调

---

### 阶段 2：可观测性（与阶段1可部分并行）

**目标**：推理服务可观测，能看到 metrics 和 traces。

| 任务 | 说明 | 依赖 |
|------|------|------|
| Prometheus 部署 | metrics 采集 | inference-service |
| Grafana 部署 | metrics 可视化 | Prometheus |
| Langfuse SDK 埋点 | tracing + token 统计 | inference-service |

**可并行**：
- Prometheus/Grafana 与推理开发并行，不影响核心流程

---

### 阶段 3：评测能力（阶段1之后）

**目标**：能跑 benchmark 并记录结果。

| 任务 | 说明 | 依赖 |
|------|------|------|
| eval-module 骨架 | 评测任务管理 | inference-service |
| lm-eval 集成 | benchmark 执行 | eval-module + inference |
| 结果持久化 | 评测结果 JSON 保存 | lm-eval 集成 |

**依赖关系**：
- eval-module 依赖 inference-service 的 /v1/chat 接口可用
- 可在阶段1完成后立即开始

---

### 阶段 4：微调能力（阶段3之后或并行）

**目标**：能训练 LoRA adapter 并验证效果。

| 任务 | 说明 | 依赖 |
|------|------|------|
| finetune-demo 骨架 | 训练任务管理 | inference-service |
| LoRA/QLoRA 集成 | PEFT + trl | finetune-demo 骨架 |
| 训练 + 评测串联 | finetune → eval 验证 | LoRA 集成 + eval-module |

**可并行**：
- finetune-demo 与 eval-module 可并行开发，通过 Mock 联调
- 评测结果验证依赖 eval-module

---

### 阶段 5：生产增强（可选，后续迭代）

| 任务 | 说明 | 依赖 |
|------|------|------|
| Triton IS 集成 | 多模型编排 | inference-service |
| TensorRT-LLM | 高性能推理 | Triton IS |
| DPO 微调 | 偏好优化 | LoRA 集成 |
| Langfuse 上报 | 评测结果上报 | eval-module + Langfuse |

---

## 并行推进建议

### 可以完全并行的路径

- **可观测性建设**（Prometheus/Grafana/Langfuse）与**推理开发**并行
- **eval-module 开发**与**finetune-demo 开发**并行（通过 Mock 接口）

### 建议并行组合

| 组合 | 说明 |
|------|------|
| 推理核心 + 可观测性 | 阶段1 + 阶段2并行 |
| eval + finetune | 阶段3 + 阶段4并行 |
| inference-service + ai-gateway | 阶段1内并行 |

---

## 关键里程碑

| 里程碑 | 验收条件 |
|--------|---------|
| **M1：推理可跑** | vLLM 服务启动，/v1/chat/completions 返回结果 |
| **M2：gateway 串联** | 通过 gateway 调用 inference 返回结果 |
| **M3：metrics 可用** | Grafana dashboard 能看到 QPS/延迟 |
| **M4：评测可跑** | lm-eval 跑通 MMLU，返回分数 |
| **M5：微调可跑** | LoRA 训练完成，adapter 保存成功 |
| **M6：训练+评测串联** | finetune 后跑 benchmark，对比基线分数 |

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval
3. https://github.com/huggingface/peft — PEFT
4. https://github.com/huggingface/trl — TRL

Risk of Staleness:
- 各工具版本更新可能影响里程碑可行性

Out of Scope Kept:
- 未写代码实现
- 未写具体排期
- 未写人员分工
