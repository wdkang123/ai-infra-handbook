# inference-service Import Map v1

## Task ID: T1201
## Title: inference-service Implementation Map Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# inference-service Import Dependency Map

本文档定义 `inference-service` 内部模块的导入依赖关系，对应 T1201 file order。

## Import Map

```
src/inference_service/
│
├── __init__.py          # 导出 __version__, InferenceService
├── __version__.py      # 纯常量，无依赖
│
├── config.py            # 纯配置，无内部依赖
│   └── （无内部 imports）
│
├── server.py           # FastAPI app + 路由，依赖 config
│   ├── from .config import InferenceConfig
│   └── from .engines.base import BaseEngine
│
├── api/
│   ├── __init__.py
│   ├── chat.py         # /v1/chat/completions
│   ├── health.py       # /health
│   └── metrics.py      # /metrics
│
├── engines/
│   ├── __init__.py     # 导出 VLLMEngine
│   ├── base.py        # 引擎抽象
│   └── vllm_engine.py # 核心 engine，依赖 vllm 库
│       ├── from vllm import LLM
│       └── from .config import InferenceConfig
│
└── main.py             # 启动入口，依赖 config + server + engines
    ├── from .config import load_config
    ├── from .server import app, set_engine
    └── from .engines import create_engine
```

## External Dependencies

| 模块 | 外部依赖 | 版本要求 |
|---|---|---|
| `server.py` | `fastapi`, `uvicorn` | ≥0.27 |
| `metrics.py` | `prometheus_client` | ≥0.17 |
| `vllm_engine.py` | `vllm` | ≥0.3 |
| `main.py` | `uvicorn` | ≥0.27 |

## Entry Point Flow

```
main.py (entry)
  │
  ├── load_config() → config.py
  │       └── InferenceConfig
  │
  ├── create_engine() → engines/vllm_engine.py
  │       └── VLLMEngine
  │
  └── set_engine(engine) → server.py (injects _engine global)
          │
          └── FastAPI app starts
                  ├── /health              → uses _engine
                  ├── /metrics             → uses api/metrics.py
                  └── /v1/chat/completions → uses _engine.predict()
```

## Key State: Engine Injection

```python
# server.py — global state
_engine: Any = None

def set_engine(engine: Any) -> None:
    global _engine
    _engine = engine

def get_engine() -> Any:
    if _engine is None:
        raise RuntimeError("Engine not initialized. Call set_engine() first.")
    return _engine
```

`main.py` 的 startup event 调用 `set_engine(create_engine(...))` 完成注入，engine 由 `engines/` 包创建。

---

Sources:
- T1001: server.py blueprint (set_engine / get_engine pattern)
- T301: MVP design
- T811: API contract

Risk of Staleness:
- Import pattern follows FastAPI + vLLM project convention; stable
