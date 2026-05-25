Task ID: T165
Task Title: 产出 finetuning sources-index v1
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 T173（LoRA/QLoRA/PEFT）、T174（Unsloth）收紧版，产出 finetuning sources-index v1。

Result:

## PEFT / LoRA / QLoRA

### 官方入口

- LoRA 原始论文：https://arxiv.org/abs/2106.09685
- QLoRA 原始论文：https://arxiv.org/abs/2305.14314
- Hugging Face PEFT：https://github.com/huggingface/peft
- Hugging Face TRL：https://github.com/huggingface/trl
- LoRA 官方 GitHub：https://github.com/microsoft/LoRA
- QLoRA 官方 GitHub：https://github.com/artidoro/qlora

### 边界说明
LoRA 是底层参数高效微调方法，QLoRA 是 LoRA + 4-bit 量化，PEFT 是 Hugging Face 维护的统一框架封装这些方法。Unsloth 是在 PEFT 接口下加速训练的内核。

### 优先阅读链接（5 个）

1. **LoRA 论文** — https://arxiv.org/abs/2106.09685
2. **QLoRA 论文** — https://arxiv.org/abs/2305.14314
3. **PEFT GitHub** — https://github.com/huggingface/peft
4. **TRL GitHub** — https://github.com/huggingface/trl
5. **LoRA 官方 GitHub** — https://github.com/microsoft/LoRA

---

## Unsloth

### 官方入口

- GitHub 主仓库：https://github.com/unslothai/unsloth
- 官方主页：https://unsloth.ai/
- Notebooks 集合：https://github.com/unslothai/notebooks
- 官方文档：https://docs.unsloth.ai/

### 边界说明
Unsloth 是微调加速层，不是完整训练平台。通过自研 CUDA kernel 加速 LoRA/QLoRA 训练，速度提升 2x、显存减半。底层依赖 PEFT/TRL/PyTorch。

### 优先阅读链接（4 个）

1. **Unsloth GitHub** — https://github.com/unslothai/unsloth
2. **Unsloth 官方主页** — https://unsloth.ai/
3. **Unsloth Notebooks** — https://github.com/unslothai/notebooks
4. **Unsloth 文档** — https://docs.unsloth.ai/

Sources:
1. https://arxiv.org/abs/2106.09685 — LoRA 原始论文
2. https://arxiv.org/abs/2305.14314 — QLoRA 原始论文
3. https://github.com/huggingface/peft — PEFT 主仓库
4. https://github.com/huggingface/trl — TRL 主仓库
5. https://github.com/microsoft/LoRA — LoRA 官方仓库
6. https://github.com/artidoro/qlora — QLoRA 官方仓库
7. https://github.com/unslothai/unsloth — Unsloth 主仓库
8. https://unsloth.ai/ — Unsloth 官方主页
9. https://github.com/unslothai/notebooks — Notebooks 集合
10. https://docs.unsloth.ai/ — Unsloth 官方文档

Risk of Staleness:
- PEFT 库版本更新快，具体 API 以实际安装版本为准
- Unsloth 版本以实际安装时为准

Out of Scope Kept:
- 未写训练教程
- 未扩写成章节
