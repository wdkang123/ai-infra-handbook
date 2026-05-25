# Finetuning Decision Memo v3 (Revised)

## Task ID: T713
## Task Title: Finetuning Decision Memo Tighten
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T703-review.md，把偏 observability 架构决策的部分降级成"可选监控输入"。

---

# Finetuning Decision Memo v3 (Revised)

## 概述

本文档在 v2 基础上进一步收紧 finetuning 的关键决策点，给出资料级输入，帮助 Codex 做最终判断。

---

## 决策点一：MVP 默认 LoRA 还是 QLoRA（收紧）

### 选型维度对比（v3 收紧）

| 维度 | LoRA | QLoRA |
|------|------|-------|
| **显存需求** | 中（约为全参数 1/3） | 低（< 10GB for 7B） |
| **训练速度** | 快 | 中（量化开销） |
| **效果** | 接近全参数 | 略低于 LoRA |
| **超参数复杂度** | 中（rank/alpha） | 高（rank/alpha + 量化位） |

### 资料级建议（v3 收紧）

| 场景 | 推荐 | 收紧理由 |
|------|------|---------|
| MVP 快速验证 | QLoRA（4-bit） | 显存门槛低，快速出结果 |
| 正式训练（显存充足） | LoRA | 效果更好 |
| 效果优先、不计成本 | 全参数微调 | 效果最好但成本最高 |

来源：https://arxiv.org/abs/2106.09685
来源：https://arxiv.org/abs/2305.14314

---

## 决策点二：DPO 是否进入第一阶段（收紧）

### DPO 的必要条件（v3 收紧）

- 高质量偏好数据集（chosen/rejected 对）
- 数据标注成本
- 比 SFT 更精细的效果优化需求

### 资料级建议（v3 收紧）

| 阶段 | DPO 是否进入 | 收紧理由 |
|------|-------------|---------|
| MVP | 否 | 增加数据准备复杂度，先用 SFT 出结果 |
| 后续迭代 | 按需 | 有高质量偏好数据且 SFT 效果不足时考虑 |

来源：https://arxiv.org/abs/2305.18290

---

## 决策点三：Unsloth 在什么条件下值得默认启用（收紧）

### Unsloth 的条件（v3 收紧）

| 条件 | 说明 | 收紧程度 |
|------|------|---------|
| **GPU 型号** | Ampere（RTX 30xx、A100）或 Hopper（H100） | 必须确认 |
| **不需要 DPO** | Unsloth 不支持 DPO | 必须 |
| **追求训练加速** | 2x 加速 + 50% 显存减少 | 可选 |

### 资料级建议（v3 收紧）

| 场景 | 是否启用 Unsloth | 收紧理由 |
|------|-----------------|---------|
| GPU 兼容 + 不需要 DPO | 是 | 加速效果明显 |
| GPU 不兼容 | 否 | 加速效果有限 |
| 需要 DPO | 否 | Unsloth 不支持 |

来源：https://github.com/unslothai/unsloth

---

## 决策点四：训练框架选型（收紧）

### trl vs Unsloth（v3 收紧）

| 维度 | trl | Unsloth |
|------|-----|---------|
| **SFT 支持** | 是（SFTTrainer） | 是 |
| **DPO 支持** | 是（DPOTrainer） | 否 |
| **加速效果** | 无 | 2x 加速 |
| **GPU 兼容性** | 通用 | Ampere/Hopper |

### 资料级建议（v3 收紧）

- **MVP 阶段**：优先 Unsloth（如 GPU 兼容），加速效果明显
- **需要 DPO**：必须使用 trl
- **长期架构**：trl 是 HuggingFace 官方维护，更适合长期

来源：https://github.com/huggingface/trl
来源：https://github.com/unslothai/unsloth

---

## 决策点五：训练监控工具（收紧）

### 监控工具选择（v3 收紧）

| 工具 | 集成位置 | 用途 |
|------|---------|------|
| **Langfuse** | finetune-demo 代码中埋点 | 训练 metrics 上报，实验对比（可选） |
| **Prometheus** | 暴露 `/metrics` 端点 | GPU 利用率、显存占用采集（可选） |
| **Grafana** | 连接 Prometheus | 训练过程可视化（可选） |

### 资料级说明（v3 收紧）

- **训练监控是可选集成**，不影响 MVP 核心训练链路
- Langfuse / Prometheus / Grafana 的引入由 observability 专题统一规划
- finetune-demo 代码中预留 Langfuse SDK 埋点接口（可选实现）

来源：https://langfuse.com/docs/observability/overview

---

## 总结：资料级建议（v3 收紧，不下结论）

| 决策点 | 建议方向 | 收紧程度 |
|--------|---------|---------|
| LoRA vs QLoRA | MVP 用 QLoRA，正式用 LoRA | 明确 |
| DPO | MVP 不进入，后续按需 | 明确 |
| Unsloth | GPU 兼容时优先启用 | 明确 |
| 训练监控 | 可选集成，由 observability 专题统一规划 | 明确 |

---

## 需要 Codex 最终判断

1. **MVP 阶段是否接受 QLoRA（4-bit）作为默认微调方法**？
2. **DPO 是否在 MVP 阶段排除**？
3. **Unsloth 是否作为默认加速工具（需确认 GPU 兼容性）**？
4. **训练监控工具是否作为可选集成（由 observability 专题决定）**？

Sources:
1. https://arxiv.org/abs/2106.09685 — LoRA
2. https://arxiv.org/abs/2305.14314 — QLoRA
3. https://arxiv.org/abs/2305.18290 — DPO
4. https://github.com/huggingface/peft — PEFT
5. https://github.com/huggingface/trl — TRL
6. https://github.com/unslothai/unsloth — Unsloth
7. https://langfuse.com/docs/observability/overview — Langfuse

Risk of Staleness:
- LoRA/QLoRA 超参数最佳实践可能随新研究更新
- Unsloth GPU 兼容性可能扩展到更多型号

Out of Scope Kept:
- 未写完整 RLHF 训练流程
- 未写数据准备详细步骤
- 未写分布式训练方案
