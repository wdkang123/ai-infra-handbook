from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from eval_module.results.result_store import ResultStore
from eval_module.runners.factory import create_runner

app = typer.Typer(name="eval-module", add_completion=False)
console = Console()


@app.command()
def run(
    task: str = typer.Option(..., "--task"),
    model: str = typer.Option(..., "--model"),
    backend_url: str = typer.Option("http://localhost:8000/v1", "--backend-url"),
    num_fewshot: int = typer.Option(5, "--num-fewshot"),
    limit: int | None = typer.Option(None, "--limit"),
    output: str = typer.Option("./results/eval_result.json", "--output"),
) -> None:
    backend_config = {"type": "vllm", "base_url": backend_url}
    try:
        runner = create_runner(backend_config)
        result = runner.run(task=task, model=model, num_fewshot=num_fewshot, limit=limit)
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from exc
    store = ResultStore(Path(output).parent)
    json_target = store.save(result, output)
    bundle = store.save_run_bundle(result, output)
    console.print(f"[bold blue]Running {task} on {model}[/bold blue]")
    console.print(f"  Backend: {backend_url}")
    console.print(f"  Few-shot: {num_fewshot}")
    if limit is not None:
        console.print(f"  Limit: {limit}")
    console.print(f"  Result: {json_target}")
    console.print(f"  Bundle: {bundle['artifact_dir']}")
    console.print(f"  Accuracy: {result.accuracy:.4f}")


@app.command()
def compare(
    baseline: str = typer.Option(..., "--baseline"),
    candidate: str = typer.Option(..., "--candidate"),
    min_delta: float = typer.Option(0.0, "--min-delta", min=0.0),
    output: str | None = typer.Option(None, "--output"),
) -> None:
    store = ResultStore(Path(output).parent if output else Path(candidate).parent)
    baseline_result = store.load(baseline)
    candidate_result = store.load(candidate)
    try:
        diff = store.build_comparison(baseline_result, candidate_result, min_delta=min_delta)
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from exc
    if output:
        json_target = store.save_comparison(diff, output)
        md_target = store.save_comparison_markdown(diff, Path(output).with_suffix(".md"))
        bundle = store.save_comparison_bundle(diff, output)
    console.print("[bold blue]Comparing evaluation results[/bold blue]")
    console.print(f"  Baseline:  {baseline}")
    console.print(f"  Candidate: {candidate}")
    if output:
        console.print(f"  JSON:      {json_target}")
        console.print(f"  Markdown:  {md_target}")
        console.print(f"  Bundle:    {bundle['artifact_dir']}")
    console.print(f"  Delta:     {diff['summary']['delta']:.4f}")
    console.print(f"  Min delta: {diff['summary']['min_delta']:.4f}")
    console.print(f"  Verdict:   {diff['summary']['verdict']}")
    console.print(f"  Release:   {diff['summary']['release_recommendation']}")


@app.command()
def leaderboard(
    results_dir: str = typer.Option("./results", "--results-dir"),
    history: str | None = typer.Option(None, "--history"),
    task: str | None = typer.Option(None, "--task"),
    backend: str | None = typer.Option(None, "--backend"),
    num_fewshot: int | None = typer.Option(None, "--num-fewshot", min=0),
    limit: int | None = typer.Option(None, "--limit", min=1),
    output: str = typer.Option("./results/leaderboard.json", "--output"),
) -> None:
    store = ResultStore(results_dir)
    report = store.build_leaderboard(
        history_path=history,
        task=task,
        backend=backend,
        num_fewshot=num_fewshot,
        limit=limit,
    )
    json_target = store.save_leaderboard(report, output)
    markdown_target = store.save_leaderboard_markdown(report, Path(output).with_suffix(".md"))
    console.print("[bold blue]Building evaluation leaderboard[/bold blue]")
    console.print(f"  History: {report['source_history']}")
    if task:
        console.print(f"  Task:    {task}")
    if backend:
        console.print(f"  Backend: {backend}")
    if num_fewshot is not None:
        console.print(f"  Few-shot: {num_fewshot}")
    console.print(f"  Runs:    {report['run_count']}")
    console.print(f"  Models:  {report['model_count']}")
    console.print(f"  JSON:    {json_target}")
    console.print(f"  Markdown: {markdown_target}")


@app.command("list-runs")
def list_runs(
    results_dir: str = typer.Option("./results", "--results-dir"),
    history: str | None = typer.Option(None, "--history"),
    task: str | None = typer.Option(None, "--task"),
    model: str | None = typer.Option(None, "--model"),
    backend: str | None = typer.Option(None, "--backend"),
    num_fewshot: int | None = typer.Option(None, "--num-fewshot", min=0),
    limit: int | None = typer.Option(None, "--limit", min=1),
    output: str = typer.Option("./results/run_index.json", "--output"),
) -> None:
    store = ResultStore(results_dir)
    report = store.build_run_index(
        history_path=history,
        task=task,
        model=model,
        backend=backend,
        num_fewshot=num_fewshot,
        limit=limit,
    )
    json_target = store.save_run_index(report, output)
    markdown_target = store.save_run_index_markdown(report, Path(output).with_suffix(".md"))
    console.print("[bold blue]Listing evaluation runs[/bold blue]")
    console.print(f"  History: {report['source_history']}")
    if task:
        console.print(f"  Task:    {task}")
    if model:
        console.print(f"  Model:   {model}")
    if backend:
        console.print(f"  Backend: {backend}")
    if num_fewshot is not None:
        console.print(f"  Few-shot: {num_fewshot}")
    console.print(f"  Runs:    {report['run_count']}")
    console.print(f"  JSON:    {json_target}")
    console.print(f"  Markdown: {markdown_target}")


@app.command("list-comparisons")
def list_comparisons(
    results_dir: str = typer.Option("./results", "--results-dir"),
    history: str | None = typer.Option(None, "--history"),
    task: str | None = typer.Option(None, "--task"),
    verdict: str | None = typer.Option(None, "--verdict"),
    recommendation: str | None = typer.Option(None, "--recommendation"),
    limit: int | None = typer.Option(None, "--limit", min=1),
    output: str = typer.Option("./results/comparison_index.json", "--output"),
) -> None:
    store = ResultStore(results_dir)
    report = store.build_comparison_index(
        history_path=history,
        task=task,
        verdict=verdict,
        recommendation=recommendation,
        limit=limit,
    )
    json_target = store.save_comparison_index(report, output)
    markdown_target = store.save_comparison_index_markdown(report, Path(output).with_suffix(".md"))
    console.print("[bold blue]Listing evaluation comparisons[/bold blue]")
    console.print(f"  History: {report['source_history']}")
    if task:
        console.print(f"  Task:    {task}")
    if verdict:
        console.print(f"  Verdict: {verdict}")
    if recommendation:
        console.print(f"  Release: {recommendation}")
    console.print(f"  Comparisons: {report['comparison_count']}")
    console.print(f"  JSON:    {json_target}")
    console.print(f"  Markdown: {markdown_target}")


@app.command("list-tasks")
def list_tasks() -> None:
    for task in create_runner({"type": "vllm", "base_url": "http://localhost:8000/v1"}).list_tasks():
        console.print(task)


if __name__ == "__main__":
    app()
