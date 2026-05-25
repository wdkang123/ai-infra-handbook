# T1212 ai-gateway Implementation Map Revision

## Task ID: T1212
## Title: ai-gateway Implementation Map Revision
## Owner: MINIMAX
## Status: READY

## Read First

- `tasks/review/T1202-review.md`

## Scope

直接就地修订以下文件，不新增平行文件：

1. `tasks/review-pending/T1202-gateway-file-order-v1.md`
2. `tasks/review-pending/T1202-gateway-import-map-v1.md`
3. `tasks/review-pending/T1202-gateway-patch-split-v1.md`
4. `tasks/review-pending/T1202-gateway-validation-matrix-v1.md`
5. `tasks/review-pending/T1202-gateway-risk-checklist-v1.md`

## Required Changes

1. 全包对齐 accepted `T1002 / T1102 / T302 / T812`
2. 鉴权按 `AuthMiddleware` / `verify_bearer_token` 口径展开
3. 不把 `auth.py` 写成依赖 `httpx`
4. 不把 accepted 资产里没有明确依据的新增文件写成 MVP 默认主线

## Guardrails

- 只修 review note 指定问题
- 不重写整包
- 完成后列出实际修改过的绝对路径
