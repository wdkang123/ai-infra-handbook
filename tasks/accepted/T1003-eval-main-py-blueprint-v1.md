# eval-module main.py Blueprint v1

## Task ID: T1003
## Title: eval-module Starter File Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T903 scaffold（runner-cli blueprint），产出 `main.py` Typer CLI 蓝图。

---

# eval-module main.py Blueprint v1

## 概述

本文档定义 `src/eval_module/main.py` 的蓝图——Typer CLI 入口，包含 run / compare / list-tasks 三个子命令。

## `src/eval_module/main.py` 模板

```python
# src/eval_module/main.py
"""
eval-module CLI entry point.

用法:
    eval-module run --task mmlu --model Qwen/Qwen2.5-0.5B-Instruct
    eval-module compare --baseline results/baseline.json --candidate results/candidate.json
    eval-module list-tasks
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(
    name="eval-module",
    help="Benchmark evaluation module powered by lm-eval-harness",
    add_completion=False,
)
console = Console()


@app.command()
def run(
    task: str = typer.Option(
        ...,
        "--task",
        help="Benchmark task (mmlu, gsm8k, humaneval, truthfulqa, ...)",
    ),
    model: str = typer.Option(
        ...,
        "--model",
        help="Model name or HuggingFace path",
    ),
    backend_url: str = typer.Option(
        "http://localhost:8000/v1",
        "--backend-url",
        help="Inference backend URL",
    ),
    num_fewshot: int = typer.Option(
        5,
        "--num-fewshot",
        help="Number of few-shot examples",
    ),
    limit: Optional[int] = typer.Option(
        None,
        "--limit",
        help="Limit number of samples (for quick testing)",
    ),
    output: str = typer.Option(
        "./results/eval_result.json",
        "--output",
        help="Output JSON file path",
    ),
) -> None:
    """
    Run a benchmark evaluation.

    Example:
        eval-module run --task mmlu --model Qwen/Qwen2.5-0.5B-Instruct \\
            --backend-url http://localhost:8000/v1
    """
    console.print(f"[bold blue]Running {task} on {model}[/bold blue]")
    console.print(f"  Backend: {backend_url}")
    console.print(f"  Few-shot: {num_fewshot}")
    if limit:
        console.print(f"  Limit: {limit} samples")

    # [PLACEHOLDER] 真实实现：
    # from eval_module.evaluator import Evaluator
    # from eval_module.results.result_store import ResultStore
    #
    # evaluator = Evaluator(
    #     backend="lm-eval",
    #     backend_config={"type": "vllm", "base_url": backend_url},
    # )
    # result = evaluator.evaluate(
    #     task=task,
    #     model=model,
    #     num_fewshot=num_fewshot,
    #     limit=limit,
    # )
    #
    # store = ResultStore(output_dir=Path(output).parent)
    # store.save(result, Path(output))
    #
    # console.print(f"[bold green]Results saved to {output}[/bold green]")
    # console.print(f"  Accuracy: {result['accuracy']:.4f}")


@app.command()
def compare(
    baseline: str = typer.Option(
        ...,
        "--baseline",
        help="Baseline result JSON file",
    ),
    candidate: str = typer.Option(
        ...,
        "--candidate",
        help="Candidate result JSON file",
    ),
    output: Optional[str] = typer.Option(
        None,
        "--output",
        help="Output file for comparison report",
    ),
) -> None:
    """
    Compare two evaluation results.

    Example:
        eval-module compare \\
            --baseline ./results/baseline.json \\
            --candidate ./results/candidate.json
    """
    console.print(f"[bold blue]Comparing evaluations[/bold blue]")

    # [PLACEHOLDER] 真实实现：
    # from eval_module.results.result_store import ResultStore
    # from eval_module.results.comparator import Comparator
    #
    # store = ResultStore()
    # baseline_result = store.load(Path(baseline))
    # candidate_result = store.load(Path(candidate))
    #
    # comparator = Comparator()
    # diff = comparator.compare(baseline_result, candidate_result)
    #
    # table = Table(title="Evaluation Comparison")
    # table.add_column("Metric", style="cyan")
    # table.add_column("Baseline", style="yellow")
    # table.add_column("Candidate", style="green")
    # table.add_column("Delta", style="magenta")
    # for key, val in diff.items():
    #     delta = val.get("delta", "—")
    #     table.add_row(
    #         key,
    #         str(val.get("baseline", "—")),
    #         str(val.get("candidate", "—")),
    #         str(delta),
    #     )
    # console.print(table)
    # if output:
    #     store.save_comparison(diff, Path(output))


@app.command()
def list_tasks() -> None:
    """List available benchmark tasks."""
    console.print("[bold blue]Available benchmark tasks[/bold blue]")

    # [PLACEHOLDER] 真实实现：
    # from eval_module.runners.lm_eval_runner import LmEvalRunner
    # runner = LmEvalRunner({"type": "vllm", "base_url": "http://localhost:8000/v1"})
    # tasks = runner.list_tasks()
    #
    # task_descriptions = {
    #     "mmlu": "Massively Multitask Language Understanding",
    #     "gsm8k": "Grade School Math 8K",
    #     "humaneval": "HumanEval Code Completion",
    #     "truthfulqa": "TruthfulQA",
    # }
    # table = Table(title="Available Tasks")
    # table.add_column("Task", style="cyan")
    # table.add_column("Description")
    # for task_name in tasks:
    #     desc = task_descriptions.get(task_name, "—")
    #     table.add_row(task_name, desc)
    # console.print(table)


if __name__ == "__main__":
    app()
```

## CLI 参数详解

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--task` | 必填 | 任务名：mmlu, gsm8k, humaneval, truthfulqa |
| `--model` | 必填 | HuggingFace 模型名或路径 |
| `--backend-url` | `http://localhost:8000/v1` | 推理后端 |
| `--num-fewshot` | `5` | few-shot 样本数 |
| `--limit` | `None` | 限制样本数（快速测试） |
| `--output` | `./results/eval_result.json` | 输出文件 |

---

Sources:
1. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval
2. https://typer.tiangolo.com/ — Typer

Risk of Staleness:
- lm-eval CLI 参数在 0.4.x 相对稳定
