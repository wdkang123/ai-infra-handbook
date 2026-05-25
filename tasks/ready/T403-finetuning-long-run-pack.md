# Task Card

Task ID: T403
Title: Finetuning Long-Run Pack v1
Owner: MINIMAX
Type: PACK-长跑专题包
Priority: P1

## Input

基于：
- `tasks/accepted/T207-lora-peft-chapter-revision.md`
- `tasks/accepted/T198-unsloth-chapter-draft.md`
- `tasks/accepted/T209-finetuning-comparison-index-tighten.md`
- `tasks/accepted/T315-finetuning-glossary-batch-04-tighten.md`
- `tasks/accepted/T304-finetune-demo-mvp-result.md`

## Expected Output

本专题包必须产出以下 4 个文件：

1. `tasks/review-pending/T403-finetuning-pack-manifest.md`
2. `tasks/review-pending/T403-finetuning-comparison-index-v2.md`
3. `tasks/review-pending/T403-finetuning-practice-catalog-v1.md`
4. `tasks/review-pending/T403-finetune-demo-training-map-v1.md`

## Deliverable Notes

### T403-finetuning-comparison-index-v2

比较对象至少包含：

- LoRA
- QLoRA
- PEFT
- TRL
- Unsloth

### T403-finetuning-practice-catalog-v1

整理 6 到 8 个最小实践入口：

- LoRA basic
- QLoRA basic
- PEFT basic
- TRL SFT
- DPO entry
- Unsloth entry

### T403-finetune-demo-training-map-v1

说明 `finetune-demo` 的训练路径拆分和资料入口，不写实现结论。

### T403-finetuning-pack-manifest

总结本包交付物、用途和需要 Codex 判断的点。

## Template

使用 MiniMax 标准输出协议。

## Acceptance Criteria

- 必须写满 4 个输出文件
- 维持 finetuning 主线
- 来源要精确
- 不扩写成完整训练平台设计

## Allowed Sources

- 已通过的 finetuning 相关资产

## Out of Scope

- 不做代码实现
- 不输出最终训练架构结论
