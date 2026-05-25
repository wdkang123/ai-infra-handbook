# T1104 finetune-demo Fixture Pack

## Task ID: T1104
## Title: finetune-demo Fixture Pack
## Owner: MINIMAX
## Status: READY

## Objective

为 `finetune-demo` 生成 implementation-ready 训练样例资产。

## Produce

1. `tasks/review-pending/T1104-finetune-jsonl-dataset-samples-v1.md`
2. `tasks/review-pending/T1104-finetune-lora-config-samples-v1.md`
3. `tasks/review-pending/T1104-finetune-training-log-samples-v1.md`
4. `tasks/review-pending/T1104-finetune-adapter-artifact-manifest-v1.md`
5. `tasks/review-pending/T1104-finetune-fixture-manifest-v1.md`

## Requirements

- dataset sample 至少给 5 条 JSONL 样例
- config sample 至少覆盖 LoRA / QLoRA 各一份
- training log sample 需体现 epoch / step / loss / save checkpoint
- adapter artifact manifest 要对齐 PEFT adapter 常见产物

## Guardrails

- 只做 fixture / sample asset，不写新章节
- 训练日志可以是仓库样例约定，但不要伪装成真实跑出来的数据
