# Task Card

Task ID: T603
Title: Finetuning / Training Zero-Touch Pack
Owner: MINIMAX
Type: PACK-0接管链式专题包
Priority: P1

## Input

基于：
- `tasks/accepted/T173-lora-peft-sources-result.md`
- `tasks/accepted/T174-unsloth-sources-result.md`
- `tasks/accepted/T198-unsloth-chapter-draft.md`
- `tasks/accepted/T207-lora-peft-chapter-revision.md`
- `tasks/accepted/T209-finetuning-comparison-index-tighten.md`
- `tasks/accepted/T304-finetune-demo-mvp-result.md`
- `tasks/accepted/T315-finetuning-glossary-batch-04-tighten.md`
- `tasks/review-pending/T601-inference-stack-decision-memo-v1.md`
- `tasks/review-pending/T602-observability-eval-decision-memo-v1.md`

## Expected Output

本专题包必须产出以下 7 个文件：

1. `tasks/review-pending/T603-finetuning-training-pack-manifest.md`
2. `tasks/review-pending/T603-finetuning-sources-index-v3.md`
3. `tasks/review-pending/T603-finetuning-comparison-index-v3.md`
4. `tasks/review-pending/T603-finetuning-practice-catalog-v3.md`
5. `tasks/review-pending/T603-finetune-demo-training-map-v2.md`
6. `tasks/review-pending/T603-finetuning-glossary-batch-07.md`
7. `tasks/review-pending/T603-finetuning-decision-memo-v2.md`

## Deliverable Notes

### sources-index-v3

补齐并收紧以下对象的稳定入口：
- PEFT
- TRL
- LoRA
- QLoRA
- bitsandbytes
- Unsloth
- preference / reward 相关入口

### comparison-index-v3

把方法、框架、工具的边界分开写，不混成一张营销型总表。

### practice-catalog-v3

整理 8 到 10 个从最小训练验证到偏工程化训练路径的实践。

### training-map-v2

给 finetune-demo 提供更完整的训练路径说明，但仍是资料级输入，不是实现设计。

### glossary-batch-07

优先术语：
- DPO
- RLHF
- Reward Model
- Preference Data
- Adapter Merge
- Safetensors
- Checkpoint
- Quantization

### decision-memo-v2

围绕以下问题给出资料级输入：
- MVP 默认 LoRA 还是 QLoRA
- DPO 是否进入第一阶段
- Unsloth 在什么条件下值得默认启用

### manifest

总结完成项、未定项、对下一包可复用的输入。

## Template

使用 MiniMax 标准输出协议。

## Acceptance Criteria

- 必须写满 7 个输出文件
- 全部围绕 finetuning / training 主线
- 所有重点链接必须是精确 URL
- 不扩写成完整训练平台方案

## Out of Scope

- 不写代码实现
