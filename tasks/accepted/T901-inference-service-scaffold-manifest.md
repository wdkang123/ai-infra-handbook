# inference-service Scaffold Manifest

## Task ID: T901
## Title: inference-service Scaffold Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T801 repo layout、API contract（已收紧为 T811）、config surface、test plan、validation checklist，产出脚手架输入模板。

---

# inference-service Scaffold Manifest

## 概述

本文档定义 inference-service 脚手架的输入清单，包含所有待 Codex 实现的文件蓝图。

## 脚手架文件清单

| 序号 | 文件路径（蓝图） | 对应 src 文件 | 说明 |
|------|----------------|--------------|------|
| 1 | `inference-service/pyproject.toml` | `pyproject.toml` | 项目元数据和依赖 |
| 2 | `inference-service/.env.example` | `.env.example` | 环境变量模板 |
| 3 | `inference-service/Makefile` | `Makefile` | 构建和启动入口 |
| 4 | `inference-service/scripts/serve.sh` | `scripts/serve.sh` | 服务启动脚本 |
| 5 | `inference-service/tests/conftest.py` | `tests/conftest.py` | pytest fixture |
| 6 | `inference-service/tests/fixtures/chat_request.json` | `tests/fixtures/` | 测试请求 fixture |
| 7 | `inference-service/examples/curl_catalog.sh` | `examples/curl_catalog.sh` | curl 命令合集 |

## pyproject.toml 依赖组

基础依赖已在 `[project.dependencies]`，安装即包含核心运行时。

| 组名 | 依赖 | 用途 |
|------|------|------|
| `sglang` | sglang>=0.1.0 | SGLang 引擎支持（可选） |
| `triton` | tritonclient[all]>=3.0.0 | Triton IS 支持（可选） |
| `test` | pytest, pytest-asyncio, pytest-cov, httpx, pytest-mock | 测试 |
| `dev` | ruff, mypy, pre-commit | 开发工具 |

## 关键 CLI 入口

```bash
# 安装（从 inference-service/ 目录执行）
pip install -e "."

# 安装带可选依赖
pip install -e ".[sglang]"
pip install -e ".[triton]"

# 开发安装
pip install -e ".[test,dev]"

# 启动服务
inference-service serve --engine vllm --model Qwen/Qwen2.5-0.5B-Instruct

# 运行测试
pytest tests/ -v
```

## 目录结构（蓝图）

```
inference-service/
├── pyproject.toml
├── .env.example
├── Makefile
├── config.yaml
├── src/
│   └── inference_service/
│       ├── __init__.py
│       ├── main.py          # CLI 入口
│       ├── server.py        # FastAPI app
│       ├── config.py        # 配置加载
│       ├── engines/
│       │   ├── base.py
│       │   └── vllm_engine.py
│       ├── models/
│       │   └── model_manager.py
│       ├── api/
│       │   └── chat.py
│       ├── metrics.py
│       └── health.py
├── tests/
│   ├── conftest.py
│   ├── fixtures/
│   │   └── chat_request.json
│   ├── test_engine.py
│   └── test_api.py
├── examples/
│   └── curl_catalog.sh
└── scripts/
    └── serve.sh
```

## 服务端口约定

| 端口 | 用途 | 环境变量 |
|------|------|---------|
| `8000` | HTTP API | `INFERENCE_PORT` |
| `9090` | Prometheus metrics | `METRICS_PORT` |

## 与 ai-gateway 的集成点

- ai-gateway 的 `models[].base_url` 需指向 `http://localhost:8000/v1`
- inference-service 不直接处理 auth，由 ai-gateway 负责

## 关键实现里程碑

| 里程碑 | 产出 | 验证文件 |
|--------|------|---------|
| M1: 服务可启动 | Uvicorn 进程在 8000 端口监听 | `curl localhost:8000/health` |
| M2: 基本推理 | `/v1/chat/completions` 返回 OpenAI 格式 | `examples/curl_catalog.sh` |
| M3: 健康检查 | `/health` 返回 engine/model 信息 | T801 validation checklist |
| M4: Metrics | `/metrics` 返回 Prometheus 格式 | T801 validation checklist |

---

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://fastapi.tiangolo.com/ — FastAPI
3. https://docs.vllm.ai/en/latest/serving/health_checks.html — vLLM Health Checks
4. https://docs.vllm.ai/en/latest/metrics.html — vLLM Metrics

Risk of Staleness:
- vLLM/FastAPI 版本更新可能改变依赖版本

Out of Scope Kept:
- 未写 Dockerfile
- 未写 K8s 部署
