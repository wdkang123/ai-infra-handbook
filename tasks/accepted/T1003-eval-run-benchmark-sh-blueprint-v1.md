# eval-module run_benchmark.sh Blueprint v1

## Task ID: T1003
## Title: eval-module Starter File Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T903 scaffold（runner-cli blueprint），产出 `run_benchmark.sh` 脚本蓝图 v1。

---

# eval-module run_benchmark.sh Blueprint v1

## 概述

本文档定义 `scripts/run_benchmark.sh` 的蓝图——便捷 benchmark 运行脚本。

## `scripts/run_benchmark.sh` 模板

```bash
#!/usr/bin/env bash
# ============================================================
# eval-module — scripts/run_benchmark.sh
# 便捷 benchmark 运行脚本
# ============================================================

set -euo pipefail

# ---------- Defaults ----------
TASK="${EVAL_TASK:-mmlu}"
MODEL="${EVAL_MODEL:-Qwen/Qwen2.5-0.5B-Instruct}"
BACKEND_URL="${EVAL_BACKEND_URL:-http://localhost:8000/v1}"
NUM_FEWSHOT="${EVAL_NUM_FEWSHOT:-5}"
LIMIT="${EVAL_LIMIT:-}"  # empty = full
RESULTS_DIR="${EVAL_RESULTS_DIR:-./results}"

# ---------- Color ----------
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info()  { echo -e "${GREEN}[INFO]${NC}  $*"; }
log_error() { echo -e "${RED}[ERROR]${NC} $*" >&2; }

# ---------- Check inference-service ----------
check_backend() {
    log_info "Checking inference-service at ${BACKEND_URL}..."
    if curl -s --max-time 5 "${BACKEND_URL}" > /dev/null 2>&1; then
        log_info "Backend is reachable"
    else
        log_error "Backend not reachable at ${BACKEND_URL}"
        log_error "Please start inference-service first"
        exit 1
    fi
}

# ---------- Run benchmark ----------
run_benchmark() {
    local task="$1"
    local timestamp
    timestamp=$(date +%Y%m%d_%H%M%S)
    local output="${RESULTS_DIR}/${task}_${timestamp}.json"

    mkdir -p "${RESULTS_DIR}"

    log_info "Running ${task} benchmark..."
    log_info "  Model:    ${MODEL}"
    log_info "  Backend:  ${BACKEND_URL}"
    log_info "  Few-shot: ${NUM_FEWSHOT}"
    log_info "  Output:   ${output}"

    local limit_arg=()
    [[ -n "$LIMIT" ]] && limit_arg=(--limit "$LIMIT")

    eval-module run \
        --task "$task" \
        --model "${MODEL}" \
        --backend-url "${BACKEND_URL}" \
        --num-fewshot "$NUM_FEWSHOT" \
        "${limit_arg[@]}" \
        --output "$output"

    log_info "Done: ${output}"
}

# ---------- Main ----------
usage() {
    cat <<EOF
Usage: $0 [task] [options]

Tasks: mmlu, gsm8k, humaneval, truthfulqa

Options:
    --model MODEL          Model name (default: Qwen/Qwen2.5-0.5B-Instruct)
    --backend-url URL       Inference backend URL (default: http://localhost:8000/v1)
    --num-fewshot N        Few-shot count (default: 5)
    --limit N              Limit samples (default: full)
    --check                Only check backend, don't run

Examples:
    $0 mmlu
    $0 gsm8k --limit 100 --num-fewshot 0
    $0 --check
EOF
}

case "${1:-}" in
    --check) check_backend ;;
    mmlu|gsm8k|humaneval|truthfulqa)
        check_backend
        run_benchmark "${1}"
        ;;
    --help|-h) usage ;;
    *)
        if [[ -n "${1:-}" ]]; then
            log_error "Unknown task: $1"
        fi
        usage
        exit 1
        ;;
esac
```

## 常用 lm-eval 直接命令（绕过 CLI 封装）

```bash
# 直接用 lm-eval 运行 MMLU
lm_eval \
    --model vllm \
    --model_args "base_url=http://localhost:8000/v1,pretrained=Qwen/Qwen2.5-0.5B-Instruct" \
    --tasks mmlu \
    --num_fewshot 5 \
    --limit 10

# GSM8K
lm_eval \
    --model vllm \
    --model_args "base_url=http://localhost:8000/v1,pretrained=Qwen/Qwen2.5-0.5B-Instruct" \
    --tasks gsm8k \
    --num_fewshot 5
```

---

Sources:
1. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval
2. https://github.com/EleutherAI/lm-evaluation-harness/tree/main/lm_eval/tasks — lm-eval tasks

Risk of Staleness:
- lm-eval CLI 参数在 0.4.x 中相对稳定
