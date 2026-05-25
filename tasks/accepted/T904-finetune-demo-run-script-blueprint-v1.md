# finetune-demo Run Script Blueprint v1

## Task ID: T904
## Title: finetune-demo Scaffold Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T804 repo layout 和 validation checklist，产出训练脚本模板。

---

# finetune-demo Run Script Blueprint v1

## 概述

本文档定义 finetune-demo 的训练启动脚本模板 `scripts/train.sh`。

## `scripts/train.sh` 模板

```bash
#!/usr/bin/env bash
# ============================================================
# finetune-demo — scripts/train.sh
# 训练启动脚本
# ============================================================

set -euo pipefail

# ---------- Defaults ----------
METHOD="${FINETUNE_METHOD:-lora}"
MODEL="${FINETUNE_MODEL_NAME:-Qwen/Qwen2.5-0.5B-Instruct}"
DATASET="${FINETUNE_DATASET_PATH:-./data/example_dataset.jsonl}"
OUTPUT_DIR="${FINETUNE_OUTPUT_DIR:-./models}"
EPOCHS="${FINETUNE_NUM_EPOCHS:-3}"
BATCH_SIZE="${FINETUNE_PER_DEVICE_BATCH_SIZE:-4}"
LR="${FINETUNE_LEARNING_RATE:-2e-4}"
GRAD_ACCUM="${FINETUNE_GRADIENT_ACCUMULATION_STEPS:-4}"
WARMUP="${FINETUNE_WARMUP_STEPS:-100}"
LOGGING_STEPS="${FINETUNE_LOGGING_STEPS:-10}"
SAVE_STEPS="${FINETUNE_SAVE_STEPS:-500}"
MAX_SEQ_LEN="${FINETUNE_MAX_SEQ_LENGTH:-512}"

# LoRA params
LORA_R="${FINETUNE_LORA_R:-16}"
LORA_ALPHA="${FINETUNE_LORA_ALPHA:-32}"
LORA_DROPOUT="${FINETUNE_LORA_DROPOUT:-0.05}"
LORA_TARGET="${FINETUNE_LORA_TARGET_MODULES:-q_proj,v_proj}"

# QLoRA params
LOAD_IN_4BIT="${FINETUNE_QLORA_LOAD_IN_4BIT:-false}"

# ---------- Color ----------
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info()  { echo -e "${GREEN}[INFO]${NC}  $*"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC}  $*"; }
log_error() { echo -e "${RED}[ERROR]${NC} $*" >&2; }

# ---------- GPU check ----------
check_gpu() {
    if command -v nvidia-smi &>/dev/null; then
        local gpu_count
        gpu_count=$(nvidia-smi --query-gpu=gpu_name --format=csv,noheader 2>/dev/null | wc -l)
        log_info "Detected $gpu_count GPU(s)"
        if [[ "$gpu_count" -eq 0 ]]; then
            log_error "No GPU detected — training requires CUDA GPU"
            exit 1
        fi
        nvidia-smi --query-gpu=name,memory.total,memory.free --format=csv
    else
        log_error "nvidia-smi not found — training requires NVIDIA GPU with CUDA"
        exit 1
    fi
}

# ---------- Dataset check ----------
check_dataset() {
    if [[ ! -f "$DATASET" ]]; then
        log_error "Dataset not found: $DATASET"
        log_error "Please set FINETUNE_DATASET_PATH or use --dataset"
        exit 1
    fi
    local lines
    lines=$(wc -l < "$DATASET")
    log_info "Dataset: $DATASET ($lines samples)"
}

# ---------- Build training command ----------
build_cmd() {
    local cmd=(finetune-demo train)
    cmd+=(--method "$METHOD")
    cmd+=(--model "$MODEL")
    cmd+=(--dataset "$DATASET")
    cmd+=(--output "$OUTPUT_DIR")
    cmd+=(--epochs "$EPOCHS")
    cmd+=(--per-device-batch-size "$BATCH_SIZE")
    cmd+=(--learning-rate "$LR")
    cmd+=(--gradient-accumulation-steps "$GRAD_ACCUM")
    cmd+=(--warmup-steps "$WARMUP")
    cmd+=(--logging-steps "$LOGGING_STEPS")
    cmd+=(--save-steps "$SAVE_STEPS")
    cmd+=(--max-seq-length "$MAX_SEQ_LEN")
    cmd+=(--lora-r "$LORA_R")
    cmd+=(--lora-alpha "$LORA_ALPHA")
    cmd+=(--lora-dropout "$LORA_DROPOUT")
    cmd+=(--lora-target-modules "$LORA_TARGET")

    if [[ "$METHOD" == "qlora" ]] || [[ "$LOAD_IN_4BIT" == "true" ]]; then
        cmd+=(--load-in-4bit)
    fi

    echo "${cmd[@]}"
}

# ---------- Run ----------
run_training() {
    log_info "Starting ${METHOD} training..."
    log_info "  Method:     ${METHOD}"
    log_info "  Model:     ${MODEL}"
    log_info "  Dataset:   ${DATASET}"
    log_info "  Output:    ${OUTPUT_DIR}"
    log_info "  Epochs:    ${EPOCHS}"
    log_info "  Batch:     ${BATCH_SIZE}"
    log_info "  LR:        ${LR}"

    local timestamp
    timestamp=$(date +%Y%m%d_%H%M%S)
    local run_dir="${OUTPUT_DIR}/${METHOD}_${timestamp}"
    mkdir -p "$run_dir"

    local cmd
    cmd=$(build_cmd)
    # Append output dir override
    cmd="${cmd/--output \"$OUTPUT_DIR\"/--output \"$run_dir\"}"

    log_info "Full command:"
    echo "  ${cmd}"
    echo ""

    if [[ "${FINETUNE_DRY_RUN:-false}" == "true" ]]; then
        log_info "Dry-run — command not executed"
        exit 0
    fi

    eval "$cmd"
}

# ---------- Main ----------
usage() {
    cat <<EOF
Usage: $0 [OPTIONS]

Start LoRA or QLoRA training.

OPTIONS:
    --method METHOD         Training method: lora | qlora (default: lora)
    --model MODEL           HuggingFace model name (default: Qwen/Qwen2.5-0.5B-Instruct)
    --dataset PATH          Dataset JSONL path (required)
    --output DIR            Output directory (default: ./models)
    --epochs N              Number of epochs (default: 3)
    --dry-run               Print command without executing
    --help                  Show this help

ENV VARS:
    FINETUNE_METHOD, FINETUNE_MODEL_NAME, FINETUNE_DATASET_PATH,
    FINETUNE_NUM_EPOCHS, FINETUNE_LORA_R, etc.

EXAMPLES:
    # LoRA training
    $0 --dataset ./data/train.jsonl --epochs 3

    # QLoRA training
    $0 --method qlora --dataset ./data/train.jsonl --epochs 3

    # Dry run
    FINETUNE_DRY_RUN=true $0 --dataset ./data/train.jsonl
EOF
}

FINETUNE_DRY_RUN="${FINETUNE_DRY_RUN:-false}"

while [[ $# -gt 0 ]]; do
    case $1 in
        --method) METHOD="$2"; shift 2 ;;
        --model) MODEL="$2"; shift 2 ;;
        --dataset) DATASET="$2"; shift 2 ;;
        --output) OUTPUT_DIR="$2"; shift 2 ;;
        --epochs) EPOCHS="$2"; shift 2 ;;
        --dry-run) FINETUNE_DRY_RUN=true; shift ;;
        --help) usage; exit 0 ;;
        *) log_error "Unknown: $1"; usage; exit 1 ;;
    esac
done

check_gpu
check_dataset
run_training

log_info "Training complete. Output: ${OUTPUT_DIR}"
```

## 训练快速参考

| 场景 | 命令 |
|------|------|
| LoRA 训练 | `scripts/train.sh --method lora --dataset ./data/train.jsonl` |
| QLoRA 训练 | `scripts/train.sh --method qlora --dataset ./data/train.jsonl` |
| 干跑（看命令） | `FINETUNE_DRY_RUN=true scripts/train.sh --dataset ./data/train.jsonl` |

## 显存需求参考

| 模型大小 | LoRA | QLoRA |
|---------|------|-------|
| 7B | ~16GB | ~5GB |
| 13B | ~28GB | ~10GB |
| 0.5B | ~4GB | ~2GB |

---

Sources:
1. https://github.com/huggingface/peft — PEFT
2. https://github.com/huggingface/trl — TRL

Risk of Staleness:
- PEFT/TRL CLI 参数尚未确定

Out of Scope Kept:
- 未写分布式训练脚本
- 未写多节点训练脚本
