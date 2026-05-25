#!/usr/bin/env bash
set -euo pipefail

export PYTHONPATH="${PYTHONPATH:-src}"
PYTHON_BIN="${PYTHON:-python3}"
"${PYTHON_BIN}" -m inference_service.main serve \
  --engine "${ENGINE:-mock}" \
  --model "${MODEL:-Qwen/Qwen2.5-0.5B-Instruct}" \
  --port "${PORT:-8000}" \
  --host "${HOST:-0.0.0.0}"
