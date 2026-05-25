# inference-service Slice Manifest v1

## Task ID: T1301
## Title: inference-service Execution Slice Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# inference-service Execution Slice Manifest

本文档索引 inference-service 的所有 execution slices，供 Codex 编码时参照。

## Slice 总览

| Slice ID | 名称 | 目标文件 | 验证入口 | 前置条件 |
|---|---|---|---|---|
| S1 | 包骨架 + 配置 | `pyproject.toml / config.py / config.yaml` | `import inference_service` | 无 |
| S2 | FastAPI 骨架 | `server.py / main.py` | `curl localhost:8000/health` | S1 |
| S3 | vLLM Engine 集成 | `engines/vllm_engine.py / engines/base.py` | `POST /v1/chat/completions` 非流式 | S2 |
| S4 | 流式输出 | `server.py` + `engines/vllm_engine.py` | SSE chunk 格式正确 | S3 |
| S5 | Prometheus Metrics | `api/metrics.py / server.py` | `curl localhost:8000/metrics` 含 `vllm_` | S2 |
| S6 | 测试骨架 | `tests/conftest.py / tests/test_api.py` | `pytest tests/` | S2 |

---

## Slice 覆盖范围

| 主线 | 覆盖 Slice |
|---|---|
| 配置层 | S1 |
| FastAPI 骨架 | S2 |
| vLLM Engine | S3, S4 |
| 可观测性 | S5 |
| 测试 | S6 |

---

## Cut Line

以下内容不进入当前 slice 集合：
- `/v1/completions`（后续扩展）
- `/v1/models`（后续扩展）
- SGLang / Triton IS 引擎实现
- 多模型并发

---

Sources:
- T1001: accepted starter manifest
- T1101: fixture assets
- T301: accepted MVP design
- T811: accepted API contract
- T1201: accepted implementation map

Risk of Staleness:
- vLLM API 可能随版本变化，但 engine 抽象接口在 MVP 阶段稳定
