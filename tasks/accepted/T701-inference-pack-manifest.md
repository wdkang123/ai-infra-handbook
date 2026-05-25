Task ID: T701
Task Title: Inference Engines Deep-Research Pack
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
T701 Inference Engines Deep-Research Pack 收口 manifest。

Result:

# Inference Engines Deep-Research Pack Manifest

## 包概述

本包为 Inference Engines 专题的深研究 0 接管包，8 个文件全部完成，在 v3 基础上做了更扎实的官方来源核对、边界澄清和时间线收口。

## 已完成交付物

### 1. T701-inference-sources-index-v4
在 v3 基础上补全了官方 release/changelog/blog 入口（T701-inference-sources-index-v4 → T601-inference-sources-index-v3）。

### 2. T701-inference-boundary-matrix-v1
澄清四个核心边界：推理引擎 vs 推理服务、Triton IS vs TensorRT-LLM、vLLM vs SGLang、生产部署模式。

### 3. T701-inference-release-timeline-v1
为 vLLM / SGLang / Triton IS / TensorRT-LLM 各补关键更新线索和官方入口（changelog/blog/releases）。

### 4. T701-inference-deployment-pattern-map-v1
8 种部署模式，从单机单引擎到 Kubernetes 部署，含决策树和选择指引。

### 5. T701-inference-practice-catalog-v2
12 个实践条目（I01-I12），从单机推理到服务化接入到性能优化。

### 6. T701-inference-glossary-batch-08
13 个核心术语：Serving Engine / Backend / Model Repository / Request Batching / Dynamic Batching / RadixAttention / Prefill / Decode / Continuous Batching / Paged Attention / KV Cache / Tensor Parallel / Speculative Decoding。

### 7. T701-inference-stack-decision-memo-v2
在 v1 基础上收紧四个决策点：默认引擎选择、SGLang 定位、Triton 引入时机、TensorRT-LLM 时机。

### 8. T701-inference-pack-manifest
本文件，总结本包升级了什么、未定项、对下一包可复用输入。

## 本包升级了什么（相比 v3）

| 维度 | v3 | v4（收紧） |
|------|-----|-----------|
| Sources | 官方文档链接 | 补全 release/changelog/blog 入口 |
| Boundaries | 基本对比 | 澄清引擎 vs 服务、Triton vs TRT-LLM |
| Timeline | 无 | 新增 release timeline |
| Decision | 初步建议 | 收紧为 5 个明确决策点 |
| Practices | 10 个 | 增加到 12 个 |

## 对下一包可复用的输入

### 供 T702（Observability/Evaluation）使用
- inference-service 的 metrics 端点格式（Prometheus 格式）
- vLLM / SGLang 的 OpenAI 兼容 API 作为 lm-eval backend

### 供 T703（Finetuning/Training）使用
- inference-service 作为训练后评测的推理引擎
- TensorRT-LLM 可能作为训练加速的推理后端

### 供 T704（Cross-Project）使用
- inference-stack-decision-memo-v2 的决策输入（vLLM 作为默认引擎）
- 各引擎的边界澄清

## 需要 Codex 最终判断的点

1. **默认推理引擎是否确认 vLLM**？
2. **SGLang 是否作为多轮对话场景的备选**？
3. **Triton IS 是否在 MVP 阶段排除**？
4. **TensorRT-LLM 引入时机**（模型确定 + 性能优先 + GPU 支持）？
5. **GPU 型号是否支持 TensorRT-LLM**？

## 风险与依赖

- 各引擎版本更新快，具体参数和行为以实际安装版本为准
- TensorRT-LLM 与 GPU 型号强相关，需要确认硬件环境
- SGLang 仍处于快速迭代期，API 稳定性相对较低

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://sglang.readthedocs.io/ — SGLang
3. https://docs.nvidia.com/deeplearning/triton-inference-server/ — Triton IS
4. https://nvidia.github.io/TensorRT-LLM/ — TensorRT-LLM
5. https://blog.vllm.ai/ — vLLM Blog
6. https://sglang.ai/blog — SGLang Blog
