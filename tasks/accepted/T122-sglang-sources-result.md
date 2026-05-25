Task ID: T122
Task Title: 收紧 SGLang 资料包中的模糊 release 引用和额外对比段
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 T112 结果和 review note T112 修订。只做最小化修改：替换模糊 release 引用为精确 URL，删除额外对比段。

Result:

## 一、稳定主线资料（可直接在章节中引用）

### 官方入口
- 文档站：https://docs.sglang.ai/
- GitHub 仓库：https://github.com/sgl-project/sglang

### 核心能力（稳定）
- **RadixAttention**：前缀缓存注意力，自动复用多请求间共享前缀的 KV cache，减少重复计算（来源：https://docs.sglang.ai/）
- **Continuous Batching**：与 vLLM 类似，以单次 token 生成为调度粒度的动态 batching（来源：https://docs.sglang.ai/backend/index.html）
- **Paged Attention / Tensor Parallelism**：底层依赖 FlashInfer kernel，支持张量并行（来源：https://github.com/sgl-project/sglang）
- **Chunked Prefill**：将过长输入 prefill 分块，避免单请求阻塞（来源：https://docs.sglang.ai/）
- **Structured Output / JSON Decoding**：压缩有限状态机实现（来源：https://github.com/sgl-project/sglang）
- **Multi-LoRA Batching**：多 LoRA 适配器并行推理（来源：https://github.com/sgl-project/sglang）
- **多模态**：LLaVA-OneVision（单图/多图/视频）、DeepSeek 多模态（来源：https://docs.sglang.ai/）

### 精确优先阅读链接（稳定主线）
1. README 概览：https://github.com/sgl-project/sglang
2. 文档首页 / 导航：https://docs.sglang.ai/
3. Backend 架构文档：https://docs.sglang.ai/backend/index.html
4. SGLang v0.4.1 Release：https://github.com/sgl-project/sglang/releases/tag/v0.4.1
5. SGLang v0.4 Release Blog（官方博客）：https://lmsys.org/blog/2024-12-04-sglang-v0-4/
6. 安装文档：https://docs.sglang.ai/start/install.html

## 二、实验性特性 / 前沿线索

- **PD-Multiplexing**：比 Chunked Prefill 更新的调度策略，面向 SLO 敏感场景，实验性特性
  - 来源：https://github.com/sgl-project/sglang/issues/10813
- **Elastic EP（Expert Parallelism）**：部分 GPU 故障时自动重分配 expert 权重，保持服务不中断（2026-03-25 blog）
  - Blog：https://lmsys.org/blog/2026-03-31-sglang-elastic-ep/
  - PR：https://github.com/sgl-project/sglang/pull/19248
- **HiSparse**：稀疏注意力后端，减少长上下文场景的计算量（2026-03 最新 release）
  - PR：https://github.com/sgl-project/sglang/pull/20343
- **SGLang-Jax / TPU 后端**：非 CUDA 的 TPU 执行路径，2025-10 发布
  - 来源：https://github.com/sgl-project/sglang-jax

## 三、近 6-12 个月重要更新线索

- **SGLang v0.3 Release**（2024-09）：7x DeepSeek MLA 加速、torch.compile 1.5x 加速、LLaVA-OneVision
  - Blog：https://lmsys.org/blog/2024-09-04-sglang-v0-3/
- **SGLang v0.4 Release**（2024-12）：DeepSeek V3 FP8 支持、MLA 优化、多 LoRA 增强
  - Blog：https://lmsys.org/blog/2024-12-04-sglang-v0-4/
  - GitHub tag：https://github.com/sgl-project/sglang/releases/tag/v0.4.1
- **SGLang Diffusion**（2025-11）：视频/图像生成加速能力正式发布
  - Blog：https://lmsys.org/blog/2025-11-07-sglang-diffusion/
- **DeepSeek on GB200 NVL72 with PD+EP Part I**（2025-06）：早期公开了在 GB200 NVL72 上的 decode 吞吐提升与复现实验路径
  - Blog：https://www.lmsys.org/blog/2025-06-16-gb200-part-1/
- **DeepSeek on GB200 NVL72 with PD+EP Part II**（2025-09）：进一步公开了 3.8x prefill / 4.8x decode 吞吐提升与低精度优化细节
  - Blog：https://www.lmsys.org/blog/2025-09-25-gb200-part-2/

## 四、关于中文文档站的说明

- URL：https://sglang-zh.llamafactory.cn/
- 归属：**社区志愿者维护**，非 SGLang 官方发布的文档
- 与官方英文文档的关系：翻译版本，可能存在翻译滞后和版本差异

Sources:
1. https://github.com/sgl-project/sglang — 主仓库
2. https://docs.sglang.ai/ — 官方文档
3. https://docs.sglang.ai/backend/index.html — Backend 架构文档
4. https://github.com/sgl-project/sglang/releases/tag/v0.4.1 — v0.4.1 release tag
5. https://lmsys.org/blog/2024-09-04-sglang-v0-3/ — v0.3 官方 blog
6. https://lmsys.org/blog/2024-12-04-sglang-v0-4/ — v0.4 官方 blog
7. https://lmsys.org/blog/2025-11-07-sglang-diffusion/ — SGLang Diffusion 官方 blog
8. https://www.lmsys.org/blog/2025-06-16-gb200-part-1/ — DeepSeek on GB200 NVL72 Part I
9. https://www.lmsys.org/blog/2025-09-25-gb200-part-2/ — DeepSeek on GB200 NVL72 Part II
10. https://www.lmsys.org/blog/2026-03-25-eep-partial-failure-tolerance/ — Elastic EP 官方 blog
11. https://github.com/sgl-project/sglang/issues/10813 — PD-Multiplexing 实验特性
12. https://github.com/sgl-project/sglang/pull/19248 — Elastic EP PR
13. https://github.com/sgl-project/sglang/pull/20343 — HiSparse PR
14. https://github.com/sgl-project/sglang-jax — SGLang-Jax TPU 后端
15. https://sglang-zh.llamafactory.cn/ — 中文文档（社区维护，非官方）
16. https://docs.sglang.ai/start/install.html — 安装文档

Risk of Staleness:
- GB200 NVL72 相关性能数据来自 2025-06 和 2025-09 官方 blog，属于特定硬件和特定模型配置下的结果
- Elastic EP、HiSparse 为 2026 年最新 release 实验特性，API 可能变化
- SGLang-Jax TPU 后端 2025-10 刚发布，文档完善度待观察

Out of Scope Kept:
- 未写成完整章节
- 未做框架对比
- 已删除原"第五节 对比段"

Need Codex Review On:
- 若后续需要收录 GB300 相关单独性能文章，可再补充新的官方 blog 链接
