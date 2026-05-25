# ai-gateway Codex Handoff v1

## Task ID: T1402
## Title: ai-gateway Codex Task Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# ai-gateway Codex Handoff

本文档是可直接复制给 Codex 的任务卡 handoff 文本。

---

## T1402-T01: 包骨架 + 配置

**任务：** 为 `ai-gateway/` 创建 Python 包骨架和配置层。

**目录结构：**
```
ai-gateway/
├── pyproject.toml
├── src/ai_gateway/
│   ├── __init__.py
│   ├── __version__.py
│   ├── config.py
├── configs/
│   ├── models.yaml
│   └── config.yaml
```

**models.yaml 格式：**
```yaml
models:
  vllm-local:
    type: vllm
    base_url: http://localhost:8000/v1
```

**config.yaml 格式：**
```yaml
auth:
  enabled: true
  api_keys:
    - dev-gateway-key-1
rate_limit:
  enabled: true
  requests_per_minute: 60
```

**禁止事项：** 不写 server.py、auth middleware、router

---

## T1402-T02: Health + Metrics 端点

**任务：** 实现 `/health` 和 `/metrics` 端点（不包含 `/v1/chat/completions`）。

**server.py 要求：**
- 定义 `HealthResponse` model — `{"status": "healthy", "version": "0.1.0", "upstream_services": {"vllm-local": "healthy"}}`
- `/health` GET — 返回 `HealthResponse`
- `/metrics` GET — 返回 Prometheus 格式字符串
- `set_config()` / `get_config()` 注入函数
- `main.py` startup 调用 `set_config()`

**验证命令：**
```bash
curl http://localhost:8080/health
curl http://localhost:8080/metrics
```

**禁止事项：** 不得在 T02 实现 `/v1/chat/completions` 的路由逻辑（属于 T04）

---

## T1402-T03: 鉴权中间件

**任务：** 实现 `middleware/auth.py`，包含 `AuthMiddleware` 类和 `verify_bearer_token()` 函数。

**auth.py 要求：**
- `AuthMiddleware(api_keys, enabled)` — 构造函数
- `async __call__(request)` — 返回 validated token 或 raise HTTPException(401)
- `verify_bearer_token(request)` — 从 app state 获取 config 调用 middleware
- 无 Authorization header → `401 {"message": "Missing Authorization header", ...}`
- 非 Bearer 格式 → `401 {"message": "Invalid Authorization header format. Expected: Bearer <key>", ...}`
- 无效 token → `401 {"message": "Invalid API key", ...}`

**验证命令：**
```bash
# 无 token
curl -s -w "\n%{http_code}" http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "vllm-local", "messages": [{"role": "user", "content": "Hi"}]}'
# 期望：401
```

---

## T1402-T04: 路由 + 代理

**任务：** 实现 router.py 和 server.py 的 `/v1/chat/completions` 路由逻辑。

**router.py 要求：**
- `_route_model(model_name, config)` → 下游 URL 或 None
- `forward_chat_request(body, downstream_url)` → httpx.AsyncClient 转发

**server.py 要求：**
- `/v1/chat/completions` POST — 调用 auth → 路由 → 转发
- 未知模型 → `HTTPException(404, {"message": "Model not found: {model}", ...})`
- 使用 `httpx.AsyncClient` 转发到下游

**错误响应格式：**
```json
{"error": {"message": "...", "type": "invalid_request_error", "code": "404"}}
```

**禁止事项：**
- 端口必须是 8080
- 不得添加 `/v1/completions` 或 `/v1/models`（已从 MVP 降级）
- auth 验证在路由之前

---

Sources:
- T1002: accepted starter manifest
- T812: accepted API contract
- T1302: accepted execution slice
