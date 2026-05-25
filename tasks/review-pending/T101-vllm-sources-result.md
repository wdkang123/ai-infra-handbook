Task ID: T101
Task Title: vLLM 官方资料与核心链接搜集
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
在 AI Infra 学习路径中，为 vLLM 准备结构化资料包，包括官方主页、文档、GitHub、核心特性、近半年更新线索，以及章节写作优先阅读链接。

Result:

## 1. 官方主页
- 文档入口（主要）：https://docs.vllm.ai/
- 项目快照页（GitHub README）：https://github.com/vllm-project/vllm

## 2. GitHub 仓库
- 主仓库：https://github.com/vllm-project/vllm
- 官方描述：A high-throughput and memory-efficient inference and serving engine for LLMs
- Star 数（2026 初）：约 55k+，活跃度高

## 3. 核心特性概览
- **PagedAttention**：受 OS 虚拟内存分页思想启发的注意力算法，将 KV cache 分块存储在不连续显存中，减少碎片化，官方称显存利用率提升最高 4 倍
- **Continuous Batching（Iteration-level Scheduling）**：以单次生成 token 为调度粒度，动态插入新请求，榨干 GPU 利用率，吞吐量比 HuggingFace Transformers 高 14-24 倍
- **OpenAI 兼容 API**：天然兼容 OpenAI API 格式，降低迁移成本
- **多后端支持**：CUDA（主力）、ROCm、CPU（AVX512）、Neuron、Intel OpenVINO、华为昇腾 Ascend
- **量化支持**：FP8、INT8、AWQ、GPTQ 等
- **多 LoRA / VAE**：生产级部署常用的扩展能力

## 4. 近 6-12 个月值得关注的更新线索
- **v0.6.x 分支**（2024 中后期）：PagedAttention 实现持续优化，prefix caching 增强，FlashAttention 集成更新
- **vLLM-Omni 发布**（2025-12）：首个全模态推理框架，统一文本/图像/音频/视频生成流水，引入模态编码器+自回归 LLM 核心+模态生成器三层架构（来源：官方公告 / GitHub release）
- **安全漏洞修复**（GHSA-hj4w-hm2g-p6w5，2025-04）：Mooncake 集成中 ZeroMQ pickle 反序列化 RCE 漏洞，已在 v0.8.5 修复；使用 Mooncake 的部署需确认版本
- **vLLM-Ascend 插件**（2026-02 活跃）：社区维护的华为昇腾后端，独立仓库维护，有独立 CI

## 5. 章节写作优先阅读链接（5-8 个）

1. **README 概览** — https://github.com/vllm-project/vllm
   用途：快速了解项目定位、核心特性列表、支持的模型与硬件

2. **文档首页 / Getting Started** — https://docs.vllm.ai/en/latest/getting_started/installation.html
   用途：安装与快速上手，确认环境依赖（CUDA 版本、Python 版本等）

3. **PagedAttention 论文 / 官方 blog 介绍** — https://www.vllm.ai/
   用途：理解 vLLM 最核心的创新来源，掌握其显存管理思想的历史脉络

4. **Serving Architecture 文档** — https://docs.vllm.ai/en/latest/design/architecture.html
   用途：了解 scheduler、worker、model runner 的分层，是写推理服务章节的结构基础

5. **AsyncLLMEngine / OpenAI API 文档** — https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html
   用途：理解 vLLM 的服务接口设计，掌握与标准 AI Gateway 对接的方式

6. **Changelog / Release 页面** — https://github.com/vllm-project/vllm/releases
   用途：追踪版本演进，特别是新特性添加与 breaking change，适合写"近况"小节

7. **vLLM-Omni 公告** — https://github.com/vllm-project/vllm/releases （搜索 "Omni"）
   用途：了解多模态融合推理的最新方向，帮助判断 vLLM 未来在 AI Infra 栈中的位置

8. **GHSA 安全公告** — https://github.com/vllm-project/vllm/security/advisories
   用途：了解部署安全红线，特别是 Mooncake 用户的版本要求

Sources:
1. https://docs.vllm.ai/ — vLLM 官方文档
2. https://github.com/vllm-project/vllm — 主仓库（含 README / release）
3. https://www.vllm.ai/ — PagedAttention 官方介绍 blog
4. https://github.com/vllm-project/vllm/security/advisories/GHSA-hj4w-hm2g-p6w5 — 安全公告
5. https://github.com/vllm-project/vllm-ascend — 昇腾后端插件
6. https://docs.sglang.ai/ — SGLang 文档（用于对照 vLLM 特性定位，非对比结论）

Risk of Staleness:
- 版本号相关：pip install 的默认版本可能随时间变化，README 中支持的 GPU 列表以实际版本为准
- 安全漏洞：Mooncake RCE 漏洞描述基于 2025-04 公告，需确认部署环境实际版本
- vLLM-Omni 发布细节（2025-12）：新项目，进化速度快，文档可能已更新
- 文档站点的 API 路径（`/en/latest/`）在 major 版本升级时可能变化

Out of Scope Kept:
- 未写成完整 vLLM 章节
- 未做 vLLM vs SGLang / Triton 深度对比
- 未包含部署教程

Need Codex Review On:
- "14-24 倍吞吐量"数字来自官方早期 blog，Codex 需确认在当前版本（0.6.x+）是否仍可引用
- TPU/昇腾等非主流后端是否需要纳入章节定位判断
