# Root Integration Service Port Matrix v1

## Task ID: T1105
## Title: Root Integration Fixture Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# Root Integration Service Port Matrix

本文档定义仓库各模块的端口、URL、依赖关系，对应真实文件 `ai-infra/configs/service_matrix.yaml`。

## 端口分配

| 模块 | 端口 | URL | 用途 |
|---|---|---|---|
| inference-service | 8000 | `http://localhost:8000` | vLLM 推理服务 |
| ai-gateway | 8080 | `http://localhost:8080` | 鉴权 + 路由代理 |
| eval-module | — | via CLI | 评测（不启动服务） |
| finetune-demo | — | via CLI | 微调（不启动服务） |
| inference-service metrics | 9090 | `http://localhost:9090/metrics` | Prometheus 抓取端口 |

---

## Service Port Matrix（YAML）

**对应文件：** `ai-infra/configs/service_matrix.yaml`

```yaml
# ai-infra Service Port Matrix
# 描述模块、端口、URL、依赖关系

services:
  inference_service:
    name: "inference-service"
    protocol: "http"
    host: "localhost"
    port: 8000
    base_path: "/v1"
    health_endpoint: "/health"
    metrics_endpoint: "/metrics"
    metrics_port: 9090        # Prometheus metrics scrape port
    startup_timeout: 120      # seconds
    dependencies: []          # 无依赖，可独立启动
    make_targets:
      install: "inference-install"
      serve: "inference-serve"
      health: "inference-health"
      test: "inference-test"

  ai_gateway:
    name: "ai-gateway"
    protocol: "http"
    host: "localhost"
    port: 8080
    base_path: "/v1"
    health_endpoint: "/health"
    metrics_endpoint: "/metrics"
    startup_timeout: 30
    dependencies:
      - service: "inference_service"
        wait_for: "/health"
        timeout: 120
    make_targets:
      install: "gateway-install"
      serve: "gateway-serve"
      health: "gateway-health"
      test: "gateway-test"

  eval_module:
    name: "eval-module"
    protocol: "http"
    host: "localhost"
    port: null                # CLI tool, no server
    backend_url: "http://localhost:8000/v1"  # inference endpoint
    dependencies:
      - service: "inference_service"
        wait_for: "/health"
    make_targets:
      install: "eval-install"
      run_mmlu: "eval-run-mmlu"
      run_gsm8k: "eval-run-gsm8k"

  finetune_demo:
    name: "finetune-demo"
    protocol: "http"
    host: "localhost"
    port: null                # CLI tool, no server
    base_model: "Qwen/Qwen2.5-0.5B-Instruct"
    dependencies: []          # 微调不依赖推理服务
    make_targets:
      install: "finetune-install"
      train: "finetune-train"
```

---

## 依赖关系图

```
inference-service :8000
        ↑
        | (waits for /health, timeout 120s)
        |
ai-gateway :8080 ←——— eval-module (uses as backend)
                              |
                              └── eval-mmlu / eval-gsm8k

finetune-demo (standalone, no dependencies)
```

---

## 启动顺序

### 启动顺序脚本（来自 `scripts/local_dev_sequence.sh`）

```bash
# Step 1: Start inference-service
cd inference-service && make serve MODEL="$MODEL" PORT=8000 &
wait_for_url "http://localhost:8000/health" "inference-service"  # max 120s

# Step 2: Start ai-gateway
cd ai-gateway && make serve PORT=8080 &
wait_for_url "http://localhost:8080/health" "ai-gateway"  # max 30s

# Done
```

---

## 端口冲突检查

**对应文件：** `ai-infra/scripts/check_ports.sh`

```bash
#!/usr/bin/env bash
# 检查必要端口是否可用
for PORT in 8000 8080; do
  if lsof -i :$PORT > /dev/null 2>&1; then
    echo "ERROR: Port $PORT is already in use"
    exit 1
  fi
done
echo "All required ports available"
```

---

## 各服务健康检查

| 服务 | 检查 URL | 期望 HTTP | 超时 |
|---|---|---|---|
| inference-service | `http://localhost:8000/health` | 200 | 120s |
| ai-gateway | `http://localhost:8080/health` | 200 | 30s |

---

Sources:
1. https://docs.vllm.ai/en/latest/serving/configuration.html — vLLM port config
2. https://github.com/Portkey-AI/gateway — Gateway port

Risk of Staleness:
- Port matrix is project-internal; defined per T805 integration contract
