# T1214 finetune-demo Implementation Map Revision

## Task ID: T1214
## Title: finetune-demo Implementation Map Revision
## Owner: MINIMAX
## Status: READY

## Read First

- `tasks/review/T1204-review.md`

## Scope

直接就地修订以下文件，不新增平行文件：

1. `tasks/review-pending/T1204-finetune-file-order-v1.md`
2. `tasks/review-pending/T1204-finetune-import-map-v1.md`
3. `tasks/review-pending/T1204-finetune-patch-split-v1.md`
4. `tasks/review-pending/T1204-finetune-validation-matrix-v1.md`
5. `tasks/review-pending/T1204-finetune-risk-checklist-v1.md`

## Required Changes

1. 全包对齐 accepted `T1004 / T1104 / T304 / T703`
2. 源码路径统一回到 `src/finetune_demo/...`
3. file order / import map / patch split 以 accepted starter manifest 的真实文件布局为主
4. 不把 accepted 中没有明确依据的新落点写成默认实现主线

## Guardrails

- 只修 review note 指定问题
- 不重写整包
- 完成后列出实际修改过的绝对路径
