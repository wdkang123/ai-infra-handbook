# inference-service Repo Layout v1

## Task ID: T801
## Task Title: inference-service Execution Prep Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T301 MVP 设计，准备 inference-service 实施前包。

---

# inference-service Repo Layout v1

## 概述

本文档定义 inference-service 模块的完整目录结构，对应 MVP 实施需求。

---

## 顶层结构

```
inference-service/
├── README.md
├── pyproject.toml
├── config.yaml
├── .env.example
├── src/
│   └── inference_service/
│       ├── __init__.py
│       ├── main.py
│       ├── server.py
│       ├── config.py
│       ├── engines/
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── vllm_engine.py
│       │   ├── sglang_engine.py
│       │   └── triton_engine.py
│       ├── models/
│       │   ├── __init__.py
│       │   └── model_manager.py
│       ├── api/
│       │   ├── __init__.py
│       │   ├── chat.py
│       │   ├── completions.py
│       │   └── models.py
│       ├── metrics.py
│       └── health.py
├── tests/
│   ├── __init__.py
│   ├── test_engine.py
│   ├── test_api.py
│   └── test_integration.py
├── examples/
│   ├── quickstart.py
│   └── streaming.py
└── scripts/
    └── serve.sh
```

---

## 目录说明

### `src/inference_service/`

| 文件 | 说明 |
|------|------|
| `__init__.py` | 包初始化 |
| `main.py` | CLI 入口，`inference-service` 命令定义 |
| `server.py` | FastAPI/Uvicorn 服务主入口 |
| `config.py` | 配置加载（YAML + 环境变量） |
| `engines/` | 推理引擎抽象层 |
| `models/` | 模型生命周期管理 |
| `api/` | OpenAI 兼容 API 路由 |
| `metrics.py` | Prometheus metrics 封装 |
| `health.py` | 健康检查端点 |

### `engines/`

| 文件 | 说明 |
|------|------|
| `base.py` | `BaseEngine` 抽象基类 |
| `vllm_engine.py` | vLLM 引擎适配（默认） |
| `sglang_engine.py` | SGLang 引擎适配 |
| `triton_engine.py` | Triton IS 引擎适配 |

### `api/`

| 文件 | 说明 |
|------|------|
| `chat.py` | `POST /v1/chat/completions` |
| `completions.py` | `POST /v1/completions` |
| `models.py` | `GET /v1/models` |

### `tests/`

| 文件 | 说明 |
|------|------|
| `test_engine.py` | 引擎抽象层单元测试 |
| `test_api.py` | API 端点单元测试 |
| `test_integration.py` | 端到端集成测试 |

### `examples/`

| 文件 | 说明 |
|------|------|
| `quickstart.py` | 快速启动示例 |
| `streaming.py` | 流式输出示例 |

---

## 关键文件内容概要

### `pyproject.toml`

```toml
[project]
name = "inference-service"
version = "0.1.0"
requires-python = ">=3.10"

dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.30.0",
    "vllm>=0.6.0",
    "sglang>=0.1.0; extra == 'sglang'",
    "tritonclient[all]>=3.0.0; extra == 'triton'",
    "prometheus-client>=0.20.0",
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
    "pyyaml>=6.0",
    "httpx>=0.27.0",
]
```

### `config.yaml`

```yaml
server:
  host: "0.0.0.0"
  port: 8000
  workers: 1

engine:
  type: "vllm"  # vllm | sglang | triton
  model_path: "./models/base"
  trust_remote_code: true

vllm:
  tensor_parallel_size: 1
  gpu_memory_utilization: 0.9
  max_model_len: 4096

metrics:
  enabled: true
  port: 9090

health:
  enabled: true
```

### `.env.example`

```bash
# 推理服务配置
INFERENCE_MODEL_PATH=./models/base
INFERENCE_ENGINE_TYPE=vllm

# vLLM 配置
VLLM_HOST=0.0.0.0
VLLM_PORT=8000
VLLM_TENSOR_PARALLEL_SIZE=1
VLLM_GPU_MEMORY_UTILIZATION=0.9

# 健康检查
HEALTH_CHECK_ENABLED=true

# Metrics
METRICS_ENABLED=true
METRICS_PORT=9090
```

---

## 与 MVP 设计（T301）的差异

| 维度 | T301 MVP | T801（本版） |
|------|---------|-------------|
| 目录深度 | 较浅 | 更完整 |
| API 层分离 | 混在 server.py | 独立 `api/` 目录 |
| Config 分离 | 提到有 config | 独立 `config.yaml` |
| 环境变量 | 未提 | 独立 `.env.example` |
| Examples | 未提 | 新增 `examples/` |
| Scripts | 未提 | 新增 `scripts/serve.sh` |

---

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://sglang.readthedocs.io/ — SGLang
3. https://docs.nvidia.com/deeplearning/triton-inference-server/ — Triton IS
4. https://fastapi.tiangolo.com/ — FastAPI

Risk of Staleness:
- 目录结构可能随项目规模调整

Out of Scope Kept:
- 未写 Dockerfile
- 未写 docker-compose
- 未写 K8s 部署文件
