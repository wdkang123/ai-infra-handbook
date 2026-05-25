# Night Run 01

目标：让 MiniMax 在无人值守的一晚中持续执行一组低耦合、可审阅、可逐条验收的任务。

## 执行原则

1. 先做修订任务，再做新资料任务
2. 只处理本文件列出的任务
3. 每完成一个任务就写入 `tasks/review-pending/`
4. 不等待人工反馈，直接继续下一个任务
5. 遇到缺少精确官方来源的情况，宁可删掉该条，不要硬写
6. 不把不同任务合并，不新增目录，不改任务边界

## 执行顺序

### Batch A：先收口现有问题

1. `T151` TensorRT-LLM 资料包补官方文档入口与更稳的更新链接
2. `T153` Glossary 第二批术语收紧
3. `T156` Triton IS 章节再修一轮

### Batch B：扩资料面

4. `T161` AI Gateway 官方资料与核心链接
5. `T162` Observability / Evaluation 官方资料与核心链接
6. `T171` Caching / Prefix Caching / Semantic Cache 官方资料与核心链接
7. `T172` Router / Model Routing 官方资料与核心链接
8. `T173` LoRA / QLoRA / PEFT 官方资料与核心链接
9. `T174` Unsloth 官方资料与核心链接
10. `T175` Inference benchmark / serving eval 官方资料与核心链接

### Batch C：如果前面全部完成，再做一个汇总索引

11. `T176` Night sources digest v1

## 停止条件

- 本文件全部任务完成
- 或者没有合法任务可做
- 或者发现任务要求与现有资料明显冲突

停止时明确输出：`Night Run 01 completed` 或 `Night Run 01 blocked`
