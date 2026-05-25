# Night Run 04

目标：让 MiniMax 在下一轮长跑里，先把 3 个还没收稳的章节修掉，再继续补微调和评测主线索引。

## 执行原则

1. 只处理本文件列出的任务
2. 每完成一个任务就写入 `tasks/review-pending/`
3. 不等待人工反馈，直接继续下一个
4. 只修任务卡要求的最小问题，不擅自重写整批材料
5. 所有重点链接必须是精确 URL

## 执行顺序

### Batch A：先收口 3 个章节

1. `T205` Evaluation 章节修订
2. `T206` Cache / Prefix Caching 章节修订
3. `T207` LoRA / PEFT 章节修订

### Batch B：再补两份索引

4. `T199` finetuning comparison-index v1
5. `T306` benchmark / evaluation sources-index v1

## 停止条件

- 本文件全部任务完成
- 或者没有合法任务可做
- 或者发现任务要求与已通过资料明显冲突

停止时明确输出：`Night Run 04 completed` 或 `Night Run 04 blocked`
