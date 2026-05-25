from __future__ import annotations

import typer
import uvicorn
from rich.console import Console

from ai_gateway.config import load_config
from ai_gateway.server import set_config

app = typer.Typer(name="ai-gateway", add_completion=False)
console = Console()


@app.callback()
def entry() -> None:
    """AI gateway command group."""


@app.command()
def serve(
    port: int = typer.Option(8080, "--port"),
    host: str = typer.Option("0.0.0.0", "--host"),
) -> None:
    cfg = load_config()
    cfg.server.port = port
    cfg.server.host = host
    set_config(cfg)
    from ai_gateway.server import app as server_app

    server_app.state.config = cfg

    console.print("[bold blue]Starting ai-gateway[/bold blue]")
    console.print(f"  Port: {port}")

    uvicorn.run("ai_gateway.server:app", host=host, port=port, reload=False, factory=False)


@app.command("health-check")
def health_check(
    url: str = typer.Option("http://localhost:8080", "--url"),
) -> None:
    import httpx

    response = httpx.get(f"{url}/health", timeout=5.0)
    response.raise_for_status()
    console.print(response.text)


if __name__ == "__main__":
    app()
