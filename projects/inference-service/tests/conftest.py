from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from inference_service.engines import MockInferenceEngine
from inference_service.server import app, set_config, set_engine


@pytest.fixture(autouse=True)
def reset_app_state() -> None:
    from inference_service.config import load_config

    config_path = Path(__file__).resolve().parents[1] / "config.yaml"
    cfg = load_config(str(config_path))
    set_config(cfg)
    set_engine(MockInferenceEngine())


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)
