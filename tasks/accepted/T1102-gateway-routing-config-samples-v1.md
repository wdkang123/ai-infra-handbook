# ai-gateway Routing Config Samples v1

## Task ID: T1102
## Title: ai-gateway Fixture Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# ai-gateway Routing Config Samples

本文档定义 ai-gateway 路由配置样本，对应真实文件 `ai-gateway/configs/`。

---

## configs/models.yaml（路由配置）

**对应文件：** `ai-gateway/configs/models.yaml`

```yaml
# Model routing configuration
# Maps upstream model names to downstream inference-service URLs

models:
  - name: "vllm-local"
    downstream: "http://localhost:8000/v1"
    enabled: true
    retry:
      enabled: true
      max_attempts: 2
      backoff_ms: 100
    timeout_ms: 30000

  - name: "Qwen2.5-0.5B-Instruct"
    downstream: "http://localhost:8000/v1"
    enabled: true
    retry:
      enabled: true
      max_attempts: 3
      backoff_ms: 200
    timeout_ms: 60000

  - name: "llama3-8b"
    downstream: "http://gpu-server-01:8000/v1"
    enabled: true
    retry:
      enabled: true
      max_attempts: 3
      backoff_ms: 300
    timeout_ms: 120000

  - name: "gpt-4"
    downstream: "https://api.openai.com/v1"
    enabled: false
    retry:
      enabled: true
      max_attempts: 1
      backoff_ms: 100
    timeout_ms: 60000
```

---

## configs/config.yaml（完整配置）

**对应文件：** `ai-gateway/configs/config.yaml`

```yaml
# ai-gateway configuration
service:
  host: "0.0.0.0"
  port: 8080
  workers: 4
  log_level: "info"

auth:
  enabled: true
  api_keys:
    - "sk-test-key-1"
    - "sk-test-key-2"
  bypass_paths:
    - "/health"
    - "/metrics"

rate_limit:
  enabled: true
  default_rpm: 60
  per_model_rpm:
    "vllm-local": 120
    "Qwen2.5-0.5B-Instruct": 60

models_config_path: "configs/models.yaml"

proxy:
  timeout_ms: 60000
  retry_enabled: true
  max_retries: 2
  retry_backoff_ms: 200
```

---

## configs/config.local.yaml（开发配置）

**对应文件：** `ai-gateway/configs/config.local.yaml`

```yaml
# Local development configuration
service:
  host: "127.0.0.1"
  port: 8080
  workers: 1
  log_level: "debug"

auth:
  enabled: false              # skip auth in local dev
  api_keys:
    - "sk-test-key-1"
  bypass_paths:
    - "/health"
    - "/metrics"

rate_limit:
  enabled: false

models_config_path: "configs/models.yaml"

proxy:
  timeout_ms: 30000
  retry_enabled: false
```

---

## 路由匹配规则

| 上游 model 名称 | 下游 URL | 行为 |
|---|---|---|
| `vllm-local` | `http://localhost:8000/v1` | 本地 vLLM 实例 |
| `Qwen2.5-0.5B-Instruct` | `http://localhost:8000/v1` | 同本地实例 |
| `llama3-8b` | `http://gpu-server-01:8000/v1` | 远程 GPU 服务器 |
| 未知 model | — | 返回 404 |

---

## 请求流向

```
Client
  |
  v
[ai-gateway:8080]  ──auth──> verify_api_key()
  |                              |
  v                        [rate limit]  (per model RPM)
  |
  v  _route_model(model_name) ──> models.yaml lookup
  |
  v  forward_chat_request() ──> downstream URL + original body
  |
  v
[downstream inference-service]
  |
  v
[response passthrough] ──> Client
```

---

Sources:
1. https://github.com/Portkey-AI/gateway — Portkey routing reference
2. https://www.gateway.com/docs — Gateway routing config

Risk of Staleness:
- Model routing schema is project-internal; stable per T1002 blueprint
