# ai-gateway curl Catalog v1

## Task ID: T902
## Title: ai-gateway Scaffold Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T812 API contract（已收紧）、T802 validation checklist，产出 curl 命令合集。

---

# ai-gateway curl Catalog v1

## 概述

本文档定义 ai-gateway 的 `examples/curl_catalog.sh`。

## `examples/curl_catalog.sh` 模板

```bash
#!/usr/bin/env bash
# ============================================================
# ai-gateway — examples/curl_catalog.sh
# ============================================================

set -euo pipefail

# ---------- Config ----------
HOST="${GATEWAY_HOST:-localhost}"
PORT="${GATEWAY_PORT:-8080}"
BASE_URL="http://${HOST}:${PORT}"
MODEL="${GATEWAY_MODEL:-vllm-local}"
AUTH_KEY="${GATEWAY_AUTH_KEY:-sk-test-key-1}"
INVALID_KEY="invalid-key-xyz"

# ---------- Color ----------
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

info()    { echo -e "${GREEN}[INFO]${NC}  $*"; }
error()   { echo -e "${RED}[ERROR]${NC} $*"; }
section() { echo -e "\n${BLUE}=== $* ===${NC}"; }

# ---------- Health ----------
health() {
    section "Health Check"
    info "GET /health"
    curl -s "${BASE_URL}/health" | python -m json.tool
}

# ---------- Metrics ----------
metrics() {
    section "Prometheus Metrics"
    info "GET /metrics"
    curl -s "${BASE_URL}/metrics" | head -20
}

# ---------- Chat: Success ----------
chat_success() {
    section "POST /v1/chat/completions — Success"
    info "model=${MODEL} + valid auth"
    curl -s -X POST "${BASE_URL}/v1/chat/completions" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer ${AUTH_KEY}" \
        -d "{
            \"model\": \"${MODEL}\",
            \"messages\": [
                {\"role\": \"system\", \"content\": \"You are helpful.\"},
                {\"role\": \"user\", \"content\": \"What is 2+2?\"}
            ],
            \"temperature\": 0.7,
            \"max_tokens\": 256
        }" | python -m json.tool
}

# ---------- Chat: Streaming ----------
chat_stream() {
    section "POST /v1/chat/completions — Streaming"
    info "model=${MODEL} + stream=true"
    curl -s -X POST "${BASE_URL}/v1/chat/completions" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer ${AUTH_KEY}" \
        -d "{
            \"model\": \"${MODEL}\",
            \"messages\": [{\"role\": \"user\", \"content\": \"Count to 3\"}],
            \"stream\": true
        }"
}

# ---------- Chat: No Auth (expect 401) ----------
chat_no_auth() {
    section "POST /v1/chat/completions — No Auth (expect 401)"
    info "No Authorization header"
    response=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X POST "${BASE_URL}/v1/chat/completions" \
        -H "Content-Type: application/json" \
        -d "{
            \"model\": \"${MODEL}\",
            \"messages\": [{\"role\": \"user\", \"content\": \"Hello\"}]
        }")
    echo "$response"
}

# ---------- Chat: Invalid Auth (expect 401) ----------
chat_invalid_auth() {
    section "POST /v1/chat/completions — Invalid Auth (expect 401)"
    info "Authorization: Bearer ${INVALID_KEY}"
    response=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X POST "${BASE_URL}/v1/chat/completions" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer ${INVALID_KEY}" \
        -d "{
            \"model\": \"${MODEL}\",
            \"messages\": [{\"role\": \"user\", \"content\": \"Hello\"}]
        }")
    echo "$response"
}

# ---------- Chat: Invalid Model (expect 404) ----------
chat_invalid_model() {
    section "POST /v1/chat/completions — Invalid Model (expect 404)"
    info "model=unknown-model-xyz"
    response=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X POST "${BASE_URL}/v1/chat/completions" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer ${AUTH_KEY}" \
        -d "{
            \"model\": \"unknown-model-xyz\",
            \"messages\": [{\"role\": \"user\", \"content\": \"Hello\"}]
        }")
    echo "$response" | python -m json.tool || echo "$response"
}

# ---------- Rate Limit Test ----------
rate_limit_test() {
    section "POST /v1/chat/completions — Rate Limit Test"
    info "Sending 65 requests (RPM=60)"
    success=0
    rate_limited=0
    for i in $(seq 1 65); do
        status=$(curl -s -o /dev/null -w "%{http_code}" -X POST "${BASE_URL}/v1/chat/completions" \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer ${AUTH_KEY}" \
            -d "{\"model\":\"${MODEL}\",\"messages\":[{\"role\":\"user\",\"content\":\"test\"}]}")
        if [[ "$status" == "200" ]]; then
            ((success++))
        elif [[ "$status" == "429" ]]; then
            ((rate_limited++))
        fi
    done
    info "Success: $success / Rate-limited: $rate_limited"
}

# ---------- All ----------
all() {
    health
    metrics
    chat_success
    chat_stream
    chat_no_auth
    chat_invalid_auth
    chat_invalid_model
}

# ---------- Help ----------
usage() {
    cat <<EOF
ai-gateway curl Catalog

Usage: $0 [command]

Commands:
    health          Health check
    metrics         Prometheus metrics
    chat            Non-streaming chat
    chat-stream     Streaming chat
    no-auth         Without auth (expect 401)
    invalid-auth    Invalid auth (expect 401)
    invalid-model   Unknown model (expect 404)
    rate-limit      Rate limit test
    all             Run all (default)

Environment variables:
    GATEWAY_HOST      Default: localhost
    GATEWAY_PORT      Default: 8080
    GATEWAY_AUTH_KEY  Default: sk-test-key-1

Examples:
    $0 health
    GATEWAY_PORT=9000 $0 chat
EOF
}

COMMAND="${1:-all}"

case "$COMMAND" in
    health)         health ;;
    metrics)        metrics ;;
    chat)           chat_success ;;
    chat-stream)    chat_stream ;;
    no-auth)        chat_no_auth ;;
    invalid-auth)   chat_invalid_auth ;;
    invalid-model)  chat_invalid_model ;;
    rate-limit)     rate_limit_test ;;
    all)            all ;;
    help|--help|-h) usage ;;
    *)              error "Unknown: $COMMAND"; usage; exit 1 ;;
esac
```

## curl 命令速查

| 场景 | 命令 | 预期结果 |
|------|------|---------|
| 健康检查 | `curl localhost:8080/health` | `{"status":"healthy",...}` |
| 成功请求 | `curl .../v1/chat/completions -H "Authorization: Bearer sk-test-key-1"` | OpenAI 格式响应 |
| 流式请求 | `curl .../v1/chat/completions -d '{"stream":true}'` | SSE 流 |
| 无 Auth | 无 `-H "Authorization"` | 401 |
| 无效 Key | `Bearer invalid-key` | 401 |
| 未知模型 | `model=unknown` | 404 |
| 超出 RPM | 连续 65+ 请求 | 429 |

## Python requests 示例

```python
import httpx

GATEWAY = "http://localhost:8080"
KEY = "sk-test-key-1"

# Success
resp = httpx.post(
    f"{GATEWAY}/v1/chat/completions",
    headers={"Authorization": f"Bearer {KEY}"},
    json={"model": "vllm-local", "messages": [{"role": "user", "content": "Hi"}]},
)
print(resp.json())

# Auth failure
resp = httpx.post(
    f"{GATEWAY}/v1/chat/completions",
    headers={"Authorization": "Bearer wrong-key"},
    json={"model": "vllm-local", "messages": [{"role": "user", "content": "Hi"}]},
)
print(resp.status_code)  # 401
```

---

Sources:
1. https://github.com/Portkey-AI/gateway — Portkey Gateway
2. https://github.com/BerriAI/litellm — LiteLLM

Risk of Staleness:
- Gateway API 响应格式可能随版本变化

Out of Scope Kept:
- 未写 Python SDK 示例
