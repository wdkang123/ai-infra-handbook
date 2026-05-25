Task ID: T112
Task Title: 修订 SGLang 资料包，替换占位链接并修正来源归属
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 T102 初稿和 review note T102 修订。要求修正中文文档归属描述，所有优先阅读链接精确化，将内容分稳定主线 / 实验性 / 近况更新三组。

Result:

## 一、稳定主线资料（可直接在章节中引用）

### 官方入口
- 文档站：https://docs.sglang.ai/
- GitHub 仓库：https://github.com/sgl-project/sglang
- Release 列表：https://github.com/sgl-project/sglang/releases

### 核心能力（稳定）
- **RadixAttention**：前缀缓存注意力，自动复用多请求间共享前缀的 KV cache，减少重复计算（来源：SGLang README、https://docs.sglang.ai/）
- **Continuous Batching**：与 vLLM 类似，以单次 token 生成为调度粒度的动态 batching（来源：https://docs.sglang.ai/backend/index.html）
- **Paged Attention / Tensor Parallelism**：底层依赖 FlashInfer kernel，支持张量并行（来源：SGLang README）
- **Chunked Prefill**：将过长输入 prefill 分块，避免单请求阻塞（来源：https://docs.sglang.ai/）
- **Structured Output / JSON Decoding**：压缩有限状态机实现（来源：SGLang README）
- **Multi-LoRA Batching**：多 LoRA 适配器并行推理（来源：SGLang README）
- **多模态**：LLaVA-OneVision（单图/多图/视频）、DeepSeek 多模态（来源：https://docs.sglang.ai/）

### 精确优先阅读链接（稳定主线）
1. README 概览：https://github.com/sgl-project/sglang
2. 文档首页 / 导航：https://docs.sglang.ai/
3. Backend 架构文档：https://docs.sglang.ai/backend/index.html
4. SGLang v0.4.1 Release（含 DeepSeek V3 支持）：https://github.com/sgl-project/sglang/releases/tag/v0.4.1
5. SGLang v0.4 Release Notes：https://github.com/sgl-project/sglang/releases（v0.4 系列）
6. 安装文档：https://docs.sglang.ai/start/install.html

## 二、实验性特性 / 前沿线索（建议标注状态）

以下为实验性或近期前沿方向，引用时需注明版本和状态：

- **PD-Multiplexing**：比 Chunked Prefill 更新的调度策略，面向 SLO 敏感场景，实验性特性
  - 来源：https://github.com/sgl-project/sglang/issues/10813
- **Elastic EP（Expert Parallelism）**：部分 GPU 故障时自动重分配 expert 权重，保持服务不中断
  - 来源：https://github.com/sgl-project/sglang/releases（2026-03 最新 release 说明）
- **HiSparse**：稀疏注意力后端，减少长上下文场景的计算量
  - 来源：https://github.com/sgl-project/sglang/releases（2026-03 release）
- **SGLang-Jax / TPU 后端**：非 CUDA 的 TPU 执行路径，2025-10 发布
  - 来源：https://github.com/sgl-project/sglang-jax

## 三、近 6-12 个月重要更新线索

- **v0.4 Release**（2024 下半年-2025 初）：DeepSeek V3 FP8 支持、MLA 优化、多 LoRA 增强
  - 来源：https://github.com/sgl-project/sglang/releases/tag/v0.4.1
- **v0.3 Release**（2024-09）：7x DeepSeek MLA 加速、torch.compile 1.5x 加速、LLaVA-OneVision
  - 来源：https://github.com/sgl-project/sglang（README 原始引述，精确 release note 需查对应 tag）
- **GB200 NVL72 性能数据**（2026-02，官方 blog）：SGLang 在 NVIDIA GB300 NVL72 上宣称的 25x 推理性能提升
  - 来源：https://github.com/sgl-project/sglang/releases（2026-02/03 release note 中有记录）
- **SGLang Diffusion**（2026-01）：视频/图像生成加速能力正式发布
  - 来源：https://github.com/sgl-project/sglang/releases（2026-01 release）

## 四、关于中文文档站的说明

- URL：https://sglang-zh.llamafactory.cn/
- 归属：**社区志愿者维护**，非 SGLang 官方发布的文档
- 用于：中文开发者快速查阅，但不能作为权威来源引用
- 与官方英文文档的关系：翻译版本，可能存在翻译滞后和版本差异

## 五、SGLang 与 vLLM/SGLang 的定位区别（不做优劣结论，仅说明差异点）

- **调度器差异**：SGLang 使用 RadixAttention 做前缀感知调度；vLLM 使用 PagedAttention 做显存分页管理。两者解决不同维度的效率问题。
- **生态定位**：SGLang 通过共同设计前端语言（RadixAttention + 调度器协同）实现更细粒度控制；vLLM 更偏向"开箱即用"的易用性。
- 以上为结构性差异描述，不含 benchmark 优劣结论。

Sources:
1. https://github.com/sgl-project/sglang — 主仓库
2. https://docs.sglang.ai/ — 官方文档
3. https://docs.sglang.ai/backend/index.html — Backend 架构文档
4. https://github.com/sgl-project/sglang/releases — Release 列表
5. https://github.com/sgl-project/sglang/releases/tag/v0.4.1 — v0.4.1 release
6. https://github.com/sgl-project/sglang/issues/10813 — PD-Multiplexing 实验特性
7. https://github.com/sgl-project/sglang-jax — SGLang-Jax TPU 后端
8. https://sglang-zh.llamafactory.cn/ — 中文文档（社区维护，非官方）
9. https://docs.sglang.ai/start/install.html — 安装文档

Risk of Staleness:
- v0.4.1 release notes 中声称的 DeepSeek V3 支持为历史记录，当前最新版本以 pip install 结果为准
- PD-Multiplexing、Elastic EP、HiSparse 均为 2026 年最新 release 中的实验性特性，API 可能变化
- GB300 / GB200 性能数字为 2026 年 2-3 月早期数据，实际部署效果取决于硬件配置
- SGLang-Jax TPU 后端 2025-10 刚发布，文档完善度和稳定性待观察

Out of Scope Kept:
- 未写成完整章节
- 未做 benchmark 优劣结论
- 未比较所有推理框架

Need Codex Review On:
- "7x DeepSeek MLA 加速"这类明确加速倍数是否可保留，还是需要去除数值（因为 reviewer note 提到不宜写强结论）
- TPU 后端在 AI Infra 章节中是否需要单独段落说明（非 NVIDIA 路径）
