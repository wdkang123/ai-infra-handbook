# inference-service Starter File Manifest

## Task ID: T1001
## Title: inference-service Starter File Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T901 scaffold blueprints（T901 pyproject / run-script / test-fixture / curl catalog），产出 inference-service 源码蓝图文件。

---

# inference-service Starter File Manifest

## 概述

本文档索引 inference-service 的所有 starter file 蓝图，供 Codex 实施时参照。

## 蓝图文件清单

| 序号 | 文件路径（蓝图） | 对应真实文件 | 说明 |
|------|----------------|-------------|------|
| 1 | `T1001-inference-main-py-blueprint-v1.md` | `src/inference_service/main.py` | CLI 入口（Typer） |
| 2 | `T1001-inference-server-py-blueprint-v1.md` | `src/inference_service/server.py` | FastAPI 服务（含 vLLM 集成） |
| 3 | `T1001-inference-config-py-blueprint-v1.md` | `src/inference_service/config.py` | 配置加载（Pydantic + YAML） |
| 4 | `T1001-inference-conftest-py-blueprint-v1.md` | `tests/conftest.py` | pytest fixtures |
| 5 | `T1001-inference-test-api-py-blueprint-v1.md` | `tests/test_api.py` | API 单元测试 |
| 6 | `T1001-inference-serve-sh-blueprint-v2.md` | `scripts/serve.sh` | 服务启动脚本 |

## 源码目录结构（蓝图）

```
inference-service/
├── src/
│   └── inference_service/
│       ├── __init__.py
│       ├── main.py          # CLI 入口（Typer）
│       ├── server.py        # FastAPI 服务
│       ├── config.py        # 配置加载
│       ├── api/
│       │   ├── __init__.py
│       │   ├── chat.py      # /v1/chat/completions
│       │   ├── health.py    # /health
│       │   └── metrics.py   # /metrics
│       └── engines/
│           ├── __init__.py
│           ├── base.py      # 引擎抽象
│           └── vllm_engine.py
├── tests/
│   ├── conftest.py
│   ├── fixtures/
│   │   ├── chat_request.json
│   │   ├── chat_request_stream.json
│   │   ├── invalid_model.json
│   │   └── empty_messages.json
│   ├── test_api.py
│   └── test_engine.py
├── scripts/
│   └── serve.sh
├── pyproject.toml
├── .env.example
└── config.yaml
```

## MVP 必须端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/health` | GET | 健康检查 |
| `/metrics` | GET | Prometheus metrics |
| `/v1/chat/completions` | POST | OpenAI 兼容推理 |

## 与 ai-gateway 集成

- inference-service 作为下游被 ai-gateway 调用
- 端口：`http://localhost:8000/v1`
- 无鉴权（内网通信）

---

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://fastapi.tiangolo.com/ — FastAPI
3. https://typer.tiangolo.com/ — Typer

Risk of Staleness:
- vLLM/OpenAI API 格式可能随版本变化

Out of Scope Kept:
- 未写 SGLang/Triton 引擎实现
- 未写多模型并发
