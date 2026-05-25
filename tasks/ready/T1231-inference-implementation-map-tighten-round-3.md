# T1231 inference-service Implementation Map Tighten Round 3

## Task ID: T1231
## Title: inference-service Implementation Map Tighten Round 3
## Owner: MINIMAX
## Status: READY

## Read First

- `tasks/review/T1221-review-round-3.md`

## Scope

直接就地修订以下文件，不新增平行文件：

1. `tasks/review-pending/T1201-inference-file-order-v1.md`
2. `tasks/review-pending/T1201-inference-import-map-v1.md`

## Required Changes

1. 去掉 import map 里把 `models.py` 当默认主线的描述
2. 修正 file order 中错误的依赖编号

## Guardrails

- 只修 review note 指定问题
- 不重写整包
- 完成后列出实际修改过的绝对路径
