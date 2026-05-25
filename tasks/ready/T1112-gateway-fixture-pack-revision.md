# T1112 ai-gateway Fixture Pack Revision

## Task ID: T1112
## Title: ai-gateway Fixture Pack Revision
## Owner: MINIMAX
## Status: READY

## Read First

- `tasks/review/T1102-review.md`

## Scope

直接就地修订以下文件，不新增平行文件：

1. `tasks/review-pending/T1102-gateway-auth-request-fixtures-v1.md`
2. `tasks/review-pending/T1102-gateway-routing-config-samples-v1.md`
3. `tasks/review-pending/T1102-gateway-error-response-samples-v1.md`
4. `tasks/review-pending/T1102-gateway-proxy-response-samples-v1.md`
5. `tasks/review-pending/T1102-gateway-fixture-manifest-v1.md`

## Required Changes

1. 对齐 auth success 返回值
2. 把 `valid_keys` 改回 accepted blueprint 使用的 `api_keys`
3. 对齐 wrong-scheme 错误消息
4. 对齐 unknown model 的 `error.code`

## Guardrails

- 只修 review note 指定问题
- 不重写整包
- 完成后列出实际修改过的绝对路径
