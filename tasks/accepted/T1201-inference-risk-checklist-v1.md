# inference-service Risk Checklist v1

## Task ID: T1201
## Title: inference-service Implementation Map Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# inference-service Risk & Blocker Checklist

本文档定义 inference-service 实现过程中的风险点与阻塞检查项，对应 T1201 risk checklist 要求。

## P0 阻塞风险（实施前必须解决）

| Risk | 描述 | 缓解方案 |
|---|---|---|
| **GPU 不可用** | vLLM 必须 GPU 环境，CPU 只能 mock | P1 阶段用 mock engine 验证 FastAPI 骨架，P2 才需要 GPU |
| **vLLM 版本兼容** | vLLM API 在 0.3 → 0.4 有 breaking change | 锁定 `vllm>=0.3,<0.5`，优先用 0.3.x |
| **模型下载失败** | HuggingFace 模型下载超时或 OOM | 提供 `download_model.sh` 脚本，优先用 Qwen2.5-0.5B-Instruct（小模型） |

---

## P1 风险（实施中监控）

| Risk | 描述 | 检测方式 | 缓解 |
|---|---|---|---|
| **FastAPI startup 顺序** | `main.py` startup event 中 engine 未初始化完成 | `/health` 返回 `degraded` 而非 `healthy` | 增加 startup_timeout 等待 |
| **Pydantic v2 兼容性** | `Field()` default 在 v2 有行为变化 | `pip show pydantic` 确认为 v2 | 使用 `Field(default=...)` 而非 `Field(...)` |
| **CORS 未配置** | 浏览器直接调用 `/v1/chat/completions` 会被拦 | 暂时只考虑服务端调用 | 后续 P2 加 CORSMiddleware |
| **端口冲突** | 8000 端口被占用 | 启动前 `lsof -i :8000` 检查 | 提供 `INFERENCE_PORT` 环境变量 |

---

## P2 风险（vLLM Engine 阶段）

| Risk | 描述 | 检测方式 | 缓解 |
|---|---|---|---|
| **GPU OOM** | Qwen2.5-0.5B-Instruct 在 8GB GPU 可加载，但 `gpu_memory_utilization` 过高会 OOM | dmesg \| grep OOM | 初始 `gpu_memory_utilization=0.5`，逐步提高 |
| **AWQ 量化依赖** | AWQ 量化模型需要 `auto-awq` 包，未安装则 fallback 失败 | 检查 `import awq` | pyproject.toml 加 `auto-awq` 依赖 |
| **模型 tokenizer 不匹配** | 本地路径和 HuggingFace ID 路径不一致 | `AutoTokenizer.from_pretrained()` 失败 | 统一用 HuggingFace model id（如 `Qwen/Qwen2.5-0.5B-Instruct`） |
| **流式输出顺序** | `predict_stream` generator 可能在并发下乱序 | SSE 测试验证 chunk 顺序 | 用 `asyncio` 而非 threading |
| **StreamingResponse 未正确终止** | SSE 流可能不发送 `data: [DONE]` | `curl -N` 观察最后一行 | 必须在 generator exhaustion 后发送 `data: [DONE]` |

---

## P3 风险（Metrics 阶段）

| Risk | 描述 | 检测方式 | 缓解 |
|---|---|---|---|
| **Prometheus 多实例** | 多次 import `prometheus_client` 会创建重复 registry | `curl /metrics` 看是否有重复 metric | 全局单例 `MetricsCollector` |
| **vllm_* 指标缺失** | 旧版 vLLM 不暴露某些指标 | `curl /metrics \| grep vllm_` 全空 | 文档注明最低 vLLM 0.3.3 |

---

## 测试阶段风险

| Risk | 描述 | 检测方式 | 缓解 |
|---|---|---|---|
| **httpx AsyncClient fixture** | pytest-asyncio 版本冲突 | `pytest tests/test_api.py` 直接报 | `conftest.py` 固定 `pytest-asyncio>=0.23` |
| **Mock engine 状态残留** | `async_client` fixture 中 engine mock 未正确 reset | 多个 test 之间状态污染 | `conftest.py` 每个 test 前 reset global `_engine` |
| **Fixture 文件路径错误** | `tests/fixtures/` 下文件名与 `conftest.py` 中 `load_fixture()` 路径不匹配 | `pytest tests/test_api.py` FileNotFoundError | fixture 文件名与 T1101 manifest 完全一致 |

---

## Blocker Checklist（实施前检查）

- [ ] GPU 可用：`nvidia-smi` 确认
- [ ] Python ≥ 3.10：`python --version`
- [ ] vLLM 已安装：`python -c "import vllm; print(vllm.__version__)"`
- [ ] 端口 8000 可用：`lsof -i :8000`
- [ ] 模型可下载：`huggingface-cli download Qwen/Qwen2.5-0.5B-Instruct --local-dir ./models/`
- [ ] `pyproject.toml` 依赖已安装：`pip install -e .`

---

## 已知 Open Issues（跟踪）

| Issue | 状态 | 说明 |
|---|---|---|
| BLK-001: vLLM 启动超时 | 已解决 | `startup_timeout=300s` |
| T1005 IT-07: metrics 断言 | 已解决 | `/metrics` 包含 `vllm_` |

---

Sources:
- T1001: server.py blueprint
- T1101: fixture assets
- T301: MVP design
- T811: API contract

Risk of Staleness:
- vLLM breaking changes monitored via version pinning; OOM risks are hardware-specific
