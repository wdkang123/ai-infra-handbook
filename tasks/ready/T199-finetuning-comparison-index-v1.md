# Task Card

Task ID: T199
Title: 产出 finetuning comparison-index v1
Owner: MINIMAX
Type: C-普通章节任务
Priority: P1

## Input

基于：
- `tasks/accepted/T165-finetuning-sources-index-v1.md`
- `tasks/accepted/T173-lora-peft-sources-result.md`
- `tasks/accepted/T174-unsloth-sources-result.md`

## Expected Output

产出一个 `comparison-index v1`，比较对象至少包含：

- LoRA
- QLoRA
- PEFT
- Unsloth

比较维度至少包含：

- 定位
- 所处层级
- 典型使用场景
- 与本项目的关系

## Template

使用 MiniMax 标准输出协议。

## Acceptance Criteria

- 保持 comparison-index 风格，不扩写成章节
- 每个维度给出来源
- 不做排名式结论

## Allowed Sources

- 已通过的 T165 / T173 / T174

## Out of Scope

- 不扩写成微调教程
- 不做性能横评
