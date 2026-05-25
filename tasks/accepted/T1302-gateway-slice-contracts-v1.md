# ai-gateway Slice Contracts v1

## Task ID: T1302
## Title: ai-gateway Execution Slice Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# ai-gateway Slice Contracts

本文档定义每个 slice 的具体目标、入口、验收命令、前置条件和完成信号。

---

## G1: 包骨架 + 配置

**目标文件：**
- `pyproject.toml`
- `src/ai_gateway/__init__.py`
- `src/ai_gateway/__version__.py`
- `src/ai_gateway/config.py`
- `configs/models.yaml`
- `configs/config.yaml`

**入口：** `python -c "from ai_gateway import config; print('OK')"`

**验收命令：**
```bash
cd ai-gateway
python -c "from ai_gateway import config; print('OK')"
```

**前置条件：** 无

**完成信号：** `import ai_gateway` 无报错

**Cut Line：** 不写 server.py、auth、router

---

## G2: 鉴权中间件

**目标文件：**
- `src/ai_gateway/middleware/__init__.py`
- `src/ai_gateway/middleware/auth.py`

**入口：** 直接 import 或通过 server.py 调用

**验收命令：**
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

# 有效 token → 透传（需 inference-service 运行）
curl -s -X POST http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-test-key-1" \
  -d '{"model": "vllm-local", "messages": [{"role": "user", "content": "Hi"}]}' \
  | python -m json.tool
# 期望：200（到达下游 inference-service）
```

**前置条件：** G1 完成

**完成信号：** 无 token 返回 401，错误 scheme 返回 401，有效 Bearer 返回 key 字符串

**Cut Line：** 不实现路由，不实现限流

---

## G3: 路由 + 代理

**目标文件：**
- `src/ai_gateway/router.py`
- `src/ai_gateway/server.py`（修改）
- `src/ai_gateway/main.py`（修改）

**入口：** 同 G2 启动方式

**验收命令：**
```bash
# 未知模型 → 404
curl -s -w "\n%{http_code}" -X POST http://localhost:8080/v1/chat/completions \
  -H "Authorization: Bearer sk-test-key-1" \
  -H "Content-Type: application/json" \
  -d '{"model": "unknown-model", "messages": [{"role": "user", "content": "Hi"}]}'
# 期望：404 + {"error": {"code": 404}}

# 已知模型 → 200（需 inference-service 运行）
curl -s -X POST http://localhost:8080/v1/chat/completions \
  -H "Authorization: Bearer sk-test-key-1" \
  -H "Content-Type: application/json" \
  -d '{"model": "vllm-local", "messages": [{"role": "user", "content": "What is 2+2?"}]}' \
  | python -m json.tool
# 期望：200 + 来自 inference-service 的真实响应
```

**前置条件：** G2 + G1 完成

**完成信号：** 路由到已知模型返回 200，未知模型返回 404

**Cut Line：** 不实现 `/v1/models`、`/v1/completions`

---

## G4: Health + Metrics

**目标文件：**
- `src/ai_gateway/server.py`（修改：`/health` + `/metrics` 端点）

**入口：** 同 G1 启动方式

**验收命令：**
```bash
# /health
curl -s http://localhost:8080/health | python -m json.tool
# 期望：{"status": "healthy", "version": "0.1.0", "upstream_services": {"vllm-local": "healthy"}}

# /metrics
curl -s http://localhost:8080/metrics | grep "ai_gateway_"
# 期望：ai_gateway_requests_total、ai_gateway_request_duration_seconds 等
```

**前置条件：** G1 完成

**完成信号：** `/health` 和 `/metrics` 返回正确格式

**Cut Line：** 不实现自定义业务 metrics

---

## G5: 限流中间件

**目标文件：**
- `src/ai_gateway/middleware/rate_limit.py`
- `src/ai_gateway/server.py`（修改）

**入口：** 同 G1 启动方式

**验收命令：**
```bash
# 快速发 65 个请求（超过 60/minute 限制）
for i in {1..65}; do
  curl -s -o /dev/null -w "%{http_code}\n" \
    -X POST http://localhost:8080/v1/chat/completions \
    -H "Authorization: Bearer sk-test-key-1" \
    -H "Content-Type: application/json" \
    -d '{"model": "vllm-local", "messages": [{"role": "user", "content": "Hi"}]}'
done | tail -5
# 期望：429 (rate limited)
```

**前置条件：** G1 完成

**完成信号：** 超出限制返回 429

**Cut Line：** 不实现 per-user 限流，不实现 Redis 后端

---

## G6: 测试骨架

**目标文件：**
- `tests/__init__.py`
- `tests/conftest.py`
- `tests/test_proxy.py`

**入口：** `pytest tests/ -v`

**验收命令：**
```bash
cd ai-gateway
pytest tests/ -v
# 期望：所有测试通过
```

**前置条件：** G3 完成

**完成信号：** pytest 全部通过

**Cut Line：** 不写集成测试（属于 root integration）

---

Sources:
- T1002: accepted starter manifest
- T1102: fixture assets
- T812: accepted API contract
- T1202: accepted implementation map
