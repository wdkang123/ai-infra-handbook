# Fixture Run 03

## Mode

微任务修订模式（直接就地修订原 fixture 文件）

## Goal

收掉 fixture 阶段剩余的 2 个最小契约问题，使 `T1101` 和 `T1103` 也能进入 `accepted/`。

## Run Order

1. `tasks/ready/T1121-inference-fixture-naming-tighten.md`
2. `tasks/ready/T1123-eval-fixture-contract-tighten.md`

## Notes

- 直接覆盖 `tasks/review-pending/` 下原文件，不新增平行文件名
- 每个任务完成后都要列出实际修改过的绝对路径
- 只修 review note 指定的问题，不重写整包
