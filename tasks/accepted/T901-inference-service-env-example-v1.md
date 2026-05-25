# inference-service .env.example Blueprint v1

## Task ID: T901
## Title: inference-service Scaffold Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T801 config surface，产出 .env.example 模板。

---

# inference-service .env.example Blueprint v1

## 概述

本文档定义 inference-service 的 `.env.example` 模板，所有字段均有注释说明。

## 模板全文

```bash
# ============================================================
# inference-service — .env.example
# 复制为 .env 后填入实际值
# ============================================================

# ---------- Server ----------

# 服务监听地址
INFERENCE_HOST=0.0.0.0

# 服务监听端口
INFERENCE_PORT=8000

# Uvicorn 工作进程数（生产环境建议 >=2）
INFERENCE_WORKERS=1

# 请求超时（秒）
INFERENCE_TIMEOUT=300

# ---------- Engine ----------

# 推理引擎类型：vllm | sglang | triton
INFERENCE_ENGINE_TYPE=vllm

# 模型路径（HuggingFace model name 或本地路径）
# 示例：Qwen/Qwen2.5-0.5B-Instruct
# 示例：./models/Qwen2.5-0.5B-Instruct
INFERENCE_MODEL_PATH=Qwen/Qwen2.5-0.5B-Instruct

# 是否信任远程代码（部分模型需要设为 true）
INFERENCE_TRUST_REMOTE_CODE=true

# ---------- vLLM 专用（ENGINE_TYPE=vllm 时生效） ----------

# Tensor 并行数（多 GPU 时调整）
VLLM_TENSOR_PARALLEL_SIZE=1

# GPU 显存利用率（0.0~1.0）
VLLM_GPU_MEMORY_UTILIZATION=0.9

# 最大模型上下文长度
VLLM_MAX_MODEL_LEN=4096

# 强制 eager 模式（调试用，默认 false）
VLLM_ENFORCE_EAGER=false

# 启用 chunked prefill（提升吞吐量）
VLLM_ENABLE_CHUNKED_PREFILL=true

# 最大批处理 token 数
VLLM_MAX_NUM_BATCHED_TOKENS=8192

# ---------- SGLang 专用（ENGINE_TYPE=sglang 时生效） ----------

SGLANG_HOST=0.0.0.0
SGLANG_PORT=8000
SGLANG_MEM_FRACTION_STATIC=0.88
SGLANG_STREAM_INTERVAL=1
SGLANG_CHUNKED_PREFILL_SIZE=8192

# ---------- Triton IS 专用（ENGINE_TYPE=triton 时生效） ----------

TRITON_MODEL_REPOSITORY=/model_repository
TRITON_PORT=8000
TRITON_HTTP_PORT=8001

# ---------- Health ----------

# 是否启用健康检查端点
HEALTH_CHECK_ENABLED=true

# ---------- Metrics ----------

# 是否启用 Prometheus metrics
METRICS_ENABLED=true

# Metrics 抓取端口
METRICS_PORT=9090

# ---------- Model Management ----------

# 模型缓存目录
INFERENCE_CACHE_DIR=./model_cache

# 模型下载超时（秒）
INFERENCE_DOWNLOAD_TIMEOUT=3600

# LoRA adapter 目录
INFERENCE_ADAPTER_DIR=./adapters
```

## 字段优先级说明

```
CLI 参数 > 环境变量 > .env 文件 > config.yaml > 默认值
```

## 最小必须字段（MVP）

```bash
# MVP 最简配置只需：
INFERENCE_ENGINE_TYPE=vllm
INFERENCE_MODEL_PATH=Qwen/Qwen2.5-0.5B-Instruct
INFERENCE_PORT=8000
```

## 开发环境 vs 生产环境

| 字段 | 开发环境 | 生产环境 |
|------|---------|---------|
| `INFERENCE_WORKERS` | 1 | >=2 |
| `VLLM_ENFORCE_EAGER` | true（方便调试） | false |
| `VLLM_GPU_MEMORY_UTILIZATION` | 0.8（留显存） | 0.9 |

---

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://docs.vllm.ai/en/latest/models/engine_args.html — vLLM Engine Arguments
3. https://pydantic-settings.readthedocs.io/ — Pydantic Settings

Risk of Staleness:
- vLLM/SGLang 环境变量可能随版本变化

Out of Scope Kept:
- 未写多模型同时加载
- 未写 GPU 感知调度
