# ai-gateway Risk Checklist v1

## Task ID: T1202
## Title: ai-gateway Implementation Map Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# ai-gateway Risk & Blocker Checklist

本文档定义 ai-gateway 实现过程中的风险点与阻塞检查项。

## P0 阻塞风险

| Risk | 描述 | 缓解方案 |
|---|---|---|
| **下游 inference-service 不可用** | `/v1/chat/completions` 代理依赖下游可用 | P2/P3 阶段用 mock server 或真实 inference-service |
| **端口 8080 冲突** | gateway 默认 8080 | 提供 `GATEWAY_PORT` 环境变量 |
| **slowapi 版本兼容** | slowapi 0.9+ 才有 `RateLimitExceeded` | `pip install slowapi>=0.9,<1.0` |

---

## P1 风险

| Risk | 描述 | 检测方式 | 缓解 |
|---|---|---|---|
| **httpx AsyncClient 未正确关闭** | 代理请求后连接泄漏 | 长时间跑后 `lsof -i :8080` 检查连接数 | 使用 `async with httpx.AsyncClient() as client:` |
| **auth bypass 逻辑反转** | `enabled=True` 时误写成 bypass auth | G03/G04/G06 测试失败即暴露 | 对照 T1002 auth middleware blueprint |
| **router 返回 None 时未抛 404** | `_route_model` 返回 None 但 server.py 没处理 | G07 测试失败即暴露 | router 返回 None → server.py raise HTTPException(404) |

---

## P2 风险

| Risk | 描述 | 检测方式 | 缓解 |
|---|---|---|---|
| **模型名映射丢失** | proxy 转发时把 `vllm-local` 直接透传给下游，但下游期望 `Qwen2.5-0.5B-Instruct` | 检查 `models.yaml` 中 `vllm-local → Qwen/Qwen2.5-0.5B-Instruct` | proxy.py 转发时替换 model name |
| **流式响应透传** | SSE 流式响应 proxy 可能破坏 chunk 格式 | IT-02 smoke 测试观察 SSE 格式 | proxy.py 直接透传 StreamingResponse |
| **X-Forwarded-* headers** | 透传时缺少 client IP 记录 | 检查 headers | proxy.py 添加 `X-Forwarded-For` / `X-Forwarded-Host` |

---

## P3 风险

| Risk | 描述 | 检测方式 | 缓解 |
|---|---|---|---|
| **RPM 限流不准** | slowapi 按 IP 限流，多 client 通过同一 gateway 时误伤 | 多并发压测观察 | per-model RPM 需模型级计数器 |
| **rate limit header 缺失** | 限流后未返回 `X-RateLimit-Remaining` | curl -v 查看 response headers | 加 middleware 添加 header |

---

## 测试阶段风险

| Risk | 描述 | 检测方式 | 缓解 |
|---|---|---|---|
| **auth mock 残留** | `conftest.py` 中 mock auth 返回固定 key，但真实 auth 启用时行为不一致 | pytest `test_auth_*` 失败 | P2 阶段后移除 auth mock |
| **httpx AsyncClient fixture** | `pytest-asyncio` 版本冲突 | `pytest tests/test_proxy.py` 报错 | `pytest-asyncio>=0.23` |
| **integration test 依赖外部服务** | `test_proxy.py` 需要真实 inference-service | 单独跑 `pytest tests/unit/` | 用 `pytest.mark.integration` 分离 |

---

## Blocker Checklist

- [ ] Python ≥ 3.10
- [ ] 端口 8080 可用：`lsof -i :8080`
- [ ] inference-service 可达（用于 P3 端到端测试）：`curl localhost:8000/health`
- [ ] `slowapi>=0.9` 已安装
- [ ] `httpx>=0.27` 已安装
- [ ] `pyproject.toml` 依赖已安装：`pip install -e ai-gateway`

---

Sources:
- T1002: server.py, auth middleware blueprints
- T1102: all fixture files
- T302: accepted MVP design
- T812: API contract

Risk of Staleness:
- Downstream dependency is the main blocker; mitigation is mock server for unit tests
