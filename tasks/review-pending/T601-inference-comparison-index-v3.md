Task ID: T601
Task Title: Inference Core Zero-Touch Pack
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 T163，从"入门比较"推进到"工程选型输入"，但仍不下最终结论。

Result:

# Inference Comparison Index v3

## 定位比较

| 对象 | 定位 | 来源 |
|------|------|------|
| **vLLM** | 高吞吐量推理引擎，Paged Attention + Continuous Batching | https://docs.vllm.ai/ |
| **SGLang** | 细粒度调度推理引擎，RadixAttention + Continuous Batching | https://sglang.readthedocs.io/ |
| **Triton IS** | 推理服务编排层，支持多后端动态批处理 | https://docs.nvidia.com/deeplearning/triton-inference-server/ |
| **TensorRT-LLM** | 编译优化型推理引擎，极致性能 | https://nvidia.github.io/TensorRT-LLM/ |

## 所处层级比较

| 对象 | 所处层级 | 说明 | 来源 |
|------|---------|------|------|
| **vLLM** | 推理引擎层 | 实际执行推理计算 | https://docs.vllm.ai/ |
| **SGLang** | 推理引擎层 | 实际执行推理计算，调度更细粒度 | https://sglang.readthedocs.io/ |
| **Triton IS** | 服务编排层 | 请求路由 + 动态批处理 + 多模型编排 | https://docs.nvidia.com/deeplearning/triton-inference-server/ |
| **TensorRT-LLM** | 推理引擎层 | 编译优化，实际执行推理 | https://nvidia.github.io/TensorRT-LLM/ |

层级关系：
```
服务编排层：Triton IS
    ↓ 调用
推理引擎层：vLLM / SGLang / TensorRT-LLM
```

## 核心能力比较

| 维度 | vLLM | SGLang | Triton IS | TensorRT-LLM |
|------|------|--------|----------|--------------|
| Paged Attention | 是 | 是 | 否 | 是 |
| Continuous Batching | 是 | 是 | 是（动态批处理） | 是 |
| Tensor Parallel | 是 | 是 | 是 | 是 |
| Prefix Caching | 部分 | RadixAttention 原生支持 | 否 | 否 |
| Speculative Decoding | 是 | 是 | 否 | 是 |
| 编译优化 | 否（动态加载） | 否 | 否 | 是（必须编译） |
| 多后端支持 | 否 | 否 | 是（TensorRT/ONNX/Python） | 否 |

## 典型使用场景

| 对象 | 典型使用场景 | 来源 |
|------|-------------|------|
| **vLLM** | 需要快速部署、模型频繁切换的研发/测试环境 | https://docs.vllm.ai/ |
| **SGLang** | 多轮对话等有共享前缀的延迟敏感场景 | https://sglang.readthedocs.io/ |
| **Triton IS** | 需要统一管理多个模型或多种推理引擎的生产环境 | https://docs.nvidia.com/deeplearning/triton-inference-server/ |
| **TensorRT-LLM** | 已确定模型、追求极致性能的生产环境 | https://nvidia.github.io/TensorRT-LLM/ |

## 与本项目关系

| 对象 | 与 inference-service 关系 | 与 ai-gateway 关系 |
|------|------------------------|------------------|
| **vLLM** | 主要推理引擎候选 | 通过 OpenAI 兼容 API 接入 |
| **SGLang** | 备选推理引擎候选 | 同上 |
| **Triton IS** | 可作为 inference-service 的上游编排层 | 可作为 gateway 下游的实际服务编排 |
| **TensorRT-LLM** | 高性能推理引擎备选 | 需要先编译模型，接入成本高 |

## MVP 适配性评估

| 对象 | MVP 适配性 | 说明 |
|------|-----------|------|
| **vLLM** | 高 | 接入简单，动态加载，研发阶段首选 |
| **SGLang** | 中 | 调度能力更强，但生态比 vLLM 小 |
| **Triton IS** | 中 | 生产环境需要，但 MVP 阶段可能冗余 |
| **TensorRT-LLM** | 低 | 需要编译，接入成本高，适合明确性能需求后引入 |

## 工程选型输入（资料级）

| 场景 | 推荐候选 | 关键依据 |
|------|---------|---------|
| **本地开发 / 快速验证** | vLLM | 动态加载，安装简单 |
| **多轮对话 / 前缀共享场景** | SGLang | RadixAttention 原生支持 |
| **生产环境多模型管理** | Triton IS | 统一编排，多后端支持 |
| **极致性能已确定模型** | TensorRT-LLM | 编译优化，性能最优 |

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://sglang.readthedocs.io/ — SGLang
3. https://docs.nvidia.com/deeplearning/triton-inference-server/ — Triton IS
4. https://nvidia.github.io/TensorRT-LLM/ — TensorRT-LLM

Risk of Staleness:
- 各引擎版本更新快，具体功能支持以实际版本为准
- TensorRT-LLM 与 GPU 型号强相关

Out of Scope Kept:
- 未写代码实现
- 未做基准性能测试对比
- 未写生产环境部署方案
