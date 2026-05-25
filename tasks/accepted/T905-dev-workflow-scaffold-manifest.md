# Developer Workflow Scaffold Manifest

## Task ID: T905
## Title: Developer Workflow Scaffold Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T815 implementation order（已收紧）、T805 integration test matrix、e2e scenario map、shared config boundary、mvp sequencing board，产出跨项目开发工作流脚手架。

---

# Developer Workflow Scaffold Manifest

## 概述

本文档定义跨项目开发工作流的脚手架输入清单。

## 脚手架文件清单

| 序号 | 文件路径（蓝图） | 对应文件 | 说明 |
|------|----------------|----------|------|
| 1 | `ai-infra/Makefile` | `Makefile` (root) | 根目录 Makefile |
| 2 | `ai-infra/.env.example` | `.env.example` (root) | 共享环境变量模板 |
| 3 | `ai-infra/scripts/local_dev_sequence.sh` | `scripts/local_dev_sequence.sh` | 本地开发顺序脚本 |
| 4 | `ai-infra/scripts/integration_smoke_test.sh` | `scripts/integration_smoke_test.sh` | 集成冒烟测试脚本 |
| 5 | `ai-infra/tasks/task-board.md` | `tasks/task-board.md` | 任务看板 |
| 6 | `ai-infra/REPO_TASK_RUNNER_MAP.md` | `REPO_TASK_RUNNER_MAP.md` | 各模块 CLI 入口映射 |
| 7 | `ai-infra/CODEX_IMPLEMENTATION_HANDOFF.md` | `CODEX_IMPLEMENTATION_HANDOFF.md` | Codex 交接文档 |

## 根目录 Makefile Target

| Target | 用途 |
|--------|------|
| `make infra-install` | 安装所有模块依赖 |
| `make infra-test` | 运行所有模块测试 |
| `make infra-serve` | 启动所有服务 |
| `make infra-smoke` | 运行冒烟测试 |
| `make infra-clean` | 清理所有构建产物 |

## 共享 .env 约定

```
# 共享：模型和端口
MODEL_NAME=Qwen/Qwen2.5-0.5B-Instruct
INFERENCE_BASE_URL=http://localhost:8000

# 共享：API Keys
OPENAI_API_KEY=replace-with-openai-api-key

# 各模块独立端口
INFERENCE_PORT=8000
GATEWAY_PORT=8080
```

## 关键实现顺序（来自 T815）

```
T0-01 → T0-02 → T0-03 → T0-04 →
T1-01 → T1-02 → T1-05 → T1-06 → T1-03 →
T1-08 → T1-09 → T1-10 → T1-11 → T1-12 →
T3-01 → T3-02 → T3-03 → T3-04 → T3-05 →
T4-01 → T4-02 → T4-05 → T4-06
```

## 与各模块的集成点

| 文件 | 用途 | 涉及模块 |
|------|------|---------|
| `tasks/task-board.md` | 任务状态追踪 | 所有模块 |
| `REPO_TASK_RUNNER_MAP.md` | 各模块 Makefile/CLI 速查 | 所有模块 |
| `CODEX_IMPLEMENTATION_HANDOFF.md` | Codex 实施交接 | Codex + MiniMax |

---

Sources:
1. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval
2. https://github.com/huggingface/peft — PEFT
3. https://docs.vllm.ai/ — vLLM

Risk of Staleness:
- 实现顺序可能因实际情况调整

Out of Scope Kept:
- 未写 CI/CD 配置
- 未写 K8s 部署
