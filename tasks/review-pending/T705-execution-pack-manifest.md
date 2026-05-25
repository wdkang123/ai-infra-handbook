# Execution Pack Manifest v1

## Task ID: T705
## Task Title: Execution Decomposition Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
把后续实施拆成若干工作流，便于 Codex 继续分发。

---

# Execution Pack Manifest v1

## 包概述

本包为 Execution Decomposition 专题的 0 接管包，7 个文件全部完成，把后续实施拆解为可分发的任务束，便于 Codex 继续分发和执行。

## 已完成交付物

### 1. T705-codex-ready-workstream-board-v1
把实施分为 4 个工作流（W1-W4），每个工作流包含若干任务，明确优先级和并行关系。

### 2. T705-project-task-breakdown-v1
按模块和阶段拆解所有实施任务，共 29 个任务，26 个 MVP 必须。

### 3. T705-validation-checklist-index-v1
为每个模块提供验收清单索引，便于 Codex 执行后快速验证。

### 4. T705-dependency-gates-v1
定义 6 个门控点（G1-G6），确保前置任务完成后才解锁后续任务。

### 5. T705-mvp-scope-cut-list-v1
明确 MVP 必须（26 个）和可选（8 个）的任务，控制范围。

### 6. T705-build-sequence-sanity-check-v1
提供构建顺序的合理性检查，确保执行路径正确。

### 7. T705-codex-review-focus-map-v1
指引 Codex 在审查各模块时需要重点关注的方向。

## 本包升级了什么（相比 T604）

| 维度 | T604 | T705（本次） |
|------|------|------------|
| 任务拆解 | 30+ 个任务 | 29 个任务，26 个 MVP 必须 |
| 工作流 | 无 | 4 个工作流（W1-W4） |
| 验收清单 | 无 | 每个模块验收清单 |
| 依赖门控 | 部分 | 6 个明确门控点 |
| 范围控制 | 无 | MVP vs 可选明确区分 |
| 执行检查 | 无 | 顺序合理性检查 |
| 审查重点 | 无 | Codex 审查方向指引 |

## 供 Codex 直接使用的输入

### 工作流分发
- T705-codex-ready-workstream-board-v1：直接按工作流分发任务

### 任务执行
- T705-project-task-breakdown-v1：完整任务列表
- T705-dependency-gates-v1：任务依赖关系
- T705-build-sequence-sanity-check-v1：执行顺序检查

### 验证
- T705-validation-checklist-index-v1：每个任务完成后验证

### 审查
- T705-codex-review-focus-map-v1：审查重点指引

### 范围控制
- T705-mvp-scope-cut-list-v1：MVP 边界确认

## 需要 Codex 确认的决策点

### 架构决策类
1. **默认推理引擎**：确认 vLLM 版本
2. **Langfuse 模式**：云端 vs self-hosted
3. **微调方法**：QLoRA 引入时机

### 执行规划类
4. **并行度**：Phase 2/3 是否真正并行
5. **门控节奏**：每个门控的验证标准

## Deep Research Run 完成度

| 专题包 | 文件数 | 完成度 |
|--------|--------|--------|
| T701 Inference Engines | 8 | 100% |
| T702 Observability/Evaluation | 8 | 100% |
| T703 Finetuning/Training | 8 | 100% |
| T704 Cross-Project Systemization | 8 | 100% |
| T705 Execution Decomposition | 8 | 100% |
| **合计** | **40** | **100%** |

---

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval
3. https://github.com/huggingface/peft — PEFT
4. https://langfuse.com/docs/observability/overview — Langfuse
5. https://github.com/huggingface/trl — TRL

---

**Deep Research Run completed.**
