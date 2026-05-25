Task ID: T704
Task Title: Cross-Project Deep-Research Pack
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
在 T604 基础上做更清晰的边界收口和推进顺序收紧。

Result:

# Project Dependency Matrix v2

## 概述

本文档在 v1 基础上进一步收口四个核心模块的依赖关系和接口边界。

---

## 模块总览（v2）

| 模块 | 职责 | MVP 边界 |
|------|------|---------|
| **inference-service** | 推理引擎管理，vLLM/SGLang serving | 核心服务，不做其他模块的管理 |
| **ai-gateway** | 请求路由、鉴权、限流、token 计量 | 入口层，不直接管理模型 |
| **eval-module** | 评测任务管理、结果记录 | 评测执行 + 结果 JSON，暂不上报 |
| **finetune-demo** | 模型微调、adapter 管理 | LoRA/QLoRA 训练，暂不支持 DPO |

---

## 依赖矩阵（v2 收紧）

| 消费者 → <br> 提供者 ↓ | inference-service | ai-gateway | eval-module | finetune-demo |
|---|---|---|---|---|
| **inference-service** | — | HTTP API | lm-eval backend | 推理后加载 adapter |
| **ai-gateway** | 上游调用 | — | — | — |
| **eval-module** | 调用 lm-eval backend | — | — | 调用 finetune adapter |
| **finetune-demo** | — | — | benchmark 结果验证 | — |

---

## 依赖方向说明（v2 收紧）

### ai-gateway → inference-service

- **依赖类型**：HTTP API 调用
- **接口**：`/v1/chat/completions`（OpenAI 兼容）
- **依赖内容**：推理能力
- **边界**：gateway 不管理 inference-service 的生命周期

### eval-module → inference-service

- **依赖类型**：lm-eval backend
- **接口**：`--model vllm --model_args base_url=http://inference-service:8000/v1`
- **依赖内容**：评测执行
- **边界**：eval-module 不直接调用推理，只通过 lm-eval

### finetune-demo → inference-service

- **依赖类型**：训练后加载 adapter 推理验证
- **接口**：adapter 加载到 inference-service 做推理
- **边界**：finetune-demo 不管理 inference-service

### eval-module → finetune-demo

- **依赖类型**：加载微调后模型做评测
- **接口**：base model + adapter 加载
- **边界**：eval-module 不管理 finetune-demo 的训练过程

### ai-gateway ← 无上游依赖

ai-gateway 是入口层，不依赖其他项目模块。

---

## 数据流向（v2 收紧）

```
用户请求
    ↓
ai-gateway（路由 / 鉴权 / 计量）
    ↓
inference-service（vLLM/SGLang）
    ↓ /metrics
Prometheus → Grafana（metrics 可视化）
    ↓ Langfuse SDK
Langfuse（tracing + token 统计）

finetune-demo（训练）
    ↓ adapter
inference-service（加载 adapter）
    ↓
eval-module（评测）
    ↓ benchmark 结果
评测结果 JSON / Langfuse（可选）
```

---

## 接口草案（v2 收紧）

### inference-service 提供

| 接口 | 说明 | MVP 必须 |
|------|------|---------|
| `POST /v1/chat/completions` | OpenAI 兼容聊天接口 | 是 |
| `GET /metrics` | Prometheus 格式 metrics | 是 |
| `GET /health` | 健康检查 | 是 |

### ai-gateway 提供

| 接口 | 说明 | MVP 必须 |
|------|------|---------|
| `POST /v1/chat/completions` | 代理到 inference-service | 是 |
| `GET /metrics` | gateway 自身 metrics | 是 |

### eval-module 提供

| 接口 | 说明 | MVP 必须 |
|------|------|---------|
| `evaluate(dataset, model)` | 运行 benchmark 评测 | 是 |
| `load_results(path)` | 加载历史评测结果 | 是 |
| `report_to_langfuse(result)` | 评测结果上报（可选） | 否 |

### finetune-demo 提供

| 接口 | 说明 | MVP 必须 |
|------|------|---------|
| `train(config, dataset)` | 执行微调训练 | 是 |
| `save_adapter(path)` | 保存 LoRA adapter | 是 |
| `load_adapter(path)` | 加载 adapter | 是 |
| `get_adapter_path()` | 获取当前 adapter 路径 | 是 |

---

## 模块职责边界（v2 新增）

| 模块 | 负责 | 不负责 |
|------|------|-------|
| **inference-service** | 推理计算、metrics 暴露 | 请求路由、训练管理 |
| **ai-gateway** | 路由、鉴权、计量 | 推理计算、评测执行 |
| **eval-module** | 评测任务编排、结果存储 | 推理计算、模型训练 |
| **finetune-demo** | 模型训练、adapter 管理 | 推理计算、评测编排 |

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://langfuse.com/docs/observability/overview — Langfuse
3. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval

Risk of Staleness:
- 具体接口以实际实现为准

Out of Scope Kept:
- 未写代码实现
- 未写完整 API 规范
- 未写错误处理机制
