# T1215 Root Integration Implementation Map Revision

## Task ID: T1215
## Title: Root Integration Implementation Map Revision
## Owner: MINIMAX
## Status: READY

## Read First

- `tasks/review/T1205-review.md`

## Scope

直接就地修订以下文件，不新增平行文件：

1. `tasks/review-pending/T1205-root-file-order-v1.md`
2. `tasks/review-pending/T1205-root-script-dependency-map-v1.md`
3. `tasks/review-pending/T1205-root-patch-split-v1.md`
4. `tasks/review-pending/T1205-root-validation-matrix-v1.md`
5. `tasks/review-pending/T1205-root-risk-checklist-v1.md`

## Required Changes

1. 全包对齐 accepted `T1005 / T1105 / T805`
2. 端口口径回到 `inference-service:8000`、`ai-gateway:8080`
3. eval-module 按 CLI / Make target 使用，不写成 `:8002` 服务
4. 根级调用链以 `Makefile` 和 `$(MAKE) -C ...` 为主，不新增 `*_serve.sh` 作为默认主线

## Guardrails

- 只修 review note 指定问题
- 不重写整包
- 完成后列出实际修改过的绝对路径
