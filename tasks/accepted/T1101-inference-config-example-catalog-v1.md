# inference-service Config Example Catalog v1

## Task ID: T1101
## Title: inference-service Fixture Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# inference-service Config Example Catalog

本文档定义 inference-service 配置文件样本，对应真实部署文件 `inference-service/configs/`。

---

## configs/.env.local

**对应文件：** `inference-service/configs/.env.local`

```
# Model configuration
MODEL_NAME=Qwen2.5-0.5B-Instruct
MODEL_PATH=Qwen/Qwen2.5-0.5B-Instruct

# vLLM engine
VLLMTensorizerMode=awq
VLLMDtype=float16
VLLMGpuMemoryUtilization=0.85
VLLMMaxNumSeqs=16
VLLMMaxNumBatchedTokens=8192

# Service
INFERENCE_PORT=8000
INFERENCE_HOST=0.0.0.0
UVICORN_WORKERS=1

# Logging
LOG_LEVEL=info
LOG_FORMAT=json
```

---

## configs/config.yaml

**对应文件：** `inference-service/configs/config.yaml`

```yaml
# inference-service configuration
service:
  host: "0.0.0.0"
  port: 8000
  workers: 1
  log_level: "info"

model:
  name: "Qwen2.5-0.5B-Instruct"
  path: "Qwen/Qwen2.5-0.5B-Instruct"
  tokenizer: "Qwen/Qwen2.5-0.5B-Instruct"

engine:
  backend: "vllm"
  tensorizer_mode: "awq"       # awq, gptq, fp8, None
  dtype: "float16"             # float16, bfloat16, float8
  gpu_memory_utilization: 0.85  # 0.0 ~ 0.95
  max_num_seqs: 16              # max concurrent sequences
  max_num_batched_tokens: 8192  # max tokens per batch
  max_model_len: 8192           # max model context length
  enforce_eager: false          # use eager mode for debugging
  download_dir: null            # local model cache dir

health:
  startup_timeout: 120          # seconds to wait for engine init
  liveness_check_interval: 30   # seconds

metrics:
  enabled: true
  port: 9090
  path: "/metrics"
```

---

## configs/config.local.yaml（开发用）

**对应文件：** `inference-service/configs/config.local.yaml`

```yaml
# Local development configuration — not for production
service:
  host: "127.0.0.1"
  port: 8000
  workers: 1
  log_level: "debug"

model:
  name: "Qwen2.5-0.5B-Instruct"
  path: "./models/Qwen2.5-0.5B-Instruct"
  tokenizer: "./models/Qwen2.5-0.5B-Instruct"

engine:
  backend: "vllm"
  tensorizer_mode: null
  dtype: "float16"
  gpu_memory_utilization: 0.8
  max_num_seqs: 8
  max_num_batched_tokens: 4096
  max_model_len: 4096
  enforce_eager: true           # true for easier debugging
  download_dir: "./models"

health:
  startup_timeout: 60
  liveness_check_interval: 15

metrics:
  enabled: true
  port: 9090
  path: "/metrics"
```

---

## configs/config.smoke.yaml（冒烟测试用）

**对应文件：** `inference-service/configs/config.smoke.yaml`

```yaml
# Smoke test configuration — minimal resources
service:
  host: "127.0.0.1"
  port: 8000
  workers: 1
  log_level: "warning"

model:
  name: "Qwen2.5-0.5B-Instruct"
  path: "Qwen/Qwen2.5-0.5B-Instruct"
  tokenizer: "Qwen/Qwen2.5-0.5B-Instruct"

engine:
  backend: "vllm"
  tensorizer_mode: null
  dtype: "float16"
  gpu_memory_utilization: 0.5    # lower for smoke test GPU
  max_num_seqs: 2
  max_num_batched_tokens: 512
  max_model_len: 1024
  enforce_eager: true
  download_dir: null

health:
  startup_timeout: 300
  liveness_check_interval: 10

metrics:
  enabled: true
  port: 9090
  path: "/metrics"
```

---

## Config 字段说明

| 字段 | 类型 | 默认 | 说明 |
|---|---|---|---|
| `service.host` | string | `0.0.0.0` | 监听地址 |
| `service.port` | int | `8000` | 服务端口 |
| `service.workers` | int | `1` | uvicorn workers |
| `model.name` | string | — | 对外暴露的模型名 |
| `model.path` | string | — | HuggingFace model id 或本地路径 |
| `engine.backend` | string | `vllm` | 推理引擎后端 |
| `engine.dtype` | string | `float16` | 计算精度 |
| `engine.gpu_memory_utilization` | float | `0.9` | vLLM GPU memory fraction |
| `engine.max_num_seqs` | int | `16` | 最大并发序列数 |
| `engine.max_model_len` | int | `8192` | 最大上下文长度 |
| `health.startup_timeout` | int | `120` | 引擎初始化超时（秒） |

---

Sources:
1. https://docs.vllm.ai/en/latest/serving/configuration.html — vLLM serving args
2. https://platform.openai.com/docs/api-reference/chat/create — OpenAI chat params

Risk of Staleness:
- vLLM `AsyncLLMEngine` config keys have been stable since v0.3
