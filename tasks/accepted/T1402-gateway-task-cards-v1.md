# ai-gateway Task Cards v1

## Task ID: T1402
## Title: ai-gateway Codex Task Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# ai-gateway Task Cards

本文档定义每个任务卡的具体输入资产、目标文件、验收命令、完成信号和 cut line。

---

## T1402-T01: 包骨架 + 配置

**Task Name:** 包骨架 + 配置

**对应 Slice:** G1

**输入资产：**
- `T1002-ai-gateway-starter-manifest.md`
- `T1002-ai-gateway-config-py-blueprint-v1.md`

**目标文件：**
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

**验收命令：**
```bash
cd ai-gateway
python -c "from ai_gateway import config; print('OK')"
```

**完成信号：** `import ai_gateway` 无报错

**Cut Line：** 不写 server.py、auth、router

---

## T1402-T02: Health + Metrics 端点

**Task Name:** Health + Metrics 端点

**对应 Slice:** G4

**输入资产：**
- `T1002-ai-gateway-server-py-blueprint-v1.md`（G4 部分）
- `T1402-T01/`（目标文件）

**目标文件：**
```
ai-gateway/src/ai_gateway/
├── server.py
└── main.py
```

**验收命令：**
```bash
cd ai-gateway && python -m ai_gateway.main &
sleep 3

curl -s http://localhost:8080/health
# 期望：{"status": "healthy", "version": "0.1.0", "upstream_services": {"vllm-local": "healthy"}}

curl -s http://localhost:8080/metrics
# 期望：Prometheus 格式

pkill -f "ai_gateway.main"
```

**完成信号：** `/health` 返回 `upstream_services`，`/metrics` 返回正确格式

**Cut Line：** `/v1/chat/completions` 暂不实现（属于 T04）；auth mock 返回 bypass（属于 T03）

---

## T1402-T03: 鉴权中间件

**Task Name:** 鉴权中间件

**对应 Slice:** G2

**输入资产：**
- `T1002-ai-gateway-auth-middleware-blueprint-v1.md`
- `T1402-T01/`

**目标文件：**
```
ai-gateway/src/ai_gateway/middleware/
├── __init__.py
└── auth.py
```

**验收命令：**
```bash
# 无 token → 401
curl -s -w "\n%{http_code}" -X POST http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "vllm-local", "messages": [{"role": "user", "content": "Hi"}]}'
# 期望：401

# 错误 scheme → 401
curl -s -w "\n%{http_code}" -X POST http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic dXNlcjpwYXNz" \
  -d '{"model": "vllm-local", "messages": [{"role": "user", "content": "Hi"}]}'
# 期望：401

# 有效 Bearer → 通过（需 T04 完成路由后端到端）
```

**完成信号：** `AuthMiddleware` 类实现，`verify_bearer_token()` 函数实现，无 token 返回 401

**Cut Line：** 不实现限流（属于 G5）

---

## T1402-T04: 路由 + 代理

**Task Name:** 路由 + 代理

**对应 Slice:** G3

**输入资产：**
- `T1002-ai-gateway-server-py-blueprint-v1.md`（G3 部分）
- `T1402-T03/`（from T03）

**目标文件：**
```
ai-gateway/src/ai_gateway/
├── router.py（修改或新增）
└── server.py（修改）
```

**验收命令：**
```bash
# 未知模型 → 404
curl -s -w "\n%{http_code}" -X POST http://localhost:8080/v1/chat/completions \
  -H "Authorization: Bearer sk-test-key-1" \
  -H "Content-Type: application/json" \
  -d '{"model": "unknown-model", "messages": [{"role": "user", "content": "Hi"}]}'
# 期望：404

# 已知模型 vllm-local → 200（需 inference-service 运行在 localhost:8000）
curl -s -X POST http://localhost:8080/v1/chat/completions \
  -H "Authorization: Bearer sk-test-key-1" \
  -H "Content-Type: application/json" \
  -d '{"model": "vllm-local", "messages": [{"role": "user", "content": "What is 2+2?"}]}'
# 期望：200 + 来自下游的响应
```

**完成信号：** 路由到已知模型返回 200，未知模型返回 404

**Cut Line：** 不实现 `/v1/models`、`/v1/completions`

---

Sources:
- T1002: accepted starter manifest
- T1102: fixture assets
- T1302: accepted execution slice
- T812: accepted API contract
