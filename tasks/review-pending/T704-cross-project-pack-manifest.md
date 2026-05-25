Task ID: T704
Task Title: Cross-Project Deep-Research Pack
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
T704 Cross-Project Deep-Research Pack 收口 manifest。

Result:

# Cross-Project Deep-Research Pack Manifest

## 包概述

本包为 Cross-Project Systemization 专题的深研究 0 接管包，8 个文件全部完成，从项目视角把各模块（inference-service / ai-gateway / eval-module / finetune-demo）串联起来，形成系统化视图。

## 已完成交付物

### 1. T704-project-dependency-matrix-v2
在 v1 基础上进一步收口四个核心模块的依赖关系、接口边界、职责边界。

### 2. T704-build-order-roadmap-v2
进一步细化 Phase 0-5 的推进路线，明确 MVP 必须任务和可选任务。

### 3. T704-interface-contract-boundary-notes-v1
说明各接口的边界：哪些是提案、哪些依赖外部工具、哪些只适合后续阶段。

### 4. T704-data-and-telemetry-flow-map-v2
收口 6 种数据类型在各模块之间的完整流向图，明确 MVP vs 后续阶段。

### 5. T704-component-ownership-map-v1
说明四个模块各自的职责范围，明确"负责什么"和"不负责什么"。

### 6. T704-mvp-milestone-board-v2
把 Phase 进一步拆细为 4 个 Phase 共 30+ 个任务，便于 Codex 后续拆任务。

### 7. T704-risk-register-v2
更新为 12 个风险，按技术/资料/实现/验证四类，含概率/影响评估和高优先级风险清单。

### 8. T704-cross-project-pack-manifest
本文件，总结本包升级了什么、未定项、需要 Codex 后续拆解的点。

## 本包升级了什么（相比 T604）

| 维度 | T604 | T704（收紧） |
|------|------|------------|
| Dependency Matrix | 基本依赖方向 | 收口接口边界和职责边界 |
| Build Order | 5 个 Phase | 细化为 30+ 个任务 |
| Interface Notes | 部分 | 新增接口边界笔记 |
| Data Flow | 流向图 | 明确 MVP vs 后续阶段 |
| Ownership | 无 | 新增模块职责边界 |
| Milestone | 基本里程碑 | 拆细为任务级 |
| Risk | 12 个风险 | 更新风险矩阵 |

## 对下一包可复用的输入

### 供 T705（Execution Decomposition）使用
- T701-inference-stack-decision-memo-v2（推理栈决策）
- T702-observability-eval-decision-memo-v2（observability/evaluation 决策）
- T703-finetuning-decision-memo-v3（finetuning 决策）
- T704-build-order-roadmap-v2（推进路线）
- T704-mvp-milestone-board-v2（任务拆分）
- T704-risk-register-v2（风险清单）

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

## 整体完成度

| 专题包 | 文件数 | 完成度 |
|--------|--------|--------|
| T701 Inference Engines | 8 | 100% |
| T702 Observability/Evaluation | 8 | 100% |
| T703 Finetuning/Training | 8 | 100% |
| T704 Cross-Project Systemization | 8 | 100% |
| **合计** | **32** | **100%** |

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://langfuse.com/docs/observability/overview — Langfuse
3. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval
4. https://github.com/huggingface/peft — PEFT
5. https://github.com/huggingface/trl — TRL
6. https://nvidia.github.io/TensorRT-LLM/ — TensorRT-LLM
