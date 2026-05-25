# inference-service curl Catalog v1

## Task ID: T901
## Title: inference-service Scaffold Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T811 API contract（已收紧）、T801 validation checklist，产出 curl 命令合集。

---

# inference-service curl Catalog v1

## 概述

本文档定义 inference-service 的 `examples/curl_catalog.sh`，包含所有端点的 curl 调用示例。

## `examples/curl_catalog.sh` 模板

```bash
#!/usr/bin/env bash
# ============================================================
# inference-service — examples/curl_catalog.sh
# 所有 API 端点 curl 调用合集
# 使用方法: bash examples/curl_catalog.sh [command]
# ============================================================

set -euo pipefail

# ---------- Config ----------
HOST="${INFERENCE_HOST:-localhost}"
PORT="${INFERENCE_PORT:-8000}"
BASE_URL="http://${HOST}:${PORT}"
MODEL="${INFERENCE_MODEL:-Qwen/Qwen2.5-0.5B-Instruct}"
TIMEOUT="${CURL_TIMEOUT:-60}"

# ---------- Color output ----------
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

info()    { echo -e "${GREEN}[INFO]${NC}  $*"; }
warn()    { echo -e "${YELLOW}[WARN]${NC}  $*"; }
error()   { echo -e "${RED}[ERROR]${NC} $*"; }
section() { echo -e "\n${BLUE}=== $* ===${NC}"; }

curl_cmd() {
    echo -e "\n${YELLOW}\$ curl${NC} $*"
    curl -s -X POST "${@:1}"
}

curl_get() {
    echo -e "\n${YELLOW}\$ curl${NC} $*"
    curl -s -X GET "${@:1}"
}

# ---------- Health Check ----------
health() {
    section "Health Check"
    info "GET /health"
    curl_get "${BASE_URL}/health" | python -m json.tool
}

# ---------- Metrics ----------
metrics() {
    section "Prometheus Metrics"
    info "GET /metrics"
    curl_get "${BASE_URL}/metrics" | head -30
}

# ---------- Chat Completions — Non-Streaming ----------
chat() {
    section "POST /v1/chat/completions (non-streaming)"
    info "model=${MODEL}"
    curl_cmd "${BASE_URL}/v1/chat/completions" \
        -H "Content-Type: application/json" \
        -d "{
            \"model\": \"${MODEL}\",
            \"messages\": [
                {\"role\": \"system\", \"content\": \"You are a helpful assistant.\"},
                {\"role\": \"user\", \"content\": \"What is the capital of France?\"}
            ],
            \"temperature\": 0.7,
            \"max_tokens\": 256,
            \"stream\": false
        }" | python -m json.tool
}

# ---------- Chat Completions — Streaming ----------
chat_stream() {
    section "POST /v1/chat/completions (streaming)"
    info "model=${MODEL} — streaming"
    curl_cmd "${BASE_URL}/v1/chat/completions" \
        -H "Content-Type: application/json" \
        -d "{
            \"model\": \"${MODEL}\",
            \"messages\": [{\"role\": \"user\", \"content\": \"Count to 5\"}],
            \"stream\": true
        }"
}

# ---------- Chat Completions — With Stop ----------
chat_with_stop() {
    section "POST /v1/chat/completions (with stop token)"
    info "model=${MODEL} — stop on 'done'"
    curl_cmd "${BASE_URL}/v1/chat/completions" \
        -H "Content-Type: application/json" \
        -d "{
            \"model\": \"${MODEL}\",
            \"messages\": [{\"role\": \"user\", \"content\": \"Say hello\"}],
            \"stop\": [\"done\"],
            \"max_tokens\": 50
        }" | python -m json.tool
}

# ---------- Error: Invalid Model ----------
chat_invalid_model() {
    section "Error Case: Invalid Model"
    info "Expected: 404 not_found_error"
    response=$(curl_cmd "${BASE_URL}/v1/chat/completions" \
        -H "Content-Type: application/json" \
        -d "{
            \"model\": \"invalid-model-xyz\",
            \"messages\": [{\"role\": \"user\", \"content\": \"test\"}]
        }")
    echo "$response" | python -m json.tool || echo "$response"
}

# ---------- Error: Empty Messages ----------
chat_empty_messages() {
    section "Error Case: Empty Messages"
    info "Expected: 422 validation_error"
    response=$(curl_cmd "${BASE_URL}/v1/chat/completions" \
        -H "Content-Type: application/json" \
        -d "{
            \"model\": \"${MODEL}\",
            \"messages\": []
        }")
    echo "$response" | python -m json.tool || echo "$response"
}

# ---------- All Endpoints ----------
all() {
    health
    metrics
    chat
    chat_stream
    chat_with_stop
    chat_invalid_model
    chat_empty_messages
}

# ---------- Help ----------
usage() {
    cat <<EOF
inference-service curl Catalog

Usage: $0 [command]

Commands:
    health              Health check
    metrics             Prometheus metrics
    chat                Chat completions (non-streaming)
    chat-stream         Chat completions (streaming)
    chat-stop           Chat completions with stop token
    invalid-model       Error case: invalid model
    empty-messages      Error case: empty messages
    all                 Run all commands (default)

Environment variables:
    INFERENCE_HOST      Default: localhost
    INFERENCE_PORT      Default: 8000
    INFERENCE_MODEL     Default: Qwen/Qwen2.5-0.5B-Instruct
    CURL_TIMEOUT        Default: 60

Examples:
    $0 health
    $0 chat-stream
    INFERENCE_PORT=9000 INFERENCE_MODEL=Qwen/Qwen2.5-1.5B-Instruct $0 all
EOF
}

# ---------- Main ----------
COMMAND="${1:-all}"

case "$COMMAND" in
    health)          health ;;
    metrics)         metrics ;;
    chat)            chat ;;
    chat-stream)     chat_stream ;;
    chat-stop)       chat_with_stop ;;
    invalid-model)   chat_invalid_model ;;
    empty-messages)  chat_empty_messages ;;
    all)             all ;;
    help|--help|-h)  usage ;;
    *)               error "Unknown command: $COMMAND"; usage; exit 1 ;;
esac
```

## curl 命令速查

| 场景 | 命令 | 预期结果 |
|------|------|---------|
| 健康检查 | `curl localhost:8000/health` | `{"status":"healthy",...}` |
| 基本推理 | `curl .../v1/chat/completions -d {...}` | OpenAI 格式响应 |
| 流式推理 | `curl .../v1/chat/completions -d '{"stream":true}'` | SSE 数据流 |
| Metrics | `curl localhost:8000/metrics` | Prometheus 格式 |
| 无效模型 | `curl .../v1/chat/completions -d '{"model":"x"}'` | 404 error |
| 空消息 | `curl .../v1/chat/completions -d '{"messages":[]}'` | 422 error |

## Python requests 示例（非 curl）

```python
# examples/quickstart.py
import httpx
import json

MODEL = "Qwen/Qwen2.5-0.5B-Instruct"
BASE_URL = "http://localhost:8000"

# Non-streaming
response = httpx.post(
    f"{BASE_URL}/v1/chat/completions",
    json={
        "model": MODEL,
        "messages": [{"role": "user", "content": "What is 2+2?"}],
        "stream": False,
    },
    timeout=60.0,
)
print(response.json())

# Streaming
with httpx.stream(
    "POST",
    f"{BASE_URL}/v1/chat/completions",
    json={
        "model": MODEL,
        "messages": [{"role": "user", "content": "Count to 3"}],
        "stream": True,
    },
    timeout=60.0,
) as response:
    for line in response.iter_lines():
        if line.startswith("data: "):
            print(line)
```

---

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://docs.vllm.ai/en/latest/getting_started/quickstart.html — vLLM Quickstart

Risk of Staleness:
- vLLM API 响应格式可能随版本变化

Out of Scope Kept:
- 未写 Python SDK 示例
- 未写 WebSocket 示例
