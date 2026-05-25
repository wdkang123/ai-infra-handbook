# inference-service First Codex Batch v1

## Task ID: T1301
## Title: inference-service Execution Slice Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# inference-service First Codex Batch

本文档定义适合第一轮真实 Codex 编码的文件批次。

## 建议批次

**第一批（当前批次）：S1 + S2**

理由：
- 无 GPU 依赖，CPU 可验证
- 独立可测试，不依赖其他 slice
- 覆盖配置层和 FastAPI 骨架，是后续所有 slice 的基础

**第二批：S5（Metrics）**

理由：与 S2 并行，依赖关系简单，可与 S2 同时开发。

**第三批：S6（测试骨架）**

理由：依赖 S2 的 app fixture，S2 完成后可立即开始。

**第四批：S3（vLLM Engine）**

理由：需要 GPU，是第一个真实集成 slice。需 inference-service 先完成 S1/S2。

**第五批：S4（流式输出）**

理由：依赖 S3 的 `predict_stream()` 方法。

---

## 第一批文件清单（S1 + S2）

### S1 产出

| 文件 | 说明 | 蓝本 |
|---|---|---|
| `src/inference_service/__init__.py` | 包声明 | T1001 |
| `src/inference_service/__version__.py` | 版本常量 | T1001 |
| `src/inference_service/config.py` | InferenceConfig dataclass + YAML 加载 | T1001 |
| `config.yaml` | 开发配置样例 | T1001 |
| `config.local.yaml` | 本地配置 | T1001 |
| `config.smoke.yaml` | 冒烟测试配置 | T1001 |
| `pyproject.toml` | 项目元数据 | T1001 |

### S2 产出

| 文件 | 说明 | 蓝本 |
|---|---|---|
| `src/inference_service/server.py` | FastAPI app，含 `/health`、`/v1/chat/completions` mock | T1001 |
| `src/inference_service/main.py` | uvicorn 入口，startup event | T1001 |

---

## 第一批 Handoff Note for Codex

1. **包结构：** `src/inference_service/` 是 Python 包根目录，`main.py` 是 uvicorn 入口
2. **配置：** `config.yaml` 放在项目根目录（不是 `configs/`），由 `config.py` 的 `load_config()` 加载
3. **Server 模式：** `server.py` 提供 `set_engine()` / `get_engine()` 注入函数；`main.py` startup 时注入 mock engine
4. **API 端点：** `/v1/chat/completions` 暂时返回 mock，等 S3 替换为真实 engine
5. **端口：** `localhost:8000`

---

Sources:
- T1001: accepted starter manifest
- T811: accepted API contract
- T1201: accepted implementation map
