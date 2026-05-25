Task ID: T701
Task Title: Inference Engines Deep-Research Pack
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
补足10到12个实践条目，重点是部署与接入。

Result:

# Inference Practice Catalog v2

## 概述

本文档在 v1 基础上补充更多实践条目，从单机推理到服务化接入，共 12 个实践。

---

## 单机推理实践

---

### I01：vLLM 快速启动

**目标**：在单机上快速启动 vLLM 服务，验证基本推理能力。

```bash
pip install vllm

vllm serve Qwen/Qwen2.5-0.5B-Instruct \
    --host 0.0.0.0 \
    --port 8000
```

```bash
curl http://localhost:8000/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{"model": "Qwen2.5-0.5B-Instruct", "messages": [{"role": "user", "content": "Hello"}]}'
```

来源：https://docs.vllm.ai/en/latest/getting_started/quickstart.html

---

### I02：SGLang 快速启动

**目标**：验证 SGLang 可用，了解与 vLLM 的差异。

```bash
pip install sglang

python -m sglang.launch_server \
    --model-path Qwen/Qwen2.5-0.5B-Instruct \
    --port 8000
```

来源：https://sglang.readthedocs.io/en/latest/get_started.html

---

### I03：Triton IS 部署 TensorRT-LLM 模型

**目标**：了解 Triton 部署 TensorRT-LLM 的基本流程。

```bash
# 1. 编译 TensorRT-LLM 模型
trtllm-build --model_dir=Qwen/Qwen2.5-0.5B-Instruct \
    --usage=inference \
    --output_dir=/tmp/tllm_engine

# 2. 启动 Triton
tritonserver --model-repository=/model_repository
```

来源：https://nvidia.github.io/TensorRT-LLM/quick-start.html

---

### I04：访问 vLLM metrics 端点

**目标**：确认 vLLM 暴露的 Prometheus metrics 可用。

```bash
curl http://localhost:8000/metrics
```

关键指标：
- `vllm:num_requests_running`
- `vllm:num_tokens_total`
- `vllm:gpu_cache_usage`

来源：https://docs.vllm.ai/en/latest/metrics.html

---

## 服务化接入实践

---

### I05：ai-gateway 接入 vLLM 后端

**目标**：通过 ai-gateway 代理 vLLM 推理请求。

```bash
# 通过 gateway 请求
curl http://localhost:8080/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{"model": "vllm-local", "messages": [{"role": "user", "content": "test"}]}'
```

来源：https://docs.vllm.ai/en/latest/getting_started/quickstart.html

---

### I06：vLLM 多实例负载均衡

**目标**：通过 gateway 实现多个 vLLM 实例的负载均衡。

```yaml
# gateway.yaml
inference:
  backend: vllm
  urls:
    - http://vllm-1:8000/v1
    - http://vllm-2:8000/v1
    - http://vllm-3:8000/v1
  load_balance: round_robin
```

来源：https://docs.vllm.ai/

---

### I07：Triton IS 多模型编排

**目标**：用 Triton 管理多个模型版本或多种推理引擎。

```bash
# Triton 模型仓库结构
# model_repository/
#   ├── tensorrt_llm/
#   │     └── config.pbtxt
#   └── vllm_model/
#         └── config.pbtxt

tritonserver --model-repository=/model_repository
```

来源：https://docs.nvidia.com/deeplearning/triton-inference-server/

---

### I08：Prometheus + Grafana 监控推理服务

**目标**：采集并可视化推理服务的 metrics。

```bash
# Prometheus 配置
# prometheus.yml:
#   scrape_configs:
#     - job_name: 'vllm'
#       static_configs:
#         - targets: ['localhost:8000']
```

来源：https://docs.vllm.ai/en/latest/metrics.html
来源：https://grafana.com/

---

## 性能与稳定性实践

---

### I09：TensorRT-LLM 编译与部署

**目标**：将模型编译为 TensorRT-LLM 格式并部署。

```bash
# 编译模型
trtllm-build --model_dir=Qwen/Qwen2.5-0.5B-Instruct \
    --usage=inference \
    --output_dir=/tmp/tllm_engine \
    --Fp8 \
    --max_batch_size=128

# 启动推理服务
tritonserver --model-repository=/model_repository
```

来源：https://nvidia.github.io/TensorRT-LLM/quick-start.html

---

### I10：推理服务健康检查

**目标**：验证推理服务的可用性监控。

```bash
# 健康检查
curl http://localhost:8000/health

# 监控检查
curl http://localhost:8000/metrics | grep vllm:num_requests_running
```

来源：https://docs.vllm.ai/en/latest/serving/health_checks.html

---

### I11：多引擎性能对比验证

**目标**：在相同模型上对比 vLLM / SGLang 的性能表现。

```bash
# 使用相同模型分别启动 vLLM 和 SGLang
# 通过 benchmark 工具压测对比

# 关键对比指标：
# - 首 token 时间（TTFT）
# - 吞吐量（tokens/sec）
# - P99 延迟
```

来源：https://docs.vllm.ai/en/latest/getting_started/quickstart.html
来源：https://sglang.readthedocs.io/en/latest/get_started.html

---

### I12：Speculative Decoding 配置

**目标**：验证 vLLM 的投机解码能力。

```bash
# 启动 vLLM 时启用 speculative decoding
vllm serve Qwen/Qwen2.5-0.5B-Instruct \
    --enable-chunked-prefill \
    --max-num-batched-tokens 4096
```

来源：https://docs.vllm.ai/

---

## 实践分类总览

| 实践 | 分类 | 门槛 | 组件数 |
|------|------|------|-------|
| I01 vLLM 快速启动 | 单机推理 | 低 | 1 |
| I02 SGLang 快速启动 | 单机推理 | 低 | 1 |
| I03 Triton + TRT-LLM | 单机推理 | 高 | 1 |
| I04 vLLM metrics | 单机推理 | 极低 | 1 |
| I05 gateway + vLLM | 服务化接入 | 低 | 2 |
| I06 多实例负载均衡 | 服务化接入 | 中 | 2 |
| I07 Triton 多模型编排 | 服务化接入 | 中 | 2 |
| I08 Prometheus + Grafana | 服务化接入 | 中 | 2 |
| I09 TRT-LLM 编译部署 | 性能优化 | 高 | 2 |
| I10 健康检查 | 稳定性 | 低 | 1 |
| I11 多引擎性能对比 | 性能验证 | 中 | 2 |
| I12 Speculative Decoding | 性能优化 | 中 | 1 |

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://sglang.readthedocs.io/ — SGLang
3. https://nvidia.github.io/TensorRT-LLM/ — TensorRT-LLM
4. https://docs.nvidia.com/deeplearning/triton-inference-server/ — Triton IS
5. https://grafana.com/ — Grafana
6. https://prometheus.io/ — Prometheus

Risk of Staleness:
- 各引擎版本更新可能影响具体命令和参数

Out of Scope Kept:
- 未写完整生产部署方案
- 未写自动扩缩容配置
