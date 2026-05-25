# Mega Run 01

目标：让 MiniMax 进入“长跑专题包模式”，一次执行 3 个专题包，而不是大量两分钟结束的微任务。

## 使用方式

先阅读：

- `prompts/minimax/long-run-worker.md`
- `tasks/long-plan-phase-03.md`
- `tasks/task-board.md`

然后严格按顺序执行以下 3 个专题包：

1. `tasks/ready/T401-observability-long-run-pack.md`
2. `tasks/ready/T402-eval-benchmark-long-run-pack.md`
3. `tasks/ready/T403-finetuning-long-run-pack.md`

## 执行原则

1. 只执行本文件列出的专题包
2. 每个专题包必须写完任务卡规定的全部输出文件
3. 每完成一个输出文件就立即写入 `tasks/review-pending/`
4. 不等待人工反馈，继续执行同包剩余交付物
5. 一个专题包结束后再进入下一个专题包
6. 所有重点链接必须是精确 URL
7. 不改目录，不改主题边界，不擅自合并不同专题

## 停止条件

- 本文件中列出的 3 个专题包全部完成
- 或者出现明确阻塞，无法继续产生合法交付物

停止时明确输出：

- `Long Run completed`
- 或 `Long Run blocked`
