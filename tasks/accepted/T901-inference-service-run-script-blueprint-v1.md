# inference-service Run Script Blueprint v1

## Task ID: T901
## Title: inference-service Scaffold Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T801 repo layout 和 T801 validation checklist，产出启动脚本模板。

---

# inference-service Run Script Blueprint v1

## 概述

本文档定义 inference-service 的服务启动脚本模板 `scripts/serve.sh`，包含常用场景。

## `scripts/serve.sh` 模板

```bash
#!/usr/bin/env bash
# ============================================================
# inference-service — scripts/serve.sh
# 服务启动脚本，支持多种场景
# ============================================================

set -euo pipefail

# ---------- Defaults ----------
ENGINE="${INFERENCE_ENGINE_TYPE:-vllm}"
MODEL="${INFERENCE_MODEL_PATH:-Qwen/Qwen2.5-0.5B-Instruct}"
PORT="${INFERENCE_PORT:-8000}"
METRICS_PORT="${METRICS_PORT:-9090}"
HOST="${INFERENCE_HOST:-0.0.0.0}"
WORKERS="${INFERENCE_WORKERS:-1}"
TIMEOUT="${INFERENCE_TIMEOUT:-300}"
GPU_UTIL="${VLLM_GPU_MEMORY_UTILIZATION:-0.9}"
MAX_LEN="${VLLM_MAX_MODEL_LEN:-4096}"

# ---------- Color output ----------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() { echo -e "${GREEN}[INFO]${NC} $*"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $*"; }
log_error() { echo -e "${RED}[ERROR]${NC} $*" >&2; }

# ---------- Help ----------
usage() {
    cat <<EOF
Usage: $0 [OPTIONS]

Start inference-service with vLLM engine.

OPTIONS:
    -e, --engine ENGINE      Engine type: vllm (default: vllm)
    -m, --model MODEL        Model name or path (default: Qwen/Qwen2.5-0.5B-Instruct)
    -p, --port PORT          HTTP port (default: 8000)
    -h, --host HOST          Listen address (default: 0.0.0.0)
    --metrics-port PORT      Prometheus metrics port (default: 9090)
    --gpu-util FLOAT        GPU memory utilization 0.0-1.0 (default: 0.9)
    --max-len INT           Max model context length (default: 4096)
    --workers INT            Uvicorn workers (default: 1)
    --timeout INT            Request timeout seconds (default: 300)
    --dry-run               Print command without executing
    --help                  Show this help message

EXAMPLES:
    # Default: vLLM + Qwen-0.5B on port 8000
    $0

    # Custom model and port
    $0 -m Qwen/Qwen2.5-1.5B-Instruct -p 8001

    # Production: more GPU memory, 2 workers
    $0 --gpu-util 0.9 --workers 2 --timeout 600

    # Debug: eager mode, single worker
    $0 --enforce-eager --workers 1
EOF
}

# ---------- Parse args ----------
DRY_RUN=false
ENFORCE_EAGER=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -e|--engine) ENGINE="$2"; shift 2 ;;
        -m|--model) MODEL="$2"; shift 2 ;;
        -p|--port) PORT="$2"; shift 2 ;;
        -h|--host) HOST="$2"; shift 2 ;;
        --metrics-port) METRICS_PORT="$2"; shift 2 ;;
        --gpu-util) GPU_UTIL="$2"; shift 2 ;;
        --max-len) MAX_LEN="$2"; shift 2 ;;
        --workers) WORKERS="$2"; shift 2 ;;
        --timeout) TIMEOUT="$2"; shift 2 ;;
        --enforce-eager) ENFORCE_EAGER=true; shift ;;
        --dry-run) DRY_RUN=true; shift ;;
        --help) usage; exit 0 ;;
        *) log_error "Unknown option: $1"; usage; exit 1 ;;
    esac
done

# ---------- Build command ----------
CMD=(inference-service serve)
CMD+=(--engine "$ENGINE")
CMD+=(--model "$MODEL")
CMD+=(--port "$PORT")
CMD+=(--host "$HOST")
CMD+=(--metrics-port "$METRICS_PORT")
CMD+=(--workers "$WORKERS")
CMD+=(--timeout "$TIMEOUT")

if [[ "$ENGINE" == "vllm" ]]; then
    CMD+=(--vllm-gpu-memory-utilization "$GPU_UTIL")
    CMD+=(--vllm-max-model-len "$MAX_LEN")
    if [[ "$ENFORCE_EAGER" == "true" ]]; then
        CMD+=(--vllm-enforce-eager)
    fi
fi

# ---------- Validate GPU ----------
check_gpu() {
    if command -v nvidia-smi &>/dev/null; then
        local gpu_count
        gpu_count=$(nvidia-smi --query-gpu=gpu_name --format=csv,noheader 2>/dev/null | wc -l)
        log_info "Detected $gpu_count GPU(s)"
        if [[ "$gpu_count" -eq 0 ]]; then
            log_warn "No GPU detected — vLLM will run in CPU mode (very slow)"
        fi
    else
        log_warn "nvidia-smi not found — cannot detect GPUs"
    fi
}

# ---------- Pre-launch check ----------
check_port() {
    if ss -tuln 2>/dev/null | grep -q ":${PORT} "; then
        log_error "Port $PORT is already in use"
        exit 1
    fi
}

# ---------- Launch ----------
log_info "Starting inference-service..."
log_info "  Engine:    $ENGINE"
log_info "  Model:     $MODEL"
log_info "  HTTP:      $HOST:$PORT"
log_info "  Metrics:   $METRICS_PORT"
[[ "$ENGINE" == "vllm" ]] && log_info "  GPU Util:  $GPU_UTIL"

check_gpu
check_port

if [[ "$DRY_RUN" == "true" ]]; then
    log_info "Dry-run — command that would be executed:"
    echo "  ${CMD[*]}"
    exit 0
fi

# Guard: wait for port to be ready
wait_for_port() {
    local max_attempts=30
    local attempt=1
    while [[ $attempt -le $max_attempts ]]; do
        if ss -tuln 2>/dev/null | grep -q ":${PORT} "; then
            return 0
        fi
        sleep 1
        ((attempt++))
    done
    log_error "Port $PORT did not become available within ${max_attempts}s"
    exit 1
}

# Trap for cleanup on Ctrl+C
trap 'log_info "Shutting down..."; kill $$' INT TERM

"${CMD[@]}" &
PID=$!

log_info "Service started with PID $PID"
log_info "Waiting for port $PORT to be ready..."
wait_for_port

log_info "Service ready at http://${HOST}:${PORT}"
log_info "Health check: curl http://localhost:${PORT}/health"
log_info "Metrics:      curl http://localhost:${PORT}/metrics"

# Keep script alive
wait $PID
```

## 常用启动场景

| 场景 | 命令 |
|------|------|
| 开发（热重载） | `python -m uvicorn inference_service.server:app --reload --port 8000` |
| 生产（vLLM） | `scripts/serve.sh --engine vllm --model Qwen/Qwen2.5-0.5B-Instruct` |
| 生产（多卡） | `scripts/serve.sh --vllm-tensor-parallel-size 4` |
| 调试（eager） | `scripts/serve.sh --enforce-eager` |
| 生产（高吞吐） | `scripts/serve.sh --workers 4 --timeout 600` |

## 服务健康检查

```bash
# 轮询等待服务就绪
until curl -s http://localhost:8000/health | grep -q '"status":"healthy"'; do
    echo "Waiting for service..."
    sleep 5
done
echo "Service is healthy"
```

## 信号处理

| 信号 | 行为 |
|------|------|
| `SIGINT` (Ctrl+C) | 优雅关闭，停止服务进程 |
| `SIGTERM` | 优雅关闭 |
| `SIGQUIT` | 强制退出 |

---

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://docs.vllm.ai/en/latest/serving/health_checks.html — vLLM Health Checks

Risk of Staleness:
- vLLM CLI 参数可能随版本变化

Out of Scope Kept:
- 未写 systemd service 文件
- 未写 supervisor 配置
