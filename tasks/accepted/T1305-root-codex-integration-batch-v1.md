# Root Integration Codex Integration Batch v1

## Task ID: T1305
## Title: Root Integration Execution Slice Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# Root Integration Codex Integration Batch

本文档定义根级联调的 Codex 编码批次，以及跨项目交接注意事项。

## 建议批次

**第一批（当前批次）：R1 + R2**

理由：
- Makefile 和开发顺序脚本是根级联调的基础
- 依赖子项目基础服务骨架，但可先写脚本框架

**第二批：R3（冒烟测试）**

理由：需要子项目 S2 + gateway G3 完成才能运行，等待周期长。

**第三批：R4（跨项目 handoff 文档）**

理由：R3 完成后才能验证完整流程。

---

## 第一批文件清单（R1 + R2）

### R1 产出

| 文件 | 说明 | 蓝本 |
|---|---|---|
| `Makefile` | 根级统一入口，`$(MAKE) -C ...` 驱动子项目 | T1005 v2 |

### R2 产出

| 文件 | 说明 | 蓝本 |
|---|---|---|
| `scripts/local_dev_sequence.sh` | 本地开发顺序启动脚本 | T1205 |

---

## 第一批 Handoff Note for Codex

### Makefile 关键设计

1. **子项目调用方式：** 使用 `$(MAKE) -C <subdir>` 模式，不直接执行 shell
2. **共享配置变量：**
   - `MODEL ?= Qwen/Qwen2.5-0.5B-Instruct`
   - `INFERENCE_PORT ?= 8000`
   - `GATEWAY_PORT ?= 8080`
3. **服务端口：**
   - inference-service: `localhost:8000`
   - ai-gateway: `localhost:8080`
   - eval-module: CLI only（不启动 server）
   - finetune-demo: CLI only（不启动 server）
4. **all-serve 顺序：** inference-service 先启动（sleep 30 确保就绪）→ gateway
5. **eval-module / finetune-demo：** 只提供 `eval-install`、`finetune-install` 等安装目标，实际运行通过子项目 Makefile

### 冒烟测试关键设计

1. **测试脚本：** `scripts/integration_smoke_test.sh`
2. **测试依赖：** `tests/fixtures/smoke_expected/` 下的预期输出文件（T1105）
3. **验证方式：** diff actual vs expected，不做模糊匹配
4. **eval-module 评测：** 通过 `make eval-run-mmlu` 调用，需要 inference-service 运行
5. **finetune-demo 训练：** 通过 `make finetune-train` 调用，不启动 server

### 跨项目交接边界

| 子项目 | 交接对象 | 交接内容 |
|---|---|---|
| inference-service | ai-gateway | `http://localhost:8000/v1` 作为下游 |
| inference-service | eval-module | `http://localhost:8000/v1` 作为评测 backend |
| inference-service | finetune-demo | adapter 权重文件，加载到 vLLM |
| ai-gateway | eval-module | `http://localhost:8080/v1` 作为可选入口 |

---

Sources:
- T1005: accepted root makefile blueprint
- T1105: root integration fixture manifest
- T805: cross-project integration prep pack
- T1205: accepted implementation map
