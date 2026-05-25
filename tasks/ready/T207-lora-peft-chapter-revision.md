# Task Card

Task ID: T207
Title: 收紧 LoRA / PEFT 章节初稿中的代码示例和边界
Owner: MINIMAX
Type: C-普通章节任务
Priority: P1

## Input

基于：
- `tasks/review-pending/T197-lora-peft-chapter-draft.md`
- `tasks/review/T197-review.md`
- `tasks/accepted/T173-lora-peft-sources-result.md`
- `tasks/accepted/T165-finetuning-sources-index-v1.md`

## Expected Output

对 `T197` 做最小修订版，只修审阅指出的问题，不重写整章。

## Template

使用 MiniMax 标准输出协议。

## Acceptance Criteria

- 修正最小实践代码中的导入和接口示例
- 删除硬编码的具体 trainable params 输出
- 收紧 Unsloth 的比重，保持本章主体是 LoRA / QLoRA / PEFT
- 保持 10 节结构

## Allowed Sources

- 已通过的 T173 / T165
- T197 当前章节草稿

## Out of Scope

- 不重写整章
- 不扩写成完整训练实践
