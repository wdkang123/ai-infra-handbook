# ai-gateway Import Map v1

## Task ID: T1202
## Title: ai-gateway Implementation Map Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# ai-gateway Import Dependency Map

本文档定义 `ai-gateway` 内部模块的导入依赖关系。

## Import Map

```
src/ai_gateway/
│
├── __init__.py
├── __version__.py           # 纯常量，无依赖
│
├── config.py                # AiGatewayConfig dataclass + YAML 加载，无内部依赖
│   └── from pydantic import BaseModel, Field
│
├── models.py                # Pydantic models，无内部依赖
│   └── from pydantic import BaseModel, Field
│
├── router.py                # 路由逻辑 + 代理转发，依赖 config
│   ├── from .config import AiGatewayConfig
│   └── import httpx
│
├── server.py                # FastAPI app，依赖 models + router + middleware
│   ├── from .models import ChatMessage, ChatCompletionsRequest, ...
│   ├── from .router import route_model
│   ├── from .middleware.auth import verify_bearer_token
│   └── from slowapi import Limiter, RateLimitExceeded
│
├── main.py                  # 启动入口
│   ├── from .config import load_config
│   ├── from .server import app, set_config
│   └── from .router import ProxyClient
│
└── middleware/
    ├── __init__.py
    ├── auth.py              # 鉴权中间件，不依赖 httpx
    │   ├── from fastapi import HTTPException, Request
    │   └── from typing import Optional
    └── rate_limit.py        # 限流中间件
        └── from slowapi import Limiter
```

## External Dependencies

| 模块 | 外部依赖 | 版本 |
|---|---|---|
| `server.py` | `fastapi`, `uvicorn`, `slowapi` | ≥0.27 |
| `router.py`（proxy 部分）| `httpx` | ≥0.27 |
| `auth.py` | 无外部 HTTP 依赖（只依赖 fastapi） | — |
| `rate_limit.py` | `slowapi` | ≥0.9 |
| `models.py` | `pydantic` | ≥2.0 |

## 关键：Auth Middleware 注入

```python
# server.py
_config: Any = None

def set_config(config: AiGatewayConfig) -> None:
    global _config
    _config = config

def get_config() -> AiGatewayConfig:
    if _config is None:
        raise RuntimeError("Config not initialized.")
    return _config

async def verify_bearer_token(request: Request) -> str:
    """验证 Bearer token，不依赖 httpx。"""
    enabled = get_config().auth.get("enabled", True) if _config else False
    if not enabled:
        return None  # auth disabled → bypass
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(401, detail={"message": "Invalid Authorization header format. Expected: Bearer <key>"})
    token = auth_header[7:]
    if token not in get_config().auth.get("api_keys", []):
        raise HTTPException(401, detail={"message": "Invalid API key"})
    return token  # 返回已验证的 key 字符串
```

**注意：** auth 成功时返回 key 字符串（而非 None），与 accepted `T1002-ai-gateway-auth-middleware-blueprint-v1.md` 一致。

---

Sources:
- T1002: server.py, auth middleware blueprints
- T1102: auth fixtures (corrected: success returns key string)
- T812: API contract

Risk of Staleness:
- Import pattern follows FastAPI + slowapi project structure; stable
