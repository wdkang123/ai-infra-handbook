# T1221 Review Round 3

## Task ID: T1221
## Title: inference-service Implementation Map Tighten Round 2
## Reviewer: CODEX
## Status: REVISE_REQUIRED

## 结论

`T1201` 已经很接近了，但还留着两处会继续把实现导向非 accepted 主线的小问题。

## Findings

1. [T1201-inference-import-map-v1.md](tasks/review-pending/T1201-inference-import-map-v1.md#L22) 到 [T1201-inference-import-map-v1.md](tasks/review-pending/T1201-inference-import-map-v1.md#L33) 仍然把 `models.py` 写成默认导入主线，但当前 file order 已经不再把它列为核心文件，这里需要统一。
2. [T1201-inference-file-order-v1.md](tasks/review-pending/T1201-inference-file-order-v1.md#L54) 还写着 `Phase 3.3 + 2.3`，但当前 Phase 2 只有 `2.1 / 2.2`，这里是上一轮删改后留下的依赖编号残影。

## Required Fix

- 直接就地修订 `T1201` 原文件，不新增平行版本。
- 去掉 import map 里把 `models.py` 当默认主线的描述。
- 把 file order 中错误的依赖编号改对，保持整包内部一致。
