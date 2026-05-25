# Mega Run 02

目标：让 MiniMax 继续使用长跑专题包模式，但把单次运行做得更重，单包不再只产 4 个文件，而是优先产 5 个文件级交付物。

## 使用方式

先阅读：

- `prompts/minimax/long-run-worker.md`
- `tasks/long-plan-phase-03.md`
- `tasks/task-board.md`

然后严格按顺序执行以下专题包：

1. `tasks/ready/T404-eval-benchmark-long-run-pack-revision.md`
2. `tasks/ready/T501-observability-long-run-pack-v2.md`
3. `tasks/ready/T502-eval-benchmark-long-run-pack-v2.md`
4. `tasks/ready/T503-finetuning-long-run-pack-v2.md`

## 执行原则

1. 只执行本文件列出的专题包
2. 每个专题包必须写完任务卡规定的全部输出文件
3. 每完成一个输出文件就立即写入 `tasks/review-pending/`
4. 不等待人工反馈，继续执行同包剩余交付物
5. 一个专题包结束后再进入下一个专题包
6. 所有重点链接必须是精确 URL
7. 不改目录，不改主题边界，不擅自合并不同专题

## 停止条件

- 本文件中列出的专题包全部完成
- 或者出现明确阻塞，无法继续产生合法交付物

停止时明确输出：

- `Long Run completed`
- 或 `Long Run blocked`
