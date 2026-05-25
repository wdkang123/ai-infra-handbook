# Task Card

Task ID: T701
Title: Inference Engines Deep-Research Pack
Owner: MINIMAX
Type: PACK-深研究0接管专题包
Priority: P1

## Input

基于：
- `tasks/accepted/T134-vllm-chapter-draft.md`
- `tasks/accepted/T145-sglang-chapter-revised.md`
- `tasks/accepted/T156-triton-chapter-revised.md`
- `tasks/accepted/T191-tensorrt-llm-chapter-draft.md`
- `tasks/accepted/T163-inference-comparison-index-v2.md`
- `tasks/accepted/T147-inference-stack-sources-index-result.md`
- `tasks/review-pending/T601-inference-sources-index-v3.md`
- `tasks/review-pending/T601-inference-comparison-index-v3.md`
- `tasks/review-pending/T601-inference-stack-decision-memo-v1.md`

## Expected Output

本专题包必须产出以下 8 个文件：

1. `tasks/review-pending/T701-inference-pack-manifest.md`
2. `tasks/review-pending/T701-inference-sources-index-v4.md`
3. `tasks/review-pending/T701-inference-boundary-matrix-v1.md`
4. `tasks/review-pending/T701-inference-release-timeline-v1.md`
5. `tasks/review-pending/T701-inference-deployment-pattern-map-v1.md`
6. `tasks/review-pending/T701-inference-practice-catalog-v2.md`
7. `tasks/review-pending/T701-inference-glossary-batch-08.md`
8. `tasks/review-pending/T701-inference-stack-decision-memo-v2.md`

## Deliverable Notes

### sources-index-v4

在 v3 基础上补稳定入口、官方 release / changelog / blog 入口。

### boundary-matrix-v1

重点澄清：
- 推理引擎 vs 推理服务
- Triton IS vs TensorRT-LLM
- vLLM / SGLang 的职责边界

### release-timeline-v1

为 vLLM / SGLang / Triton IS / TensorRT-LLM 各补关键更新线索入口，写成资料时间线，不做新闻评论。

### deployment-pattern-map-v1

整理从单机、单服务、多服务到网关接入的部署模式。

### practice-catalog-v2

补足 10 到 12 个实践条目，重点是部署与接入。

### glossary-batch-08

优先术语：
- Serving Engine
- Backend
- Model Repository
- Request Batching
- Dynamic Batching
- RadixAttention
- Prefill
- Decode

### decision-memo-v2

在 v1 基础上进一步收紧默认路线与引入时机，但仍不下最终结论。

### manifest

总结本包升级了什么、未定项和对下一包可复用输入。

## Template

使用 MiniMax 标准输出协议。

## Acceptance Criteria

- 必须写满 8 个输出文件
- 全部围绕 inference engines 主线
- 所有重点链接必须是精确 URL
- 不扩写成完整部署白皮书

## Out of Scope

- 不写代码实现
