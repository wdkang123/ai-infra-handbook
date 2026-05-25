#!/usr/bin/env bash
set -euo pipefail

export PYTHONPATH="${PYTHONPATH:-src}"
PYTHON_BIN="${PYTHON:-python3}"
"${PYTHON_BIN}" -m finetune_demo.main train \
  --method "${METHOD:-lora}" \
  --model "${MODEL:-Qwen/Qwen2.5-0.5B-Instruct}" \
  --dataset "${DATASET:-./data/train.jsonl}" \
  --output "${OUTPUT:-./outputs}"
