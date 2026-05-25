# ai-gateway Patch Split v1

## Task ID: T1202
## Title: ai-gateway Implementation Map Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# ai-gateway Patch Split Proposal

本文档定义 ai-gateway 的分批实现顺序，每批可独立验证。

## Patch 批次概览

| Patch | 名称 | 目标文件 | 验证方式 |
|---|---|---|---|
| P0 | 骨架 + 配置 | `pyproject.toml / config.py / models.py` | `import ai_gateway` |
| P1 | FastAPI 骨架 | `server.py / main.py` | `curl localhost:8080/health` 返回 200 |
| P2 | 鉴权中间件 | `middleware/auth.py` | 无 token → 401，有 token → 透传 |
| P3 | 路由 + 代理 | `router.py / server.py` | 路由 404，代理 200 |
| P4 | 限流中间件 | `middleware/rate_limit.py` | RPM 超限 → 429 |
| P5 | 测试骨架 | `tests/conftest.py / test_proxy.py` | `pytest tests/` 全部通过 |

---

## Patch 0: 项目骨架

**文件：**
- `pyproject.toml`
- `src/ai_gateway/__init__.py`
- `src/ai_gateway/__version__.py`
- `src/ai_gateway/config.py`
- `src/ai_gateway/models.py`
- `configs/models.yaml`
- `configs/config.yaml`

**验证：**
```bash
cd ai-gateway
python -c "from ai_gateway import config, models; print('OK')"
```

---

## Patch 1: FastAPI 骨架

**文件：**
- `src/ai_gateway/server.py`（骨架，auth/routing 用 mock）
- `src/ai_gateway/main.py`

**实现要点：**
- `set_config()` / `get_config()` 状态注入
- `/health` 返回 mock `HealthResponse`
- `/v1/chat/completions` mock 返回 200（不调真实下游）
- `verify_bearer_token()` mock 直接 return `"sk-test-key-1"`（跳过真实验证）

**验证：**
```bash
cd ai-gateway && python -m ai_gateway.main &

curl -s http://localhost:8080/health | python -m json.tool
# 期望：{"status": "healthy", "version": "0.1.0"}

curl -s -X POST http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "vllm-local", "messages": [{"role": "user", "content": "Hi"}]}' \
  | python -m json.tool
# 期望：200 + mock ChatCompletionsResponse

pkill -f "ai_gateway.main"
```

---

## Patch 2: 鉴权中间件

**文件：**
- `src/ai_gateway/middleware/__init__.py`
- `src/ai_gateway/middleware/auth.py`
- `src/ai_gateway/server.py`（修改：注入真实 `verify_bearer_token`）

**实现要点：**
- `AuthMiddleware(api_keys, enabled)` 类（不依赖 httpx）
- `enabled=False` → `return None`（bypass auth）
- `enabled=True` + 无 token → 401
- `enabled=True` + invalid scheme → 401 + message: `"Invalid Authorization header format. Expected: Bearer <key>"`
- `enabled=True` + invalid key → 401
- `enabled=True` + valid Bearer → 返回 key 字符串

**验证：**
```bash
# 无 token → 401
curl -s -w "\n%{http_code}" -X POST http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "vllm-local", "messages": [{"role": "user", "content": "Hi"}]}'
# 期望：401 + {"error": {"message": "Missing Authorization header", ...}}

# 错误 scheme → 401
curl -s -w "\n%{http_code}" -X POST http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic dXNlcjpwYXNz" \
  -d '{"model": "vllm-local", "messages": [{"role": "user", "content": "Hi"}]}'
# 期望：401 + {"error": {"message": "Invalid Authorization header format. Expected: Bearer <key>", ...}}

# 有效 token → 透传
curl -s -X POST http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-test-key-1" \
  -d '{"model": "vllm-local", "messages": [{"role": "user", "content": "Hi"}]}' \
  | python -m json.tool
# 期望：200（到达下游）
```

**对应 fixture：** T1102 `T1102-gateway-auth-request-fixtures-v1.md`

---

## Patch 3: 路由 + 代理

**文件：**
- `src/ai_gateway/router.py`
- `src/ai_gateway/server.py`（修改：真实路由调用）

**实现要点：**
- `router.py`: `_route_model(name, config)` → 下游 URL 或 None
- `None` → HTTPException 404
- `router.py`: `forward_chat_request(body, downstream_url)` → httpx AsyncClient（proxy 逻辑在 router.py 内）

**验证：**
```bash
# 未知模型 → 404
curl -s -w "\n%{http_code}" -X POST http://localhost:8080/v1/chat/completions \
  -H "Authorization: Bearer sk-test-key-1" \
  -H "Content-Type: application/json" \
  -d '{"model": "unknown-model", "messages": [{"role": "user", "content": "Hi"}]}'
# 期望：404 + {"error": {"code": "404"}}

# 已知模型 → 200（需 inference-service 运行）
curl -s -X POST http://localhost:8080/v1/chat/completions \
  -H "Authorization: Bearer sk-test-key-1" \
  -H "Content-Type: application/json" \
  -d '{"model": "vllm-local", "messages": [{"role": "user", "content": "What is 2+2?"}]}' \
  | python -m json.tool
# 期望：200 + 来自 inference-service 的真实响应
```

**对应 fixture：** T1102 `T1102-gateway-error-response-samples-v1.md`

---

## Patch 4: 限流中间件

**文件：**
- `src/ai_gateway/middleware/rate_limit.py`
- `src/ai_gateway/server.py`（修改：挂载 `@limiter.limit`）

**验证：**
```bash
# 快速发 61 个请求（超过 60/minute）
for i in {1..65}; do
  curl -s -o /dev/null -w "%{http_code}\n" \
    -X POST http://localhost:8080/v1/chat/completions \
    -H "Authorization: Bearer sk-test-key-1" \
    -H "Content-Type: application/json" \
    -d '{"model": "vllm-local", "messages": [{"role": "user", "content": "Hi"}]}'
done | tail -5
# 期望：429 (rate limited)
```

**对应 fixture：** T1102 `error_responses/429_rate_limit.json`

---

## Patch 5: 测试骨架

**文件：**
- `tests/__init__.py`
- `tests/conftest.py`
- `tests/test_proxy.py`

**验证：**
```bash
cd ai-gateway
pytest tests/ -v
```

---

## Patch 依赖关系图

```
P0 (骨架)
  │
  └── P1 (FastAPI 骨架)
          │
          ├── P2 (鉴权)           ← P1 中 verify_bearer_token mock 替换为真实
          │       │
          │       └── P3 (路由+代理) ← 依赖 P2 auth 通过后才能路由
          │
          └── P4 (限流)            ← 与 P2/P3 并行
                  │
                  └── P5 (测试)    ← 依赖 P1~P4 全部完成
```

**注意：** P3（路由+代理）需 inference-service 真实运行才能端到端验证。

---

Sources:
- T1002: server.py, auth middleware blueprints
- T1102: auth fixtures, routing fixtures, error fixtures
- T302: accepted MVP design
- T812: accepted API contract

Risk of Staleness:
- Patch ordering follows standard FastAPI middleware project structure; stable
