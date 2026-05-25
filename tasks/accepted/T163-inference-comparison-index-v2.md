Task ID: T163
Task Title: 产出 inference stack comparison-index v2 草稿（加入 TensorRT-LLM）
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 T142 comparison-index v1 和 T147 sources-index，加入 TensorRT-LLM，扩展为 4 个组件的 v2 对比索引。

Result:

## 对比维度一：定位

| 框架 | 定位 | 来源 |
|------|------|------|
| vLLM | LLM 专用推理与服务引擎，基于 PagedAttention 优化显存管理和吞吐 | https://github.com/vllm-project/vllm |
| SGLang | LLM 专用推理与服务框架，基于 RadixAttention 做前缀感知调度和灵活前端语言 | https://github.com/sgl-project/sglang |
| Triton IS | 通用推理服务平台，支持多框架模型统一部署，不是 LLM 专用 | https://github.com/triton-inference-server/server |
| TensorRT-LLM | LLM 推理优化后端，提供 Python API 构建 TensorRT 引擎用于高效推理 | https://github.com/NVIDIA/TensorRT-LLM |

## 对比维度二：主要接口形态

| 框架 | 接口 | 来源 |
|------|------|------|
| vLLM | OpenAI 兼容 REST/gRPC API | https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html |
| SGLang | OpenAI 兼容 REST API | https://docs.sglang.ai/ |
| Triton IS | HTTP/REST + gRPC 双协议，模型仓库 + config.pbtxt | https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/ |
| TensorRT-LLM | Python API（模型构建）+ C++/Python Runtime（引擎执行）；通过 Triton backend 间接暴露 HTTP/gRPC 接口 | https://github.com/NVIDIA/TensorRT-LLM |

## 对比维度三：主要优化方向

| 框架 | 核心优化点 | 来源 |
|------|-----------|------|
| vLLM | PagedAttention（KV cache 分页）、Continuous Batching、FlashAttention 集成、多后端（CUDA/ROCm/CPU）| https://docs.vllm.ai/ |
| SGLang | RadixAttention（前缀共享）、PD 分离（prefill-decode disaggregation）、Chunked Prefill、Multi-LoRA | https://docs.sglang.ai/backend/index.html |
| Triton IS | 多模型动态 batching、多框架统一服务（TensorRT/PyTorch/ONNX）、Kubernetes 集成、Prometheus 监控 | https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/ |
| TensorRT-LLM | TensorRT 引擎编译（Kernel Fusion、量化 FP8/INT8/INT4、SmoothQuant、CUDA Graph）、张量并行/管道并行 | https://github.com/NVIDIA/TensorRT-LLM |

## 对比维度四：典型使用场景

| 框架 | 典型场景 | 来源 |
|------|---------|------|
| vLLM | 纯 LLM 推理服务，需要高吞吐和 OpenAI 兼容接口的生产部署 | https://github.com/vllm-project/vllm |
| SGLang | 复杂 Agent 场景（多轮对话、结构化输出、多模态）、需要前缀共享的长上下文应用 | https://github.com/sgl-project/sglang |
| Triton IS | 企业多模型统一管理、异构模型服务（CV+NLP+LLM 混合部署）、需要 Kubernetes 生产级治理 | https://www.nvidia.com/en-us/ai-data-science/products/triton-inference-server/ |
| TensorRT-LLM | NVIDIA GPU 上的极致推理性能优化、需要编译优化换最大吞吐的生产 LLM 部署 | https://github.com/NVIDIA/TensorRT-LLM |

## 对比维度五：与本项目的关系

| 框架 | 在 AI Infra 学习路径中的位置 | 来源 |
|------|--------------------------|------|
| vLLM | 理解 LLM 推理引擎的入门首选，理解 PagedAttention 和 Continuous Batching 的经典实现 | https://docs.vllm.ai/ |
| SGLang | 理解调度器差异化设计（RadixAttention vs PagedAttention）、Agent 场景下的调度优势 | https://docs.sglang.ai/ |
| Triton IS | 理解生产级推理服务架构（协议层、模型管理层、多框架统一） | https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/ |
| TensorRT-LLM | 理解"算子层优化 + 服务层分离"架构，是 Triton IS + TensorRT-LLM 组合的算子层基础 | https://github.com/NVIDIA/TensorRT-LLM |

## 对比维度六：不适合的场景

| 框架 | 不适合以此为主要推理引擎的场景 | 来源 |
|------|--------------------------|------|
| vLLM | 需要多框架统一管理的场景（非其核心设计目标） | https://docs.vllm.ai/ |
| SGLang | 硬件受限时（当前以 CUDA 为首选，AMD ROCm / TPU 成熟度较低） | https://docs.sglang.ai/ |
| Triton IS | 以最大化 LLM 吞吐为首要目标的场景（单独用 Triton IS 而不配合专用 LLM 引擎/优化后端，无法充分发挥 LLM 效率） | https://www.nvidia.com/en-us/ai-data-science/products/triton-inference-server/ |
| TensorRT-LLM | 需要开箱即用、自带 OpenAI 兼容 API 的场景（TensorRT-LLM 是底层优化库，不是完整 serving 平台） | https://github.com/NVIDIA/TensorRT-LLM |

Sources:
1. https://github.com/vllm-project/vllm — vLLM 定位
2. https://github.com/sgl-project/sglang — SGLang 定位
3. https://github.com/triton-inference-server/server — Triton IS 定位
4. https://github.com/NVIDIA/TensorRT-LLM — TensorRT-LLM 定位
5. https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html — vLLM 接口
6. https://docs.sglang.ai/ — SGLang 接口
7. https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/ — Triton IS 接口
8. https://github.com/NVIDIA/TensorRT-LLM — TensorRT-LLM 接口形态
9. https://docs.sglang.ai/backend/index.html — SGLang 优化方向
10. https://www.nvidia.com/en-us/ai-data-science/products/triton-inference-server/ — Triton IS 产品定位
11. https://github.com/NVIDIA/TensorRT-LLM/tree/main/triton_backend — TensorRT-LLM 与 Triton IS 关系

Risk of Staleness:
- vLLM 和 SGLang 版本更新快，具体能力以实际安装版本为准
- TensorRT-LLM 版本迭代快，pip install 的默认版本以实际安装时为准
- Triton IS 的品牌在 NVIDIA 产品整合后可能变化（已更名为 Dynamo-Triton）

Out of Scope Kept:
- 未写 benchmark 排名
- 未做 vLLM/SGLang/TensorRT-LLM 三者之间的吞吐优劣对比
- 未扩写成章节

Need Codex Review On:
- TensorRT-LLM 的定位描述是否需要进一步区分"优化后端"与"推理引擎"
