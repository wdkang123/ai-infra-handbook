Task ID: T702
Task Title: Observability / Evaluation Deep-Research Pack
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
补到10到12个实践条目，兼顾 tracing、metrics、offline eval、benchmark 对照。

Result:

# Observability Practice Catalog v4

## 概述

本文档在 v3 基础上补充更多实践，覆盖 tracing、metrics、offline eval、benchmark 对照，共 12 个实践。

---

## Tracing / Prompt Logging 实践

---

### O01：Langfuse Python SDK 埋点

**目标**：在代码中埋点，验证 trace 数据上报成功。

```bash
pip install langfuse
```

```python
from langfuse import Langfuse
langfuse = Langfuse()

with langfuse.span(name="llm_call") as span:
    span.input = prompt
    response = call_vllm(prompt)
    span.output = response
```

来源：https://langfuse.com/docs/observability/overview

---

### O02：Langfuse + ai-gateway trace 串联

**目标**：验证请求从 gateway 到 inference-service 的完整 trace 可追踪。

```bash
# 通过 gateway 发送请求
curl http://localhost:8080/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{"model": "vllm-local", "messages": [{"role": "user", "content": "test"}]}'

# 在 Langfuse dashboard 查看完整调用链
```

来源：https://langfuse.com/docs/observability/overview

---

### O03：OpenTelemetry 自定义 span

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

## Metrics / Dashboard 实践

---

### O04：访问 vLLM Prometheus metrics 端点

**目标**：确认 vLLM 服务暴露的 metrics 格式正确。

```bash
curl http://localhost:8000/metrics
```

来源：https://docs.vllm.ai/en/latest/metrics.html

---

### O05：Prometheus 抓取 vLLM metrics

**目标**：配置 Prometheus 抓取 inference-service metrics。

```bash
# prometheus.yml:
#   scrape_configs:
#     - job_name: 'vllm'
#       static_configs:
#         - targets: ['localhost:8000']
```

来源：https://prometheus.io/docs/prometheus/latest/getting_started/

---

### O06：Grafana 导入 vLLM dashboard

**目标**：使用现成 dashboard JSON 快速可视化。

```bash
# Grafana → Dashboards → Import → 上传 vLLM dashboard JSON
```

来源：https://grafana.com/

---

### O07：Langfuse 查看 token 用量统计

**目标**：在 dashboard 查看 prompt tokens 和 completion tokens 用量。

```python
langfuse = Langfuse()
# 在 span 中自动记录 token 用量
```

来源：https://langfuse.com/docs/observability/overview

---

## Offline Eval 实践

---

### E01：lm-eval 运行单个 benchmark

**目标**：在标准数据集上跑通评测。

```bash
lm_eval --model vllm \
    --model_args pretrained=your-model-path \
    --tasks mmlu \
    --batch_size 8
```

来源：https://github.com/EleutherAI/lm-evaluation-harness

---

### E02：多 benchmark 综合评测

**目标**：一次运行多个 benchmark。

```bash
lm_eval --model vllm \
    --model_args pretrained=your-model-path \
    --tasks mmlu,gsm8k,humaneval \
    --batch_size 8
```

来源：https://github.com/EleutherAI/lm-evaluation-harness

---

### E03：评测结果 JSON 持久化

**目标**：评测结果持久化，供后续版本对比。

```python
import json
results = evaluator.simple_evaluate(
    model="vllm",
    model_args="pretrained=your-model",
    tasks=["mmlu", "gsm8k"]
)
with open("eval_results.json", "w") as f:
    json.dump(results, f, indent=2)
```

来源：https://github.com/EleutherAI/lm-evaluation-harness

---

## Benchmark 对照实践

---

### E04：对比两个模型的评测结果

**目标**：验证 eval-module 的版本对比能力。

```python
baseline = run_eval(model="baseline-model", tasks=["mmlu"])
candidate = run_eval(model="candidate-model", tasks=["mmlu"])
for task in ["mmlu"]:
    diff = candidate[task] - baseline[task]
    print(f"{task}: {baseline[task]:.4f} → {candidate[task]:.4f} ({diff:+.4f})")
```

来源：https://github.com/EleutherAI/lm-evaluation-harness

---

### E05：Open LLM Leaderboard 查看评测标准

**目标**：了解开源社区 benchmark 评测标准。

```bash
# 浏览器访问
https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard
```

来源：https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard

---

### E06：LLM-as-Judge 主观评测

**目标**：用 GPT-4 作为 Judge 评估模型回复质量。

```python
from langfuse import Langfuse
langfuse = Langfuse()

def judge_with_gpt4(prompt, response):
    judge_result = call_gpt4_judge(prompt, response)
    with langfuse.span(name="judge_eval") as span:
        span.set_attribute("judge_score", judge_result.score)
    return judge_result
```

来源：https://langfuse.com/docs/observability/llm-as-judge

---

## 实践分类总览

| 实践 | 分类 | 门槛 | 组件数 |
|------|------|------|-------|
| O01 Langfuse 埋点 | Tracing | 低 | 1 |
| O02 Gateway + Langfuse trace | Tracing | 中 | 2 |
| O03 OTel 自定义 span | Tracing | 中 | 1 |
| O04 vLLM metrics | Metrics | 极低 | 1 |
| O05 Prometheus 抓取 | Metrics | 低 | 2 |
| O06 Grafana dashboard | Metrics | 低 | 2 |
| O07 Token 用量统计 | Metrics | 低 | 1 |
| E01 lm-eval benchmark | Offline Eval | 低 | 1 |
| E02 多 benchmark 综合 | Offline Eval | 低 | 1 |
| E03 结果持久化 | Offline Eval | 低 | 1 |
| E04 版本对比 | Benchmark 对照 | 低 | 1 |
| E05 Leaderboard 观察 | Benchmark 对照 | 极低 | 1 |
| E06 LLM-as-Judge | Benchmark 对照 | 中 | 2 |

Sources:
1. https://langfuse.com/docs/observability/overview — Langfuse
2. https://docs.vllm.ai/en/latest/metrics.html — vLLM metrics
3. https://prometheus.io/ — Prometheus
4. https://grafana.com/ — Grafana
5. https://opentelemetry.io/ — OpenTelemetry
6. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval
7. https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard — Open LLM Leaderboard
8. https://langfuse.com/docs/observability/llm-as-judge — LLM-as-Judge

Risk of Staleness:
- 各工具 SDK 接口更新快，以官方文档为准

Out of Scope Kept:
- 未写完整监控告警配置
- 未写评测结果数据库持久化
- 未写分布式 tracing 跨服务上下文传递
