Task ID: T703
Task Title: Finetuning / Training Deep-Research Pack
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
T703 Finetuning / Training Deep-Research Pack 收口 manifest。

Result:

# Finetuning / Training Deep-Research Pack Manifest

## 包概述

本包为 Finetuning / Training 专题的深研究 0 接管包，8 个文件全部完成，围绕微调方法、框架、工具的边界澄清、更新时间线和决策输入展开。

## 已完成交付物

### 1. T703-finetuning-sources-index-v4
补齐 PEFT/TRL/Unsloth/bitsandbytes/preference data/reward modeling 的稳定入口和更新入口。

### 2. T703-finetuning-boundary-matrix-v1
澄清五个边界：方法 vs 框架 vs 工具、LoRA vs QLoRA、SFT/DPO/RLHF 关系、Framework vs Training Library、Adapter Merging vs Model Merging。

### 3. T703-finetuning-release-timeline-v1
收口 PEFT/TRL/Unsloth/bitsandbytes 的关键更新线索和稳定入口。

### 4. T703-finetuning-practice-catalog-v4
12 个实践条目（F01-F12），从小样本验证到训练路径检查。

### 5. T703-finetune-demo-training-map-v3
继续推进 finetune-demo 的训练路径文档，v3 版本明确了 LoRA/QLoRA 决策和 DPO 时机。

### 6. T703-finetuning-glossary-batch-08
14 个核心术语：SFT/DPO/RLHF/Preference Pair/Reward Model/Adapter/Merge/Quantized Training/Checkpoint/bitsandbytes/Target Modules/Gradient Checkpointing/Safetensors/ChatML。

### 7. T703-finetuning-decision-memo-v3
进一步收紧 5 个决策点：LoRA vs QLoRA、DPO 第一阶段、Unsloth 启用条件、训练框架选型、训练监控工具。

### 8. T703-finetuning-pack-manifest
本文件，总结本包升级了什么、未定项、对下一包可复用输入。

## 本包升级了什么（相比 v3）

| 维度 | v3 | v4（收紧） |
|------|-----|-----------|
| Sources | 官方文档链接 | 补全 release 入口 |
| Boundaries | 基本对比 | 细化到 5 类边界澄清 |
| Timeline | 部分 | 新增 release-timeline |
| Decision | 5 个决策点 | 进一步收紧 |
| Practices | 10 个 | 增加到 12 个 |

## 对下一包可复用的输入

### 供 T704（Cross-Project）使用
- T703-finetuning-decision-memo-v3 的决策输入
- finetune-demo 的训练路径（LoRA/QLoRA/DPO 选择）
- 训练监控工具选择（Langfuse Cloud）

### 供 T705（Execution Decomposition）使用
- T701-inference-stack-decision-memo-v2（推理栈决策）
- T702-observability-eval-decision-memo-v2（observability 决策）
- T703-finetuning-decision-memo-v3（finetuning 决策）

## 需要 Codex 最终判断的点

1. **MVP 阶段是否接受 QLoRA（4-bit）作为默认微调方法**？
2. **DPO 是否在 MVP 阶段排除**？
3. **Unsloth 是否作为默认加速工具（需确认 GPU 兼容性）**？
4. **训练监控是否强制使用 Langfuse Cloud**？

## 风险与依赖

- LoRA/QLoRA 超参数配置复杂，需要根据实际模型调整
- Unsloth 加速效果依赖 GPU 型号（Ampere/Hopper）
- DPO 需要高质量偏好数据集，数据准备成本高

Sources:
1. https://arxiv.org/abs/2106.09685 — LoRA
2. https://arxiv.org/abs/2305.14314 — QLoRA
3. https://arxiv.org/abs/2305.18290 — DPO
4. https://github.com/huggingface/peft — PEFT
5. https://github.com/huggingface/trl — TRL
6. https://github.com/unslothai/unsloth — Unsloth
7. https://langfuse.com/docs/observability/overview — Langfuse
