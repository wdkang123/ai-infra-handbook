# inference-service main.py Blueprint v1

## Task ID: T1001
## Title: inference-service Starter File Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T901 scaffold（pyproject / run-script），产出 `main.py` CLI 入口蓝图。

---

# inference-service main.py Blueprint v1

## 概述

本文档定义 `src/inference_service/main.py` 的蓝图——Typer CLI 入口，不包含真实逻辑（占位符）。

## `src/inference_service/main.py` 模板

```python
# src/inference_service/main.py
"""
inference-service CLI entry point.

用法:
    inference-service serve --engine vllm --model Qwen/Qwen2.5-0.5B-Instruct --port 8000
"""
from __future__ import annotations

import sys
from typing import Optional

import typer
from rich.console import Console

app = typer.Typer(
    name="inference-service",
    help="OpenAI-compatible inference service powered by vLLM",
    add_completion=False,
)
console = Console()


@app.command()
def serve(
    engine: str = typer.Option(
        "vllm",
        "--engine",
        help="Engine type: vllm | sglang | triton",
    ),
    model: str = typer.Option(
        "Qwen/Qwen2.5-0.5B-Instruct",
        "--model",
        help="HuggingFace model name or path",
    ),
    port: int = typer.Option(8000, "--port", help="HTTP server port"),
    host: str = typer.Option("0.0.0.0", "--host", help="Server host"),
    metrics_port: int = typer.Option(9090, "--metrics-port", help="Prometheus metrics port"),
    workers: int = typer.Option(1, "--workers", help="Uvicorn workers"),
    timeout: int = typer.Option(300, "--timeout", help="Request timeout in seconds"),
    # vLLM specific
    vllm_gpu_memory_utilization: float = typer.Option(
        0.9,
        "--vllm-gpu-memory-utilization",
        help="vLLM GPU memory utilization (0.0–1.0)",
    ),
    vllm_max_model_len: int = typer.Option(
        4096,
        "--vllm-max-model-len",
        help="vLLM max model context length",
    ),
    vllm_enforce_eager: bool = typer.Option(
        False,
        "--vllm-enforce-eager",
        help="vLLM enforce eager mode (disable CUDA graphs)",
    ),
) -> None:
    """
    Start the inference service.

    Example:
        inference-service serve --engine vllm --model Qwen/Qwen2.5-0.5B-Instruct --port 8000
    """
    console.print(f"[bold blue]Starting inference-service[/bold blue]")
    console.print(f"  Engine: {engine}")
    console.print(f"  Model:  {model}")
    console.print(f"  Port:   {port}")

    # [PLACEHOLDER] 真实实现：
    # 1. 加载 config.py 的配置
    # 2. 根据 engine 类型初始化对应引擎
    # 3. 调用 run_server() 启动 FastAPI
    # raise NotImplementedError("Codex: implement this")


@app.command()
def health_check(
    url: str = typer.Option("http://localhost:8000", "--url", help="Service URL"),
) -> None:
    """
    Check if the inference service is healthy.

    Example:
        inference-service health-check --url http://localhost:8000
    """
    import httpx
    try:
        resp = httpx.get(f"{url}/health", timeout=5.0)
        resp.raise_for_status()
        console.print(f"[green]Healthy:[/green] {resp.json()}")
    except Exception as e:
        console.print(f"[red]Unhealthy:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def version() -> None:
    """Show version information."""
    from inference_service import __version__
    console.print(f"inference-service v{__version__}")


if __name__ == "__main__":
    app()
```

## Typer CLI 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--engine` | str | `vllm` | 引擎类型 |
| `--model` | str | `Qwen/Qwen2.5-0.5B-Instruct` | 模型名 |
| `--port` | int | `8000` | HTTP 端口 |
| `--host` | str | `0.0.0.0` | 监听地址 |
| `--metrics-port` | int | `9090` | Prometheus 端口 |
| `--workers` | int | `1` | Uvicorn workers |
| `--timeout` | int | `300` | 请求超时（秒） |
| `--vllm-gpu-memory-utilization` | float | `0.9` | vLLM GPU 显存占用 |
| `--vllm-max-model-len` | int | `4096` | 最大上下文长度 |
| `--vllm-enforce-eager` | bool | `False` | 禁用 CUDA graphs |

## 模块版本常量（占位）

```python
# src/inference_service/__init__.py
__version__ = "0.1.0"
```

---

Sources:
1. https://typer.tiangolo.com/ — Typer
2. https://docs.vllm.ai/ — vLLM

Risk of Staleness:
- Typer 参数解析方式在 0.12+ 稳定

Out of Scope Kept:
- 未写 completions 端点（已由 /v1/chat/completions 替代）
