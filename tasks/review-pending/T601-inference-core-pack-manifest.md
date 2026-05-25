Task ID: T601
Task Title: Inference Core Zero-Touch Pack
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
T601 Inference Core Zero-Touch Pack 收口 manifest。

Result:

# Inference Core Zero-Touch Pack Manifest

## 包概述

本包为 Inference Core 专题的 0 接管链式长跑包，7 个文件全部完成，围绕推理引擎（vLLM/SGLang/Triton/TensorRT-LLM）展开，产出工程级资料索引。

## 已完成交付物

### 1. T601-inference-sources-index-v3
vLLM / SGLang / Triton IS / TensorRT-LLM 的稳定入口与边界说明。

### 2. T601-inference-comparison-index-v3
四个推理引擎的定位/层级/能力/场景/与本项目关系对比，资料级工程选型输入。

### 3. T601-inference-deployment-practice-catalog-v1
10 个最小实践，从单机推理（I01-I04）到服务化接入（I05-I10）。

### 4. T601-inference-glossary-batch-07
10 个核心术语：Continuous Batching / Paged Attention / KV Cache / Prefix Caching / Tensor Parallel / Pipeline Parallel / Speculative Decoding / Scheduler / RadixAttention / TensorRT-LLM Backend。

### 5. T601-inference-stack-decision-memo-v1
三个决策点的资料级输入：本地开发默认路线、服务化分工边界、TensorRT-LLM 前提条件。

### 6. T601-inference-integration-map-v1
Inference core 如何映射到 inference-service、ai-gateway、observability、benchmark/evaluation 四个模块。

### 7. T601-inference-core-pack-manifest
本文件，总结完成项、未定项、对下一包可复用输入。

## 各交付物关系

```
sources-index-v3（入口 + 边界）
    ↓
comparison-index-v3（选型输入）
    ↓
glossary-batch-07（术语定义）
    ↓
deployment-practice-catalog-v1（实践路径）
    ↓
decision-memo-v1（决策输入）
    ↓
integration-map-v1（模块映射）
    ↓
manifest（本文件）
```

## 对下一包可复用的输入

### 供 T602（Observability/Evaluation）使用
- inference-service 的 metrics 端点格式（Prometheus 格式）
- inference-service 与 Langfuse / Prometheus 的集成说明
- inference-service 作为 lm-eval backend 的配置方式

### 供 T603（Finetuning/Training）使用
- inference-service 作为训练后评测的推理引擎
- vLLM/SGLang 的部署实践路径

### 供 T604（Cross-Project Systemization）使用
- inference-stack-decision-memo-v1 的决策输入
- inference-integration-map-v1 的模块关系

## 需要 Codex 最终判断的点

1. **本地开发默认引擎**：是否确认 vLLM 作为 MVP 默认推理引擎？
2. **Triton IS 引入时机**：是否在 MVP 阶段引入 Triton IS，还是后续按需？
3. **TensorRT-LLM 优先级**：是否作为后续性能优化的必选路径？
4. **SGLang 定位**：是否需要 SGLang 作为备选引擎（多轮对话场景）？

## 风险与依赖

- 各引擎版本更新快，具体参数和行为以实际安装版本为准
- TensorRT-LLM 与 GPU 型号强相关，需要确认团队硬件环境
- Triton IS 的引入会增加运维复杂度

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://sglang.readthedocs.io/ — SGLang
3. https://docs.nvidia.com/deeplearning/triton-inference-server/ — Triton IS
4. https://nvidia.github.io/TensorRT-LLM/ — TensorRT-LLM
5. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval
