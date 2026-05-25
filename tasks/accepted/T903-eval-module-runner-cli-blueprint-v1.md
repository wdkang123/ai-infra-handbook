# eval-module Runner CLI Blueprint v1

## Task ID: T903
## Title: eval-module Scaffold Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T803 API contract 和 T803 validation checklist（已收紧为 T813），产出 CLI 脚本模板。

---

# eval-module Runner CLI Blueprint v1

## 概述

本文档定义 eval-module 的 CLI 入口和 benchmark runner 脚本模板。

## `eval-module` CLI 入口模板

```python
# src/eval_module/main.py
"""
eval-module CLI entry point.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from eval_module import Evaluator, ResultStore, Comparator

app = typer.Typer(
    name="eval-module",
    help="Benchmark evaluation module powered by lm-eval-harness",
    add_completion=False,
)
console = Console()


@app.command()
def run(
    task: str = typer.Option(..., "--task", help="Benchmark task (mmlu, gsm8k, ...)"),
    model: str = typer.Option(..., "--model", help="Model name or path"),
    backend_url: str = typer.Option(
        "http://localhost:8000/v1",
        "--backend-url",
        help="Inference backend URL",
    ),
    num_fewshot: int = typer.Option(5, "--num-fewshot", help="Number of few-shot examples"),
    limit: Optional[int] = typer.Option(None, "--limit", help="Limit number of samples"),
    output: str = typer.Option(
        "./results/eval_result.json",
        "--output",
        help="Output file path",
    ),
) -> None:
    """Run a benchmark evaluation."""
    console.print(f"[bold blue]Running {task} on {model}[/bold blue]")
    console.print(f"  Backend: {backend_url}")
    console.print(f"  Few-shot: {num_fewshot}")

    evaluator = Evaluator(
        backend="lm-eval",
        backend_config={"type": "vllm", "base_url": backend_url},
    )

    result = evaluator.evaluate(
        task=task,
        model=model,
        num_fewshot=num_fewshot,
        limit=limit,
    )

    # Save result
    store = ResultStore(output_dir=Path(output).parent)
    store.save(result, Path(output))

    console.print(f"[bold green]Results saved to {output}[/bold green]")
    console.print(f"  Task: {result.task}")
    console.print(f"  Accuracy: {result.accuracy:.4f}")


@app.command()
def compare(
    baseline: str = typer.Option(..., "--baseline", help="Baseline result JSON file"),
    candidate: str = typer.Option(..., "--candidate", help="Candidate result JSON file"),
    output: Optional[str] = typer.Option(None, "--output", help="Output file"),
) -> None:
    """Compare two evaluation results."""
    store = ResultStore()

    baseline_result = store.load(Path(baseline))
    candidate_result = store.load(Path(candidate))

    comparator = Comparator()
    diff = comparator.compare(baseline_result, candidate_result)

    # Display table
    table = Table(title="Evaluation Comparison")
    table.add_column("Metric", style="cyan")
    table.add_column("Baseline", style="yellow")
    table.add_column("Candidate", style="green")
    table.add_column("Delta", style="magenta")

    for key, val in diff.items():
        delta = val.get("delta", "—")
        table.add_row(key, str(val.get("baseline", "—")), str(val.get("candidate", "—")), str(delta))

    console.print(table)

    if output:
        store.save_comparison(diff, Path(output))


@app.command()
def list_tasks() -> None:
    """List available benchmark tasks."""
    evaluator = Evaluator(backend="lm-eval")
    tasks = evaluator.list_tasks()

    table = Table(title="Available Tasks")
    table.add_column("Task", style="cyan")
    table.add_column("Description")

    task_descriptions = {
        "mmlu": "Massively Multitask Language Understanding",
        "gsm8k": "Grade School Math 8K",
        "humaneval": "HumanEval Code Completion",
        "truthfulqa": "TruthfulQA",
    }

    for task_name in tasks:
        desc = task_descriptions.get(task_name, "—")
        table.add_row(task_name, desc)

    console.print(table)


if __name__ == "__main__":
    app()
```

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

## 常用 lm-eval 直接命令（不通过 CLI 封装）

```bash
# 直接用 lm-eval 运行 MMLU（绕过 eval-module CLI）
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

Out of Scope Kept:
- 未写自动化报告生成脚本
- 未写定时评测 cron 脚本
