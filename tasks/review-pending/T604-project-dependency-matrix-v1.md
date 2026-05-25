Task ID: T604
Task Title: Cross-Project Systemization Pack
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
把4个项目（inference-service / ai-gateway / eval-module / finetune-demo）之间的输入、输出、依赖方向整理清楚。

Result:

# Project Dependency Matrix v1

## 概述

本文档整理 4 个核心项目模块之间的依赖方向和接口关系。

---

## 模块总览

| 模块 | 职责 |
|------|------|
| **inference-service** | 推理引擎管理，vLLM/SGLang serving |
| **ai-gateway** | 请求路由、鉴权、限流、token 计量 |
| **eval-module** | 评测任务管理、结果记录 |
| **finetune-demo** | 模型微调、adapter 管理 |

---

## 依赖矩阵

| 消费者 → <br> 提供者 ↓ | inference-service | ai-gateway | eval-module | finetune-demo |
|---|---|---|---|---|
| **inference-service** | — | HTTP API（/v1/chat/completions） | lm-eval backend | 推理后加载 adapter |
| **ai-gateway** | 上游调用 inference-service | — | — | — |
| **eval-module** | 调用 lm-eval backend | — | — | 调用 finetune adapter |
| **finetune-demo** | — | — | benchmark 结果验证 | — |

---

## 依赖方向说明

### ai-gateway → inference-service

- **依赖类型**：HTTP API 调用
- **接口**：`/v1/chat/completions`（OpenAI 兼容）
- **依赖内容**：推理能力

### eval-module → inference-service

- **依赖类型**：lm-eval backend
- **接口**：`--model vllm --model_args base_url=http://inference-service:8000/v1`
- **依赖内容**：评测执行

### finetune-demo → inference-service

- **依赖类型**：训练后加载 adapter 推理验证
- **接口**：adapter 加载到 inference-service 做推理
- **依赖内容**：推理验证

### eval-module → finetune-demo

- **依赖类型**：加载微调后模型做评测
- **接口**：base model + adapter 加载
- **依赖内容**：评测微调后模型

### ai-gateway ← 无上游依赖

ai-gateway 是入口层，不依赖其他项目模块。

---

## 数据流向

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
eval-module（评测）
    ↓ benchmark 结果
评测结果 JSON / Langfuse（可选）
```

---

## 接口草案（提案级）

### inference-service 提供

| 接口 | 说明 |
|------|------|
| `POST /v1/chat/completions` | OpenAI 兼容聊天接口 |
| `GET /metrics` | Prometheus 格式 metrics |
| `GET /health` | 健康检查 |

### ai-gateway 提供

| 接口 | 说明 |
|------|------|
| `POST /v1/chat/completions` | 代理到 inference-service |
| `GET /metrics` | gateway 自身 metrics |

### eval-module 提供

| 接口 | 说明 |
|------|------|
| `evaluate(dataset, model)` | 运行 benchmark 评测 |
| `load_results(path)` | 加载历史评测结果 |

### finetune-demo 提供

| 接口 | 说明 |
|------|------|
| `train(config, dataset)` | 执行微调训练 |
| `save_adapter(path)` | 保存 LoRA adapter |
| `load_adapter(path)` | 加载 adapter |

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
