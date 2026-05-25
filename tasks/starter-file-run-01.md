# Starter File Run 01

目标：让 MiniMax 一次性连续执行 5 个 starter file blueprint 专题包，产出接近未来真实源码文件的蓝图。

## 使用方式

先阅读：

- `prompts/minimax/starter-worker.md`
- `tasks/long-plan-phase-08.md`
- `tasks/task-board.md`

然后严格按顺序执行以下专题包：

1. `tasks/ready/T1001-inference-starter-file-pack.md`
2. `tasks/ready/T1002-ai-gateway-starter-file-pack.md`
3. `tasks/ready/T1003-eval-module-starter-file-pack.md`
4. `tasks/ready/T1004-finetune-demo-starter-file-pack.md`
5. `tasks/ready/T1005-root-dev-starter-file-pack.md`

## 执行原则

1. 只执行本文件列出的专题包
2. 每个专题包必须写完任务卡规定的全部输出文件
3. 每完成一个输出文件就立即写入 `tasks/review-pending/`
4. 不等待人工反馈，继续执行同包剩余交付物
5. 一个专题包结束后立刻进入下一个专题包
6. 后续专题包允许复用同一轮前面已生成的合法文件
7. 所有重点链接必须是精确 URL
8. 不改目录，不改主题边界，不擅自跳包

## 停止条件

- 本文件中列出的专题包全部完成
- 或者出现明确阻塞

停止时明确输出：

- `Starter File Run completed`
- 或 `Starter File Run blocked`
