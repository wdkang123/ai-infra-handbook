Task ID: T102
Task Title: SGLang 官方资料与核心链接搜集
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
在 AI Infra 学习路径中，为 SGLang 准备结构化资料包，包括官方主页、文档、GitHub、核心能力、近况更新，以及章节写作优先阅读链接。

Result:

## 1. 官方主页 / 文档入口
- 文档站：https://docs.sglang.ai/
- GitHub 仓库：https://github.com/sgl-project/sglang

## 2. GitHub 仓库
- 主仓库：https://github.com/sgl-project/sglang
- 官方描述：A high-performance serving framework for large language models and multimodal models
- Star 数（2026 初）：约 14k+，增长较快
- 官方维护的中文文档（部分）：https://sglang-zh.llamafactory.cn/

## 3. 核心能力摘要
- **RadixAttention**：前缀缓存注意力，在多请求共享前缀场景（如 system prompt、few-shot examples）下自动复用 KV cache，减少重复计算，官方称带来 5x 加速
- **Prefill-Decode Disaggregation（PD 分离）**：将 prefill（输入处理）和 decode（逐 token 生成）部署在不同 GPU 节点，2025-09 起支持大规模 Expert Parallelism（EP）
- **Continuous Batching + Paged Attention**：和 vLLM 类似的支持，底层依赖 FlashInfer 等高效 kernel
- **Chunked Prefill**：将过长输入的 prefill 分块，避免单请求阻塞排队延迟
- **Speculative Decoding**：加速生成质量
- **Multi-LoRA Batching**：多 LoRA 适配器并行推理
- **Structured Output / JSON Decoding**：压缩有限状态机实现 3x JSON 解码加速
- **多后端**：NVIDIA GPU（主力）、AMD ROCm、Intel CPU（via sglang-llamafactory）、TPU（via SGLang-Jax backend，2025-10）
- **多模态支持**：LLaVA-OneVision（单图/多图/视频）、DeepSeek 多模态、Diffusion（WAN、Qwen-Image）

## 4. 近 6-12 个月值得关注的更新线索
- **GB300 NVL72 性能突破**（2026-02）：官方 blog 宣布在 NVIDIA GB300 NVL72 上达到 25x 推理性能提升，标题为 "Unlocking 25x Inference Performance with SGLang"
- **SGLang Diffusion**（2026-01）：视频/图像生成加速能力正式发布
- **SGLang-Jax / TPU 支持**（2025-10）：SGLang 原生运行在 TPU 上，不再仅依赖 CUDA
- **DeepSeek on GB200 NVL72 with PD+EP**（2025-09）：PD 分离 + 大规模 Expert Parallelism 结合，Prefill 3.8x、Decode Throughput 4.8x 提升
- **PD-Multiplexing**（2025-09 活跃）：比 ChunkPrefill 更新的调度策略，实验性特性，面向 SLO 敏感场景
- **v0.4 → v0.5 版本演进**：2024 下半年快速迭代，LoRA 支持、多模态显著增强

## 5. 章节写作优先阅读链接（5-8 个）

1. **README 概览** — https://github.com/sgl-project/sglang
   用途：项目定位、核心特性列表（RadixAttention、PD 分离、连续批处理等）、新手指南

2. **文档首页** — https://docs.sglang.ai/index.html
   用途：导航到各子章节，了解文档结构与覆盖范围

3. **Architecture / Backend 文档** — https://docs.sglang.ai/backend/index.html
   用途：理解 SGLang 运行时内部结构，适合写框架对比时的结构化描述

4. **RadixAttention Blog** — https://github.com/sgl-project/sglang （README 或 blog 链接）
   用途：理解 SGLang 区别于 vLLM 的核心差异点——前缀缓存机制

5. **GB300 25x Performance Blog**（2026-02）— https://github.com/sgl-project/sglang/releases 或官方 blog
   用途：SGLang 最新性能里程碑，反映硬件协同设计方向

6. **DeepSeek + GB200 PD+EP Blog**（2025-09）— https://github.com/sgl-project/sglang/releases
   用途：理解 PD 分离与 Expert Parallelism 的工程落地，是推理服务分布式设计的参考

7. **PD-Multiplexing Issue** — https://github.com/sgl-project/sglang/issues/10813
   用途：理解 SGLang 调度器的演进方向，调度策略的实验状态

8. **LLaVA-OneVision 支持 Blog**（2024-08）— https://github.com/sgl-project/sglang
   用途：多模态服务路径，SGLang 在视觉语言模型上的能力边界

Sources:
1. https://docs.sglang.ai/ — SGLang 官方文档
2. https://github.com/sgl-project/sglang — 主仓库（含 README / releases / issues）
3. https://sglang-zh.llamafactory.cn/ — 中文文档（社区维护，部分内容可能滞后）
4. https://github.com/sgl-project/sglang/issues/10813 — PD-Multiplexing 设计与 benchmark
5. https://docs.sglang.ai/backend/index.html — 后端架构文档
6. https://github.com/sgl-project/sglang/tree/main/sgl-kernel — sgl-kernel 自研 kernel

Risk of Staleness:
- GB300 25x 性能数据来自 2026-02 早期 blog，实际部署效果取决于硬件配置与模型
- PD-Multiplexing 仍在实验阶段（issue #10813），API 和行为可能变化
- TPU 后端（SGLang-Jax）2025-10 才发布，稳定性与文档完善度待观察
- 版本号（v0.4/v0.5）与当前最新版本需以 pip install 的实际版本为准

Out of Scope Kept:
- 未写成完整 SGLang 章节
- 未做 benchmark 优劣结论
- 未比较所有推理框架

Need Codex Review On:
- "5x RadixAttention 加速"来自 2024-01 blog，Codex 需判断在当前版本和真实生产场景下是否仍可引用
- TPU 后端对 AI Infra 章节定位的影响——是否需要单独说明非 NVIDIA 路径
