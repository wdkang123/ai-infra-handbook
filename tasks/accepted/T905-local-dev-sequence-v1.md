# Local Dev Sequence v1

## Task ID: T905
## Title: Developer Workflow Scaffold Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T815 implementation order 和 T805 integration test matrix，产出本地开发顺序脚本。

---

# Local Dev Sequence v1

## 概述

本文档定义 Codex 执行本地开发的标准顺序，确保模块按正确依赖关系启动。

## `scripts/local_dev_sequence.sh` 模板

```bash
#!/usr/bin/env bash
# ============================================================
# ai-infra — scripts/local_dev_sequence.sh
# 本地开发环境启动顺序脚本
# 遵循 T815 实现顺序
# ============================================================

set -euo pipefail

# ---------- Config ----------
MODEL="${MODEL_NAME:-Qwen/Qwen2.5-0.5B-Instruct}"
INFERENCE_PORT="${INFERENCE_PORT:-8000}"
GATEWAY_PORT="${GATEWAY_PORT:-8080}"
BASE_URL="http://localhost:${INFERENCE_PORT}"
START_WAIT=30

# ---------- Color ----------
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

log()    { echo -e "${GREEN}[SEQ]${NC}  $*"; }
warn()   { echo -e "${YELLOW}[WARN]${NC} $*"; }
error()  { echo -e "${RED}[ERR]${NC}  $*" >&2; }
section(){ echo -e "\n${BLUE}=== $* ===${NC}"; }

# ---------- Check utility ----------
check_service() {
    local name="$1"
    local url="$2"
    local max_attempts=10
    local attempt=1
    while [[ $attempt -le $max_attempts ]]; do
        if curl -s --max-time 5 "$url" > /dev/null 2>&1; then
            log "$name is ready at $url"
            return 0
        fi
        echo -n "."
        sleep 2
        ((attempt++))
    done
    error "$name not ready at $url after ${max_attempts} attempts"
    return 1
}

# ---------- Stop all ----------
stop_all() {
    section "Stopping all services"
    pkill -f "inference-service" 2>/dev/null || true
    pkill -f "ai-gateway" 2>/dev/null || true
    pkill -f "uvicorn" 2>/dev/null || true
    sleep 2
    log "All services stopped"
}

# ---------- Step 0: Verify dependencies ----------
verify_dependencies() {
    section "Step 0: Verifying dependencies"
    local missing=()
    for cmd in curl git python pip make; do
        if ! command -v $cmd &>/dev/null; then
            missing+=("$cmd")
        fi
    done
    if [[ ${#missing[@]} -gt 0 ]]; then
        error "Missing dependencies: ${missing[*]}"
        exit 1
    fi
    log "All required commands available"
}

# ---------- Step 1: Install all modules ----------
install_all() {
    section "Step 1: Installing all modules"
    log "Installing inference-service..."
    make -C inference-service install-dev || warn "inference-service install failed"

    log "Installing ai-gateway..."
    make -C ai-gateway install-dev || warn "ai-gateway install failed"

    log "Installing eval-module..."
    make -C eval-module install-dev || warn "eval-module install failed"

    log "Installing finetune-demo..."
    make -C finetune-demo install-dev || warn "finetune-demo install failed"

    log "All modules installed"
}

# ---------- Step 2: Start inference-service ----------
start_inference() {
    section "Step 2: Starting inference-service (T1-02)"
    log "Model: ${MODEL}, Port: ${INFERENCE_PORT}"

    # Check if already running
    if curl -s --max-time 2 "${BASE_URL}/health" > /dev/null 2>&1; then
        warn "inference-service already running, skipping start"
    else
        make -C inference-service serve \
            MODEL="$MODEL" \
            PORT="$INFERENCE_PORT" &

        log "Waiting ${START_WAIT}s for inference-service to load model..."
        sleep "$START_WAIT"
    fi

    check_service "inference-service" "${BASE_URL}/health" || {
        error "inference-service failed to start"
        exit 1
    }
    log "inference-service ready"
}

# ---------- Step 3: Start ai-gateway ----------
start_gateway() {
    section "Step 3: Starting ai-gateway (T1-08)"
    log "Gateway Port: ${GATEWAY_PORT}"

    if curl -s --max-time 2 "http://localhost:${GATEWAY_PORT}/health" > /dev/null 2>&1; then
        warn "ai-gateway already running, skipping start"
    else
        make -C ai-gateway serve PORT="$GATEWAY_PORT" &
        sleep 5
    fi

    check_service "ai-gateway" "http://localhost:${GATEWAY_PORT}/health" || {
        error "ai-gateway failed to start"
        exit 1
    }
    log "ai-gateway ready"
}

# ---------- Step 4: Smoke test ----------
smoke_test() {
    section "Step 4: Running smoke tests (IT-01)"
    log "Testing inference-service directly..."
    curl -s -X POST "${BASE_URL}/v1/chat/completions" \
        -H "Content-Type: application/json" \
        -d "{
            \"model\": \"${MODEL}\",
            \"messages\": [{\"role\": \"user\", \"content\": \"Hi\"}]
        }" | python -m json.tool || {
        error "inference-service smoke test failed"
        exit 1
    }

    log "Testing ai-gateway with auth..."
    curl -s -X POST "http://localhost:${GATEWAY_PORT}/v1/chat/completions" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer dev-gateway-key-1" \
        -d "{
            \"model\": \"vllm-local\",
            \"messages\": [{\"role\": \"user\", \"content\": \"Hi\"}]
        }" | python -m json.tool || {
        error "ai-gateway smoke test failed"
        exit 1
    }

    log "Smoke tests passed"
}

# ---------- Step 5: Setup eval data (optional) ----------
setup_eval() {
    section "Step 5: Optional — Verify eval-module"
    log "eval-module CLI check..."
    make -C eval-module run-mmlu LIMIT=5 MODEL="$MODEL" \
        BACKEND_URL="${BASE_URL}/v1" || warn "eval-module test failed (ok if not ready)"
}

# ---------- Main ----------
usage() {
    cat <<EOF
Usage: $0 [command]

Commands:
    start       Start all services in correct order
    stop        Stop all services
    restart     Stop and start
    smoke       Run smoke tests only
    install     Install all modules without starting
    help        Show this help

Examples:
    $0 start        # Full start
    $0 smoke       # Smoke test only
    $0 stop        # Stop all
EOF
}

COMMAND="${1:-start}"

case "$COMMAND" in
    start)
        verify_dependencies
        install_all
        start_inference
        start_gateway
        smoke_test
        log "Local dev environment ready!"
        log "  inference-service: http://localhost:${INFERENCE_PORT}"
        log "  ai-gateway:        http://localhost:${GATEWAY_PORT}"
        ;;
    stop)    stop_all ;;
    restart) stop_all; $0 start ;;
    smoke)   smoke_test ;;
    install) install_all ;;
    help|--help|-h) usage ;;
    *)        error "Unknown: $COMMAND"; usage; exit 1 ;;
esac
```

## 开发流程

```bash
# 第一次设置
make install   # 安装所有依赖
make start     # 启动所有服务

# 每次开发
make smoke     # 验证所有服务正常

# 完成后
make stop      # 停止所有服务
```

## 依赖顺序图

```
Step 1: install_all
           │
Step 2: start_inference ──→ inference-service (port 8000)
           │                         │
Step 3: start_gateway ────────────→ ai-gateway (port 8080)
           │
Step 4: smoke_test ───────────────→ E2E validation
           │
Step 5: setup_eval ──────────────→ eval-module (可选)
```

---

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval

Risk of Staleness:
- 模型加载时间随模型大小变化（30s 可能不够）

Out of Scope Kept:
- 未写自动重启脚本
- 未写模型热更新
