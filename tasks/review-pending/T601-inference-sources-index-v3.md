Task ID: T601
Task Title: Inference Core Zero-Touch Pack
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 T134/T145/T156/T191/T163/T147/T301/T302，补齐 vLLM/SGLang/Triton/TensorRT-LLM 的稳定入口与边界。

Result:

# Inference Sources Index v3

## vLLM

### 官方入口

| 维度 | 内容 |
|------|------|
| **文档** | https://docs.vllm.ai/ |
| **GitHub** | https://github.com/vllm-project/vllm |
| **PyPI** | https://pypi.org/project/vllm/ |

### 核心能力

- Paged Attention（显存管理）
- Continuous Batching（动态批处理）
- Tensor Parallel（张量并行）
- OpenAI API 兼容接口

### 稳定入口

- 快速开始：https://docs.vllm.ai/en/latest/getting_started/quickstart.html
- 支持模型列表：https://docs.vllm.ai/en/latest/models/supported_models.html
- 可用参数：https://docs.vllm.ai/en/latest/models/engine_args.html

### 边界说明

- vLLM 侧重推理服务，不含训练能力
- TensorRT-LLM 需要先编译模型，vLLM 支持动态加载

来源：https://docs.vllm.ai/

---

## SGLang

### 官方入口

| 维度 | 内容 |
|------|------|
| **文档** | https://sglang.readthedocs.io/ |
| **GitHub** | https://github.com/sgl-project/sglang |
| **Blog** | https://sglang.ai/ |

### 核心能力

- RadixAttention（前缀感知的注意力调度）
- Continuous Batching
- 张量并行
- 更细粒度的调度控制

### 稳定入口

- 快速开始：https://sglang.readthedocs.io/en/latest/get_started.html
- 支持模型：https://sglang.readthedocs.io/en/latest/models/supported_models.html
- 调度配置：https://sglang.readthedocs.io/en/latest/benchmark_results.html

### 边界说明

- SGLang 与 vLLM 功能高度重叠，但调度策略不同
- RadixAttention 对有共享前缀的场景（如多轮对话）有优势

来源：https://sglang.readthedocs.io/

---

## NVIDIA Triton Inference Server

### 官方入口

| 维度 | 内容 |
|------|------|
| **文档** | https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/ |
| **GitHub** | https://github.com/triton-inference-server/server |
| **NGC** | https://catalog.ngc.nvidia.com/containers/nvidia/tritonserver |

### 核心能力

- 支持 TensorRT、TensoRT-LLM、ONNX、Python 后端
- 动态批处理（Dynamic Batching）
- 模型编排（Ensemble）
- HTTP/gRPC 接口

### 稳定入口

- 快速开始：https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/getting_started.html
- 支持后端：https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/backend_lib.html
- TensorRT-LLM 后端：https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/llm_integration.html

### 边界说明

- Triton 侧重推理服务编排，不是推理引擎本身
- 需要配合 TensorRT/TensorRT-LLM 使用

来源：https://docs.nvidia.com/deeplearning/triton-inference-server/

---

## TensorRT-LLM

### 官方入口

| 维度 | 内容 |
|------|------|
| **文档** | https://nvidia.github.io/TensorRT-LLM/ |
| **GitHub** | https://github.com/NVIDIA/TensorRT-LLM |
| **NGC 容器** | https://catalog.ngc.nvidia.com/containers/nvidia/tensorrt-llm |

### 核心能力

- FP8/BF16 低精度推理
- Tensor Parallel（张量并行）
- Paged Attention（与 vLLM 类似）
- Speculative Decoding（投机解码）

### 稳定入口

- 快速开始：https://nvidia.github.io/TensorRT-LLM/quick-start.html
- 支持模型：https://nvidia.github.io/TensorRT-LLM/models/gpt.html
- 优化指南：https://nvidia.github.io/TensorRT-LLM/optimization.html

### 边界说明

- TensorRT-LLM 需要先编译模型，不支持动态加载
- 适合已确定模型、追求极致性能的生产场景
- 与 Triton 集成需要额外配置

来源：https://nvidia.github.io/TensorRT-LLM/

---

## 与本项目关系

| 组件 | 与 inference-service 关系 | 与 ai-gateway 关系 |
|------|------------------------|------------------|
| vLLM | 主要推理引擎候选 | 通过 OpenAI API 兼容接口接入 |
| SGLang | 备选推理引擎候选 | 同上 |
| Triton IS | 生产环境服务编排 | 支持 HTTP/gRPC 上游调用 |
| TensorRT-LLM | 高性能推理引擎（需编译） | 可通过 Triton 或直接接入 |

## 优先阅读链接

1. https://docs.vllm.ai/en/latest/getting_started/quickstart.html — vLLM 快速开始
2. https://sglang.readthedocs.io/en/latest/get_started.html — SGLang 快速开始
3. https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/getting_started.html — Triton 快速开始
4. https://nvidia.github.io/TensorRT-LLM/quick-start.html — TensorRT-LLM 快速开始

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://sglang.readthedocs.io/ — SGLang
3. https://docs.nvidia.com/deeplearning/triton-inference-server/ — Triton IS
4. https://nvidia.github.io/TensorRT-LLM/ — TensorRT-LLM
5. https://github.com/vllm-project/vllm — vLLM GitHub
6. https://github.com/sgl-project/sglang — SGLang GitHub
7. https://github.com/triton-inference-server/server — Triton GitHub
8. https://github.com/NVIDIA/TensorRT-LLM — TensorRT-LLM GitHub

Risk of Staleness:
- 各引擎版本更新快，具体参数和行为以实际安装版本为准
- TensorRT-LLM 与具体 GPU 型号（Hopper/Ampere）相关

Out of Scope Kept:
- 未写推理引擎代码实现
- 未写完整生产部署方案
- 未写多卡分布式训练配置
