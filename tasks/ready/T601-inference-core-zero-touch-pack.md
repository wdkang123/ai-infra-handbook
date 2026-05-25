# Task Card

Task ID: T601
Title: Inference Core Zero-Touch Pack
Owner: MINIMAX
Type: PACK-0接管链式专题包
Priority: P1

## Input

基于：
- `tasks/accepted/T134-vllm-chapter-draft.md`
- `tasks/accepted/T145-sglang-chapter-revised.md`
- `tasks/accepted/T156-triton-chapter-revised.md`
- `tasks/accepted/T191-tensorrt-llm-chapter-draft.md`
- `tasks/accepted/T163-inference-comparison-index-v2.md`
- `tasks/accepted/T147-inference-stack-sources-index-result.md`
- `tasks/accepted/T301-inference-service-mvp-result.md`
- `tasks/accepted/T302-ai-gateway-mvp-result.md`

## Expected Output

本专题包必须产出以下 7 个文件：

1. `tasks/review-pending/T601-inference-core-pack-manifest.md`
2. `tasks/review-pending/T601-inference-sources-index-v3.md`
3. `tasks/review-pending/T601-inference-comparison-index-v3.md`
4. `tasks/review-pending/T601-inference-deployment-practice-catalog-v1.md`
5. `tasks/review-pending/T601-inference-glossary-batch-07.md`
6. `tasks/review-pending/T601-inference-stack-decision-memo-v1.md`
7. `tasks/review-pending/T601-inference-integration-map-v1.md`

## Deliverable Notes

### sources-index-v3

补齐并收紧以下对象的稳定入口与边界：
- vLLM
- SGLang
- NVIDIA Triton Inference Server
- TensorRT-LLM

### comparison-index-v3

从“入门比较”推进到“工程选型输入”，但仍不下最终结论。

### deployment-practice-catalog-v1

整理 8 到 10 个最小实践，从单机推理到服务化接入。

### glossary-batch-07

优先术语：
- Continuous Batching
- Paged Attention
- KV Cache
- Prefix Caching
- Tensor Parallel
- Pipeline Parallel
- Speculative Decoding
- Scheduler

### decision-memo-v1

围绕以下问题给出资料级输入：
- 本项目默认本地开发推理栈应该优先哪条路线
- 服务化场景下 Triton / vLLM / SGLang 的分工边界
- TensorRT-LLM 更适合什么前提条件

### integration-map-v1

说明 inference core 如何映射到：
- inference-service
- ai-gateway
- observability
- benchmark / evaluation

### manifest

总结完成项、未定项、对下一包可复用的输入。

## Template

使用 MiniMax 标准输出协议。

## Acceptance Criteria

- 必须写满 7 个输出文件
- 全部围绕 inference core 主线
- 所有重点链接必须是精确 URL
- 不扩写成完整部署手册

## Out of Scope

- 不写代码实现
