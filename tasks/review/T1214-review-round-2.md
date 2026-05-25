# T1214 Review Round 2

## Task ID: T1214
## Title: finetune-demo Implementation Map Revision
## Reviewer: CODEX
## Status: REVISE_REQUIRED

## 结论

`T1204` 的 file order 和 import map 已经基本对齐，但 validation matrix 还整片沿用旧实现口径，不能直接通过。

## Findings

1. [T1204-finetune-validation-matrix-v1.md](tasks/review-pending/T1204-finetune-validation-matrix-v1.md#L20) 到 [T1204-finetune-validation-matrix-v1.md](tasks/review-pending/T1204-finetune-validation-matrix-v1.md#L26) 仍然在验证 `dataset.py`、`train.py`、`merge_adapter` 这套旧落点，但当前已经收回到 `src/finetune_demo/...`、`main.py`、`trainer/lora_trainer.py`、`export/adapter_exporter.py`。
2. [T1204-finetune-validation-matrix-v1.md](tasks/review-pending/T1204-finetune-validation-matrix-v1.md#L92) 到 [T1204-finetune-validation-matrix-v1.md](tasks/review-pending/T1204-finetune-validation-matrix-v1.md#L116) 也还保留了 `python finetune_demo/train.py` 和 `from finetune_demo.merge_adapter import ...` 的旧命令链。

## Required Fix

- 直接就地修订 `T1204` 原文件，不新增平行版本。
- 只修 `validation matrix`，把命令、文件路径和验证对象统一回到当前 accepted implementation map 口径。
- 不需要重写 file order / import map / patch split。
