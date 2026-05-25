# T1105 Root Integration Fixture Pack

## Task ID: T1105
## Title: Root Integration Fixture Pack
## Owner: MINIMAX
## Status: READY

## Objective

为仓库根级联调流程生成第一批 implementation-ready 样例资产。

## Produce

1. `tasks/review-pending/T1105-root-env-profiles-v1.md`
2. `tasks/review-pending/T1105-root-smoke-expected-output-v1.md`
3. `tasks/review-pending/T1105-root-service-port-matrix-v1.md`
4. `tasks/review-pending/T1105-root-blocker-entry-examples-v1.md`
5. `tasks/review-pending/T1105-root-fixture-manifest-v1.md`

## Requirements

- env profile 至少覆盖 local dev / smoke test 两套
- smoke expected output 要覆盖：
  - direct inference 200
  - gateway proxy 200
  - auth 401
  - unknown model 404
  - metrics pass
- port matrix 要明确模块、端口、URL、依赖关系
- blocker entry example 要和当前任务系统风格一致

## Guardrails

- 只做 fixture / sample asset，不写新章节
- 输出物应能直接服务后续脚本与测试实现
