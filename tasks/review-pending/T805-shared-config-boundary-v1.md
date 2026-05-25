# Shared Config Boundary v1

## Task ID: T805
## Task Title: Cross-Project Integration Prep Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T801-T804 config surface，准备共享配置边界。

---

# Shared Config Boundary v1

## 概述

本文档定义四个核心模块之间的共享配置边界，明确哪些配置是独立的，哪些需要共享。

---

## 配置边界总览

| 配置类 | inference-service | ai-gateway | eval-module | finetune-demo | 共享 |
|--------|-----------------|------------|------------|---------------|-----|
| 服务端口 | 8000 | 8080 | — | — | 否 |
| 模型路径 | ✓ | — | — | ✓ | base model 路径 |
| API Keys | — | ✓ | — | — | 否 |
| Backend URL | — | ✓ | ✓ | — | inference-service URL |
| Metrics 端口 | 9090 | 9091 | — | — | 否 |

---

## 独立配置（不共享）

### inference-service

```yaml
# 独立配置
server:
  host: "0.0.0.0"
  port: 8000

vllm:
  tensor_parallel_size: 1
  gpu_memory_utilization: 0.9

metrics:
  port: 9090
```

### ai-gateway

```yaml
# 独立配置
server:
  port: 8080

auth:
  enabled: true
  api_keys:
    - "dev-gateway-key-1"

rate_limit:
  default_rpm: 60
```

### eval-module

```yaml
# 独立配置
backend:
  type: "vllm"
  base_url: "http://localhost:8000/v1"

datasets:
  mmlu:
    num_fewshot: 5
```

### finetune-demo

```yaml
# 独立配置
training:
  method: "qlora"
  model:
    name_or_path: "Qwen/Qwen2.5-0.5B-Instruct"
```

---

## 共享配置（需要协调）

### Backend URL

| 模块 | 配置 | 值 |
|------|------|-----|
| inference-service | listen | `0.0.0.0:8000` |
| ai-gateway | `models[].base_url` | `http://localhost:8000/v1` |
| eval-module | `backend.base_url` | `http://localhost:8000/v1` |

### Model Path

| 模块 | 配置 | 说明 |
|------|------|------|
| inference-service | `engine.model_path` | 部署的模型 |
| finetune-demo | `model.name_or_path` | 训练的 base model |

建议：保持一致，避免模型版本不匹配。

---

## 配置传递方式

### 方式一：环境变量

```bash
# .env（共享）
INFERENCE_BASE_URL=http://localhost:8000
MODEL_NAME=Qwen/Qwen2.5-0.5B-Instruct

# inference-service
INFERENCE_PORT=8000
MODEL_PATH=${MODEL_NAME}

# ai-gateway
GATEWAY_PORT=8080
INFERENCE_URL=${INFERENCE_BASE_URL}/v1

# eval-module
EVAL_BACKEND_BASE_URL=${INFERENCE_BASE_URL}/v1

# finetune-demo
FINETUNE_MODEL=${MODEL_NAME}
```

### 方式二：统一配置文件

```yaml
# shared-config.yaml（所有模块共享）
model:
  name: "Qwen/Qwen2.5-0.5B-Instruct"
  base_url: "http://localhost:8000"
```

---

## 端口分配

| 端口 | 模块 | 说明 |
|------|------|------|
| 8000 | inference-service | 推理 API |
| 8080 | ai-gateway | Gateway 入口 |
| 9090 | inference-service metrics | Prometheus 抓取 |
| 9091 | ai-gateway metrics | Prometheus 抓取 |

---

## 配置冲突处理

| 冲突场景 | 处理方式 |
|---------|---------|
| 端口冲突 | 各模块使用独立端口 |
| 模型版本不一致 | 共享配置统一版本 |
| Backend URL 不一致 | eval/finetune 使用相同 URL |

---

Sources:
1. https://docs.vllm.ai/ — vLLM

Risk of Staleness:
- 端口分配可能因环境调整

Out of Scope Kept:
- 未写完整配置管理系统
