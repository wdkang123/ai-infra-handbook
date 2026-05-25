# Root .env.example Blueprint v2

## Task ID: T1005
## Title: Root / Dev Workflow Starter File Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T905 scaffold（root-env-example blueprint v1），产出 v2 版本共享 .env.example。

---

# Root .env.example Blueprint v2

## 概述

本文档定义仓库根目录的共享 `.env.example` v2 蓝图，所有模块共享的环境变量在此定义。

## `.env.example` 模板

```bash
# ============================================================
# ai-infra — .env.example (shared, root level)
# 复制到各模块的 .env 或直接使用根目录 .env
# ============================================================

# ---------- Shared Model Config ----------
# 所有模块使用相同的模型
MODEL_NAME=Qwen/Qwen2.5-0.5B-Instruct
MODEL_CACHE_DIR=./model_cache

# ---------- Shared Inference Config ----------
# inference-service 监听地址
INFERENCE_HOST=0.0.0.0
INFERENCE_PORT=8000

# 所有使用 inference-service 的模块使用相同 URL
INFERENCE_BASE_URL=http://localhost:8000/v1

# ---------- Gateway Config ----------
GATEWAY_HOST=0.0.0.0
GATEWAY_PORT=8080

# ---------- External API Keys ----------
OPENAI_API_KEY=replace-with-openai-api-key
ANTHROPIC_API_KEY=replace-with-anthropic-api-key

# ---------- Metrics Ports ----------
# Prometheus metrics 各模块独立
INFERENCE_METRICS_PORT=9090
GATEWAY_METRICS_PORT=9091

# ---------- Finetune Config ----------
FINETUNE_MODEL=${MODEL_NAME}
FINETUNE_OUTPUT_DIR=./models
FINETUNE_ADAPTER_DIR=./adapters

# ---------- Development Mode ----------
# set to 'true' to disable auth and rate-limiting in dev
DEV_MODE=false

# ---------- Eval Config ----------
EVAL_BACKEND_URL=http://localhost:8000/v1
EVAL_RESULTS_DIR=./results
```

## 字段说明

| 字段 | 说明 | 共享范围 |
|------|------|---------|
| `MODEL_NAME` | 使用的模型 | 所有模块 |
| `INFERENCE_BASE_URL` | inference-service 地址 | gateway, eval, finetune |
| `INFERENCE_PORT` | inference-service 端口 | inference-service |
| `GATEWAY_PORT` | gateway 端口 | gateway |
| `OPENAI_API_KEY` | OpenAI API Key | gateway |
| `DEV_MODE` | 开发模式（关闭鉴权） | gateway |
| `EVAL_BACKEND_URL` | 评测后端 URL | eval-module |

## 端口分配

| 端口 | 模块 | 说明 |
|------|------|------|
| 8000 | inference-service | 推理 API |
| 8080 | ai-gateway | Gateway 入口 |
| 9090 | inference-service metrics | Prometheus 抓取 |
| 9091 | ai-gateway metrics | Prometheus 抓取 |

## 使用方式

```bash
# 方式 1：在根目录创建 .env，各模块读取
cp .env.example .env
# 各模块需要 .env 时：ln -s ../.env modules/xxx/.env

# 方式 2：各模块独立 .env
cp .env.example inference-service/.env
cp .env.example ai-gateway/.env
cp .env.example eval-module/.env
cp .env.example finetune-demo/.env
```

---

Sources:
1. https://docs.vllm.ai/ — vLLM
