Task ID: T147
Task Title: 产出 inference stack sources-index v1
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 T111、T122、T113 三个已通过资料包，产出 inference stack 资料索引 v1，包含组件名、官方主页/GitHub、优先阅读链接（3 条/组件）及用途说明。

Result:

## vLLM

### 官方入口
- 文档站：https://docs.vllm.ai/
- GitHub 仓库：https://github.com/vllm-project/vllm

### 优先阅读链接（3 条）

1. **README 概览** — https://github.com/vllm-project/vllm
   用途：快速了解项目定位、核心特性列表、支持模型与硬件

2. **Architecture 文档** — https://docs.vllm.ai/en/latest/design/architecture.html
   用途：理解 vLLM 内部架构（scheduler、worker、model runner 分层），是写推理服务章节的结构基础

3. **OpenAI 兼容接口文档** — https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html
   用途：掌握 API 形态，是 AI Gateway 对接的标准接口

## SGLang

### 官方入口
- 文档站：https://docs.sglang.ai/
- GitHub 仓库：https://github.com/sgl-project/sglang

### 优先阅读链接（3 条）

1. **README 概览** — https://github.com/sgl-project/sglang
   用途：项目定位、核心特性（RadixAttention、PD 分离、多模态）、新手指南

2. **Backend 架构文档** — https://docs.sglang.ai/backend/index.html
   用途：理解 SGLang 运行时内部结构和调度策略

3. **安装文档** — https://docs.sglang.ai/start/install.html
   用途：快速上手 SGLang，包含 pip/源码/docker 多种安装方式

## NVIDIA Triton Inference Server

### 官方入口
- 文档站：https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/
- GitHub 仓库：https://github.com/triton-inference-server/server

### 优先阅读链接（3 条）

1. **官方文档首页** — https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/
   用途：导航到各子章节，了解文档结构与覆盖范围

2. **Model Repository 指南** — https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/model_repository.html
   用途：理解 Triton IS 的核心抽象——以文件系统目录组织模型和版本

3. **Getting Started** — https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/getting_started.html
   用途：官方入门指南，包含 Docker 部署和快速验证步骤

## 资料用途总览

| 资料类型 | 用途 | 适用组件 |
|---------|------|---------|
| Architecture 文档 | 理解内部原理和分层设计 | vLLM、SGLang |
| OpenAI 兼容 API 文档 | Gateway 层对接标准接口 | vLLM、SGLang |
| Model Repository 文档 | 生产部署架构参考 | Triton IS |
| 安装文档 | 快速搭建实验环境 | vLLM、SGLang、Triton IS |
| Getting Started | Docker 快速验证 | Triton IS |

Sources:
1. https://docs.vllm.ai/ — vLLM 官方文档
2. https://github.com/vllm-project/vllm — vLLM 主仓库
3. https://docs.sglang.ai/ — SGLang 官方文档
4. https://github.com/sgl-project/sglang — SGLang 主仓库
5. https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/ — Triton IS 官方文档
6. https://github.com/triton-inference-server/server — Triton IS 主仓库

Risk of Staleness:
- vLLM 和 SGLang 版本更新快，具体 API 以实际安装版本为准
- Triton IS release 版本随时间变化

Out of Scope Kept:
- 未扩展到新组件（仅限 vLLM / SGLang / Triton IS）
- 未写分析长文

Need Codex Review On:
- 是否需要在 sources-index 中补充 TensorRT-LLM（当前仅 vLLM / SGLang / Triton IS）
