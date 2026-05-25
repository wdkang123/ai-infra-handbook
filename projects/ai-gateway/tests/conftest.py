from __future__ import annotations

import pytest
from ai_gateway.config import load_config
from ai_gateway.server import app, set_config
from fastapi.testclient import TestClient


def _test_config():
    cfg = load_config()
    cfg.auth.enabled = True
    cfg.auth.api_keys = ["dev-gateway-key-1"]
    return cfg


@pytest.fixture()
def client() -> TestClient:
    cfg = _test_config()
    set_config(cfg)
    app.state.config = cfg
    return TestClient(app)
