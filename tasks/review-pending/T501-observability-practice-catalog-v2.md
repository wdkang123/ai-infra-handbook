Task ID: T501
Task Title: Observability Long-Run Pack v2
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 T401-practice-catalog-v1，补充更多"从单机到多组件"的最小实践。

Result:

# Observability Practice Catalog v2

## 概述

本目录在 v1 基础上补充更多实践，覆盖从单机单步骤到多组件协同的完整路径。

## 单机单步骤实践（低门槛）

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

**目标**：确认 vLLM 服务暴露的 metrics 格式正确。

```bash
curl http://localhost:8000/metrics
```

来源：https://docs.vllm.ai/

---

### P03：Grafana 导入 vLLM dashboard

**目标**：使用现成 dashboard JSON 快速可视化。

```bash
# Grafana → Dashboards → Import → 上传 vLLM dashboard JSON
```

来源：https://grafana.com/

---

## 单机多步骤实践

---

### P04：用 Langfuse 记录推理全链路

**目标**：从请求到响应全链路可观测。

```python
from langfuse import Langfuse
langfuse = Langfuse()

def call_inference(prompt, model):
    with langfuse.span(name="inference") as span:
        span.set_attribute("model", model)
        # 调用推理服务
        response = call_vllm(prompt, model=model)
        span.set_attribute("tokens", len(response))
        return response
```

来源：https://langfuse.com/docs/observability/overview

---

### P05：通过 Langfuse 查看 token 用量统计

**目标**：在 dashboard 查看各请求的 prompt tokens 和 completion tokens 用量。

来源：https://langfuse.com/docs/observability/overview

---

### P06：OpenTelemetry 自定义 span

**目标**：用 OTel SDK 在自定义推理代码中埋点。

```bash
pip install opentelemetry-api opentelemetry-sdk
```

```python
from opentelemetry import trace
tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("推理调用") as span:
    span.set_attribute("model", "Qwen2.5-0.5B")
    response = call_model("Hello")
```

来源：https://opentelemetry.io/

---

## 多组件协同实践

---

### P07：ai-gateway + Langfuse trace 串联

**目标**：验证请求从 gateway 到 inference-service 的完整 trace 可追踪。

```bash
# 1. 启动 inference-service（Langfuse SDK 集成）
# 2. 启动 ai-gateway
# 3. 通过 gateway 发送请求
curl http://localhost:8080/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{"model": "vllm-local", "messages": [{"role": "user", "content": "test"}]}'

# 4. 在 Langfuse dashboard 查看完整调用链
```

来源：https://langfuse.com/docs/observability/overview

---

### P08：inference-service + Prometheus + Grafana 多组件监控

**目标**：验证 metrics 从 inference-service 到 Grafana 的完整数据流。

```bash
# 1. Prometheus 配置抓取 vLLM metrics
# prometheus.yml:
#   scrape_configs:
#     - job_name: 'vllm'
#       static_configs:
#         - targets: ['localhost:8000']

# 2. 启动 Prometheus
# 3. 启动 Grafana，导入 vLLM dashboard
# 4. 发送测试请求，观察 QPS 和延迟变化
```

来源：https://prometheus.io/
来源：https://grafana.com/

---

### P09：eval-module + Langfuse 评测结果上报

**目标**：验证评测结果可上报 Langfuse 并与推理 trace 关联。

```python
from langfuse import Langfuse
langfuse = Langfuse()

def run_eval_and_report(dataset, model):
    with langfuse.span(name="eval_run") as span:
        result = run_evaluation(dataset, model)
        # 上报评测结果
        span.set_attribute("eval_score", result.score)
        span.set_attribute("dataset", dataset)
        return result
```

来源：https://langfuse.com/docs/observability/overview

---

### P10：OpenTelemetry + Langfuse 端到端追踪

**目标**：用 OTel 采集，Langfuse 作为后端存储和展示。

```python
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc import span_exporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(span_exporter())
)

tracer = trace.get_tracer(__name__)
with tracer.start_as_current_span("推理调用") as span:
    response = call_model("test")
```

来源：https://opentelemetry.io/

---

## 实践分类总览

| 实践 | 分类 | 门槛 | 组件数 |
|------|------|------|-------|
| P01 Langfuse trace | 单机单步骤 | 低 | 1 |
| P02 vLLM metrics | 单机单步骤 | 极低 | 1 |
| P03 Grafana dashboard | 单机单步骤 | 低 | 1 |
| P04 Langfuse 全链路 | 单机多步骤 | 低 | 1 |
| P05 Token 用量统计 | 单机多步骤 | 低 | 1 |
| P06 OTel 自定义 span | 单机多步骤 | 中 | 1 |
| P07 Gateway + Langfuse | 多组件 | 中 | 2 |
| P08 Prometheus + Grafana | 多组件 | 中 | 2 |
| P09 Eval + Langfuse | 多组件 | 中 | 2 |
| P10 OTel + Langfuse | 多组件 | 中 | 2 |

Sources:
1. https://langfuse.com/docs/observability/overview — Langfuse
2. https://docs.vllm.ai/ — vLLM
3. https://grafana.com/ — Grafana
4. https://prometheus.io/ — Prometheus
5. https://opentelemetry.io/ — OpenTelemetry

Risk of Staleness:
- 各工具 SDK 接口更新快，具体以官方文档为准
- Grafana dashboard JSON 可能需要适配新版本

Out of Scope Kept:
- 未写完整监控告警配置
- 未写分布式 tracing 跨服务上下文传递
- 未写数据持久化配置
