# Build Sequence Sanity Check v1

## Task ID: T705
## Task Title: Execution Decomposition Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
把后续实施拆成若干工作流，便于 Codex 继续分发。

---

# Build Sequence Sanity Check v1

## 概述

本文档提供构建顺序的合理性检查，确保执行路径正确。

---

## 顺序检查原则

1. **基础设施先行**：Phase 0 必须在所有阶段之前
2. **依赖单向**：不允许循环依赖
3. **可独立验证**：每个阶段完成后可独立验证
4. **关键路径最短**：MVP 完成路径最长

---

## Phase 执行顺序检查

### Phase 0 → Phase 1
```
T0-01 → T0-02 → T0-03 → T0-04 → T1-01
```
✅ 正确：基础设施完成后才能开始推理核心

### Phase 1 内部
```
T1-01 → T1-02 → T1-05/T1-06 → T1-03 → T1-04 → T1-07
                ↓
            T1-08 → T1-09 → T1-10 → T1-11 → T1-12
```
✅ 正确：服务启动后才能实现 API，API 就绪后才能串联

### Phase 1 → Phase 2/3/4
```
Phase 1 完成 → Phase 2 可并行 Phase 3
                         ↓
                      Phase 4
```
✅ 正确：推理就绪后，评测和微调可并行开始

### Phase 3 → Phase 4 串联
```
T3-02 lm-eval 可用 → T4-06 可执行
                           ↓
                     微调后 benchmark 可跑
```
✅ 正确：评测工具就绪后才能验证微调效果

---

## 常见错误模式

### ❌ 循环依赖
```
A 依赖 B，B 依赖 C，C 依赖 A
```
✅ 预防：依赖图必须是有向无环图（DAG）

### ❌ 前置未完成就启动后续
```
T1-02 未完成 → T1-03 开始
```
✅ 预防：门控检查清单必须执行

### ❌ 跳过验证步骤
```
T1-02 服务启动 → 直接 T1-12 串联
```
✅ 预防：每个阶段必须独立验证后再继续

### ❌ 可并行任务串行执行
```
Phase 2 完成 → Phase 3 开始 → Phase 4 开始
```
✅ 预防：Phase 2/3 可并行，应充分利用

---

## 构建顺序速查

| 当前阶段 | 可开始的任务 | 必须等待的任务 |
|---------|------------|--------------|
| Phase 0 | T1-01, T3-01, T4-01 | - |
| Phase 1 中期 | T2-01 | T1-06 |
| Phase 1 完成 | Phase 2/3 所有任务 | G4 解锁 |
| Phase 3 完成 | T4-06 | T3-03/T3-04 |
| Phase 4 完成 | MVP 评审 | T4-06 |

---

## 快速回归检查

每次开始新任务前，执行以下检查：

```bash
# 1. 检查前置任务状态
cat TASKBOARD.md | grep -E "T[0-4]-[0-9]+.*completed"

# 2. 检查依赖门控
# G1: T0-01~T0-04 全部 completed?
# G2: T1-02 completed?
# G3: T1-03 completed?

# 3. 验证前置产出
# inference-service: curl http://localhost:8000/health
# gateway: curl http://localhost:8080/health
# eval-module: lm_eval --model dummy --tasks mmlu
```

---

## 执行节奏建议

| 阶段 | 建议并行度 | 预计任务数 |
|------|----------|----------|
| Phase 0 | 1（串行） | 4 |
| Phase 1 | 2（基础设施和 Gateway 并行） | 12 |
| Phase 2 | 1（串行，仅 T2-01） | 1 |
| Phase 3 | 2（lm-eval 和 benchmark 并行） | 6 |
| Phase 4 | 2（LoRA 和保存加载并行） | 4 |

---

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval
3. https://github.com/huggingface/peft — PEFT

Risk of Staleness:
- 实际执行可能需要调整并行度

Out of Scope Kept:
- 未写自动化检查脚本
- 未写详细排期
