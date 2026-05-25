# ai-gateway File Order v1

## Task ID: T1202
## Title: ai-gateway Implementation Map Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# ai-gateway File Implementation Order

本文档定义 `ai-gateway/` 目录的编码实现顺序，基于 accepted `T1002 / T1102 / T302 / T812` blueprints。

## 文件实现顺序

### Phase 0: 骨架

| Order | 文件路径 | 目的 | 依赖 |
|---|---|---|---|
| 0.1 | `src/__init__.py` | 包声明 | 无 |
| 0.2 | `src/ai_gateway/__init__.py` | 模块命名空间 | 无 |
| 0.3 | `src/ai_gateway/__version__.py` | `__version__` | 无 |
| 0.4 | `pyproject.toml` | 项目元数据 | 无 |
| 0.5 | `configs/models.yaml` | 路由配置样例 | 无 |
| 0.6 | `configs/config.yaml` | 完整配置样例 | 无 |

### Phase 1: 配置层

| Order | 文件路径 | 目的 | 依赖 |
|---|---|---|---|
| 1.1 | `src/ai_gateway/config.py` | AiGatewayConfig dataclass + YAML 加载 | 无 |

**实现要点：** 对应 T1102 `T1102-gateway-routing-config-samples-v1.md` 的 `models.yaml` 格式，`api_keys` 字段来自 accepted T1002 blueprint。

### Phase 2: 鉴权中间件

| Order | 文件路径 | 目的 | 依赖 |
|---|---|---|---|
| 2.1 | `src/ai_gateway/middleware/__init__.py` | Middleware 包 | 无 |
| 2.2 | `src/ai_gateway/middleware/auth.py` | Bearer token 验证 | Phase 1 |

**实现要点：** 来自 accepted `T1002-ai-gateway-auth-middleware-blueprint-v1.md`，`AuthMiddleware(api_keys, enabled)` 类，`verify_bearer_token(request)` 函数。不依赖 `httpx`。成功时返回已验证的 key 字符串（非 None）。

### Phase 3: 路由层

| Order | 文件路径 | 目的 | 依赖 |
|---|---|---|---|
| 3.1 | `src/ai_gateway/router.py` | Router 类 + 路由函数 | Phase 1 |

**实现要点：** `_route_model(model_name, config)` 查询 `models.yaml`，返回下游 URL 或 None（404）。

### Phase 4: FastAPI 应用骨架

| Order | 文件路径 | 目的 | 依赖 |
|---|---|---|---|
| 4.1 | `src/ai_gateway/server.py` | FastAPI app + 端点 | Phase 2 + 3 |
| 4.2 | `src/ai_gateway/models.py` | Pydantic models | Phase 1 |
| 4.3 | `src/ai_gateway/main.py` | uvicorn 启动入口 | Phase 2 + 4.1 |

**实现要点：** 来自 accepted `T1002-ai-gateway-server-py-blueprint-v1.md`，`set_config()` / `get_config()` 注入。`/health` 返回 `HealthResponse`，`/v1/chat/completions` 实现路由 + 代理 + 错误处理。

### Phase 5: 代理转发

| Order | 文件路径 | 目的 | 依赖 |
|---|---|---|---|
| 5.1 | `src/ai_gateway/router.py` 修改 | 增加 `forward_chat_request()` | Phase 3 + Phase 4.1 |
| 5.2 | `src/ai_gateway/main.py` 修改 | startup 中初始化 proxy | Phase 5.1 |

**实现要点：** 使用 `httpx.AsyncClient` 转发请求到下游，对应 T1102 `T1102-gateway-proxy-response-samples-v1.md`。

### Phase 6: 限流

| Order | 文件路径 | 目的 | 依赖 |
|---|---|---|---|
| 6.1 | `src/ai_gateway/middleware/rate_limit.py` | Rate limit 中间件 | Phase 2 |
| 6.2 | `src/ai_gateway/server.py` 修改 | 挂载限流装饰器 | Phase 6.1 |

### Phase 7: 测试骨架

| Order | 文件路径 | 目的 | 依赖 |
|---|---|---|---|
| 7.1 | `tests/__init__.py` | 测试包 | 无 |
| 7.2 | `tests/conftest.py` | pytest fixtures | Phase 4.1 |
| 7.3 | `tests/test_proxy.py` | 代理逻辑测试 | Phase 5.1 + 7.2 |

---

## 目录结构

```
ai-gateway/
├── src/ai_gateway/
│   ├── __init__.py
│   ├── __version__.py
│   ├── config.py           ← Phase 1
│   ├── models.py           ← Phase 4
│   ├── router.py           ← Phase 3/5
│   ├── server.py            ← Phase 4
│   ├── main.py              ← Phase 4/5
│   └── middleware/
│       ├── __init__.py
│       ├── auth.py          ← Phase 2
│       └── rate_limit.py    ← Phase 6
├── configs/
│   ├── models.yaml          ← Phase 0
│   └── config.yaml          ← Phase 0
├── tests/
│   ├── __init__.py
│   ├── conftest.py          ← Phase 7
│   └── test_proxy.py        ← Phase 7
├── scripts/
│   └── serve.sh             ← Phase 0 (沿用 T902 scaffold)
├── pyproject.toml            ← Phase 0
└── .env.example              ← Phase 0
```

---

Sources:
- T1002: server.py, auth middleware blueprints
- T1102: routing config, auth fixtures
- T302: accepted MVP design
- T812: accepted API contract

Risk of Staleness:
- Phase ordering follows standard FastAPI middleware project structure; stable
