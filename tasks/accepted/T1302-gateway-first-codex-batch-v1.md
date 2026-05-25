# ai-gateway First Codex Batch v1

## Task ID: T1302
## Title: ai-gateway Execution Slice Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# ai-gateway First Codex Batch

本文档定义适合第一轮真实 Codex 编码的文件批次。

## 建议批次

**第一批（当前批次）：G1 + G4**

理由：
- 无外部依赖（不需要 inference-service 运行）
- 独立可验证
- G4 的 `/health` + `/metrics` 可在 CPU 环境完成

**第二批：G2（鉴权中间件）**

理由：独立于 router，可单独开发和测试。

**第三批：G5（限流）**

理由：与 G2 并行开发，独立于路由逻辑。

**第四批：G3（路由 + 代理）**

理由：需要 inference-service 端到端验证，G2 是其前置依赖。

**第五批：G6（测试骨架）**

理由：依赖 G3 完成后。

---

## 第一批文件清单（G1 + G4）

### G1 产出

| 文件 | 说明 | 蓝本 |
|---|---|---|
| `src/ai_gateway/__init__.py` | 包声明 | T1002 |
| `src/ai_gateway/__version__.py` | 版本常量 | T1002 |
| `src/ai_gateway/config.py` | AiGatewayConfig dataclass + YAML 加载 | T1002 |
| `configs/models.yaml` | 路由配置样例 | T1002 |
| `configs/config.yaml` | 完整配置样例 | T1002 |
| `pyproject.toml` | 项目元数据 | T1002 |

### G4 产出

| 文件 | 说明 | 蓝本 |
|---|---|---|
| `src/ai_gateway/server.py` | FastAPI app，`/health` 和 `/metrics` 端点 | T1002 |
| `src/ai_gateway/main.py` | uvicorn 入口 | T1002 |

---

## 第一批 Handoff Note for Codex

1. **包结构：** `src/ai_gateway/` 是 Python 包根目录
2. **配置加载：** `config.py` 从 `configs/models.yaml` 和 `configs/config.yaml` 加载
3. **端口：** `localhost:8080`
4. **api_keys：** 测试用 `dev-gateway-key-1`（来自 accepted T1002 blueprint）
5. **AuthMiddleware：** 当前批次 G4 暂不实现 auth middleware，G2 实现时在 server.py 中替换 `verify_bearer_token` mock 为真实实现
6. **路由：** 当前批次 G4 `/v1/chat/completions` 返回 mock，等 G3 实现时替换为真实路由

---

Sources:
- T1002: accepted starter manifest
- T812: accepted API contract
- T1202: accepted implementation map
