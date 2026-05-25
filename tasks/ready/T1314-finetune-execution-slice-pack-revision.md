# T1314 finetune-demo Execution Slice Pack Revision

## Task ID: T1314
## Title: finetune-demo Execution Slice Pack Revision
## Owner: MINIMAX
## Status: READY

## Read First

- `tasks/review/T1304-review.md`

## Scope

直接就地修订以下文件，不新增平行文件：

1. `tasks/review-pending/T1304-finetune-slice-contracts-v1.md`
2. `tasks/review-pending/T1304-finetune-first-codex-batch-v1.md`

## Required Changes

1. 把 CLI 参数口径统一回 accepted `T1004` 蓝图
2. 把 `load_config()`、`LoRATrainer(...)` 的示例改成与 accepted 蓝图一致的对象用法

## Guardrails

- 只修 review note 指定问题
- 不重写整包
- 完成后列出实际修改过的绝对路径
