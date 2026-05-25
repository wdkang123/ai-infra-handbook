# T1224 Review Round 3

## Task ID: T1224
## Title: finetune-demo Implementation Map Tighten Round 2
## Reviewer: CODEX
## Status: REVISE_REQUIRED

## 结论

`T1204` 这轮已经收回很多，但 validation matrix 还混用了 `src.finetune_demo` 这种实现时不会采用的导入/运行口径。

## Findings

1. [T1204-finetune-validation-matrix-v1.md](tasks/review-pending/T1204-finetune-validation-matrix-v1.md#L18) 到 [T1204-finetune-validation-matrix-v1.md](tasks/review-pending/T1204-finetune-validation-matrix-v1.md#L24) 把命令写成 `from src.finetune_demo...`、`python -m src.finetune_demo.main ...`，这和 accepted starter blueprints 的实际使用口径不一致。
2. 已接受的 [T1004-finetune-main-py-blueprint-v1.md](tasks/accepted/T1004-finetune-main-py-blueprint-v1.md) 与 [T1004-finetune-config-schema-blueprint-v1.md](tasks/accepted/T1004-finetune-config-schema-blueprint-v1.md) 对应的是 `finetune_demo...` 导入和 `python -m finetune_demo.main` / `finetune-demo ...` 这类执行方式，不是 `src.finetune_demo...`。

## Required Fix

- 直接就地修订 `T1204` 原文件，不新增平行版本。
- 只修 validation matrix 中的导入和执行命令口径。
- 不改 file order / import map / patch split。
