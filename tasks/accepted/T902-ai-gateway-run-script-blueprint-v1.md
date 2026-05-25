# ai-gateway Run Script Blueprint v1

## Task ID: T902
## Title: ai-gateway Scaffold Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T802 repo layout 和 validation checklist，产出启动脚本模板。

---

# ai-gateway Run Script Blueprint v1

## 概述

本文档定义 ai-gateway 的服务启动脚本模板 `scripts/serve.sh`。

## `scripts/serve.sh` 模板

```bash
#!/usr/bin/env bash
# ============================================================
# ai-gateway — scripts/serve.sh
# ============================================================

set -euo pipefail

# ---------- Defaults ----------
PORT="${GATEWAY_PORT:-8080}"
METRICS_PORT="${METRICS_PORT:-9091}"
HOST="${GATEWAY_HOST:-0.0.0.0}"
WORKERS="${GATEWAY_WORKERS:-1}"
TIMEOUT="${GATEWAY_TIMEOUT:-300}"
AUTH_ENABLED="${AUTH_ENABLED:-true}"
RATE_LIMIT_ENABLED="${RATE_LIMIT_ENABLED:-true}"
LOG_LEVEL="${LOGGING_LEVEL:-INFO}"

# ---------- Color output ----------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info()  { echo -e "${GREEN}[INFO]${NC}  $*"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC}  $*"; }
log_error() { echo -e "${RED}[ERROR]${NC} $*" >&2; }

# ---------- Help ----------
usage() {
    cat <<EOF
Usage: $0 [OPTIONS]

Start ai-gateway proxy server.

OPTIONS:
    -p, --port PORT           Gateway HTTP port (default: 8080)
    --metrics-port PORT       Prometheus metrics port (default: 9091)
    -h, --host HOST           Listen address (default: 0.0.0.0)
    --workers INT             Uvicorn workers (default: 1)
    --timeout INT             Request timeout seconds (default: 300)
    --auth-disabled           Disable auth middleware
    --rate-limit-disabled     Disable rate limit middleware
    --log-level LEVEL         Log level: DEBUG|INFO|WARNING|ERROR (default: INFO)
    --dry-run                 Print command without executing
    --help                    Show this help

ENVIRONMENT:
    GATEWAY_PORT, GATEWAY_HOST, AUTH_ENABLED, RATE_LIMIT_ENABLED, etc.
    can also be set via environment variables.

EXAMPLES:
    # Default
    $0

    # Production
    $0 --port 8080 --workers 4 --log-level INFO

    # Dev (no auth/rate-limit)
    $0 --auth-disabled --rate-limit-disabled --log-level DEBUG
EOF
}

# ---------- Parse args ----------
DRY_RUN=false
AUTH_ARG=""
RATE_LIMIT_ARG=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -p|--port)          PORT="$2"; shift 2 ;;
        --metrics-port)     METRICS_PORT="$2"; shift 2 ;;
        -h|--host)          HOST="$2"; shift 2 ;;
        --workers)          WORKERS="$2"; shift 2 ;;
        --timeout)          TIMEOUT="$2"; shift 2 ;;
        --auth-disabled)    AUTH_ENABLED=false; shift ;;
        --rate-limit-disabled) RATE_LIMIT_ENABLED=false; shift ;;
        --log-level)        LOG_LEVEL="$2"; shift 2 ;;
        --dry-run)          DRY_RUN=true; shift ;;
        --help)             usage; exit 0 ;;
        *)                  log_error "Unknown: $1"; usage; exit 1 ;;
    esac
done

# ---------- Build command ----------
CMD=(ai-gateway serve)
CMD+=(--port "$PORT")
CMD+=(--host "$HOST")
CMD+=(--workers "$WORKERS")
CMD+=(--timeout "$TIMEOUT")
CMD+=(--metrics-port "$METRICS_PORT")
CMD+=(--log-level "$LOG_LEVEL")

if [[ "$AUTH_ENABLED" == "false" ]]; then
    CMD+=(--no-auth)
fi
if [[ "$RATE_LIMIT_ENABLED" == "false" ]]; then
    CMD+=(--no-rate-limit)
fi

# ---------- Pre-launch check ----------
check_port() {
    if ss -tuln 2>/dev/null | grep -q ":${PORT} "; then
        log_error "Port $PORT is already in use"
        exit 1
    fi
}

# ---------- Launch ----------
log_info "Starting ai-gateway..."
log_info "  HTTP:     $HOST:$PORT"
log_info "  Metrics:  $METRICS_PORT"
[[ "$AUTH_ENABLED" == "false" ]] && log_warn "  Auth:     DISABLED"
[[ "$RATE_LIMIT_ENABLED" == "false" ]] && log_warn "  RateLim: DISABLED"

check_port

if [[ "$DRY_RUN" == "true" ]]; then
    log_info "Dry-run — command that would be executed:"
    echo "  ${CMD[*]}"
    exit 0
fi

# Trap for cleanup
trap 'log_info "Shutting down..."; kill $$' INT TERM

"${CMD[@]}" &
PID=$!

log_info "Gateway started with PID $PID"
log_info "Health:    curl http://localhost:${PORT}/health"
log_info "Metrics:   curl http://localhost:${PORT}/metrics"

wait $PID
```

## 常用启动场景

| 场景 | 命令 |
|------|------|
| 开发（关闭鉴权和限流） | `scripts/serve.sh --auth-disabled --rate-limit-disabled --log-level DEBUG` |
| 生产 | `scripts/serve.sh --workers 4` |
| 仅限流无鉴权 | `scripts/serve.sh --auth-disabled` |
| 干跑 | `scripts/serve.sh --dry-run` |

## 服务健康检查

```bash
# 轮询等待服务就绪
until curl -s http://localhost:8080/health | grep -q '"status":"healthy"'; do
    echo "Waiting for gateway..."
    sleep 2
done
echo "Gateway is healthy"
```

---

Sources:
1. https://github.com/Portkey-AI/gateway — Portkey Gateway
2. https://github.com/laurentS/slowapi — Slowapi

Risk of Staleness:
- Gateway CLI 参数尚未确定（取决于 FastAPI/Typer 实现）

Out of Scope Kept:
- 未写 systemd service
- 未写 supervisor 配置
