# T1201 Review

## Task ID: T1201
## Title: inference-service Implementation Map Pack
## Reviewer: CODEX
## Status: REVISE_REQUIRED

## 结论

这轮 implementation map 的主问题不是“细节差一点”，而是实现图整体偏离了已接受的 starter blueprints，会直接把后续真实编码带到另一套目录和端点口径上，需要最小修订。

## Findings

1. `T1201-inference-file-order-v1.md` 把目录结构写成了另一套实现：既有 `src/inference_service/version.py`，又在后面的目录树里写 `__version__.py`；同时还引入了 `models.py`、`metrics.py`、`engine/` 单数目录。这与已接受的 [T1001-inference-starter-manifest.md](tasks/accepted/T1001-inference-starter-manifest.md) 不一致，accepted 口径是 `api/` 和 `engines/`，而不是这里这套新结构。
2. `T1201-inference-import-map-v1.md` 里的入口流又把聊天端点写成了 `/v1/chat`，但已接受的 API 契约和 starter blueprint 都是 `/v1/chat/completions`。另外 import map 也把实现组织成 `.engine.factory`，而 accepted starter manifest 明确是 `engines/`。
3. `T1201` 整包的 file order / import map / patch split / validation matrix 必须服务“按 accepted 蓝图落地”，不能一边引用 `T1001/T1101/T811`，一边在 implementation map 里重开一套新文件、新模块和新目录。

## Required Fix

- 直接就地修订 `tasks/review-pending/` 下的 `T1201` 原文件，不新增平行版本。
- 全包统一对齐已接受的 `T1001 / T1101 / T301 / T811`：
  - 端点只写 `/health`、`/metrics`、`/v1/chat/completions`
  - 目录和文件命名优先沿用 accepted starter manifest
  - 不再引入与 accepted 蓝图冲突的 `version.py`、`engine/` 单数目录、`/v1/chat`
- patch split、validation matrix、risk checklist 也要回到 accepted 蓝图边界，而不是基于新发明的实现结构展开。
