# Root Integration Slice Manifest v1

## Task ID: T1305
## Title: Root Integration Execution Slice Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# Root Integration Execution Slice Manifest

本文档索引根级联调的所有 execution slices，供 Codex 编码时参照。

## Slice 总览

| Slice ID | 名称 | 目标文件 | 验证入口 | 前置条件 |
|---|---|---|---|---|
| R1 | Makefile 入口 | `Makefile` | `make help` | 无 |
| R2 | 本地开发顺序 | `scripts/local_dev_sequence.sh` | 服务按顺序启动 | R1 |
| R3 | 冒烟测试 | `scripts/integration_smoke_test.sh` | `make infra-smoke` | R1 + 子项目 S2 + gateway G3 |
| R4 | 跨项目 handoff | `CODEX_IMPLEMENTATION_HANDOFF.md` | 服务间正确对接 | R3 |

---

## Slice 覆盖范围

| 主线 | 覆盖 Slice |
|---|---|
| Makefile 入口 | R1 |
| 本地开发 | R2 |
| 集成测试 | R3 |
| 跨项目交接 | R4 |

---

## Cut Line

以下内容不进入当前 slice 集合：
- CI/CD pipeline
- Kubernetes 部署
- 多环境配置（dev/staging/prod）
- 根级监控/dashboard

---

Sources:
- T1005: accepted root makefile blueprint
- T1105: root integration fixture manifest
- T805: cross-project integration prep pack
- T1205: accepted implementation map

Risk of Staleness:
- Makefile 接口和 script 接口相对稳定
