# Root Integration Codex Task Pack Manifest v1

## Task ID: T1405
## Title: Root Integration Codex Task Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# Root Integration Codex Task Pack Manifest

本文档索引根级联调的 Codex 实现任务卡。

## 任务卡清单

| Task ID | 任务名称 | 输入资产 | 目标文件 | 验证入口 |
|---|---|---|---|---|
| T1405-R1 | Makefile 入口 | T1005 root makefile blueprint v2 | `Makefile` | `make help` |
| T1405-R2 | 本地开发顺序 | T1005 local dev sequence blueprint v2 + T1405-R1 | `scripts/local_dev_sequence.sh` | `bash scripts/local_dev_sequence.sh` |
| T1405-R3 | 冒烟测试 | T1005 smoke test blueprint v2 + T1405-R1 | `scripts/integration_smoke_test.sh` | `make infra-smoke` |
| T1405-R4 | 跨项目 handoff | T1305 slice contracts + all above | `CODEX_IMPLEMENTATION_HANDOFF.md` | 文档审阅 |

---

## 与 Slice 的对应关系

| Task ID | 对应 Slice |
|---|---|
| T1405-R1 | R1 |
| T1405-R2 | R2 |
| T1405-R3 | R3 |
| T1405-R4 | R4 |

---

## Cut Line

以下内容不进入当前 task pack：
- CI/CD pipeline
- Kubernetes 部署
- 多环境配置（dev/staging/prod）
- 根级监控/dashboard
- Helper script 主线

---

Sources:
- T1005: accepted root makefile blueprint v2
- T1305: accepted execution slice pack
- T1105: root integration fixture pack
- T805: cross-project integration prep pack
