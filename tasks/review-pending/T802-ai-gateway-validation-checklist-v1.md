# ai-gateway Validation Checklist v1

## Task ID: T802
## Task Title: ai-gateway Execution Prep Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T302 MVP 设计，准备 ai-gateway 实施前包。

---

# ai-gateway Validation Checklist v1

## 概述

本文档定义 ai-gateway 的验收清单，供 Codex 执行后快速验证。

---

## 验收清单总览

| 类别 | 检查项数 | 必须项 |
|------|---------|-------|
| 服务启动 | 4 | 4 |
| 代理功能 | 6 | 6 |
| 鉴权 | 4 | 4 |
| 限流 | 4 | 4 |
| 计量 | 3 | 3 |
| 健康检查 | 2 | 2 |
| Metrics | 2 | 2 |
| **合计** | **25** | **25** |

---

## 服务启动验收

- [ ] `ai-gateway serve` 命令可执行
- [ ] 服务监听端口 8080 可访问
- [ ] 无启动报错
- [ ] 日志显示配置加载成功

---

## 代理功能验收

### 基本代理（必须）

- [ ] `POST /v1/chat/completions` 代理成功
- [ ] `POST /v1/completions` 代理成功
- [ ] 响应格式与下游一致
- [ ] 流式输出（SSE）正常透传
- [ ] 404 时的错误响应正确
- [ ] 502 时的错误响应正确（下游不可用）

---

## 鉴权验收（必须）

- [ ] 有效 Bearer token 请求通过
- [ ] 无 Authorization header 返回 401
- [ ] 无效 token 返回 401
- [ ] Auth disable 时无 token 也通过

---

## 限流验收（必须）

- [ ] RPM 内请求通过
- [ ] 超出 RPM 返回 429
- [ ] 限流响应头正确（`X-RateLimit-*`）
- [ ] Per-model RPM 分别计数

---

## 计量验收（必须）

- [ ] 每个请求的 `requests_total` +1
- [ ] `tokens_total` 正确累加（从下游响应提取）
- [ ] `duration_seconds` 正确记录

---

## 健康检查验收

- [ ] `GET /health` 返回 200
- [ ] 响应包含 `status` 和 `version`

---

## Metrics 验收

- [ ] `GET /metrics` 返回 Prometheus 格式
- [ ] 包含 `ai_gateway_requests_total` 指标

---

## 快速验证命令

### 服务启动验证

```bash
# 1. 启动 inference-service（如未启动）
# inference-service serve --engine vllm --model Qwen/Qwen2.5-0.5B-Instruct &

# 2. 启动 gateway
ai-gateway serve --port 8080 &

# 3. 等待启动
sleep 10

# 4. 检查进程
ps aux | grep ai-gateway
```

### 健康检查

```bash
curl -s http://localhost:8080/health | python -m json.tool
```

预期输出：
```json
{
    "status": "healthy",
    "version": "0.1.0",
    "upstream_services": {
        "vllm-local": "healthy"
    }
}
```

### 基本代理验证

```bash
# 成功请求
curl -s -X POST http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer dev-gateway-key-1" \
  -d '{"model":"vllm-local","messages":[{"role":"user","content":"Hello"}]}' | python -m json.tool

# 无 auth 请求（预期 401）
curl -s -X POST http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"vllm-local","messages":[{"role":"user","content":"Hello"}]}'
```

### 限流验证

```bash
# 连续发送超过 RPM 的请求
for i in {1..65}; do
  curl -s -o /dev/null -w "%{http_code}\n" \
    -X POST http://localhost:8080/v1/chat/completions \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer dev-gateway-key-1" \
    -d '{"model":"vllm-local","messages":[{"role":"user","content":"test"}]}'
done
```

预期：大部分返回 200，最后几个返回 429。

### Metrics 验证

```bash
curl -s http://localhost:8080/metrics | grep ai_gateway
```

---

Sources:
1. https://github.com/Portkey-AI/gateway — Portkey Gateway
2. https://github.com/BerriAI/litellm — LiteLLM

Risk of Staleness:
- 验证命令可能因版本更新变化

Out of Scope Kept:
- 未写自动化验收脚本
- 未写错误排查指南
