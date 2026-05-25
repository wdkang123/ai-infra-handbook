# inference-service File Order v1

## Task ID: T1201
## Title: inference-service Implementation Map Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# inference-service File Implementation Order

本文档定义 `inference-service/` 目录的编码实现顺序，基于 accepted `T1001 / T1101 / T301 / T811` blueprints。

## 文件实现顺序

### Phase 0: 最小骨架（无外部依赖）

| Order | 文件路径 | 目的 | 依赖 |
|---|---|---|---|
| 0.1 | `src/__init__.py` | 包声明 | 无 |
| 0.2 | `src/inference_service/__init__.py` | 模块命名空间 | 无 |
| 0.3 | `src/inference_service/__version__.py` | `__version__` | 无 |
| 0.4 | `pyproject.toml` | 项目元数据、依赖 | 无 |
| 0.5 | `.env.example` | 环境变量模板 | 无 |

### Phase 1: 配置层

| Order | 文件路径 | 目的 | 依赖 |
|---|---|---|---|
| 1.1 | `src/inference_service/config.py` | 配置加载（dataclass） | 无 |
| 1.2 | `config.yaml` | 开发配置样例 | 无 |
| 1.3 | `config.local.yaml` | 本地开发配置 | 无 |
| 1.4 | `config.smoke.yaml` | 冒烟测试配置 | 无 |

**实现要点：** `config.py` 定义 `InferenceConfig` dataclass，从 `.env` + `config.yaml` 加载。T1101 的 `T1101-inference-config-example-catalog-v1.md` 为配置文件蓝本。

### Phase 2: FastAPI 应用骨架

| Order | 文件路径 | 目的 | 依赖 |
|---|---|---|---|
| 2.1 | `src/inference_service/server.py` | FastAPI app、路由 | Phase 1 |
| 2.2 | `src/inference_service/main.py` | uvicorn 启动入口 | Phase 1 + 2.1 |

**实现要点：** `server.py` 是 T1001 的核心蓝本，包含 `/health`、`/metrics`、`/v1/chat/completions` 三个端点骨架。`set_engine()` / `get_engine()` 状态注入函数需实现。

### Phase 3: vLLM Engine 集成

| Order | 文件路径 | 目的 | 依赖 |
|---|---|---|---|
| 3.1 | `src/inference_service/engines/__init__.py` | Engines 包 | Phase 2 |
| 3.2 | `src/inference_service/engines/base.py` | 引擎抽象 | Phase 2 |
| 3.3 | `src/inference_service/engines/vllm_engine.py` | VLLMEngine 封装 | Phase 2 |
| 3.4 | `main.py` 修改：调用 `set_engine()` | 注入 engine | Phase 3.3 + 2.2 |

**实现要点：** vLLM engine 初始化在 `main.py` startup event 中调用。`VLLMEngine.predict()` 和 `predict_stream()` 方法需实现，对应 T1101 fixture 中的 SSE chunk 格式。

### Phase 4: 指标与可观测性

| Order | 文件路径 | 目的 | 依赖 |
|---|---|---|---|
| 4.1 | `src/inference_service/api/metrics.py` | Prometheus metrics 端点 | Phase 2 |
| 4.2 | `src/inference_service/server.py` 修改：挂载 `/metrics` | Prometheus 输出 | Phase 4.1 |

**实现要点：** `metrics.py` 封装 vLLM 原生指标 + `inference_service_*` 自定义指标，对应 T1101 `metrics_idle_state.txt` / `metrics_active_workload.txt` fixture。

### Phase 5: 测试骨架

| Order | 文件路径 | 目的 | 依赖 |
|---|---|---|---|
| 5.1 | `tests/__init__.py` | 测试包 | 无 |
| 5.2 | `tests/conftest.py` | pytest fixtures：`async_client`、`mock_vllm_response` | Phase 2 |
| 5.3 | `tests/test_api.py` | API 端点测试 | Phase 2 + 5.2 |
| 5.4 | `tests/fixtures/` | fixture 文件 | Phase 5.2 |

**实现要点：** `tests/test_api.py` 骨架来自 T1001 `T1001-inference-test-api-py-blueprint-v1.md`，fixture 文件来自 T1101 `T1101-inference-request-fixtures-v1.md`。

### Phase 6: 服务脚本

| Order | 文件路径 | 目的 | 依赖 |
|---|---|---|---|
| 6.1 | `scripts/serve.sh` | 本地启动脚本 | Phase 3 |
| 6.2 | `scripts/download_model.sh` | 模型下载脚本 | 无 |

---

## 目录结构

```
inference-service/
├── src/inference_service/
│   ├── __init__.py
│   ├── __version__.py
│   ├── config.py          ← Phase 1
│   ├── server.py          ← Phase 2
│   ├── main.py            ← Phase 2/3
│   ├── api/
│   │   ├── __init__.py
│   │   ├── chat.py        ← Phase 2 (/v1/chat/completions)
│   │   ├── health.py      ← Phase 2 (/health)
│   │   └── metrics.py     ← Phase 4 (/metrics)
│   └── engines/
│       ├── __init__.py
│       ├── base.py        ← Phase 3
│       └── vllm_engine.py ← Phase 3
├── config.yaml           ← Phase 1
├── config.local.yaml     ← Phase 1
├── config.smoke.yaml     ← Phase 1
├── scripts/
│   ├── serve.sh           ← Phase 6
│   └── download_model.sh  ← Phase 6
├── tests/
│   ├── __init__.py
│   ├── conftest.py        ← Phase 5
│   ├── test_api.py       ← Phase 5
│   └── fixtures/          ← Phase 5
├── pyproject.toml         ← Phase 0
└── .env.example           ← Phase 0
```

---

## 编码阻塞点

| 文件 | 阻塞原因 | 解法 |
|---|---|---|
| `server.py` (Phase 2) | 需要 `config.py` 中的模型名、端口等 | Phase 1 先完成 |
| `main.py` (Phase 3) | 需要 `vllm_engine.py` 实例化 | Phase 3.2 先完成 |
| `tests/conftest.py` (Phase 5) | 需要 `server.py` app 注入 mock engine | Phase 2 先完成 |

---

Sources:
- T1001: accepted starter blueprint (server.py)
- T1101: fixture assets
- T301: accepted MVP design
- T811: accepted API contract

Risk of Staleness:
- Phase ordering follows standard FastAPI + vLLM project structure; stable
