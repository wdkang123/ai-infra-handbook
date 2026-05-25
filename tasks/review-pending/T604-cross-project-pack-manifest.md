Task ID: T604
Task Title: Cross-Project Systemization Pack
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
T604 Cross-Project Systemization Pack 收口 manifest。

Result:

# Cross-Project Systemization Pack Manifest

## 包概述

本包为 Cross-Project Systemization 专题的 0 接管链式长跑包，7 个文件全部完成，从项目视角把各模块（inference-service / ai-gateway / eval-module / finetune-demo）串联起来，形成系统化视图。

## 已完成交付物

### 1. T604-project-dependency-matrix-v1
4 个模块的依赖方向和接口关系，request/response/traces/metrics/eval result/finetune artifact 的流向说明。

### 2. T604-build-order-roadmap-v1
5 个阶段（Phase 0-5）的推进路线，按最小可验证路径优先：先推理核心，再可观测性，再评测/微调。

### 3. T604-component-interface-contract-sketch-v1
各模块的提案级接口草案（inference-service / ai-gateway / eval-module / finetune-demo），明确输入/输出，不写成已实现。

### 4. T604-data-and-telemetry-flow-map-v1
6 种数据类型在各模块之间的完整流向图：request、response、trace、metric、eval result、finetune artifact。

### 5. T604-mvp-milestone-board-draft-v1
6 个 Phase 的里程碑草案（T0-01 到 T5-06），每个里程碑有验收条件和 Codex 判断点。

### 6. T604-risk-register-v1
12 个推进风险，按技术/资料/实现/验证四类，含概率/影响评估和缓解措施。

### 7. T604-cross-project-pack-manifest
本文件，总结完成项、未定项、需要 Codex 后续拆解的点。

## 各交付物关系

```
dependency-matrix（模块关系）
    ↓
data-flow-map（数据流向）
    ↓
interface-sketch（接口草案）
    ↓
build-order-roadmap（推进路线）
    ↓
milestone-board（里程碑）
    ↓
risk-register（风险清单）
    ↓
manifest（本文件）
```

## 对后续工作的输入

### 来自前面专题包的输入

| 专题包 | 关键输入 |
|--------|---------|
| **T601** | vLLM 作为 MVP 默认引擎，TensorRT-LLM 作为后续性能优化 |
| **T602** | Langfuse 作为 MVP tracing 工具，lm-eval 作为评测执行层 |
| **T603** | QLoRA 作为 MVP 默认微调方法，DPO 后续按需 |

## 需要 Codex 后续拆解的点

### 架构决策类
1. **默认推理引擎**：确认 vLLM 还是 SGLang
2. **Langfuse 模式**：self-hosted 还是云端
3. **微调方法**：QLoRA 是否作为 MVP 默认
4. **评测结果上报**：是否上报 Langfuse

### 执行规划类
5. **Phase 优先级**：Phase 2（可观测性）和 Phase 3（评测）是否可以并行
6. **Triton IS 引入时机**：是否在 Phase 5 之前引入
7. **Unsloth 启用条件**：GPU 兼容性确认

### 接口契约类
8. **接口草案确认**：各模块接口是否需要调整
9. **trace_id 传递机制**：Langfuse trace 如何串联 gateway 和 inference-service

## 风险清单（高优先级）

| 风险 | 优先级 |
|------|-------|
| R-02 GPU 显存不足 | 高 |
| R-07 lm-eval API 变更 | 高 |
| R-09 DPO 数据获取成本 | 高 |
| R-12 接口契约缺失 | 高 |

## 整体完成度

| 专题包 | 文件数 | 完成度 |
|--------|--------|--------|
| T601 Inference Core | 7 | 100% |
| T602 Observability/Evaluation | 7 | 100% |
| T603 Finetuning/Training | 7 | 100% |
| T604 Cross-Project Systemization | 7 | 100% |
| **合计** | **28** | **100%** |

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://langfuse.com/docs/observability/overview — Langfuse
3. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval
4. https://github.com/huggingface/peft — PEFT
5. https://github.com/huggingface/trl — TRL
6. https://nvidia.github.io/TensorRT-LLM/ — TensorRT-LLM
