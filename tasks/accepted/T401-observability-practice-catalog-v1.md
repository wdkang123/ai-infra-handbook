Task ID: T401
Task Title: Observability Long-Run Pack v1
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 T204/T301/T302，整理 8 个低门槛最小实践，覆盖 tracing、metrics、token usage、dashboard、request logging。

Result:

# Observability Practice Catalog v1

## 概述

本目录整理 8 个低门槛 observability 最小实践，每个实践均可独立完成，无需搭建复杂平台。

## 实践列表

---

### P01：安装 Langfuse 并采集第一个 trace

**目标**：使用 Langfuse Python SDK 在代码中埋点，验证 trace 数据上报成功。

```bash
pip install langfuse
```

```python
from langfuse import Langfuse
langfuse = Langfuse()

def call_model(prompt):
    with langfuse.span(name="llm_call") as span:
        span.input = prompt
        response = call_vllm(prompt)
        span.output = response
        return response
```

来源：https://langfuse.com/docs/observability/overview

---

### P02：访问 vLLM Prometheus metrics 端点

**目标**：确认 vLLM 服务暴露的 metrics 格式正确，可被 Prometheus 抓取。

```bash
# 启动 vLLM
vllm serve Qwen/Qwen2.5-0.5B-Instruct --port 8000

# 获取 metrics（文本格式）
curl http://localhost:8000/metrics

# 关键指标：vllm:num_requests_total、vllm:prompt_tokens_total、vllm:completion_tokens_total
```

来源：https://docs.vllm.ai/

---

### P03：配置 Grafana Dashboard 展示 vLLM QPS 和 P99 Latency

**目标**：使用 Grafana + Prometheus 可视化推理服务的核心指标。

```bash
# 安装 Prometheus 并配置抓取 vLLM metrics
# prometheus.yml 配置：
#   scrape_configs:
#     - job_name: 'vllm'
#       static_configs:
#         - targets: ['localhost:8000']
```

来源：https://grafana.com/
来源：https://prometheus.io/

---

### P04：通过 Langfuse 查看 token 用量统计

**目标**：在 Langfuse dashboard 查看各请求的 prompt tokens 和 completion tokens 用量。

```python
from langfuse import Langfuse
langfuse = Langfuse()

# Langfuse 自动记录 token 用量
response = call_model("Hello")
# 在 dashboard 查看 Usage 标签页
```

来源：https://langfuse.com/docs/observability/overview

---

### P05：Grafana 导入 vLLM metrics dashboard

**目标**：使用现成 dashboard JSON 快速可视化，避免从头配置。

```bash
# 下载 vLLM Grafana dashboard JSON
# 导入到 Grafana：Dashboards → Import → 上传 JSON
# 推荐来源：Grafana Labs 社区 dashboard
```

来源：https://grafana.com/

---

### P06：ai-gateway 记录请求日志

**目标**：通过 ai-gateway 的日志输出确认请求路由和 token 统计正常工作。

```bash
# 启动 ai-gateway（带日志）
ai-gateway serve \
    --port 8080 \
    --models '{"vllm-local": {"base_url": "http://localhost:8000/v1"}}' \
    --log-level info

# 发送请求后查看日志输出
curl http://localhost:8080/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{"model": "vllm-local", "messages": [{"role": "user", "content": "test"}]}'
```

来源：https://github.com/langfuse/langfuse

---

### P07：使用 OpenTelemetry SDK 为推理代码添加 span

**目标**：用 OpenTelemetry Python SDK 在自定义推理代码中埋点。

```bash
pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp
```

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.grpc import span_exporter

trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("推理调用") as span:
    span.set_attribute("model", "Qwen2.5-0.5B")
    response = call_model("Hello")
    span.set_attribute("tokens", len(response))
```

来源：https://opentelemetry.io/

---

### P08：使用 Phoenix（ Arize）采集 LLM trace

**目标**：使用 Phoenix 采集本地 trace 数据，验证 LLM 专用的 span 分析能力。

```bash
pip install arize-phoenix
```

```python
import phoenix as px
px.launch_app()

# Phoenix 自动采集 span
from openinference.instrumentation.langchain import LangChainInstrumentor
LangChainInstrumentor().instrument()
```

来源：https://github.com/Arize-AI/phoenix

---

## 实践分类

| 实践 | 分类 | 工具 | 门槛 |
|------|------|------|------|
| P01 Langfuse trace | tracing | Langfuse | 低（pip + Python） |
| P02 vLLM metrics | metrics | curl | 极低（curl） |
| P03 Grafana Dashboard | metrics 可视化 | Grafana + Prometheus | 中 |
| P04 Langfuse token 用量 | token usage | Langfuse | 低 |
| P05 vLLM Grafana dashboard | metrics 可视化 | Grafana | 低（导入 JSON） |
| P06 ai-gateway 请求日志 | logging | ai-gateway | 低 |
| P07 OTel 自定义 span | tracing | OpenTelemetry | 中 |
| P08 Phoenix trace | tracing | Phoenix | 低（pip + Python） |

Sources:
1. https://langfuse.com/docs/observability/overview — Langfuse
2. https://docs.vllm.ai/ — vLLM
3. https://grafana.com/ — Grafana
4. https://prometheus.io/ — Prometheus
5. https://opentelemetry.io/ — OpenTelemetry
6. https://github.com/Arize-AI/phoenix — Phoenix

Risk of Staleness:
- 各工具 SDK 接口更新快，具体以官方文档为准
- Grafana dashboard JSON 可能需要适配新版本

Out of Scope Kept:
- 未写完整监控告警配置
- 未写分布式 tracing 跨服务上下文传递
- 未写数据持久化配置
