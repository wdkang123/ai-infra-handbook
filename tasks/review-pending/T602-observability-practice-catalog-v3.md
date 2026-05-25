Task ID: T602
Task Title: Observability / Evaluation Zero-Touch Pack
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
整理10到12个低门槛实践：tracing/prompt logging、metrics dashboard、离线评测、benchmark对照、arena观察。

Result:

# Observability Practice Catalog v3

## 概述

本文档在 v2 基础上补充更多低门槛实践，覆盖 tracing/metrics、离线评测、benchmark 对照等场景。

---

## 可观测性实践

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

### O02：访问 vLLM Prometheus metrics 端点

**目标**：确认 vLLM 服务暴露的 metrics 格式正确。

```bash
curl http://localhost:8000/metrics
```

来源：https://docs.vllm.ai/en/latest/metrics.html

---

### O03：Prometheus 抓取 vLLM metrics

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

### O04：Grafana 导入 vLLM dashboard

**目标**：使用现成 dashboard JSON 快速可视化。

```bash
# Grafana → Dashboards → Import → 上传 vLLM dashboard JSON
```

来源：https://grafana.com/

---

### O05：OpenTelemetry 自定义 span

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

### O06：Langfuse 查看 token 用量统计

**目标**：在 dashboard 查看 prompt tokens 和 completion tokens 用量。

```python
langfuse = Langfuse()
# 在 span 中自动记录 token 用量
```

来源：https://langfuse.com/docs/observability/overview

---

## 评测实践

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

### E02：lm-eval + vLLM backend 串联

**目标**：验证 eval-module → inference-service 的评测链路。

```bash
lm_eval --model vllm \
    --model_args base_url=http://inference-service:8000/v1 \
    --tasks mmlu,gsm8k
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
| O01 Langfuse 埋点 | 可观测性 | 低 | 1 |
| O02 vLLM metrics | 可观测性 | 极低 | 1 |
| O03 Prometheus 抓取 | 可观测性 | 低 | 2 |
| O04 Grafana dashboard | 可观测性 | 低 | 2 |
| O05 OTel 自定义 span | 可观测性 | 中 | 1 |
| O06 Token 用量统计 | 可观测性 | 低 | 1 |
| E01 lm-eval benchmark | 评测 | 低 | 1 |
| E02 lm-eval + vLLM | 评测 | 低 | 2 |
| E03 结果持久化 | 评测 | 低 | 1 |
| E04 版本对比 | 评测 | 低 | 1 |
| E05 Leaderboard 观察 | 评测 | 极低 | 1 |
| E06 LLM-as-Judge | 评测 | 中 | 2 |

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
- lm-eval API 可能有版本变化

Out of Scope Kept:
- 未写完整监控告警配置
- 未写评测结果数据库持久化
- 未写分布式 tracing 跨服务上下文传递
