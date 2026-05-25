#!/usr/bin/env bash
set -euo pipefail

export PYTHONPATH="${PYTHONPATH:-src}"
PYTHON_BIN="${PYTHON:-python3}"
"${PYTHON_BIN}" -m ai_gateway.main serve \
  --port "${PORT:-8080}" \
  --host "${HOST:-0.0.0.0}"
