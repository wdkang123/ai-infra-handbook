# inference-service Codex Handoff v1

## Task ID: T1401
## Title: inference-service Codex Task Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# inference-service Codex Handoff

本文档是可直接复制给 Codex 的任务卡 handoff 文本。

---

## T1401-T01: 包骨架 + 配置

**任务：** 为 `inference-service/` 创建 Python 包骨架和配置层。

**目录结构：**
```
inference-service/
├── pyproject.toml
├── src/inference_service/
│   ├── __init__.py
│   ├── __version__.py
│   └── config.py
├── config.yaml
├── config.local.yaml
└── config.smoke.yaml
```

**config.py 要求：**
- `load_config()` 返回 `InferenceServiceConfig` Pydantic 对象
- 从 `config.yaml` 加载配置
- 支持环境变量覆盖（`INFERENCE_SERVER__PORT=9000` 等）
- 子配置：`server.ServerConfig`、`engine.EngineConfig`、`vllm.VLLMConfig`、`metrics.MetricsConfig`

**config.yaml 格式：**
```yaml
server:
  host: "0.0.0.0"
  port: 8000
engine:
  type: "vllm"
  model_path: "Qwen/Qwen2.5-0.5B-Instruct"
vllm:
  tensor_parallel_size: 1
  gpu_memory_utilization: 0.9
  max_model_len: 4096
```

**验证命令：**
```bash
cd inference-service
python -c "from inference_service import config; print('OK')"
```

---

## T1401-T02: FastAPI 骨架

**任务：** 实现 `server.py` 和 `main.py`，包含 `/health`、`/v1/chat/completions` mock 端点。

**关键模式：**

1. **server.py** 必须定义：
   - `set_engine(engine)` / `get_engine()` — 全局 engine 注入
   - `HealthResponse` model — 返回 `status`、`engine`、`model`、`gpu_available`
   - `ChatCompletionsRequest` model — Pydantic model
   - `ChatCompletionsResponse` model — OpenAI 兼容响应
   - `/health` GET — 返回 mock HealthResponse
   - `/v1/chat/completions` POST — 返回 mock ChatCompletionsResponse（PLACEHOLDER）

2. **main.py** 必须定义：
   - uvicorn 启动入口
   - startup event 中 `set_engine(mock_engine)`
   - `MODEL_NAME` 环境变量控制模型名

**验收命令：**
```bash
cd inference-service && python -m inference_service.main &
sleep 3
curl -s http://localhost:8000/health
pkill -f "inference_service.main"
```

**禁止事项：**
- 不得实现真实 vLLM engine（属于后续任务）
- 不得实现 `/metrics`（属于后续任务）
- 不得修改端口（必须是 8000）
- 不得添加 `/v1/completions` 或 `/v1/models`（已从 MVP 降级）

---

Sources:
- T1001: accepted starter manifest
- T811: accepted API contract
- T1301: accepted execution slice
