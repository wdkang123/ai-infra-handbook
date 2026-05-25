#!/usr/bin/env bash
set -euo pipefail

export PYTHONPATH="${PYTHONPATH:-src}"
PYTHON_BIN="${PYTHON:-python3}"
"${PYTHON_BIN}" -m eval_module.main run \
  --task "${TASK:-mmlu}" \
  --model "${MODEL:-Qwen/Qwen2.5-0.5B-Instruct}" \
  --backend-url "${BACKEND_URL:-http://localhost:8000/v1}"
