# ai-gateway main.py Blueprint v1

## Task ID: T1002
## Title: ai-gateway Starter File Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T902 scaffold（pyproject / run-script），产出 `main.py` CLI 入口蓝图。

---

# ai-gateway main.py Blueprint v1

## 概述

本文档定义 `src/ai_gateway/main.py` 的蓝图——Typer CLI 入口。

## `src/ai_gateway/main.py` 模板

```python
# src/ai_gateway/main.py
"""
ai-gateway CLI entry point.

用法:
    ai-gateway serve --port 8080
"""
from __future__ import annotations

import sys

import typer
from rich.console import Console

app = typer.Typer(
    name="ai-gateway",
    help="AI Gateway: proxy, auth, rate-limit, and observability layer",
    add_completion=False,
)
console = Console()


@app.command()
def serve(
    port: int = typer.Option(8080, "--port", help="Gateway HTTP port"),
    host: str = typer.Option("0.0.0.0", "--host", help="Server host"),
    metrics_port: int = typer.Option(9091, "--metrics-port", help="Prometheus metrics port"),
    workers: int = typer.Option(1, "--workers", help="Uvicorn workers"),
    timeout: int = typer.Option(300, "--timeout", help="Request timeout in seconds"),
    no_auth: bool = typer.Option(False, "--no-auth", help="Disable auth middleware (dev only)"),
    no_rate_limit: bool = typer.Option(
        False, "--no-rate-limit", help="Disable rate limit middleware (dev only)"
    ),
    log_level: str = typer.Option("INFO", "--log-level", help="Log level: DEBUG|INFO|WARNING|ERROR"),
) -> None:
    """
    Start the AI Gateway proxy server.

    Example:
        ai-gateway serve --port 8080
    """
    console.print(f"[bold blue]Starting ai-gateway[/bold blue]")
    console.print(f"  Port:   {port}")
    console.print(f"  Auth:   {'DISABLED' if no_auth else 'enabled'}")
    console.print(f"  Rate:   {'DISABLED' if no_rate_limit else 'enabled'}")

    # [PLACEHOLDER] 真实实现：
    # 1. 加载 config.py
    # 2. 初始化 auth middleware（如果 no_auth=False）
    # 3. 初始化 rate_limit middleware（如果 no_rate_limit=False）
    # 4. 启动 FastAPI via uvicorn
    # raise NotImplementedError("Codex: implement this")


@app.command()
def health_check(
    url: str = typer.Option("http://localhost:8080", "--url", help="Gateway URL"),
) -> None:
    """Check if the gateway is healthy."""
    import httpx
    try:
        resp = httpx.get(f"{url}/health", timeout=5.0)
        resp.raise_for_status()
        console.print(f"[green]Healthy:[/green] {resp.json()}")
    except Exception as e:
        console.print(f"[red]Unhealthy:[/red] {e}")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
```

## Typer CLI 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--port` | int | `8080` | Gateway HTTP 端口 |
| `--host` | str | `0.0.0.0` | 监听地址 |
| `--metrics-port` | int | `9091` | Prometheus 端口 |
| `--workers` | int | `1` | Uvicorn workers |
| `--timeout` | int | `300` | 请求超时（秒） |
| `--no-auth` | bool | `False` | 禁用鉴权（开发用） |
| `--no-rate-limit` | bool | `False` | 禁用限流（开发用） |
| `--log-level` | str | `INFO` | 日志级别 |

## 模块版本常量（占位）

```python
# src/ai_gateway/__init__.py
__version__ = "0.1.0"
```

---

Sources:
1. https://typer.tiangolo.com/ — Typer
2. https://github.com/Portkey-AI/gateway — Portkey Gateway
