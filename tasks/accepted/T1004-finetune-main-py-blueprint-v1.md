# finetune-demo main.py Blueprint v1

## Task ID: T1004
## Title: finetune-demo Starter File Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T904 scaffold（pyproject / run-script），产出 `main.py` Typer CLI 蓝图。

---

# finetune-demo main.py Blueprint v1

## 概述

本文档定义 `src/finetune_demo/main.py` 的蓝图——Typer CLI 入口。

## `src/finetune_demo/main.py` 模板

```python
# src/finetune_demo/main.py
"""
finetune-demo CLI entry point.

用法:
    finetune-demo train --method lora --model Qwen/Qwen2.5-0.5B-Instruct --dataset ./data/train.jsonl
    finetune-demo save --checkpoint ./models/lora/checkpoint-500 --output ./models/lora/adapter
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

app = typer.Typer(
    name="finetune-demo",
    help="Fine-tuning demo with LoRA/QLoRA using PEFT and TRL",
    add_completion=False,
)
console = Console()


@app.command()
def train(
    method: str = typer.Option(
        "lora",
        "--method",
        help="Training method: lora | qlora",
    ),
    model: str = typer.Option(
        "Qwen/Qwen2.5-0.5B-Instruct",
        "--model",
        help="HuggingFace model name or path",
    ),
    dataset: str = typer.Option(
        ...,
        "--dataset",
        help="Dataset JSONL file path",
    ),
    output: str = typer.Option(
        "./models",
        "--output",
        help="Output directory for checkpoints",
    ),
    epochs: int = typer.Option(3, "--epochs", help="Number of training epochs"),
    per_device_batch_size: int = typer.Option(
        4, "--per-device-batch-size", help="Batch size per device"
    ),
    learning_rate: float = typer.Option(
        2e-4, "--learning-rate", help="Learning rate"
    ),
    gradient_accumulation_steps: int = typer.Option(
        4, "--gradient-accumulation-steps", help="Gradient accumulation steps"
    ),
    warmup_steps: int = typer.Option(100, "--warmup-steps", help="Warmup steps"),
    logging_steps: int = typer.Option(10, "--logging-steps", help="Logging frequency"),
    save_steps: int = typer.Option(500, "--save-steps", help="Checkpoint save frequency"),
    max_seq_length: int = typer.Option(512, "--max-seq-length", help="Max sequence length"),
    lora_r: int = typer.Option(16, "--lora-r", help="LoRA rank"),
    lora_alpha: int = typer.Option(32, "--lora-alpha", help="LoRA alpha"),
    lora_dropout: float = typer.Option(0.05, "--lora-dropout", help="LoRA dropout"),
    lora_target_modules: str = typer.Option(
        "q_proj,v_proj", "--lora-target-modules", help="LoRA target modules (comma-separated)"
    ),
    load_in_4bit: bool = typer.Option(False, "--load-in-4bit", help="Use 4-bit quantization (QLoRA)"),
    config: Optional[str] typer.Option(None, "--config", help="YAML config file"),
) -> None:
    """
    Train a LoRA or QLoRA adapter.

    Example:
        finetune-demo train --method lora --model Qwen/Qwen2.5-0.5B-Instruct \\
            --dataset ./data/train.jsonl --epochs 3
    """
    console.print(f"[bold blue]Starting {method.upper()} training[/bold blue]")
    console.print(f"  Model:   {model}")
    console.print(f"  Dataset: {dataset}")
    console.print(f"  Output:  {output}")

    # [PLACEHOLDER] 真实实现：
    # from finetune_demo.config import FinetuneConfig
    # from finetune_demo.trainer.lora_trainer import LoRATrainer
    #
    # # Load from YAML config if provided
    # if config:
    #     cfg = FinetuneConfig.from_yaml(Path(config))
    # else:
    #     cfg = FinetuneConfig.from_cli(
    #         method=method, model=model, dataset=dataset, output=output,
    #         epochs=epochs, per_device_batch_size=per_device_batch_size,
    #         learning_rate=learning_rate,
    #         lora_r=lora_r, lora_alpha=lora_alpha,
    #         load_in_4bit=load_in_4bit,
    #     )
    #
    # trainer = LoRATrainer(config=cfg)
    # trainer.train()


@app.command()
def save(
    checkpoint: str = typer.Option(
        ...,
        "--checkpoint",
        help="Checkpoint directory path",
    ),
    output: str = typer.Option(
        ...,
        "--output",
        help="Output directory for saved adapter",
    ),
) -> None:
    """
    Save a trained adapter from a checkpoint.

    Example:
        finetune-demo save \\
            --checkpoint ./models/lora/checkpoint-500 \\
            --output ./models/lora/adapter
    """
    console.print(f"[bold blue]Saving adapter[/bold blue]")
    console.print(f"  Checkpoint: {checkpoint}")
    console.print(f"  Output:     {output}")

    # [PLACEHOLDER] 真实实现：
    # from finetune_demo.adapter.saver import AdapterSaver
    # saver = AdapterSaver()
    # saver.save(Path(checkpoint), Path(output))
    # console.print(f"[bold green]Adapter saved to {output}[/bold green]")


@app.command()
def list_checkpoints(
    output_dir: str = typer.Option("./models", "--output-dir", help="Model output directory"),
) -> None:
    """List all checkpoints in the output directory."""
    console.print(f"[bold blue]Checkpoints in {output_dir}[/bold blue]")

    # [PLACEHOLDER]
    # from finetune_demo.utils import list_checkpoints
    # checkpoints = list_checkpoints(Path(output_dir))
    # for ckpt in checkpoints:
    #     console.print(f"  - {ckpt}")


if __name__ == "__main__":
    app()
```

## CLI 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--method` | `lora` | 训练方法：lora \| qlora |
| `--model` | `Qwen/Qwen2.5-0.5B-Instruct` | HuggingFace 模型名 |
| `--dataset` | 必填 | 训练数据集 JSONL 路径 |
| `--output` | `./models` | 输出目录 |
| `--epochs` | `3` | 训练轮数 |
| `--per-device-batch-size` | `4` | 每设备 batch size |
| `--learning-rate` | `2e-4` | 学习率 |
| `--lora-r` | `16` | LoRA rank |
| `--lora-alpha` | `32` | LoRA alpha |
| `--load-in-4bit` | `False` | 4-bit 量化（QLoRA） |

---

Sources:
1. https://github.com/huggingface/peft — PEFT
2. https://github.com/huggingface/trl — TRL
