# inference-service Validation Checklist v1

## Task ID: T801
## Task Title: inference-service Execution Prep Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T301 MVP 设计，准备 inference-service 实施前包。

---

# inference-service Validation Checklist v1

## 概述

本文档定义 inference-service 的验收清单，供 Codex 执行后快速验证。

---

## 验收清单总览

| 类别 | 检查项数 | 必须项 |
|------|---------|-------|
| 服务启动 | 5 | 5 |
| API 调用 | 6 | 6 |
| 健康检查 | 3 | 3 |
| Metrics | 3 | 3 |
| 模型加载 | 3 | 3 |
| 配置加载 | 3 | 3 |
| **合计** | **23** | **23** |

---

## 服务启动验收

- [ ] `inference-service serve` 命令可执行
- [ ] 服务监听端口 8000 可访问
- [ ] 无启动报错
- [ ] 日志显示模型加载成功
- [ ] Uvicorn 进程正常运行

---

## API 调用验收

### `/v1/chat/completions`（必须）

- [ ] POST 请求返回 200
- [ ] 响应格式符合 OpenAI 规范
- [ ] 非流式响应 `stream: false` 正常
- [ ] 流式响应 `stream: true` 正常（SSE 格式）
- [ ] `model` 参数正确路由
- [ ] `messages` 格式验证生效

### `/v1/completions`（必须）

- [ ] POST 请求返回 200
- [ ] 响应格式符合 OpenAI 规范
- [ ] `prompt` 参数正确处理

### `/v1/models`（必须）

- [ ] GET 请求返回 200
- [ ] 包含当前加载模型信息

---

## 健康检查验收

- [ ] `GET /health` 返回 200
- [ ] 响应包含 `status: healthy`
- [ ] 响应包含 `engine` 和 `model` 字段

---

## Metrics 验收

- [ ] `GET /metrics` 返回 Prometheus 格式
- [ ] 包含 `vllm_num_requests_running` 指标
- [ ] 包含 `vllm_num_tokens_total` 指标

---

## 模型加载验收

- [ ] Base model 加载成功
- [ ] 推理结果正确（非乱码）
- [ ] 模型切换（通过 config）可用

---

## 配置加载验收

- [ ] `config.yaml` 正确加载
- [ ] 环境变量覆盖 YAML 配置
- [ ] 默认值在配置缺失时生效

---

## 快速验证命令

### 服务启动验证

```bash
# 后台启动服务
inference-service serve \
  --engine vllm \
  --model Qwen/Qwen2.5-0.5B-Instruct \
  --port 8000 &

# 等待 30 秒
sleep 30

# 检查进程
ps aux | grep inference-service
```

### 健康检查

```bash
curl -s http://localhost:8000/health | python -m json.tool
```

预期输出：
```json
{
    "status": "healthy",
    "engine": "vllm",
    "model": "Qwen2.5-0.5B-Instruct",
    "gpu_available": true
}
```

### 基本推理验证

```bash
curl -s -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen2.5-0.5B-Instruct",
    "messages": [{"role": "user", "content": "What is 2+2?"}]
  }' | python -m json.tool
```

预期输出：包含 `choices[0].message.content` 字段。

### Metrics 验证

```bash
curl -s http://localhost:8000/metrics | head -20
```

预期输出：Prometheus 格式文本，包含 `vllm_` 前缀指标。

### 流式推理验证

```bash
curl -s -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen2.5-0.5B-Instruct",
    "messages": [{"role": "user", "content": "Count to 5"}],
    "stream": true
  }'
```

预期输出：SSE 格式流式数据。

---

## 错误场景验证

### 无效模型

```bash
curl -s -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "invalid-model",
    "messages": [{"role": "user", "content": "test"}]
  }'
```

预期：返回 404 错误。

### 空消息

```bash
curl -s -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen2.5-0.5B-Instruct",
    "messages": []
  }'
```

预期：返回 422 validation error。

---

Sources:
1. https://docs.vllm.ai/en/latest/getting_started/quickstart.html — vLLM Quickstart
2. https://docs.vllm.ai/en/latest/serving/health_checks.html — vLLM Health Checks
3. https://docs.vllm.ai/en/latest/metrics.html — vLLM Metrics

Risk of Staleness:
- 验证命令可能因版本更新变化

Out of Scope Kept:
- 未写自动化验收脚本
- 未写错误排查指南
