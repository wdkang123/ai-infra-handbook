# Night Run 03

目标：让 MiniMax 在下一轮长跑里，一边收口现有两章，一边继续批量铺正文章节，保持低耦合和可逐条验收。

## 执行原则

1. 只处理本文件列出的任务
2. 每完成一个任务就写入 `tasks/review-pending/`
3. 不等待人工反馈，直接继续下一个
4. 只修任务卡要求的最小问题，不擅自重写整批材料
5. 所有关键链接必须是精确 URL

## 执行顺序

### Batch A：先收口两章

1. `T203` AI Gateway 章节修订
2. `T204` Observability 章节修订

### Batch B：继续批量铺正文

3. `T195` Evaluation 章节初稿
4. `T196` Cache / Prefix Caching 章节初稿
5. `T197` LoRA / PEFT 章节初稿
6. `T198` Unsloth 章节初稿

## 停止条件

- 本文件全部任务完成
- 或者没有合法任务可做
- 或者发现任务要求与已通过资料明显冲突

停止时明确输出：`Night Run 03 completed` 或 `Night Run 03 blocked`
