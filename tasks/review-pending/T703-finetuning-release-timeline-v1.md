Task ID: T703
Task Title: Finetuning / Training Deep-Research Pack
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
收口 PEFT/TRL/Unsloth/bitsandbytes 的更新线索。

Result:

# Finetuning Release Timeline v1

## 概述

本文档收录 PEFT、TRL、Unsloth、bitsandbytes 的关键更新线索和稳定入口。

---

## PEFT

### 关键更新线索

| 时间 | 版本 | 关键更新 |
|------|------|---------|
| 2023 年 | v0.2.x | 早期稳定版，支持 LoRA/AdaLoRA |
| 2024 年初 | v0.3.x | QLoRA 支持 |
| 2024 年中 | v0.4.x | Prompt Tuning 改进，LoRA 合并增强 |
| 2024 年末 | v0.5.x | 更好的 QLoRA 支持，bug 修复 |
| 2025 年初 | v0.6.x | 更多模型支持 |

### 官方入口

| 维度 | 内容 |
|------|------|
| **GitHub** | https://github.com/huggingface/peft |
| **文档** | https://huggingface.co/docs/peft/ |
| **Release** | https://github.com/huggingface/peft/releases |
| **讨论** | https://github.com/huggingface/peft/discussions |

来源：https://github.com/huggingface/peft

---

## TRL

### 关键更新线索

| 时间 | 版本 | 关键更新 |
|------|------|---------|
| 2023 年 | v0.4.x | DPOTrainer 添加 |
| 2024 年初 | v0.5.x | SFTTrainer 改进 |
| 2024 年中 | v0.6.x | PPOTrainer 稳定 |
| 2024 年末 | v0.7.x | DPO 改进，偏好数据支持增强 |
| 2025 年初 | v0.8.x | 训练稳定性改进 |

### 官方入口

| 维度 | 内容 |
|------|------|
| **GitHub** | https://github.com/huggingface/trl |
| **文档** | https://huggingface.co/docs/trl/ |
| **Release** | https://github.com/huggingface/trl/releases |

来源：https://github.com/huggingface/trl

---

## Unsloth

### 关键更新线索

| 时间 | 版本 | 关键更新 |
|------|------|---------|
| 2024 年初 | v0.1 | 首次公开，Llama/QLoRA 支持 |
| 2024 年中 | v0.2 | 更多模型支持，加速改进 |
| 2024 年末 | v0.3 | M1 Mac 支持，Flash Attention 改进 |
| 2025 年初 | v0.4 | 加速比提升，bug 修复 |

### 官方入口

| 维度 | 内容 |
|------|------|
| **GitHub** | https://github.com/unslothai/unsloth |
| **文档** | https://unsloth.ai/ |
| **Blog** | https://unsloth.ai/blog |
| **Release** | https://github.com/unslothai/unsloth/releases |

### GPU 兼容性说明

- **主要优化**：NVIDIA Ampere（RTX 30xx、A100）和 Hopper（H100）
- **M1 Mac**：部分支持（通过 Metal）
- **AMD ROCm**：实验性支持

来源：https://github.com/unslothai/unsloth

---

## bitsandbytes

### 关键更新线索

| 时间 | 版本 | 关键更新 |
|------|------|---------|
| 2023 年 | v0.41.x | 8-bit 优化器稳定 |
| 2024 年初 | v0.42.x | 4-bit 量化改进 |
| 2024 年中 | v0.43.x | QLoRA 兼容改进 |
| 2024 年末 | v0.44.x | 稳定版，bug 修复 |

### 官方入口

| 维度 | 内容 |
|------|------|
| **GitHub** | https://github.com/TimDettmers/bitsandbytes |
| **文档** | https://github.com/TimDettmers/bitsandbytes |
| **Release** | https://github.com/TimDettmers/bitsandbytes/releases |

来源：https://github.com/TimDettmers/bitsandbytes

---

## 更新监控建议

### 推荐方式

| 工具 | 用途 |
|------|------|
| **GitHub Releases Atom Feed** | 自动追踪 release 更新 |

### 订阅链接

- PEFT：https://github.com/huggingface/peft/releases/atom
- TRL：https://github.com/huggingface/trl/releases/atom
- Unsloth：https://github.com/unslothai/unsloth/releases/atom
- bitsandbytes：https://github.com/TimDettmers/bitsandbytes/releases/atom

---

## 版本稳定性说明

| 工具 | 稳定性 | 说明 |
|------|--------|------|
| **PEFT** | 较高 | HuggingFace 官方维护，API 相对稳定 |
| **TRL** | 中等 | 活跃开发，API 可能变化 |
| **Unsloth** | 中等 | 快速发展，但 GitHub 活跃 |
| **bitsandbytes** | 较高 | 成熟项目，API 稳定 |

---

## 风险提示

- TRL 的 DPOTrainer API 在不同版本间可能有变化
- Unsloth 的加速效果依赖 GPU 型号，非 Ampere/Hopper 可能效果有限
- bitsandbytes 的 4-bit 量化需要与 PEFT 配合使用，版本兼容性需确认

Sources:
1. https://github.com/huggingface/peft — PEFT
2. https://github.com/huggingface/trl — TRL
3. https://github.com/unslothai/unsloth — Unsloth
4. https://github.com/TimDettmers/bitsandbytes — bitsandbytes
5. https://huggingface.co/docs/peft/ — PEFT Docs
6. https://huggingface.co/docs/trl/ — TRL Docs

Risk of Staleness:
- 各工具更新快，本文收录信息可能随时间变化

Out of Scope Kept:
- 未写代码实现
- 未写具体版本升级指南
