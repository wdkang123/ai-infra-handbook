# T1211 inference-service Implementation Map Revision

## Task ID: T1211
## Title: inference-service Implementation Map Revision
## Owner: MINIMAX
## Status: READY

## Read First

- `tasks/review/T1201-review.md`

## Scope

直接就地修订以下文件，不新增平行文件：

1. `tasks/review-pending/T1201-inference-file-order-v1.md`
2. `tasks/review-pending/T1201-inference-import-map-v1.md`
3. `tasks/review-pending/T1201-inference-patch-split-v1.md`
4. `tasks/review-pending/T1201-inference-validation-matrix-v1.md`
5. `tasks/review-pending/T1201-inference-risk-checklist-v1.md`

## Required Changes

1. 全包对齐 accepted `T1001 / T1101 / T301 / T811`
2. 只保留 `/health`、`/metrics`、`/v1/chat/completions`
3. 目录和文件命名回到 accepted starter manifest 主口径
4. 不再把与 accepted 冲突的 `version.py`、`engine/` 单数目录、`/v1/chat` 写成默认实现主线

## Guardrails

- 只修 review note 指定问题
- 不重写整包
- 完成后列出实际修改过的绝对路径
