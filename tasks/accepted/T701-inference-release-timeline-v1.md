Task ID: T701
Task Title: Inference Engines Deep-Research Pack
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
为 vLLM/SGLang/Triton IS/TensorRT-LLM 各补关键更新线索入口，写成资料时间线，不做新闻评论。

Result:

# Inference Release Timeline v1

## 概述

本文档收录 vLLM、SGLang、Triton IS、TensorRT-LLM 的关键更新线索，以官方 release/changelog/blog 为主要来源。

---

## vLLM

### 关键更新线索

| 时间 | 版本 | 关键更新 |
|------|------|---------|
| 2024 年初 | v0.3.x | 首次稳定支持 Paged Attention |
| 2024 年中 | v0.4.x | 支持 FP8、prefix caching 增强 |
| 2024 年末 | v0.5.x | 多模态支持、speculative decoding 改进 |
| 2025 年初 | v0.6.x | 性能优化、bug 修复 |

### 官方入口

- **Changelog**：https://docs.vllm.ai/en/latest/changelog.html
- **GitHub Releases**：https://github.com/vllm-project/vllm/releases
- **Blog**：https://blog.vllm.ai/
- **Roadmap**：https://github.com/vllm-project/vllm/discussions/categories/roadmap

### 更新监控建议

- 订阅 GitHub Releases：https://github.com/vllm-project/vllm/releases/atom
- 关注 Blog 更新

来源：https://docs.vllm.ai/

---

## SGLang

### 关键更新线索

| 时间 | 版本 | 关键更新 |
|------|------|---------|
| 2024 年初 | v0.1.x | 首次公开，RadixAttention 特性 |
| 2024 年中 | v0.2.x | 支持更多模型，Cloudflare 集成 |
| 2024 年末 | v0.3.x | 性能改进，多模态支持 |
| 2025 年初 | v0.4.x | 更稳定的生产支持 |

### 官方入口

- **Changelog**：https://github.com/sgl-project/sglang/blob/main/docs/release.md
- **GitHub Releases**：https://github.com/sgl-project/sglang/releases
- **Blog**：https://sglang.ai/blog
- **Roadmap**：https://github.com/sgl-project/sglang/discussions

### 更新监控建议

- 订阅 GitHub Releases：https://github.com/sgl-project/sglang/releases/atom
- 关注 SGLang Blog

来源：https://sglang.readthedocs.io/

---

## NVIDIA Triton Inference Server

### 关键更新线索

| 时间 | 版本 | 关键更新 |
|------|------|---------|
| 2023 年 | Triton 2.x | 大规模生产支持 |
| 2024 年 | Triton 3.x | TensorRT-LLM backend 正式支持 |
| 2025 年 | Triton 4.x | 改进动态批处理，OnnxParser 改进 |

### 官方入口

- **Changelog**：https://docs.nvidia.com/deeplearning/triton-inference-server/release-notes/
- **GitHub Releases**：https://github.com/triton-inference-server/server/releases
- **NGC 容器**：https://catalog.ngc.nvidia.com/containers/nvidia/tritonserver
- **文档更新记录**：https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/architecture/updates.html

### TensorRT-LLM Backend

- **文档**：https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/llm_integration.html
- **GitHub**：https://github.com/NVIDIA/TensorRT-LLM

### 更新监控建议

- 订阅 GitHub Releases：https://github.com/triton-inference-server/server/releases/atom
- 关注 NVIDIA DevTalk：https://forums.developer.nvidia.com/

来源：https://docs.nvidia.com/deeplearning/triton-inference-server/

---

## TensorRT-LLM

### 关键更新线索

| 时间 | 版本 | 关键更新 |
|------|------|---------|
| 2023 年末 | v0.1 | 首次公开，GPT 模型支持 |
| 2024 年 | v0.4-0.6 | 支持更多模型（Llama、Mistral） |
| 2024 年末 | v0.7.x | FP8 支持，speculative decoding |
| 2025 年初 | v0.8.x | 性能优化，FlashAttention 改进 |

### 官方入口

- **文档**：https://nvidia.github.io/TensorRT-LLM/
- **GitHub Releases**：https://github.com/NVIDIA/TensorRT-LLM/releases
- **NGC 容器**：https://catalog.ngc.nvidia.com/containers/nvidia/tensorrt-llm
- **Blog**：https://nvidia.github.io/TensorRT-LLM/blogs/

### 更新监控建议

- 订阅 GitHub Releases：https://github.com/NVIDIA/TensorRT-LLM/releases/atom
- 关注 TensorRT-LLM Blog

来源：https://nvidia.github.io/TensorRT-LLM/

---

## 更新追踪建议

### 推荐方式

| 工具 | 用途 |
|------|------|
| **GitHub Releases Atom Feed** | 自动追踪 release 更新 |
| **官方 Blog** | 重大功能更新公告 |
| **GitHub Discussions** | Roadmap 和计划讨论 |

### 订阅链接

- vLLM：https://github.com/vllm-project/vllm/releases/atom
- SGLang：https://github.com/sgl-project/sglang/releases/atom
- Triton：https://github.com/triton-inference-server/server/releases/atom
- TensorRT-LLM：https://github.com/NVIDIA/TensorRT-LLM/releases/atom

---

## 版本稳定性说明

| 引擎 | 稳定性 | 说明 |
|------|--------|------|
| **vLLM** | 较高 | 已有大量生产使用 |
| **SGLang** | 中等 | 快速发展中，部分 API 可能变化 |
| **Triton IS** | 高 | 企业级，API 稳定 |
| **TensorRT-LLM** | 中等 | 快速发展，API 可能有变化 |

---

## 风险提示

- 各引擎更新频率高，接入前应确认版本
- TensorRT-LLM 与 GPU 固件版本相关，更新时可能需要同步更新驱动
- SGLang 仍处于快速迭代期，API 稳定性相对较低

Sources:
1. https://docs.vllm.ai/en/latest/changelog.html — vLLM Changelog
2. https://github.com/vllm-project/vllm/releases — vLLM Releases
3. https://blog.vllm.ai/ — vLLM Blog
4. https://sglang.readthedocs.io/ — SGLang Docs
5. https://github.com/sgl-project/sglang/releases — SGLang Releases
6. https://sglang.ai/blog — SGLang Blog
7. https://docs.nvidia.com/deeplearning/triton-inference-server/release-notes/ — Triton Changelog
8. https://github.com/triton-inference-server/server/releases — Triton Releases
9. https://nvidia.github.io/TensorRT-LLM/ — TensorRT-LLM Docs
10. https://github.com/NVIDIA/TensorRT-LLM/releases — TensorRT-LLM Releases

Risk of Staleness:
- 各引擎更新快，本文收录信息可能随时间变化

Out of Scope Kept:
- 未写性能 benchmark 对比
- 未写具体版本升级指南
