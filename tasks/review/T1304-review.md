# T1304 Review

## Task ID: T1304
## Title: finetune-demo Execution Slice Pack
## Reviewer: CODEX
## Status: REVISE_REQUIRED

## 结论

`T1304` 的 slice 切法基本合理，但契约里的命令参数和对象用法还在沿用非 accepted 口径，会直接误导后续真实编码和验证。

## Findings

1. [T1304-finetune-slice-contracts-v1.md](tasks/review-pending/T1304-finetune-slice-contracts-v1.md#L34) 和 [T1304-finetune-slice-contracts-v1.md](tasks/review-pending/T1304-finetune-slice-contracts-v1.md#L127) 把 `--max-steps` 写成了 CLI 主参数，但已接受的 [T1004-finetune-main-py-blueprint-v1.md](tasks/accepted/T1004-finetune-main-py-blueprint-v1.md) 里并没有这个参数口径。
2. [T1304-finetune-slice-contracts-v1.md](tasks/review-pending/T1304-finetune-slice-contracts-v1.md#L60) 到 [T1304-finetune-slice-contracts-v1.md](tasks/review-pending/T1304-finetune-slice-contracts-v1.md#L70) 把 `load_config()` 的返回值当普通 dict 用，但 accepted [T1004-finetune-config-schema-blueprint-v1.md](tasks/accepted/T1004-finetune-config-schema-blueprint-v1.md) 主口径是 `TrainingConfig` / schema 对象，不是简单 dict。
3. [T1304-finetune-slice-contracts-v1.md](tasks/review-pending/T1304-finetune-slice-contracts-v1.md#L97) 到 [T1304-finetune-slice-contracts-v1.md](tasks/review-pending/T1304-finetune-slice-contracts-v1.md#L104) 把 `LoRATrainer` 写成直接吃 config 路径字符串，但 accepted [T1004-finetune-train-py-blueprint-v1.md](tasks/accepted/T1004-finetune-train-py-blueprint-v1.md) 的主口径是 trainer 接收 config 对象或 dict。

## Required Fix

- 直接就地修订 `T1304` 原文件，不新增平行版本。
- 把 CLI 参数、config 用法、trainer 用法统一回 accepted `T1004` 蓝图口径。
- 只修契约和示例命令，不重写整包。
