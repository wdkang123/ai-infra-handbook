Task ID: T142
Task Title: 收紧 comparison-index 中缺来源和过强结论的维度
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 T132 初稿和 review note T142 修订。只为"与本项目关系"和"不适合的场景"补来源、软化结论，其余维度保留。

Result:

## 对比维度一：定位

| 框架 | 定位 | 来源 |
|------|------|------|
| vLLM | LLM 专用推理与服务引擎，基于 PagedAttention 优化显存管理和吞吐 | https://github.com/vllm-project/vllm |
| SGLang | LLM 专用推理与服务框架，基于 RadixAttention 做前缀感知调度和灵活前端语言 | https://github.com/sgl-project/sglang |
| Triton IS | 通用推理服务平台，支持多框架模型统一部署，不是 LLM 专用 | https://github.com/triton-inference-server/server |

## 对比维度二：主要接口形态

| 框架 | 接口 | 来源 |
|------|------|------|
| vLLM | OpenAI 兼容 REST/gRPC API | https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html |
| SGLang | OpenAI 兼容 REST API | https://docs.sglang.ai/ |
| Triton IS | HTTP/REST + gRPC 双协议，模型仓库 + config.pbtxt | https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/ |

## 对比维度三：主要优化方向

| 框架 | 核心优化点 | 来源 |
|------|-----------|------|
| vLLM | PagedAttention（KV cache 分页）、Continuous Batching、FlashAttention 集成、多后端（CUDA/ROCm/CPU）| https://docs.vllm.ai/ |
| SGLang | RadixAttention（前缀共享）、PD 分离（prefill-decode disaggregation）、Chunked Prefill、Multi-LoRA | https://docs.sglang.ai/backend/index.html |
| Triton IS | 多模型动态 batching、多框架统一服务（TensorRT/PyTorch/ONNX）、Kubernetes 集成、Prometheus 监控 | https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/ |

## 对比维度四：典型使用场景

| 框架 | 典型场景 | 来源 |
|------|---------|------|
| vLLM | 纯 LLM 推理服务，需要高吞吐和 OpenAI 兼容接口的生产部署 | https://github.com/vllm-project/vllm |
| SGLang | 复杂 Agent 场景（多轮对话、结构化输出、多模态）、需要前缀共享的长上下文应用 | https://github.com/sgl-project/sglang |
| Triton IS | 企业多模型统一管理、异构模型服务（CV+NLP+LLM 混合部署）、需要 Kubernetes 生产级治理 | https://www.nvidia.com/en-us/ai-data-science/products/triton-inference-server/ |

## 对比维度五：与本项目的关系

| 框架 | 在 AI Infra 学习路径中的位置 | 来源 |
|------|--------------------------|------|
| vLLM | 理解 LLM 推理引擎的入门首选，理解 PagedAttention 和 Continuous Batching 的经典实现 | https://docs.vllm.ai/ |
| SGLang | 理解调度器差异化设计（RadixAttention vs PagedAttention）、Agent 场景下的调度优势 | https://docs.sglang.ai/ |
| Triton IS | 理解生产级推理服务架构（协议层、模型管理层、多框架统一） | https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/ |

## 对比维度六：不适合的场景

| 框架 | 不适合以此为主要推理引擎的场景 | 来源 |
|------|--------------------------|------|
| vLLM | 需要多框架统一管理的场景（非其核心设计目标） | https://docs.vllm.ai/ |
| SGLang | 硬件受限时（当前以 CUDA 为首选，AMD ROCm / TPU 成熟度较低） | https://docs.sglang.ai/ |
| Triton IS | 以最大化 LLM 吞吐为首要目标的场景（单独用 Triton IS 而不配合专用 LLM 引擎/优化后端，无法充分发挥 LLM 效率） | https://www.nvidia.com/en-us/ai-data-science/products/triton-inference-server/ |

Sources:
1. https://github.com/vllm-project/vllm — vLLM 定位
2. https://github.com/sgl-project/sglang — SGLang 定位
3. https://github.com/triton-inference-server/server — Triton IS 定位
4. https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html — vLLM 接口
5. https://docs.sglang.ai/ — SGLang 接口
6. https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/ — Triton IS 接口
7. https://docs.sglang.ai/backend/index.html — SGLang 优化方向
8. https://www.nvidia.com/en-us/ai-data-science/products/triton-inference-server/ — Triton IS 产品定位

Risk of Staleness:
- vLLM 和 SGLang 版本更新快，具体能力以实际安装版本为准
- Triton IS 的品牌定位在 NVIDIA 产品整合后可能变化

Out of Scope Kept:
- 未加入 TensorRT-LLM 作为对比维度
- 未写 benchmark 排名

Need Codex Review On:
- "不适合的场景"措辞是否仍有偏强之嫌，Codex 需最终把关
