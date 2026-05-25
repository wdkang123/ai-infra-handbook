#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON:-$ROOT_DIR/.venv/bin/python}"
MODEL="${MODEL:-Qwen/Qwen2.5-0.5B-Instruct}"
INFERENCE_PORT="${INFERENCE_PORT:-8000}"
GATEWAY_PORT="${GATEWAY_PORT:-8080}"

if [[ "$PYTHON_BIN" == */* && "$PYTHON_BIN" != /* ]]; then
  PYTHON_BIN="$ROOT_DIR/$PYTHON_BIN"
fi

start_inference_service() {
  (cd "$ROOT_DIR" && make inference-serve PYTHON="$PYTHON_BIN" MODEL="$MODEL" INFERENCE_PORT="$INFERENCE_PORT")
}

start_ai_gateway() {
  (cd "$ROOT_DIR" && make gateway-serve PYTHON="$PYTHON_BIN" GATEWAY_PORT="$GATEWAY_PORT")
}

wait_for_url() {
  local url="$1"
  local retries=30
  while [ "$retries" -gt 0 ]; do
    if curl -fsS "$url" >/dev/null 2>&1; then
      return 0
    fi
    retries=$((retries - 1))
    sleep 1
  done
  echo "Timed out waiting for $url" >&2
  return 1
}

stop_all() {
  pkill -f "inference_service.main" 2>/dev/null || true
  pkill -f "ai_gateway.main" 2>/dev/null || true
}

case "${1:-}" in
  start)
    stop_all
    start_inference_service
    wait_for_url "http://localhost:${INFERENCE_PORT}/health"
    start_ai_gateway
    wait_for_url "http://localhost:${GATEWAY_PORT}/health"
    ;;
  stop)
    stop_all
    ;;
  restart)
    stop_all
    start_inference_service
    wait_for_url "http://localhost:${INFERENCE_PORT}/health"
    start_ai_gateway
    wait_for_url "http://localhost:${GATEWAY_PORT}/health"
    ;;
  *)
    echo "Usage: $0 {start|stop|restart}" >&2
    exit 1
    ;;
esac
