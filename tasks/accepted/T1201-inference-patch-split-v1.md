# inference-service Patch Split v1

## Task ID: T1201
## Title: inference-service Implementation Map Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# inference-service Patch Split Proposal

本文档定义 inference-service 的分批实现顺序，每批可独立验证，覆盖 T1201 的 patch split 要求。

## Patch 批次概览

| Patch | 名称 | 目标文件 | 验证方式 |
|---|---|---|---|
| P0 | 骨架 + 配置 | `pyproject.toml / config.py` | `import inference_service` |
| P1 | FastAPI 骨架 | `server.py / main.py` | `curl localhost:8000/health` 返回 200 |
| P2 | vLLM Engine | `engines/vllm_engine.py / engines/base.py` | `POST /v1/chat/completions` 非流式返回 |
| P3 | 流式输出 | `server.py`（`_stream_chat`） | SSE chunk 格式正确 |
| P4 | Prometheus Metrics | `api/metrics.py / server.py` | `curl localhost:8000/metrics` 含 `vllm_` |
| P5 | 测试骨架 | `tests/conftest.py / tests/test_api.py` | `pytest tests/` 全部通过 |

---

## Patch 0: 项目骨架

**文件：**
- `pyproject.toml`
- `src/inference_service/__init__.py`
- `src/inference_service/__version__.py`
- `src/inference_service/config.py`

**验证：**
```bash
cd inference-service
python -c "from inference_service import config; print('OK')"
```

**产出：** 可导入的 Python 包，配置和模型类定义完毕。

---

## Patch 1: FastAPI 骨架

**文件：**
- `src/inference_service/server.py`（骨架，engine 用 mock）
- `src/inference_service/main.py`

**实现要点：**
- 实现 `set_engine()` / `get_engine()` 状态函数
- `/health` 返回 mock `HealthResponse`
- `/v1/chat/completions` 返回 mock `ChatCompletionsResponse`（不调 engine）
- `main.py` startup 调用 `set_engine(mock_engine)`

**验证：**
```bash
# 启动服务
cd inference-service && python -m inference_service.main &

# 健康检查
curl -s http://localhost:8000/health | python -m json.tool
# 期望：{"status": "healthy", "engine": "mock", ...}

# 推理（mock 响应）
curl -s -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "Qwen2.5-0.5B-Instruct", "messages": [{"role": "user", "content": "Hi"}]}' \
  | python -m json.tool
# 期望：200 + mock ChatCompletionsResponse

# 停止
pkill -f "inference_service.main"
```

---

## Patch 2: vLLM Engine 集成

**文件：**
- `src/inference_service/engines/__init__.py`
- `src/inference_service/engines/base.py`
- `src/inference_service/engines/vllm_engine.py`
- `src/inference_service/main.py`（修改：真实 engine）

**实现要点：**
- `VLLMEngine` 封装 `vllm.LLM`
- `predict()` → 非流式推理
- `predict_stream()` → 生成器，逐 token yield
- `main.py` startup 创建真实 engine 并 `set_engine()`

**验证：**
```bash
cd inference-service && MODEL_NAME=Qwen/Qwen2.5-0.5B-Instruct python -m inference_service.main &

# 非流式推理（需 GPU 环境）
curl -s -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "Qwen2.5-0.5B-Instruct", "messages": [{"role": "user", "content": "What is 2+2?"}]}' \
  | python -m json.tool
# 期望：200 + 真实 LLM 响应

pkill -f "inference_service.main"
```

---

## Patch 3: 流式输出

**文件：**
- `src/inference_service/server.py`（修改：`_stream_chat` 实现）
- `src/inference_service/engines/vllm_engine.py`（修改：`predict_stream`）

**验证：**
```bash
curl -N -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "Qwen2.5-0.5B-Instruct", "messages": [{"role": "user", "content": "Count to 3"}], "stream": true}' \
  | head -10
# 期望：SSE chunks，Content-Type: text/event-stream
# 最后一行：data: [DONE]
```

对应 T1101 SSE fixture: `T1101-inference-stream-sse-samples-v1.md`

---

## Patch 4: Prometheus Metrics

**文件：**
- `src/inference_service/api/metrics.py`
- `src/inference_service/server.py`（修改：`/metrics` 端点实现）

**验证：**
```bash
curl -s http://localhost:8000/metrics | grep "^vllm_"
# 期望：vllm_num_requests_running、vllm_num_tokens_total 等
```

对应 T1101 `metrics_idle_state.txt` / `metrics_active_workload.txt` fixtures。

---

## Patch 5: 测试骨架

**文件：**
- `tests/__init__.py`
- `tests/conftest.py`
- `tests/test_api.py`
- `tests/fixtures/`

**验证：**
```bash
cd inference-service
pytest tests/ -v
# 期望：所有测试通过（T1001 test_api.py fixture 为验收标准）
```

---

## Patch 依赖关系图

```
P0 (骨架)
  │
  └── P1 (FastAPI 骨架)
          │
          ├── P2 (vLLM Engine)          ← P1 的 /v1/chat/completions 用 mock，P2 替换为真实
          │       │
          │       └── P3 (流式输出)     ← 依赖 P2 的 predict_stream
          │
          ├── P4 (Prometheus Metrics)   ← 与 P2/P3 并行
          │
          └── P5 (测试骨架)             ← 依赖 P1 骨架完整
```

**注意：** P2（vLLM Engine）是唯一需要真实 GPU 的 patch，其余均可 CPU 测试。

---

Sources:
- T1001: server.py blueprint
- T1101: fixture assets
- T301: MVP design

Risk of Staleness:
- Patch ordering follows standard vLLM + FastAPI project convention; stable
