# inference-service Slice Contracts v1

## Task ID: T1301
## Title: inference-service Execution Slice Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# inference-service Slice Contracts

本文档定义每个 slice 的具体目标、入口、验收命令、前置条件和完成信号。

---

## S1: 包骨架 + 配置

**目标文件：**
- `pyproject.toml`
- `src/inference_service/__init__.py`
- `src/inference_service/__version__.py`
- `src/inference_service/config.py`
- `config.yaml`

**入口：** `python -c "from inference_service import config; print('OK')"`

**验收命令：**
```bash
cd inference-service
python -c "from inference_service import config; print('OK')"
```

**前置条件：** 无

**完成信号：** `import inference_service` 无报错，config.yaml 可读

**Cut Line：** 不写 server.py、engine、测试骨架

---

## S2: FastAPI 骨架

**目标文件：**
- `src/inference_service/server.py`
- `src/inference_service/main.py`

**入口：** `python -m inference_service.main`（后台运行）

**验收命令：**
```bash
# 启动
cd inference-service && python -m inference_service.main &
sleep 3

# 健康检查
curl -s http://localhost:8000/health
# 期望：{"status": "healthy", "engine": "mock", ...}

# Mock 推理（不调 engine）
curl -s -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "Qwen2.5-0.5B-Instruct", "messages": [{"role": "user", "content": "Hi"}]}'
# 期望：200 + ChatCompletionsResponse

pkill -f "inference_service.main"
```

**前置条件：** S1 完成

**完成信号：** `/health` 返回 200，`/v1/chat/completions` mock 返回 200

**Cut Line：** 不实现真实 engine，不实现 `/metrics`

---

## S3: vLLM Engine 集成

**目标文件：**
- `src/inference_service/engines/__init__.py`
- `src/inference_service/engines/base.py`
- `src/inference_service/engines/vllm_engine.py`
- `src/inference_service/main.py`（修改：真实 engine 初始化）

**入口：** `MODEL_NAME=Qwen/Qwen2.5-0.5B-Instruct python -m inference_service.main`

**验收命令：**
```bash
cd inference-service && MODEL_NAME=Qwen/Qwen2.5-0.5B-Instruct python -m inference_service.main &
sleep 10

curl -s -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "Qwen2.5-0.5B-Instruct", "messages": [{"role": "user", "content": "What is 2+2?"}]}'
# 期望：200 + 真实 LLM 响应

pkill -f "inference_service.main"
```

**前置条件：** S2 完成

**完成信号：** 非流式推理返回真实 LLM 响应

**Cut Line：** 不实现流式，不实现 `/metrics`

---

## S4: 流式输出

**目标文件：**
- `src/inference_service/server.py`（修改：`_stream_chat`）
- `src/inference_service/engines/vllm_engine.py`（修改：`predict_stream`）

**入口：** 同 S3 启动方式

**验收命令：**
```bash
curl -N -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "Qwen2.5-0.5B-Instruct", "messages": [{"role": "user", "content": "Count to 3"}], "stream": true}' \
  | head -10
# 期望：SSE chunks，Content-Type: text/event-stream
# 最后一行：data: [DONE]
```

**前置条件：** S3 完成

**完成信号：** SSE 格式正确，`data: [DONE]` 结束

**Cut Line：** 不实现 `/v1/completions`、`/v1/models`

---

## S5: Prometheus Metrics

**目标文件：**
- `src/inference_service/api/metrics.py`
- `src/inference_service/server.py`（修改：`/metrics` 端点）

**入口：** S2 启动方式即可，无需真实 engine

**验收命令：**
```bash
curl -s http://localhost:8000/metrics | grep "^vllm_"
# 期望：vllm_num_requests_running、vllm_num_tokens_total 等
```

**前置条件：** S2 完成

**完成信号：** `/metrics` 返回 Prometheus 格式，含 `vllm_` 前缀

**Cut Line：** 不实现自定义业务 metrics（后续扩展）

---

## S6: 测试骨架

**目标文件：**
- `tests/__init__.py`
- `tests/conftest.py`
- `tests/test_api.py`

**入口：** `pytest tests/ -v`

**验收命令：**
```bash
cd inference-service
pytest tests/ -v
# 期望：所有测试通过
```

**前置条件：** S2 完成

**完成信号：** pytest 全部通过

**Cut Line：** 不写集成测试（属于 root integration）

---

Sources:
- T1001: accepted starter manifest
- T1101: fixture assets
- T811: accepted API contract
- T1201: accepted implementation map
