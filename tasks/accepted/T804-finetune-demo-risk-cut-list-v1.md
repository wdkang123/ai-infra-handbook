# finetune-demo Risk Cut List v1

## Task ID: T804
## Task Title: finetune-demo Execution Prep Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T713 决策 memo，准备 finetune-demo 实施前包。

---

# finetune-demo Risk Cut List v1

## 概述

本文档定义 finetune-demo 的主要风险和缓解措施，供 Codex 实施前参考。

---

## 风险清单

| 风险 ID | 风险描述 | 影响 | 概率 | 缓解措施 |
|---------|---------|------|------|---------|
| R-01 | GPU 显存不足导致 OOM | 高 | 高 | 使用 QLoRA；降低 batch_size |
| R-02 | LoRA 超参数敏感导致效果差 | 中 | 中 | 参考默认参数；从小 r 开始 |
| R-03 | PEFT/TRL API 变更 | 中 | 低 | 锁定版本；Mock 测试 |
| R-04 | Unsloth GPU 兼容性问题 | 中 | 中 | 确认 GPU 型号；备选 PEFT |
| R-05 | DPO 数据成本被低估 | 高 | 高 | MVP 不进入 DPO |

---

## 风险详解

### R-01：GPU 显存不足

**风险描述**：LoRA/QLoRA 训练显存需求超出实际硬件。

**影响**：训练失败，OOM。

**缓解措施**：
- 使用 QLoRA 4-bit 量化
- 降低 `per_device_train_batch_size`（从 4 → 2 → 1）
- 降低 `gradient_accumulation_steps`
- 使用更小的模型（0.5B/1B）

**显存估算**：
- QLoRA 7B：~5GB
- QLoRA 13B：~10GB
- LoRA 7B：~16GB

来源：https://arxiv.org/abs/2305.14314

---

### R-02：LoRA 超参数敏感

**风险描述**：LoRA 的 r/alpha 对效果影响大。

**影响**：训练效果不佳。

**缓解措施**：
- MVP 使用默认参数（r=16, alpha=32）
- 先跑小规模测试验证
- 参考 PEFT 官方示例

**推荐起始参数**：
```yaml
lora:
  r: 16
  lora_alpha: 32
  target_modules: ["q_proj", "v_proj"]
```

来源：https://arxiv.org/abs/2106.09685

---

### R-03：PEFT/TRL API 变更

**风险描述**：PEFT 或 TRL 版本更新导致 API 不兼容。

**影响**：需要修改代码。

**缓解措施**：
- 锁定版本：`peft>=0.10.0,<0.11.0`，`trl>=0.8.0,<0.9.0`
- 单元测试 Mock 外部依赖
- 参考官方 examples

来源：https://github.com/huggingface/peft
来源：https://github.com/huggingface/trl

---

### R-04：Unsloth GPU 兼容性

**风险描述**：Unsloth 只支持 Ampere/Hopper GPU。

**影响**：非兼容 GPU 无法使用加速。

**缓解措施**：
- 先确认 GPU 型号：`nvidia-smi`
- 不兼容时使用 PEFT 原生实现
- 备选：降低模型大小或 batch_size

**GPU 兼容性**：
| GPU 系列 | Unsloth 支持 |
|---------|-------------|
| Ampere (RTX 30xx, A100) | 是 |
| Hopper (H100) | 是 |
| Turing (RTX 20xx) | 否 |
| 其他 | 否 |

来源：https://github.com/unslothai/unsloth

---

### R-05：DPO 数据成本被低估

**风险描述**：DPO 需要高质量偏好数据集，标注成本高。

**影响**：DPO 无法在 MVP 阶段落地。

**缓解措施**：
- MVP 不实现 DPO
- MVP 之后评估 DPO 需求
- 如需要 DPO，先准备数据集

来源：https://arxiv.org/abs/2305.18290

---

## MVP 阶段必须规避的风险

| 风险 | 规避措施 |
|------|---------|
| GPU OOM | 使用 QLoRA + 小模型 |
| 效果差 | 从默认参数开始 |
| 加速不可用 | 备选 PEFT 原生 |

---

## 风险决策点

| 决策点 | 选项 | 建议 |
|--------|------|------|
| 默认微调方法 | LoRA / QLoRA | QLoRA（MVP） |
| Unsloth 引入 | 是 / 否 | GPU 确认后决定 |
| DPO 引入 | MVP 否 | MVP 不进入 |
| 模型大小 | 0.5B / 3B / 7B | 0.5B（MVP） |

---

Sources:
1. https://arxiv.org/abs/2106.09685 — LoRA
2. https://arxiv.org/abs/2305.14314 — QLoRA
3. https://arxiv.org/abs/2305.18290 — DPO
4. https://github.com/huggingface/peft — PEFT
5. https://github.com/huggingface/trl — TRL
6. https://github.com/unslothai/unsloth — Unsloth

Risk of Staleness:
- LoRA 超参数最佳实践可能随新研究更新

Out of Scope Kept:
- 未写完整应急预案
- 未写数据准备流程
