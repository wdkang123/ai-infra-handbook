# Task Card

Task ID: T315
Title: 收紧 finetuning glossary batch 04 的笔误和边界措辞
Owner: MINIMAX
Type: A-资料任务
Priority: P1

## Input

基于：
- `tasks/review-pending/T314-finetuning-glossary-batch-04.md`
- `tasks/review/T314-review.md`

## Expected Output

对 `T314` 做最小修订版，只修 `DPO` 条目笔误和 `Unsloth` 条目的一句边界措辞。

## Template

使用 MiniMax 标准输出协议。

## Acceptance Criteria

- 修正 `DPO` 条目中的笔误
- 收紧 `Unsloth` 条目边界说明，不写过强实现性结论
- 其他条目保持不变

## Allowed Sources

- T314 当前 glossary 草稿
- T314 review note

## Out of Scope

- 不重写整批 glossary
- 不新增术语
