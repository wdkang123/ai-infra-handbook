# T1204 Review

## Task ID: T1204
## Title: finetune-demo Implementation Map Pack
## Reviewer: CODEX
## Status: REVISE_REQUIRED

## 结论

这轮 finetune implementation map 把 accepted starter manifest 的路径体系和文件落点改掉了，尤其是 `src/` 约定被丢掉，会直接让后续实现偏仓库结构。

## Findings

1. `T1204-finetune-file-order-v1.md` 主要使用顶层 `finetune_demo/...` 路径，但已接受的 [T1004-finetune-starter-manifest.md](tasks/accepted/T1004-finetune-starter-manifest.md) 明确要求源码位于 `src/finetune_demo/...`。
2. 同一份 file order 还把实现主线改成了 `train.py`、`merge_adapter.py`、`dataset.py` 等另一套落点，而 accepted starter manifest 的主口径是 `main.py`、`config.py`、`trainer/lora_trainer.py`、`scripts/train.sh`，以及 `trainer/`、`adapter/`、`export/` 子目录。
3. implementation map 可以细化 accepted 结构，但不能跳过 accepted manifest 重新定义真实文件布局；否则后续 Codex 会面对两套互相冲突的“准实现规范”。

## Required Fix

- 直接就地修订 `tasks/review-pending/` 下的 `T1204` 原文件，不新增平行版本。
- 全包统一对齐已接受的 `T1004 / T1104 / T304 / T703`：
  - 源码路径统一回到 `src/finetune_demo/...`
  - file order / import map / patch split / validation matrix 以 accepted starter manifest 中的真实文件布局为主
  - 不再把 `train.py`、`merge_adapter.py` 等新落点写成默认实现主线，除非它们在 accepted 资产中已有明确依据
- 保持 finetune 主题边界，不把 implementation map 扩写成新一轮架构重设计。
