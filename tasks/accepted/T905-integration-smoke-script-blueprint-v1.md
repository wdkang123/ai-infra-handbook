# Integration Smoke Script Blueprint v1

## Task ID: T905
## Title: Developer Workflow Scaffold Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T805 integration test matrix，产出集成冒烟测试脚本模板。

---

# Integration Smoke Script Blueprint v1

## 概述

本文档定义集成冒烟测试脚本，对应 T805 integration test matrix 的 P0 测试项。

## `scripts/integration_smoke_test.sh` 模板

```bash
#!/usr/bin/env bash
# ============================================================
# ai-infra — scripts/integration_smoke_test.sh
# 集成冒烟测试，对应 T805 IT-01 ~ IT-07 P0 项
# ============================================================

set -euo pipefail

# ---------- Config ----------
INFERENCE_URL="${INFERENCE_URL:-http://localhost:8000}"
GATEWAY_URL="${GATEWAY_URL:-http://localhost:8080}"
MODEL="${MODEL_NAME:-Qwen/Qwen2.5-0.5B-Instruct}"
AUTH_KEY="${SMOKE_AUTH_KEY:-dev-gateway-key-1}"
RESULTS_DIR="${SMOKE_RESULTS_DIR:-./results/smoke}"

# ---------- Color ----------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

PASS=0
FAIL=0

pass() { echo -e "${GREEN}[PASS]${NC}  $*"; ((PASS++)); }
fail() { echo -e "${RED}[FAIL]${NC}  $*"; ((FAIL++)); }
info() { echo -e "${YELLOW}[INFO]${NC}  $*"; }

# ---------- Setup ----------
setup() {
    mkdir -p "$RESULTS_DIR"
    info "Smoke test results: $RESULTS_DIR"
}

# ---------- IT-01: ai-gateway → inference-service ----------
test_it01() {
    info "=== IT-01: Gateway → Inference (basic proxy) ==="
    local response
    response=$(curl -s -w "\n%{http_code}" -X POST "${GATEWAY_URL}/v1/chat/completions" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer ${AUTH_KEY}" \
        -d "{
            \"model\": \"vllm-local\",
            \"messages\": [{\"role\": \"user\", \"content\": \"What is 2+2?\"}]
        }")
    local status
    status=$(echo "$response" | tail -1)
    local body
    body=$(echo "$response" | head -1)

    if [[ "$status" == "200" ]]; then
        pass "IT-01: Gateway proxy returned 200"
        echo "$body" >> "${RESULTS_DIR}/it01.json"
    else
        fail "IT-01: Expected 200, got $status"
    fi
}

# ---------- IT-01b: Direct inference-service ----------
test_it01_direct() {
    info "=== IT-01b: Direct inference-service ==="
    local response
    response=$(curl -s -w "\n%{http_code}" -X POST "${INFERENCE_URL}/v1/chat/completions" \
        -H "Content-Type: application/json" \
        -d "{
            \"model\": \"${MODEL}\",
            \"messages\": [{\"role\": \"user\", \"content\": \"What is 2+2?\"}]
        }")
    local status
    status=$(echo "$response" | tail -1)

    if [[ "$status" == "200" ]]; then
        pass "IT-01b: inference-service direct returned 200"
    else
        fail "IT-01b: Expected 200, got $status"
    fi
}

# ---------- IT-02: Streaming ----------
test_it02() {
    info "=== IT-02: Streaming ==="
    local output
    output=$(curl -s -X POST "${INFERENCE_URL}/v1/chat/completions" \
        -H "Content-Type: application/json" \
        -d "{
            \"model\": \"${MODEL}\",
            \"messages\": [{\"role\": \"user\", \"content\": \"Count to 3\"}],
            \"stream\": true
        }" | head -5)

    if echo "$output" | grep -q "data:"; then
        pass "IT-02: Streaming response contains SSE data"
    else
        fail "IT-02: Streaming response missing SSE data"
    fi
}

# ---------- IT-03: Health checks ----------
test_it03() {
    info "=== IT-03: Health checks ==="
    local status
    status=$(curl -s -o /dev/null -w "%{http_code}" "${INFERENCE_URL}/health")
    if [[ "$status" == "200" ]]; then
        pass "IT-03: inference-service /health returned 200"
    else
        fail "IT-03: inference-service /health expected 200, got $status"
    fi

    status=$(curl -s -o /dev/null -w "%{http_code}" "${GATEWAY_URL}/health")
    if [[ "$status" == "200" ]]; then
        pass "IT-03: ai-gateway /health returned 200"
    else
        fail "IT-03: ai-gateway /health expected 200, got $status"
    fi
}

# ---------- IT-04: Auth — no token ----------
test_it04() {
    info "=== IT-04: Gateway auth (no token, expect 401) ==="
    local status
    status=$(curl -s -o /dev/null -w "%{http_code}" -X POST "${GATEWAY_URL}/v1/chat/completions" \
        -H "Content-Type: application/json" \
        -d "{
            \"model\": \"vllm-local\",
            \"messages\": [{\"role\": \"user\", \"content\": \"Hi\"}]
        }")
    if [[ "$status" == "401" ]]; then
        pass "IT-04: No token → 401"
    else
        fail "IT-04: Expected 401, got $status"
    fi
}

# ---------- IT-05: Auth — invalid token ----------
test_it05() {
    info "=== IT-05: Gateway auth (invalid token, expect 401) ==="
    local status
    status=$(curl -s -o /dev/null -w "%{http_code}" -X POST "${GATEWAY_URL}/v1/chat/completions" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer invalid-key-xyz" \
        -d "{
            \"model\": \"vllm-local\",
            \"messages\": [{\"role\": \"user\", \"content\": \"Hi\"}]
        }")
    if [[ "$status" == "401" ]]; then
        pass "IT-05: Invalid token → 401"
    else
        fail "IT-05: Expected 401, got $status"
    fi
}

# ---------- IT-06: Unknown model ----------
test_it06() {
    info "=== IT-06: Gateway (unknown model, expect 404) ==="
    local status
    status=$(curl -s -o /dev/null -w "%{http_code}" -X POST "${GATEWAY_URL}/v1/chat/completions" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer ${AUTH_KEY}" \
        -d "{
            \"model\": \"unknown-model-xyz\",
            \"messages\": [{\"role\": \"user\", \"content\": \"Hi\"}]
        }")
    if [[ "$status" == "404" ]]; then
        pass "IT-06: Unknown model → 404"
    else
        fail "IT-06: Expected 404, got $status"
    fi
}

# ---------- IT-07: Metrics endpoints ----------
test_it07() {
    info "=== IT-07: Metrics endpoints ==="
    local body
    body=$(curl -s "${INFERENCE_URL}/metrics")
    if echo "$body" | grep -q "vllm_"; then
        pass "IT-07: inference-service /metrics contains vllm_ metrics"
    else
        fail "IT-07: inference-service /metrics missing vllm_ metrics"
    fi

    body=$(curl -s "${GATEWAY_URL}/metrics")
    if echo "$body" | grep -q "ai_gateway_"; then
        pass "IT-07: ai-gateway /metrics contains ai_gateway_ metrics"
    else
        fail "IT-07: ai-gateway /metrics missing ai_gateway_ metrics"
    fi
}

# ---------- Summary ----------
summary() {
    echo ""
    echo "=========================================="
    echo -e "Smoke Test Summary: ${GREEN}${PASS} passed${NC}, ${RED}${FAIL} failed${NC}"
    echo "=========================================="
    if [[ $FAIL -gt 0 ]]; then
        exit 1
    fi
    exit 0
}

# ---------- Main ----------
setup
test_it01_direct
test_it01
test_it02
test_it03
test_it04
test_it05
test_it06
test_it07
summary
```

## 冒烟测试覆盖矩阵

| 测试 ID | 场景 | 预期结果 | IT 覆盖 |
|---------|------|---------|---------|
| IT-01 | Gateway → Inference | 200 + response | IT-01 |
| IT-01b | Direct Inference | 200 + response | IT-01 |
| IT-02 | Streaming | SSE data | IT-01 |
| IT-03 | Health both | 200 | IT-01 |
| IT-04 | No auth | 401 | IT-03 |
| IT-05 | Invalid auth | 401 | IT-03 |
| IT-06 | Unknown model | 404 | IT-01 |
| IT-07 | Metrics | Prometheus format | IT-05 |

## 运行方式

```bash
# 完整冒烟测试
bash scripts/integration_smoke_test.sh

# 指定不同端口
INFERENCE_URL=http://localhost:9000 GATEWAY_URL=http://localhost:9080 \
  bash scripts/integration_smoke_test.sh
```

---

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://github.com/Portkey-AI/gateway — Portkey Gateway

Risk of Staleness:
- 冒烟测试可能因实现细节调整

Out of Scope Kept:
- 未写完整集成测试（需要 GPU）
- 未写评测冒烟测试（IT-04, IT-07）
