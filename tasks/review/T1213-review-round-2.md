# T1213 Review Round 2

## Task ID: T1213
## Title: eval-module Implementation Map Revision
## Reviewer: CODEX
## Status: REVISE_REQUIRED

## 结论

`T1203` 的主干已经明显收回来了，但还有两处旧口径残留，会继续干扰后续实现和测试理解。

## Findings

1. [T1203-eval-import-map-v1.md](tasks/review-pending/T1203-eval-import-map-v1.md#L53) 还保留了 `eval_result.py` 这一行，但当前文档正文里已经不再有该文件；这会让 import map 自己内部出现不一致。
2. [T1203-eval-risk-checklist-v1.md](tasks/review-pending/T1203-eval-risk-checklist-v1.md#L59) 仍写着 `runner.evaluate()` 是 async 函数，但 accepted runner 主入口已经是 `run(...)`，这里是上一轮遗留口径。

## Required Fix

- 直接就地修订 `T1203` 原文件，不新增平行版本。
- 去掉 `eval_result.py` 的残留描述，统一回到当前 implementation map 口径。
- 把 `runner.evaluate()` 改成与 accepted runner blueprint 一致的 `run(...)` 说法。
