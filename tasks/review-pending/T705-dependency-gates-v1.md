# Dependency Gates v1

## Task ID: T705
## Task Title: Execution Decomposition Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
把后续实施拆成若干工作流，便于 Codex 继续分发。

---

# Dependency Gates v1

## 概述

本文档定义任务间的依赖门控，确保前置任务完成后才解锁后续任务。

---

## 门控总览

| 门控 ID | 名称 | 解锁条件 | 阻塞任务 |
|--------|------|---------|---------|
| G1 | 基础设施就绪 | T0-01 ~ T0-04 完成 | Phase 1 所有任务 |
| G2 | 推理引擎就绪 | T1-02 完成 | T1-03, T1-04, T1-06 |
| G3 | 推理 API 就绪 | T1-03 完成 | T1-12 |
| G4 | Gateway 就绪 | T1-12 完成 | 端到端验证 |
| G5 | 评测就绪 | T3-02 完成 | T3-03, T3-04, T4-06 |
| G6 | 微调就绪 | T4-02 完成 | T4-05, T4-06 |

---

## 门控详解

### G1：基础设施就绪

**解锁条件**：
- T0-01 项目仓库骨架
- T0-02 CI 基础
- T0-03 README 初版
- T0-04 任务看板

**阻塞**：
- Phase 1 所有任务

**验证方式**：
```bash
ls -la /path/to/repo
pytest --collect-only  # CI 可运行
```

---

### G2：推理引擎就绪

**解锁条件**：
- T1-02 vLLM 集成（服务可启动）

**阻塞**：
- T1-03 OpenAI 兼容 API
- T1-04 模型加载
- T1-06 /metrics 端点

**验证方式**：
```bash
curl http://localhost:8000/health  # 返回 200
```

---

### G3：推理 API 就绪

**解锁条件**：
- T1-03 OpenAI 兼容 API（/v1/chat/completions 可调用）

**阻塞**：
- T1-12 gateway → inference 串联

**验证方式**：
```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -d '{"model":"default","messages":[{"role":"user","content":"test"}]}'
```

---

### G4：Gateway 就绪

**解锁条件**：
- T1-12 gateway → inference 串联（端到端可跑）

**阻塞**：
- 整体系统联调
- Phase 2 可观测性任务（T2-04, T2-05）

**验证方式**：
```bash
curl -X POST http://localhost:8080/v1/chat/completions \
  -H "Authorization: Bearer test-token" \
  -d '{"model":"default","messages":[{"role":"user","content":"test"}]}'
```

---

### G5：评测就绪

**解锁条件**：
- T3-02 lm-eval 集成（lm-eval 可运行）

**阻塞**：
- T3-03 MMLU benchmark
- T3-04 GSM8K benchmark
- T4-06 训练+评测串联

**验证方式**：
```bash
lm_eval --model dummy --tasks mmlu  # 快速验证
```

---

### G6：微调就绪

**解锁条件**：
- T4-02 PEFT/LoRA 集成（LoRA adapter 可训练）

**阻塞**：
- T4-05 adapter 保存/加载
- T4-06 训练+评测串联

**验证方式**：
```bash
python train.py --method lora --rank 8  # 小规模验证
```

---

## 门控依赖图

```
G1（基础设施）
    ↓
G2（推理引擎就绪）
    ↓
G3（推理 API 就绪）
    ↓
G4（Gateway 就绪）
    ↓
  整体联调

G5（评测就绪）
    ↓
G6（微调就绪）
    ↓
T4-06（训练+评测串联）
```

---

## 并行门控

以下门控可并行执行：

| 并行组 | 门控 | 说明 |
|--------|------|------|
| 组 A | G2, G5, G6 | Phase 1/3/4 可并行初始化 |
| 组 B | G3 依赖 G2 | G2 完成后 G3 解锁 |
| 组 C | G4 依赖 G3 | G3 完成后 G4 解锁 |

---

## 门控检查清单

### 开始 Phase 1 之前
- [ ] G1 所有前置任务完成

### 开始 Phase 2/3/4 之前
- [ ] G4 解锁（G1+G2+G3 完成）

### MVP 评审之前
- [ ] G1 ~ G6 全部解锁
- [ ] T1-01 ~ T4-06 MVP 必须任务全部完成

---

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval
3. https://github.com/huggingface/peft — PEFT

Risk of Staleness:
- 依赖关系可能因架构调整变化

Out of Scope Kept:
- 未写自动化门控检查脚本
- 未写门控超时处理
