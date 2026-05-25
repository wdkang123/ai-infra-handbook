from __future__ import annotations

import typer
import uvicorn
from rich.console import Console

from inference_service.config import load_config
from inference_service.engines import create_engine
from inference_service.server import set_config, set_engine

app = typer.Typer(name="inference-service", add_completion=False)
console = Console()


@app.callback()
def entry() -> None:
    """Inference service command group."""


@app.command()
def serve(
    engine: str = typer.Option("mock", "--engine"),
    model: str = typer.Option("Qwen/Qwen2.5-0.5B-Instruct", "--model"),
    engine_base_url: str | None = typer.Option(None, "--engine-base-url"),
    engine_api_key: str | None = typer.Option(None, "--engine-api-key"),
    port: int = typer.Option(8000, "--port"),
    host: str = typer.Option("0.0.0.0", "--host"),
) -> None:
    cfg = load_config()
    cfg.engine.type = engine
    cfg.engine.model_path = model
    if engine_base_url is not None:
        cfg.engine.base_url = engine_base_url
    if engine_api_key is not None:
        cfg.engine.api_key = engine_api_key
    cfg.server.port = port
    cfg.server.host = host
    set_config(cfg)
    set_engine(create_engine(cfg))

    console.print("[bold blue]Starting inference-service[/bold blue]")
    console.print(f"  Engine: {engine}")
    console.print(f"  Model:  {model}")
    if cfg.engine.base_url:
        console.print(f"  Upstream: {cfg.engine.base_url}")
    console.print(f"  Port:   {port}")

    uvicorn.run(
        "inference_service.server:app",
        host=host,
        port=port,
        reload=False,
        factory=False,
    )


@app.command("health-check")
def health_check(
    url: str = typer.Option("http://localhost:8000", "--url"),
) -> None:
    import httpx

    response = httpx.get(f"{url}/health", timeout=5.0)
    response.raise_for_status()
    console.print(response.text)


@app.command()
def version() -> None:
    console.print("inference-service 0.1.0")


if __name__ == "__main__":
    app()
