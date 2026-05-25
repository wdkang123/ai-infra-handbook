# Task Card

Task ID: T703
Title: Finetuning / Training Deep-Research Pack
Owner: MINIMAX
Type: PACK-深研究0接管专题包
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
- `tasks/review-pending/T603-finetuning-sources-index-v3.md`
- `tasks/review-pending/T603-finetuning-comparison-index-v3.md`
- `tasks/review-pending/T603-finetuning-decision-memo-v2.md`

## Expected Output

本专题包必须产出以下 8 个文件：

1. `tasks/review-pending/T703-finetuning-pack-manifest.md`
2. `tasks/review-pending/T703-finetuning-sources-index-v4.md`
3. `tasks/review-pending/T703-finetuning-boundary-matrix-v1.md`
4. `tasks/review-pending/T703-finetuning-release-timeline-v1.md`
5. `tasks/review-pending/T703-finetuning-practice-catalog-v4.md`
6. `tasks/review-pending/T703-finetune-demo-training-map-v3.md`
7. `tasks/review-pending/T703-finetuning-glossary-batch-08.md`
8. `tasks/review-pending/T703-finetuning-decision-memo-v3.md`

## Deliverable Notes

### sources-index-v4

补齐 PEFT / TRL / Unsloth / bitsandbytes / preference data / reward modeling 的稳定入口和更新入口。

### boundary-matrix-v1

重点澄清：
- 方法 vs 框架 vs 工具
- LoRA vs QLoRA
- SFT / DPO / RLHF 的关系

### release-timeline-v1

收口 PEFT / TRL / Unsloth / bitsandbytes 的更新线索。

### practice-catalog-v4

补到 10 到 12 个实践条目，从小样本验证到训练路径检查。

### training-map-v3

继续推进 finetune-demo 的训练路径文档，但仍是资料级输入。

### glossary-batch-08

优先术语：
- SFT
- DPO
- RLHF
- Preference Pair
- Reward Model
- Adapter
- Merge
- Quantized Training

### decision-memo-v3

进一步收紧默认方法和第一阶段不做什么。

### manifest

总结本包升级了什么、未定项和对下一包可复用输入。

## Template

使用 MiniMax 标准输出协议。

## Acceptance Criteria

- 必须写满 8 个输出文件
- 全部围绕 finetuning / training 主线
- 所有重点链接必须是精确 URL
- 不扩写成完整训练平台白皮书

## Out of Scope

- 不写代码实现
