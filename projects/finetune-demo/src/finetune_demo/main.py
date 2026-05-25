from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from finetune_demo.config import load_config_from_cli
from finetune_demo.dataset_registry import (
    build_dataset_registry_diff,
    build_dataset_registry_report,
    render_dataset_registry_diff_markdown,
    render_dataset_registry_markdown,
    save_dataset_registry_diff,
    save_dataset_registry_diff_markdown,
    save_dataset_registry_markdown,
    save_dataset_registry_report,
)
from finetune_demo.export.adapter_exporter import (
    build_export_history_report,
    export_adapter,
    render_export_history_markdown,
    save_export_history_markdown,
    save_export_history_report,
)
from finetune_demo.run_history import (
    build_run_history_report,
    render_run_history_markdown,
    save_run_history_markdown,
    save_run_history_report,
)
from finetune_demo.trainer.lora_trainer import LoRATrainer

app = typer.Typer(name="finetune-demo", add_completion=False)
console = Console()


@app.command()
def train(
    method: str | None = typer.Option(None, "--method"),
    model: str | None = typer.Option(None, "--model"),
    dataset: str | None = typer.Option(None, "--dataset"),
    output: str | None = typer.Option(None, "--output"),
    epochs: int | None = typer.Option(None, "--epochs"),
    per_device_batch_size: int | None = typer.Option(None, "--per-device-batch-size"),
    learning_rate: float | None = typer.Option(None, "--learning-rate"),
    lora_r: int | None = typer.Option(None, "--lora-r"),
    lora_alpha: int | None = typer.Option(None, "--lora-alpha"),
    load_in_4bit: bool | None = typer.Option(None, "--load-in-4bit/--no-load-in-4bit"),
    config: str | None = typer.Option(None, "--config"),
) -> None:
    try:
        cfg = load_config_from_cli(
            method=method,
            model=model,
            dataset=dataset,
            output=output,
            epochs=epochs,
            per_device_batch_size=per_device_batch_size,
            learning_rate=learning_rate,
            lora_r=lora_r,
            lora_alpha=lora_alpha,
            load_in_4bit=load_in_4bit,
            config=config,
        )
        trainer = LoRATrainer(config=cfg)
        trainer.train()
    except (FileNotFoundError, ValueError) as exc:
        raise typer.BadParameter(str(exc)) from exc
    output_dir = Path(cfg.output_dir)
    console.print(f"[bold blue]Starting {cfg.method.upper()} training[/bold blue]")
    console.print(f"  Model:   {cfg.model.name_or_path}")
    console.print(f"  Dataset: {cfg.data.train_file}")
    console.print(f"  Output:  {cfg.output_dir}")
    console.print(f"  Epochs:  {cfg.num_train_epochs}")
    console.print(f"  Batch:   {cfg.per_device_train_batch_size}")
    console.print(f"  LR:      {cfg.learning_rate}")
    console.print(f"  LoRA r:  {cfg.lora.r}")
    console.print(f"  Alpha:   {cfg.lora.lora_alpha}")
    console.print(f"  4-bit:   {cfg.qlora.load_in_4bit}")
    if config:
        console.print(f"  Config:  {config}")
    console.print(f"  State:   {output_dir / 'trainer_state.json'}")
    console.print(f"  Manifest: {output_dir / 'run_manifest.json'}")
    console.print(f"  Checkpoint: {output_dir / 'checkpoint-0001'}")


@app.command()
def save(
    checkpoint: str = typer.Option(..., "--checkpoint"),
    output: str = typer.Option(..., "--output"),
) -> None:
    try:
        exported = export_adapter(checkpoint, output)
    except (FileNotFoundError, NotADirectoryError) as exc:
        raise typer.BadParameter(str(exc)) from exc
    console.print("[bold blue]Saving adapter[/bold blue]")
    console.print(f"  Checkpoint: {checkpoint}")
    console.print(f"  Output:     {output}")
    console.print(f"  Exported:   {exported}")
    console.print(f"  Manifest:   {Path(output) / 'export_manifest.json'}")


@app.command("list-datasets")
def list_datasets(
    registry: str = typer.Option("./outputs/dataset_registry.jsonl", "--registry"),
    dataset_id: str | None = typer.Option(None, "--dataset-id"),
    method: str | None = typer.Option(None, "--method"),
    model: str | None = typer.Option(None, "--model"),
    output: str | None = typer.Option(None, "--output"),
    markdown_output: str | None = typer.Option(None, "--markdown-output"),
) -> None:
    report = build_dataset_registry_report(registry, dataset_id=dataset_id, method=method, model=model)
    console.print("[bold blue]Listing registered datasets[/bold blue]")
    console.print(f"  Registry: {report['registry_file']}")
    console.print(f"  Entries:  {report['entry_count']}")
    console.print(f"  Datasets: {report['dataset_count']}")
    if dataset_id:
        console.print(f"  Filter:   {dataset_id}")
    if method:
        console.print(f"  Method:   {method}")
    if model:
        console.print(f"  Model:    {model}")
    console.print(f"  Duplicates: {report['duplicate_entry_count']}")
    for dataset in report["datasets"]:
        console.print(
            "  - "
            f"{dataset['dataset_id']} "
            f"records={dataset['records']} "
            f"runs={dataset['registered_count']} "
            f"models={','.join(dataset['models'])}"
        )
    if output:
        json_target = save_dataset_registry_report(report, output)
        console.print(f"  JSON:     {json_target}")
    if markdown_output:
        markdown_target = save_dataset_registry_markdown(report, markdown_output)
        console.print(f"  Markdown: {markdown_target}")
    if not output and not markdown_output:
        console.print(render_dataset_registry_markdown(report))


@app.command("diff-datasets")
def diff_datasets(
    registry: str = typer.Option("./outputs/dataset_registry.jsonl", "--registry"),
    left: str = typer.Option(..., "--left"),
    right: str = typer.Option(..., "--right"),
    output: str | None = typer.Option(None, "--output"),
    markdown_output: str | None = typer.Option(None, "--markdown-output"),
) -> None:
    try:
        report = build_dataset_registry_diff(registry, left_dataset_id=left, right_dataset_id=right)
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from exc
    console.print("[bold blue]Diffing registered datasets[/bold blue]")
    console.print(f"  Registry: {report['registry_file']}")
    console.print(f"  Left:     {left}")
    console.print(f"  Right:    {right}")
    console.print(f"  Same sha: {str(report['identical_dataset_sha256']).lower()}")
    console.print(f"  Changes:  {len(report['changed_fields'])}")
    if output:
        json_target = save_dataset_registry_diff(report, output)
        console.print(f"  JSON:     {json_target}")
    if markdown_output:
        markdown_target = save_dataset_registry_diff_markdown(report, markdown_output)
        console.print(f"  Markdown: {markdown_target}")
    if not output and not markdown_output:
        console.print(render_dataset_registry_diff_markdown(report))


@app.command("list-exports")
def list_exports(
    history: str = typer.Option("./outputs/export_history.jsonl", "--history"),
    dataset_id: str | None = typer.Option(None, "--dataset-id"),
    model: str | None = typer.Option(None, "--model"),
    limit: int | None = typer.Option(None, "--limit", min=1),
    output: str | None = typer.Option(None, "--output"),
    markdown_output: str | None = typer.Option(None, "--markdown-output"),
) -> None:
    report = build_export_history_report(history, dataset_id=dataset_id, model=model, limit=limit)
    console.print("[bold blue]Listing exports[/bold blue]")
    console.print(f"  History: {report['source_history']}")
    if dataset_id:
        console.print(f"  Dataset: {dataset_id}")
    if model:
        console.print(f"  Model:   {model}")
    console.print(f"  Exports: {report['export_count']}")
    console.print(f"  Models:  {report['model_count']}")
    if output:
        json_target = save_export_history_report(report, output)
        console.print(f"  JSON:     {json_target}")
    if markdown_output:
        markdown_target = save_export_history_markdown(report, markdown_output)
        console.print(f"  Markdown: {markdown_target}")
    if not output and not markdown_output:
        console.print(render_export_history_markdown(report))


@app.command("list-runs")
def list_runs(
    history: str = typer.Option("./outputs/run_history.jsonl", "--history"),
    dataset_id: str | None = typer.Option(None, "--dataset-id"),
    model: str | None = typer.Option(None, "--model"),
    method: str | None = typer.Option(None, "--method"),
    limit: int | None = typer.Option(None, "--limit", min=1),
    output: str | None = typer.Option(None, "--output"),
    markdown_output: str | None = typer.Option(None, "--markdown-output"),
) -> None:
    report = build_run_history_report(
        history,
        dataset_id=dataset_id,
        model=model,
        method=method,
        limit=limit,
    )
    console.print("[bold blue]Listing finetune runs[/bold blue]")
    console.print(f"  History: {report['source_history']}")
    if dataset_id:
        console.print(f"  Dataset: {dataset_id}")
    if model:
        console.print(f"  Model:   {model}")
    if method:
        console.print(f"  Method:  {method}")
    console.print(f"  Runs:    {report['run_count']}")
    console.print(f"  Models:  {report['model_count']}")
    if output:
        json_target = save_run_history_report(report, output)
        console.print(f"  JSON:     {json_target}")
    if markdown_output:
        markdown_target = save_run_history_markdown(report, markdown_output)
        console.print(f"  Markdown: {markdown_target}")
    if not output and not markdown_output:
        console.print(render_run_history_markdown(report))


@app.command()
def export(
    checkpoint: str = typer.Option(..., "--checkpoint"),
    output: str = typer.Option(..., "--output"),
) -> None:
    try:
        exported = export_adapter(checkpoint, output)
    except (FileNotFoundError, NotADirectoryError) as exc:
        raise typer.BadParameter(str(exc)) from exc
    console.print("[bold blue]Exporting adapter[/bold blue]")
    console.print(f"  Checkpoint: {checkpoint}")
    console.print(f"  Output:     {output}")
    console.print(f"  Exported:   {exported}")
    console.print(f"  Manifest:   {Path(output) / 'export_manifest.json'}")


if __name__ == "__main__":
    app()
