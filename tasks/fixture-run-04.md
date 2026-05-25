# Fixture Run 04

## Mode

微任务修订模式（直接就地修订原 fixture 文件）

## Goal

只收掉 `T1101` 和 `T1103` 剩余的两个硬问题。

## Run Order

1. `tasks/ready/T1131-inference-request-fixture-rename-fix.md`
2. `tasks/ready/T1133-eval-backend-cli-fix.md`

## Notes

- 直接覆盖 `tasks/review-pending/` 下原文件，不新增平行文件名
- 只修 review note 指定的问题，不重写整包
- 每个任务完成后都要列出实际修改过的绝对路径
