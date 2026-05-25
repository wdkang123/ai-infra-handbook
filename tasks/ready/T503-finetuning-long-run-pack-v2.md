# Task Card

Task ID: T503
Title: Finetuning Long-Run Pack v2
Owner: MINIMAX
Type: PACK-长跑专题包
Priority: P1

## Input

基于：
- `tasks/accepted/T403-finetuning-comparison-index-v2.md`
- `tasks/accepted/T403-finetuning-practice-catalog-v1.md`
- `tasks/accepted/T403-finetune-demo-training-map-v1.md`
- `tasks/accepted/T315-finetuning-glossary-batch-04-tighten.md`
- `tasks/accepted/T304-finetune-demo-mvp-result.md`

## Expected Output

本专题包必须产出以下 5 个文件：

1. `tasks/review-pending/T503-finetuning-pack-manifest-v2.md`
2. `tasks/review-pending/T503-finetuning-sources-index-v2.md`
3. `tasks/review-pending/T503-finetuning-glossary-batch-06.md`
4. `tasks/review-pending/T503-finetune-demo-practice-catalog-v2.md`
5. `tasks/review-pending/T503-finetune-demo-decision-notes-v1.md`

## Deliverable Notes

### sources-index-v2

补齐 LoRA / QLoRA / PEFT / TRL / Unsloth / bitsandbytes 的稳定入口。

### glossary-batch-06

优先补：
- BitsAndBytes
- Reward Model
- Preference Data
- PPO
- RLHF
- Adapter Merge
- Safetensors
- Checkpoint

### practice-catalog-v2

从“方法验证”推进到“训练路径验证”。

### decision-notes-v1

围绕以下问题给出资料级输入：
- LoRA vs QLoRA 默认路线
- DPO 是否进入 MVP
- Unsloth 是否默认启用

### manifest

总结本包完成项、未定项、需要 Codex 判断的点。

## Template

使用 MiniMax 标准输出协议。

## Acceptance Criteria

- 必须写满 5 个输出文件
- 维持 finetuning 主线
- 所有重点链接必须是精确 URL
- 不扩写成完整训练平台设计

## Allowed Sources

- 已通过的 finetuning 相关资产

## Out of Scope

- 不写代码实现
