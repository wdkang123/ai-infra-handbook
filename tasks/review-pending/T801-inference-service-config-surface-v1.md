# inference-service Config Surface v1

## Task ID: T801
## Task Title: inference-service Execution Prep Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T301 MVP 设计，准备 inference-service 实施前包。

---

# inference-service Config Surface v1

## 概述

本文档定义 inference-service 的配置项清单，对应 `config.yaml` 和环境变量。

---

## 配置项总览

| 配置类 | 配置项数 | MVP 必须 |
|--------|---------|---------|
| Server | 4 | 4 |
| Engine | 3 | 3 |
| vLLM | 6 | 5 |
| SGLang | 5 | 4 |
| Triton | 3 | 2 |
| Metrics | 2 | 2 |
| Health | 1 | 1 |
| 模型管理 | 3 | 2 |
| **合计** | **27** | **23** |

---

## Server 配置

| 配置项 | 环境变量 | 默认值 | 说明 | MVP 必须 |
|--------|---------|-------|------|---------|
| `server.host` | `INFERENCE_HOST` | `0.0.0.0` | 服务监听地址 | 是 |
| `server.port` | `INFERENCE_PORT` | `8000` | 服务监听端口 | 是 |
| `server.workers` | `INFERENCE_WORKERS` | `1` | Uvicorn 工作进程数 | 是 |
| `server.timeout` | `INFERENCE_TIMEOUT` | `300` | 请求超时（秒） | 是 |

---

## Engine 配置

| 配置项 | 环境变量 | 默认值 | 说明 | MVP 必须 |
|--------|---------|-------|------|---------|
| `engine.type` | `INFERENCE_ENGINE_TYPE` | `vllm` | 引擎类型 | 是 |
| `engine.model_path` | `INFERENCE_MODEL_PATH` | `./models/base` | 模型路径 | 是 |
| `engine.trust_remote_code` | `INFERENCE_TRUST_REMOTE_CODE` | `true` | 是否信任远程代码 | 是 |

---

## vLLM 配置

| 配置项 | 环境变量 | 默认值 | 说明 | MVP 必须 |
|--------|---------|-------|------|---------|
| `vllm.tensor_parallel_size` | `VLLM_TENSOR_PARALLEL_SIZE` | `1` | Tensor 并行数 | 是 |
| `vllm.gpu_memory_utilization` | `VLLM_GPU_MEMORY_UTILIZATION` | `0.9` | GPU 显存利用率 | 是 |
| `vllm.max_model_len` | `VLLM_MAX_MODEL_LEN` | `4096` | 最大模型上下文长度 | 是 |
| `vllm.enforce_eager` | `VLLM_ENFORCE_EAGER` | `false` | 强制 eager 模式 | 否 |
| `vllm.enable_chunked_prefill` | `VLLM_ENABLE_CHUNKED_PREFILL` | `true` | 启用 chunked prefill | 否 |
| `vllm.max_num_batched_tokens` | `VLLM_MAX_NUM_BATCHED_TOKENS` | `8192` | 最大批处理 token 数 | 否 |

来源：https://docs.vllm.ai/en/latest/models/engine_args.html

---

## SGLang 配置

| 配置项 | 环境变量 | 默认值 | 说明 | MVP 必须 |
|--------|---------|-------|------|---------|
| `sglang.port` | `SGLANG_PORT` | `8000` | SGLang 监听端口 | 是 |
| `sglang.host` | `SGLANG_HOST` | `0.0.0.0` | SGLang 监听地址 | 是 |
| `sglang.mem_fraction_static` | `SGLANG_MEM_FRACTION_STATIC` | `0.88` | 静态显存比例 | 否 |
| `sglang.stream_interval` | `SGLANG_STREAM_INTERVAL` | `1` | 流式输出间隔 | 否 |
| `sglang.chunked_prefill_size` | `SGLANG_CHUNKED_PREFILL_SIZE` | `8192` | chunked prefill 大小 | 否 |

来源：https://sglang.readthedocs.io/en/latest/get_started.html

---

## Triton IS 配置

| 配置项 | 环境变量 | 默认值 | 说明 | MVP 必须 |
|--------|---------|-------|------|---------|
| `triton.model_repository` | `TRITON_MODEL_REPOSITORY` | `/model_repository` | 模型仓库路径 | 是 |
| `triton.port` | `TRITON_PORT` | `8000` | Triton gRPC 端口 | 否 |
| `triton.http_port` | `TRITON_HTTP_PORT` | `8001` | Triton HTTP 端口 | 否 |

来源：https://docs.nvidia.com/deeplearning/triton-inference-server/

---

## Metrics 配置

| 配置项 | 环境变量 | 默认值 | 说明 | MVP 必须 |
|--------|---------|-------|------|---------|
| `metrics.enabled` | `METRICS_ENABLED` | `true` | 是否启用 metrics | 是 |
| `metrics.port` | `METRICS_PORT` | `9090` | Metrics 抓取端口 | 是 |

---

## Health 配置

| 配置项 | 环境变量 | 默认值 | 说明 | MVP 必须 |
|--------|---------|-------|------|---------|
| `health.enabled` | `HEALTH_CHECK_ENABLED` | `true` | 是否启用健康检查 | 是 |

---

## 模型管理配置

| 配置项 | 环境变量 | 默认值 | 说明 | MVP 必须 |
|--------|---------|-------|------|---------|
| `model.cache_dir` | `INFERENCE_CACHE_DIR` | `./model_cache` | 模型缓存目录 | 是 |
| `model.download_timeout` | `INFERENCE_DOWNLOAD_TIMEOUT` | `3600` | 模型下载超时（秒） | 否 |
| `model.adapter_dir` | `INFERENCE_ADAPTER_DIR` | `./adapters` | LoRA adapter 目录 | 是 |

---

## 配置加载优先级

```
CLI 参数 > 环境变量 > config.yaml > 默认值
```

---

## config.yaml 示例

```yaml
server:
  host: "0.0.0.0"
  port: 8000
  workers: 1
  timeout: 300

engine:
  type: "vllm"
  model_path: "./models/Qwen2.5-0.5B-Instruct"
  trust_remote_code: true

vllm:
  tensor_parallel_size: 1
  gpu_memory_utilization: 0.9
  max_model_len: 4096
  enable_chunked_prefill: true

metrics:
  enabled: true
  port: 9090

health:
  enabled: true

model:
  cache_dir: "./model_cache"
  adapter_dir: "./adapters"
```

---

Sources:
1. https://docs.vllm.ai/en/latest/models/engine_args.html — vLLM Engine Arguments
2. https://sglang.readthedocs.io/en/latest/get_started.html — SGLang
3. https://docs.nvidia.com/deeplearning/triton-inference-server/ — Triton IS

Risk of Staleness:
- vLLM/SGLang/Triton 配置项可能随版本变化

Out of Scope Kept:
- 未写多模型配置
- 未写灰度发布配置
