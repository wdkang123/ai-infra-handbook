# Fixture Run 02

## Mode

微任务修订模式（直接就地修订原 fixture 文件）

## Goal

收掉 `T1101 / T1102 / T1103 / T1105` 这四个 fixture pack 中暴露出的契约问题。

## Run Order

1. `tasks/ready/T1111-inference-fixture-pack-revision.md`
2. `tasks/ready/T1112-gateway-fixture-pack-revision.md`
3. `tasks/ready/T1113-eval-fixture-pack-revision.md`
4. `tasks/ready/T1115-root-fixture-pack-revision.md`

## Notes

- 直接覆盖 `tasks/review-pending/` 下原文件，不新增平行文件名
- 每个任务完成后都要列出实际修改过的绝对路径
- 只修 review note 指定的问题，不重写整包
