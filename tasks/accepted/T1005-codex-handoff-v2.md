# Codex Implementation Handoff Blueprint v2

## Task ID: T1005
## Title: Root / Dev Workflow Starter File Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T905 scaffold（codex-implementation-handoff v1），产出 v2 版本 Codex 交接文档。

---

# Codex Implementation Handoff Blueprint v2

## 概述

本文档定义 MiniMax 向 Codex 交接实施工作的规范 v2，包含输入资产、任务顺序、验收标准。

## 交接资产清单

### T1001 — inference-service Starter File Pack（6 个文件）

| 文件 | 用途 |
|------|------|
| `T1001-inference-starter-manifest.md` | 所有蓝图文件索引 |
| `T1001-inference-main-py-blueprint-v1.md` | CLI 入口蓝图 |
| `T1001-inference-server-py-blueprint-v1.md` | FastAPI 服务蓝图 |
| `T1001-inference-config-py-blueprint-v1.md` | 配置加载蓝图 |
| `T1001-inference-conftest-py-blueprint-v1.md` | pytest fixtures |
| `T1001-inference-test-api-py-blueprint-v1.md` | API 测试蓝图 |
| `T1001-inference-serve-sh-blueprint-v2.md` | 启动脚本 |

加上 T901 scaffold 的 pyproject、.env.example、Makefile、curl catalog。

### T1002 — ai-gateway Starter File Pack（6 个文件）

同上结构，对应 ai-gateway 模块。

### T1003 — eval-module Starter File Pack（6 个文件）

同上结构，对应 eval-module 模块。

### T1004 — finetune-demo Starter File Pack（6 个文件）

同上结构，对应 finetune-demo 模块。

### T1005 — Root / Dev Workflow Starter File Pack（7 个文件）

跨项目工作流脚手架。

---

## Codex 实施顺序（来自 T815）

### 阶段 1：基础设施（T0-01 ~ T0-04）

```
T0-01 → T0-02 → T0-03 → T0-04
```

| 任务 | 输入 | 产出 |
|------|------|------|
| T0-01 | — | `inference-service/`, `ai-gateway/`, `eval-module/`, `finetune-demo/` 目录骨架 |
| T0-02 | T901-T905 scaffold packs | 各模块 `pyproject.toml`、lint/test 配置 |
| T0-03 | — | README.md（各模块） |
| T0-04 | — | `tasks/task-board.md` |

### 阶段 2：inference-service（T1-02 ~ T1-07）

```
T1-02 → T1-05 → T1-06 → T1-03 → T1-07
```

| 任务 | 输入 | 产出 |
|------|------|------|
| T1-02 | T1001 pyproject + main.py | vLLM 集成，`inference-service serve` 可执行 |
| T1-05 | T1001 server.py | `/health` 端点实现 |
| T1-06 | T1001 server.py | `/metrics` 端点实现 |
| T1-03 | T1001 test-api + curl catalog | `/v1/chat/completions` 实现（OpenAI 兼容） |
| T1-07 | T1001 config.py | 模型版本管理 |

### 阶段 3：ai-gateway（T1-08 ~ T1-12）

```
T1-08 → T1-09 → T1-10 → T1-11 → T1-12
```

| 任务 | 输入 | 产出 |
|------|------|------|
| T1-09 | T1002 server.py | 路由逻辑实现 |
| T1-10 | T1002 auth-middleware | 鉴权中间件实现 |
| T1-11 | T1002 server.py | 限流中间件实现 |
| T1-12 | T1002 smoke test | E2E 串联（gateway → inference） |

### 阶段 4：eval-module（T3-02 ~ T3-06）

```
T3-02 → T3-03 → T3-04 → T3-05 → T3-06
```

| 任务 | 输入 | 产出 |
|------|------|------|
| T3-02 | T1003 runner.py | lm-eval 集成 |
| T3-03 | T1003 main.py + test-runner | MMLU benchmark 可运行 |
| T3-04 | T1003 main.py + test-runner | GSM8K benchmark 可运行 |
| T3-05 | T1003 result-store | 结果 JSON 持久化 |
| T3-06 | T1003 result-store + comparator | 历史结果对比 |

### 阶段 5：finetune-demo（T4-02 ~ T4-06）

```
T4-02 → T4-05 → T4-06
```

| 任务 | 输入 | 产出 |
|------|------|------|
| T4-02 | T1004 train.py + test-train | LoRA adapter 可训练 |
| T4-05 | T1004 train.py | adapter 保存/加载 |
| T4-06 | T1004 config-schema | 训练+评测串联 |

---

## 关键验收节点

| 节点 | 验证命令 |
|------|---------|
| inference-service 可启动 | `curl localhost:8000/health` → `{"status":"healthy"}` |
| gateway 可代理 | `curl .../v1/chat/completions -H "Authorization: Bearer dev-gateway-key-1"` → 200 |
| MMLU 可跑 | `eval-module run --task mmlu` → accuracy 分数 |
| LoRA 可训练 | `finetune-demo train --method lora --dataset ./data/train.jsonl` → adapter 产物 |
| 冒烟测试全过 | `bash scripts/integration_smoke_test.sh` → 0 failed |

---

## 禁止事项

- Codex 不得擅自修改目录结构（已由 scaffold manifest 固定）
- Codex 不得删除 MVP 必须端点（/v1/chat/completions, /health, /metrics）
- Codex 不得在未经 MiniMax 确认的情况下添加新依赖
- `/v1/completions` 和 `/v1/models` 暂不实现（已从 MVP 降级）

---

## 交接后 Codex 行动规范

1. 按阶段顺序执行，不跳阶段
2. 每完成一个任务的代码实现，更新 `tasks/task-board.md` 状态
3. 遇到阻塞立即记录到 `BLOCKERS.md`
4. 不确定的地方不要猜，向 MiniMax 提问

---

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval
3. https://github.com/huggingface/peft — PEFT
4. https://github.com/Portkey-AI/gateway — Portkey Gateway

Risk of Staleness:
- 实现顺序可能因实际情况调整（由 MiniMax 决策）

Out of Scope Kept:
- 未写详细人员分工
- 未写 CI/CD 配置
