Task ID: T704
Task Title: Cross-Project Deep-Research Pack
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
把四个模块各自负责什么、不负责什么梳理清楚。

Result:

# Component Ownership Map v1

## 概述

本文档说明四个核心模块各自的职责范围，明确"负责什么"和"不负责什么"。

---

## inference-service

### 负责

| 职责 | 说明 |
|------|------|
| **推理引擎管理** | vLLM / SGLang 的部署和生命周期 |
| **OpenAI 兼容 API** | `/v1/chat/completions` 等接口 |
| **metrics 暴露** | Prometheus 格式的 `/metrics` 端点 |
| **健康检查** | `/health` 端点 |
| **模型加载** | 加载 base model 和 adapter |

### 不负责

| 职责 | 说明 |
|------|------|
| 请求路由 | 由 ai-gateway 负责 |
| 鉴权/限流 | 由 ai-gateway 负责 |
| 评测任务编排 | 由 eval-module 负责 |
| 训练过程 | 由 finetune-demo 负责 |

---

## ai-gateway

### 负责

| 职责 | 说明 |
|------|------|
| **请求路由** | 将请求路由到正确的 inference-service |
| **鉴权** | 验证请求凭证 |
| **限流** | 控制请求速率 |
| **Token 计量** | 记录 token 用量 |
| **OpenAI 兼容代理** | 代理到 inference-service |

### 不负责

| 职责 | 说明 |
|------|------|
| 推理计算 | 由 inference-service 负责 |
| 模型管理 | 由 inference-service 负责 |
| 评测执行 | 由 eval-module 负责 |
| 模型训练 | 由 finetune-demo 负责 |

---

## eval-module

### 负责

| 职责 | 说明 |
|------|------|
| **评测任务编排** | 管理评测任务的创建和执行 |
| **lm-eval 调用** | 调用 lm-eval 执行 benchmark |
| **结果持久化** | 评测结果保存为 JSON |
| **结果对比** | 历史评测结果对比 |
| **模型评测接口** | `evaluate(dataset, model)` |

### 不负责

| 职责 | 说明 |
|------|------|
| 推理计算 | 由 inference-service 负责 |
| 训练过程 | 由 finetune-demo 负责 |
| 路由/鉴权 | 由 ai-gateway 负责 |
| LLM-as-Judge | MVP 不实现（后续迭代） |
| 评测结果上报 Langfuse | MVP 不实现（后续迭代） |

---

## finetune-demo

### 负责

| 职责 | 说明 |
|------|------|
| **训练编排** | 管理训练任务的创建和执行 |
| **LoRA/QLoRA 训练** | PEFT/TRL 执行训练 |
| **Adapter 管理** | 保存/加载/合并 LoRA adapter |
| **训练参数配置** | rank/alpha/target_modules 等 |
| **训练结果返回** | adapter 路径和 metrics |

### 不负责

| 职责 | 说明 |
|------|------|
| 推理计算 | 由 inference-service 负责 |
| 评测执行 | 由 eval-module 负责 |
| 路由/鉴权 | 由 ai-gateway 负责 |
| DPO 训练 | MVP 不实现（后续迭代） |
| 训练 metrics 上报 Langfuse | 可选，后续迭代 |

---

## 模块职责边界总结

| 模块 | 核心职责 | MVP 边界 |
|------|---------|---------|
| **inference-service** | 推理计算 | 不负责路由/鉴权/训练/评测 |
| **ai-gateway** | 路由/鉴权/计量 | 不负责推理/训练/评测 |
| **eval-module** | 评测任务管理 | 不负责推理/训练/路由 |
| **finetune-demo** | 训练任务管理 | 不负责推理/评测/路由 |

---

## 模块间职责不重叠

| 边界 | 说明 |
|------|------|
| 推理计算 | 只在 inference-service |
| 路由/鉴权 | 只在 ai-gateway |
| 评测编排 | 只在 eval-module |
| 训练编排 | 只在 finetune-demo |

---

## 协作接口

```
ai-gateway → inference-service（HTTP API）
eval-module → inference-service（lm-eval backend）
finetune-demo → inference-service（adapter 加载推理）
eval-module → finetune-demo（加载微调后模型评测）
```

---

## 常见职责混淆

| 混淆 | 事实 |
|------|------|
| "eval-module 负责推理" | 推理由 inference-service 负责，eval-module 只管理评测 |
| "finetune-demo 负责评测" | 评测由 eval-module 负责，finetune-demo 只负责训练 |
| "gateway 负责模型加载" | 模型加载由 inference-service 负责 |
| "inference-service 负责路由" | 路由由 ai-gateway 负责 |

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval
3. https://github.com/huggingface/peft — PEFT

Risk of Staleness:
- 具体职责以实际代码实现为准

Out of Scope Kept:
- 未写代码实现
- 未写详细接口规范
