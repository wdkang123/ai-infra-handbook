Task ID: T103
Task Title: Triton 官方资料与核心链接搜集
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
在推理服务栈中为 Triton 准备结构化资料包，包括官方主页、文档、GitHub、核心定位、近况更新，以及章节写作优先阅读链接。

Result:

## 1. 官方主页 / 文档入口
- 官方文档站（英文）：https://triton-lang.org/
- 官方文档（主路径）：https://www.triton-lang.org/ 或 https://triton.readthedocs.io/
- Triton 中文站（社区维护）：https://triton.hyper.ai/
- GitHub 仓库：https://github.com/triton-lang/triton

## 2. GitHub 仓库
- 主仓库（triton-lang/triton）：https://github.com/triton-lang/triton
- 官方描述：A language and compiler for writing highly efficient custom Deep-Learning primitives
- Star 数（2026 初）：约 12k+
- 已从 OpenAI 迁移至 triton-lang 组织名下维护（2024 年中完成组织迁移）

## 3. 核心定位摘要
Triton 是 OpenAI 推出的以 Python 为编程界面、面向 DNN 自定义算子开发的编译器。其核心定位是：
- **降低 GPU 高性能算子开发门槛**：让无 CUDA 背景的研究者也能写出接近专家水平的 kernel
- **Tiled 计算抽象**：将矩阵乘法等操作分解为"块"（tile），编译器自动生成并行代码
- **多芯片支持**：NVIDIA（主力）、AMD ROCm、Intel CPU（triton-cpu 分支）、Qualcomm 等
- **生态系统位置**：FlashAttention、Unsloth、Liger-Kernel、FlagGems 等多个高性能库基于 Triton 构建；PyTorch 2.0+ 的 `torch.compile` 也利用了 Triton 生态

## 4. 近 6-12 个月值得关注的更新线索
- **Triton Conference 2025**（2025-10-21）：第三届开发者大会在微软硅谷园区举办，材料已上网；议程涵盖编译器改进、新后端支持、生产落地案例
- **Triton-CPU 分支持续活跃**（2024 下半年至 2025）：triton-cpu 作为独立长期分支开发，推进 CPU 后端生产可用性
- **多芯片生态扩展**：AMD ROCm 支持逐步成熟，Qualcomm 等非 NVIDIA 芯片后端在路线图上
- **版本迭代**：pip install triton（稳定版）vs pip install triton-nightly（每夜版），API 变化集中在 2.x-3.x 过渡期
- **Liger-Kernel 等训练 kernel 集合**（2025）：LinkedIn 开源的 Liger-Kernel 宣称 20% 训练吞吐提升、60% 内存降低，展示了 Triton 在训练侧的实用价值

## 5. 章节写作优先阅读链接（5-8 个）

1. **Triton 官方介绍 Blog** — https://openai.com/blog/triton/
   用途：OpenAI 官方发布公告，理解 Triton 创世动机与核心设计哲学（"比 CUDA 生产力高，比 DSL 灵活"）

2. **Triton 论文**（MAPL 2019）：https://dl.acm.org/doi/10.1145/3315508.3329973
   用途：理解 Triton IR 和 tile-based 计算模型，是读懂编译器行为的基础参考文献

3. **官方文档首页 / Tutorials** — https://www.triton-lang.org/
   用途：安装指南、快速上手教程，适合了解 Triton 代码风格

4. **Triton Conference 2025 材料** — https://github.com/triton-lang/triton （Conference 信息）
   用途：最新生态进展、实战案例、生产环境部署经验

5. **GitHub README** — https://github.com/triton-lang/triton
   用途：项目当前状态、nightly/stable 版本说明、依赖关系

6. **Triton-CPU 分支** — https://github.com/triton-lang/triton-cpu
   用途：了解 CPU 后端当前成熟度，判断是否适合作为章节补充方向

7. **Liger-Kernel GitHub** — https://github.com/linkedin/Liger-Kernel
   用途：Triton 在训练侧高性能 kernel 的实际案例，展示 Triton 在 AI Infra 栈中的下游依赖

8. **Triton Conference 2024 材料**（上届）：https://github.com/triton-lang/triton 或官方存档
   用途：对照了解一年间 Triton 的变化方向

Sources:
1. https://openai.com/blog/triton/ — OpenAI 官方发布 blog
2. https://github.com/triton-lang/triton — 主仓库（含 README / releases / conference 信息）
3. https://triton.hyper.ai/ — 中文文档（HyperAI 社区维护，内容相对完整）
4. https://dl.acm.org/doi/10.1145/3315508.3329973 — Triton 原始论文
5. https://github.com/linkedin/Liger-Kernel — Liger-Kernel（训练 kernel 案例）
6. https://github.com/triton-lang/triton-cpu — CPU 后端独立分支

Risk of Staleness:
- Triton Conference 2025 材料刚发布，具体演讲录像和 slide 质量参差不齐
- triton-nightly 版本 API 不稳定，文档与实际安装版本可能存在差异
- triton-lang 组织迁移后，部分旧链接（openai/triton）已重定向，需确认使用新组织下的路径
- CPU 后端（triton-cpu）仍为实验分支，生产使用前需确认版本

Out of Scope Kept:
- 未写成完整 Triton 章节
- 未做 vLLM/SGLang vs Triton 优劣结论
- 未写部署教程

Need Codex Review On:
- "Liger-Kernel 20% 吞吐"数字来自 LinkedIn 官方公告，Codex 需确认在目标场景（而非全部场景）下的适用性
- Triton 在推理服务栈中的具体切入位置——是 kernel 实现层、compiler 层还是独立章节，需要 Codex 做架构判断
