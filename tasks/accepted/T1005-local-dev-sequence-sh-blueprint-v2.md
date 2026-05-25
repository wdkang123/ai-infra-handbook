# Local Dev Sequence Script Blueprint v2

## Task ID: T1005
## Title: Root / Dev Workflow Starter File Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T905 scaffold（local-dev-sequence blueprint v1），产出 v2 版本本地开发顺序脚本。

---

# Local Dev Sequence Script Blueprint v2

## 概述

本文档定义 `scripts/local_dev_sequence.sh` 的 v2 蓝图——本地开发时各服务的启动顺序脚本。

## `scripts/local_dev_sequence.sh` 模板

```bash
#!/usr/bin/env bash
# ============================================================
# ai-infra — scripts/local_dev_sequence.sh
# 本地开发顺序脚本：按正确顺序启动/停止所有服务
# ============================================================

set -euo pipefail

# ---------- Config ----------
INFERENCE_PORT="${INFERENCE_PORT:-8000}"
GATEWAY_PORT="${GATEWAY_PORT:-8080}"
INFERENCE_URL="http://localhost:${INFERENCE_PORT}"
GATEWAY_URL="http://localhost:${GATEWAY_PORT}"
MODEL="${MODEL:-Qwen/Qwen2.5-0.5B-Instruct}"
MAX_WAIT=60  # seconds to wait for each service

# ---------- Color ----------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info()  { echo -e "${BLUE}[INFO]${NC}  $*"; }
log_ok()    { echo -e "${GREEN}[OK]${NC}   $*"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC}  $*"; }
log_error() { echo -e "${RED}[ERROR]${NC} $*"; }

# ---------- Helpers ----------
wait_for_url() {
    local url="$1"
    local name="$2"
    local max_attempts=$((MAX_WAIT / 2))
    local attempt=1
    log_info "Waiting for $name at $url..."
    while [[ $attempt -le $max_attempts ]]; do
        if curl -s --max-time 2 "$url" > /dev/null 2>&1; then
            log_ok "$name is ready"
            return 0
        fi
        sleep 2
        ((attempt++))
    done
    log_error "$name failed to start within ${MAX_WAIT}s"
    return 1
}

stop_service() {
    local name="$1"
    local pattern="$2"
    local pids
    pids=$(pgrep -f "$pattern" 2>/dev/null || true)
    if [[ -n "$pids" ]]; then
        log_info "Stopping $name (PIDs: $pids)..."
        echo "$pids" | xargs kill 2>/dev/null || true
        sleep 1
    fi
}

# ---------- Start ----------
start_inference_service() {
    log_info "=== Starting inference-service ==="
    stop_service "inference-service" "inference-service"
    cd inference-service && make serve MODEL="$MODEL" PORT="$INFERENCE_PORT" &
    cd - > /dev/null
    wait_for_url "${INFERENCE_URL}/health" "inference-service"
}

start_ai_gateway() {
    log_info "=== Starting ai-gateway ==="
    stop_service "ai-gateway" "ai-gateway"
    cd ai-gateway && make serve PORT="$GATEWAY_PORT" &
    cd - > /dev/null
    wait_for_url "${GATEWAY_URL}/health" "ai-gateway"
}

# ---------- Stop ----------
stop_all() {
    log_info "=== Stopping all services ==="
    stop_service "inference-service" "inference-service"
    stop_service "ai-gateway" "ai-gateway"
    log_ok "All services stopped"
}

# ---------- Status ----------
status_check() {
    log_info "=== Service Status ==="
    for svc in "inference-service:${INFERENCE_URL}/health" "ai-gateway:${GATEWAY_URL}/health"; do
        local name="${svc%%:*}"
        local url="${svc##*:}"
        if curl -s --max-time 2 "$url" > /dev/null 2>&1; then
            log_ok "$name: running"
        else
            log_warn "$name: not running"
        fi
    done
}

# ---------- Main ----------
usage() {
    cat <<EOF
Usage: $0 [command]

Commands:
    start       Start all services in correct order
    stop        Stop all services
    restart     Restart all services
    status      Check service status
    help        Show this help

Examples:
    $0 start
    $0 stop
    $0 status
EOF
}

case "${1:-}" in
    start)
        stop_all
        start_inference_service
        start_ai_gateway
        log_ok "All services started"
        echo "  inference-service: ${INFERENCE_URL}"
        echo "  ai-gateway:        ${GATEWAY_URL}"
        ;;
    stop)
        stop_all
        ;;
    restart)
        stop_all
        sleep 2
        start_inference_service
        start_ai_gateway
        log_ok "All services restarted"
        ;;
    status)
        status_check
        ;;
    help|--help|-h)
        usage
        ;;
    *)
        usage
        ;;
esac
```

## 服务启动顺序（重要）

```
1. inference-service（必须先启动）
   ↓ wait for /health
2. ai-gateway（依赖 inference-service）
   ↓ wait for /health
Done
```

## 冒烟测试顺序

```bash
# 1. 启动所有服务
./scripts/local_dev_sequence.sh start

# 2. 等待就绪
sleep 5

# 3. 运行冒烟测试
make infra-smoke

# 4. 停止所有服务
./scripts/local_dev_sequence.sh stop
```

---

Sources:
1. https://docs.vllm.ai/ — vLLM
