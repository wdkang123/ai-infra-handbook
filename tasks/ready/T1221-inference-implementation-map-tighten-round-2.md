# T1221 inference-service Implementation Map Tighten Round 2

## Task ID: T1221
## Title: inference-service Implementation Map Tighten Round 2
## Owner: MINIMAX
## Status: READY

## Read First

- `tasks/review/T1211-review-round-2.md`

## Scope

直接就地修订以下文件，不新增平行文件：

1. `tasks/review-pending/T1201-inference-file-order-v1.md`
2. `tasks/review-pending/T1201-inference-import-map-v1.md`
3. `tasks/review-pending/T1201-inference-patch-split-v1.md`

## Required Changes

1. 配置主路径统一回到 accepted `T1001` starter manifest 口径
2. `models.py` 不再作为 MVP 默认主线文件
3. file order / import map / patch split 的核心文件集合彼此对齐

## Guardrails

- 只修 review note 指定问题
- 不重写整包
- 完成后列出实际修改过的绝对路径
