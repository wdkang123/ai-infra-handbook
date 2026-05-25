# T1204 finetune-demo Implementation Map Pack

## Task ID: T1204
## Title: finetune-demo Implementation Map Pack
## Owner: MINIMAX
## Status: READY

## Objective

基于 accepted 的 `T1004 / T1104 / T304` 等资产，为 `finetune-demo` 生成 implementation map。

## Produce

1. `tasks/review-pending/T1204-finetune-file-order-v1.md`
2. `tasks/review-pending/T1204-finetune-import-map-v1.md`
3. `tasks/review-pending/T1204-finetune-patch-split-v1.md`
4. `tasks/review-pending/T1204-finetune-validation-matrix-v1.md`
5. `tasks/review-pending/T1204-finetune-risk-checklist-v1.md`

## Requirements

- 覆盖 `main.py / config.py / trainer/lora_trainer.py / tests/conftest.py / tests/test_trainer.py / scripts/train.sh`
- validation matrix 至少覆盖 config load、LoRA path、QLoRA path、adapter save
- patch split 要体现“先跑通配置和假训练，再接真实 trainer”
