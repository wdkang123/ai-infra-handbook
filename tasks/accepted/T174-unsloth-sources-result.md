Task ID: T174
Task Title: 搜集 Unsloth 官方资料与核心链接
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
搜集 Unsloth 官方资料包，包含官方入口、核心定位、与 LoRA/QLoRA/PEFT 关系、最近更新线索、优先阅读链接。

Result:

## 一、官方入口

- **GitHub 主仓库**：https://github.com/unslothai/unsloth
- **官方主页**：https://unsloth.ai/
- **Notebooks 集合**：https://github.com/unslothai/notebooks
- **官方文档**：https://docs.unsloth.ai/

## 二、核心定位摘要

Unsloth 是一个专注于**加速 LLM 微调**的开源项目，核心价值：
- 提供优化过的 CUDA kernel，使 LoRA/QLoRA 微调速度提升 2x
- 显存占用减少约 50%（官方数据，实际效果因场景而异）
- 支持主流开源模型（Qwen、DeepSeek、Gemma、LLaMA 等）
- 提供免费的 Google Colab Notebooks，降低入门门槛

**Unsloth 不是完整的训练平台**，而是**微调加速层**，底层依赖 PyTorch、TRL（Hugging Face）、PEFT。

## 三、与 LoRA / QLoRA / PEFT 的关系

- Unsloth 使用 **LoRA 和 QLoRA** 作为微调方法（通过 PEFT 接口封装）
- Unsloth 通过自研 CUDA kernel **加速 LoRA/QLoRA 的训练阶段**（而非推理阶段）
- Unsloth 已被 **Hugging Face TRL** 集成，作为训练后端之一
- 关系图：PEFT（接口层）→ Unsloth/原生（加速层）→ PyTorch（计算层）

## 四、最近 6-12 个月更新线索（有精确来源的）

- **Unsloth 支持 DeepSeek V3 / Qwen 2.5 / Gemma 2** 等新模型
  - 来源：https://github.com/unslothai/unsloth
- **TRL 集成 Unsloth**：DPOTrainer、SFTTrainer 可使用 Unsloth 加速
  - 来源：https://github.com/huggingface/trl
- **llama.cpp 优化贡献**：Unsloth 团队也维护 llama.cpp 的 fork
  - 来源：https://github.com/unslothai/llama.cpp

## 五、精确优先阅读链接（6 个）

1. **Unsloth GitHub 主仓库**：https://github.com/unslothai/unsloth
2. **Unsloth 官方主页**：https://unsloth.ai/
3. **Unsloth Notebooks**：https://github.com/unslothai/notebooks
4. **Unsloth 文档**：https://docs.unsloth.ai/
5. **TRL GitHub（含 Unsloth 集成）**：https://github.com/huggingface/trl
6. **Unsloth llama.cpp fork**：https://github.com/unslothai/llama.cpp

Sources:
1. https://github.com/unslothai/unsloth — Unsloth 主仓库
2. https://unsloth.ai/ — Unsloth 官方主页
3. https://github.com/unslothai/notebooks — Notebooks 集合
4. https://docs.unsloth.ai/ — Unsloth 官方文档
5. https://github.com/huggingface/trl — TRL 主仓库（含 Unsloth 集成）
6. https://github.com/unslothai/llama.cpp — Unsloth llama.cpp fork

Risk of Staleness:
- Unsloth 版本更新快，官方 Notebooks 以实际安装版本为准
- 加速效果为官方数据，实际性能因模型、硬件、batch size 不同而有差异
- Unsloth 为独立项目，非 Hugging Face 官方产品

Out of Scope Kept:
- 未写完整训练章节
- 未与其他微调框架做优劣对比
- 未写结论排名
