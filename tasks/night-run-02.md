# Night Run 02

目标：让 MiniMax 在无人值守的长时间任务里，继续推进“索引 + 章节 + MVP 设计”三条线，但仍保持低耦合、可逐条验收。

## 执行原则

1. 只处理本文件列出的任务
2. 每完成一个任务就写入 `tasks/review-pending/`
3. 不等待人工反馈，直接继续下一个任务
4. 如果发现来源不够硬，宁可删掉该条，不要硬写
5. 不改目录，不改任务边界，不把多个任务合并
6. 设计稿里的 CLI / SDK 示例必须标注为“提案接口”，不能写成“仓库已实现”

## 执行顺序

### Batch A：先做可复用索引

1. `T164` gateway / cache / router sources-index v1
2. `T165` finetuning sources-index v1

### Batch B：再做章节初稿

3. `T193` AI Gateway 章节初稿
4. `T194` Observability 章节初稿

### Batch C：最后做项目设计稿

5. `T303` eval-module MVP 目录与边界设计
6. `T304` finetune-demo MVP 目录与边界设计

## 停止条件

- 本文件全部任务完成
- 或者没有合法任务可做
- 或者发现任务要求与已通过资料明显冲突

停止时明确输出：`Night Run 02 completed` 或 `Night Run 02 blocked`
