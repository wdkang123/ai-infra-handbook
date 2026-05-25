# Observability Hook Plan v1

## Task ID: T805
## Task Title: Cross-Project Integration Prep Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T714 依赖矩阵，准备可观测性集成计划。

---

# Observability Hook Plan v1

## 概述

本文档定义四个核心模块的可观测性集成计划，包括 metrics、traces、logs 的集成点。

---

## 可观测性分层

| 层次 | 内容 | 模块覆盖 |
|------|------|---------|
| Metrics | Prometheus 指标 | inference-service, ai-gateway |
| Traces | OpenTelemetry | ai-gateway, eval-module |
| Logs | 结构化日志 | 所有模块 |

---

## Metrics 集成

### Prometheus Metrics 端点

| 模块 | 端点 | 端口 | 主要指标 |
|------|------|------|---------|
| inference-service | `/metrics` | 9090 | vllm_num_requests_running, vllm_tokens_total |
| ai-gateway | `/metrics` | 9091 | ai_gateway_requests_total, ai_gateway_tokens_total |

### Prometheus 抓取配置

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'inference-service'
    static_configs:
      - targets: ['localhost:9090']
  - job_name: 'ai-gateway'
    static_configs:
      - targets: ['localhost:9091']
```

---

## Traces 集成

### OpenTelemetry Trace

ai-gateway 作为入口，应生成 root trace。

```
ai-gateway trace（root）
  ↓
inference-service trace（child）
  ↓
响应
```

### Langfuse 集成（可选）

| 模块 | 集成方式 | 说明 |
|------|---------|------|
| ai-gateway | Langfuse SDK 埋点 | token 用量 trace |
| eval-module | Langfuse SDK 埋点 | 评测结果上报（可选） |
| finetune-demo | Langfuse SDK 埋点 | 训练 metrics 上报（可选） |

---

## Logs 集成

### 结构化日志格式

```json
{
  "timestamp": "2026-04-03T12:00:00Z",
  "level": "INFO",
  "module": "inference-service",
  "request_id": "req-xxx",
  "message": "Request completed",
  "duration_ms": 150,
  "model": "Qwen2.5-0.5B-Instruct"
}
```

### 日志收集

| 模块 | 日志位置 | 收集方式 |
|------|---------|---------|
| inference-service | stdout | fluentd/filebeat |
| ai-gateway | stdout | fluentd/filebeat |
| eval-module | file | 本地文件 |
| finetune-demo | file | 本地文件 |

---

## 可观测性集成优先级

| 优先级 | 集成点 | 说明 |
|--------|--------|------|
| P0 | inference-service /metrics | Prometheus 抓取 |
| P0 | ai-gateway /metrics | Prometheus 抓取 |
| P1 | Langfuse tracing（可选） | trace 上报 |
| P2 | Langfuse metrics（可选） | 训练 metrics 上报 |

---

## 集成检查点

- [ ] inference-service `/metrics` 端点可抓取
- [ ] ai-gateway `/metrics` 端点可抓取
- [ ] Prometheus 可抓取所有 metrics
- [ ] Grafana 可展示 metrics（可选）

---

Sources:
1. https://docs.vllm.ai/en/latest/metrics.html — vLLM Metrics
2. https://langfuse.com/docs/observability/overview — Langfuse
3. https://prometheus.io/ — Prometheus

Risk of Staleness:
- 可观测性方案可能因工具版本调整

Out of Scope Kept:
- 未写完整监控告警配置
