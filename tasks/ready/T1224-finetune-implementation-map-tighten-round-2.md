# T1224 finetune-demo Implementation Map Tighten Round 2

## Task ID: T1224
## Title: finetune-demo Implementation Map Tighten Round 2
## Owner: MINIMAX
## Status: READY

## Read First

- `tasks/review/T1214-review-round-2.md`

## Scope

直接就地修订以下文件，不新增平行文件：

1. `tasks/review-pending/T1204-finetune-validation-matrix-v1.md`

## Required Changes

1. 把旧的 `dataset.py / train.py / merge_adapter` 验证链改成当前 implementation map 口径
2. 命令路径、模块名、验证对象统一回到 `src/finetune_demo/...`、`main.py`、`trainer/lora_trainer.py`、`export/adapter_exporter.py`

## Guardrails

- 只修 review note 指定问题
- 不重写整包
- 完成后列出实际修改过的绝对路径
