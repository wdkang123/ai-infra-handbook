# Root / Dev Workflow Starter File Manifest

## Task ID: T1005
## Title: Root / Dev Workflow Starter File Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T905 scaffold blueprints（root-makefile / root-env / smoke-script / repo-task-runner / codex-handoff），产出根级开发工作流蓝图文件。

---

# Root / Dev Workflow Starter File Manifest

## 概述

本文档索引根级开发工作流的 starter file 蓝图，供 Codex 实施时参照。

## 蓝图文件清单

| 序号 | 文件路径（蓝图） | 对应真实文件 | 说明 |
|------|----------------|-------------|------|
| 1 | `T1005-root-makefile-blueprint-v2.md` | `ai-infra/Makefile` | 根目录 Makefile（v2） |
| 2 | `T1005-root-env-example-v2.md` | `ai-infra/.env.example` | 共享环境变量（v2） |
| 3 | `T1005-local-dev-sequence-sh-blueprint-v2.md` | `ai-infra/scripts/local_dev_sequence.sh` | 本地开发顺序脚本 |
| 4 | `T1005-integration-smoke-sh-blueprint-v2.md` | `ai-infra/scripts/integration_smoke_test.sh` | 集成冒烟测试脚本 |
| 5 | `T1005-blockers-md-blueprint-v1.md` | `ai-infra/BLOCKERS.md` | 阻塞问题追踪 |
| 6 | `T1005-codex-handoff-v2.md` | `ai-infra/CODEX_IMPLEMENTATION_HANDOFF.md` | Codex 交接文档 |
| 7 | (沿用 T905 scaffold) | `ai-infra/REPO_TASK_RUNNER_MAP.md` | CLI/Makefile 速查（沿用） |

## 目录结构（蓝图）

```
ai-infra/
├── Makefile                              # 根目录 Makefile
├── .env.example                          # 共享环境变量
├── BLOCKERS.md                           # 阻塞问题追踪
├── CODEX_IMPLEMENTATION_HANDOFF.md       # Codex 交接文档
├── REPO_TASK_RUNNER_MAP.md              # 各模块 CLI/Makefile 速查
├── scripts/
│   ├── local_dev_sequence.sh             # 本地开发顺序脚本
│   └── integration_smoke_test.sh           # 集成冒烟测试
└── tasks/
    └── task-board.md                      # 任务看板
```

## 跨项目 Makefile Target

| Target | 说明 |
|--------|------|
| `make infra-install` | 安装所有模块 |
| `make infra-test` | 运行所有模块测试 |
| `make infra-serve` | 启动所有服务 |
| `make infra-smoke` | 运行冒烟测试 |
| `make infra-clean` | 清理构建产物 |

---

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval

Risk of Staleness:
- 服务启动顺序可能因实际情况调整
