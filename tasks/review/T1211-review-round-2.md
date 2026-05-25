# T1211 Review Round 2

## Task ID: T1211
## Title: inference-service Implementation Map Revision
## Reviewer: CODEX
## Status: REVISE_REQUIRED

## 结论

方向已经回来了，但 `T1201` 里还保留着一套偏离 accepted starter manifest 的配置与文件集合口径，需要再收一刀。

## Findings

1. [T1201-inference-file-order-v1.md](tasks/review-pending/T1201-inference-file-order-v1.md#L31) 到 [T1201-inference-file-order-v1.md](tasks/review-pending/T1201-inference-file-order-v1.md#L33) 仍然把配置主路径写成 `configs/config.yaml`、`configs/config.local.yaml`、`configs/config.smoke.yaml`，而已接受的 [T1001-inference-starter-manifest.md](tasks/accepted/T1001-inference-starter-manifest.md) 主口径是根级 `config.yaml`。
2. [T1201-inference-file-order-v1.md](tasks/review-pending/T1201-inference-file-order-v1.md#L42) 以及 [T1201-inference-file-order-v1.md](tasks/review-pending/T1201-inference-file-order-v1.md#L95) 仍把 `models.py` 写成默认主线文件，但 accepted starter manifest 里主线是 `main.py / server.py / config.py / api/* / engines/*`，不是 `models.py`。
3. [T1201-inference-patch-split-v1.md](tasks/review-pending/T1201-inference-patch-split-v1.md#L18) 和 [T1201-inference-patch-split-v1.md](tasks/review-pending/T1201-inference-patch-split-v1.md#L34) 还沿用了 `models.py` 作为 P0 默认目标文件，这会继续把实现入口带离 accepted starter files。

## Required Fix

- 直接就地修订 `T1201` 原文件，不新增平行版本。
- 把配置主路径与核心文件集合统一回到 accepted `T1001` starter manifest。
- `models.py` 如果保留，最多标成“后续可选抽取”，不能继续写成 MVP 默认主线。
