# Project Task Breakdown v1 (Revised)

## Task ID: T715
## Task Title: Project Task Breakdown Tighten
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T705-review.md，补全可观测性任务拆解，解决 T2-01 ~ T2-05 编号断裂问题。

---

# Project Task Breakdown v1 (Revised)

## 概述

本文档把 AI 基础设施项目的所有实施任务按模块和阶段拆解，便于执行跟踪。

---

## 任务总览

| 模块 | 任务数 | MVP 必须 |
|------|--------|---------|
| inference-service | 7 | 7 |
| ai-gateway | 5 | 5 |
| eval-module | 6 | 6 |
| finetune-demo | 7 | 4 |
| 可观测性 | 5 | 1 |
| 基础设施 | 4 | 4 |
| **合计** | **34** | **27** |

---

## inference-service 任务拆解

| 任务 ID | 任务 | 验收条件 | 依赖 |
|---------|------|---------|------|
| T1-01 | MVP 设计文档 | 文档完成 | - |
| T1-02 | vLLM 集成 | 服务可启动 | T1-01 |
| T1-03 | OpenAI 兼容 API | /v1/chat/completions 可调用 | T1-02 |
| T1-04 | 模型加载（base + adapter） | 模型加载成功 | T1-03 |
| T1-05 | /health 健康检查 | 返回正常 | T1-02 |
| T1-06 | /metrics 端点 | Prometheus 格式可抓取 | T1-02 |
| T1-07 | 模型版本管理 | 版本切换可用 | T1-04 |

---

## ai-gateway 任务拆解

| 任务 ID | 任务 | 验收条件 | 依赖 |
|---------|------|---------|------|
| T1-08 | MVP 设计文档 | 文档完成 | - |
| T1-09 | 路由逻辑实现 | 路由到正确后端 | T1-08 |
| T1-10 | 鉴权中间件 | Token 验证可用 | T1-08 |
| T1-11 | 限流中间件 | QPS 控制可用 | T1-08 |
| T1-12 | gateway → inference 串联 | 端到端可跑 | T1-09, T1-10, T1-03 |

---

## eval-module 任务拆解

| 任务 ID | 任务 | 验收条件 | 依赖 |
|---------|------|---------|------|
| T3-01 | MVP 设计文档 | 文档完成 | - |
| T3-02 | lm-eval 集成 | lm-eval 可运行 | T3-01 |
| T3-03 | MMLU benchmark | 分数正常返回 | T3-02 |
| T3-04 | GSM8K benchmark | 分数正常返回 | T3-02 |
| T3-05 | 结果 JSON 持久化 | 文件保存成功 | T3-03 或 T3-04 |
| T3-06 | 历史结果对比 | 两个结果可对比 | T3-05 |

---

## finetune-demo 任务拆解

| 任务 ID | 任务 | 验收条件 | MVP 必须 | 依赖 |
|---------|------|---------|---------|------|
| T4-01 | MVP 设计文档 | 文档完成 | 是 | - |
| T4-02 | PEFT/LoRA 集成 | LoRA adapter 可训练 | 是 | T4-01 |
| T4-03 | QLoRA 集成 | 4-bit 量化可训练 | 否 | T4-02 |
| T4-04 | trl SFTTrainer 集成 | SFT 可运行 | 否 | T4-02 |
| T4-05 | adapter 保存/加载 | 持久化可用 | 是 | T4-02 |
| T4-06 | 训练+评测串联 | 微调后 benchmark 可跑 | 是 | T4-05, T3-03 |
| T4-07 | Unsloth 加速 | 加速效果可验证 | 否 | T4-02 |

---

## 可观测性任务拆解

| 任务 ID | 任务 | 验收条件 | MVP 必须 | 依赖 |
|---------|------|---------|---------|------|
| T2-01 | vLLM /metrics 端点 | metrics 可抓取 | 是 | T1-06 |
| T2-02 | Prometheus 部署 | metrics 存储可用 | 否 | T2-01 |
| T2-03 | Grafana + vLLM dashboard | dashboard 可查看 | 否 | T2-02 |
| T2-04 | Langfuse SDK 埋点 | trace 数据上报成功 | 否 | T2-01 |
| T2-05 | gateway tracing | token 用量可统计 | 否 | T1-12 |

---

## 基础设施任务拆解

| 任务 ID | 任务 | 验收条件 | 依赖 |
|---------|------|---------|------|
| T0-01 | 项目仓库骨架 | 目录结构符合预期 | - |
| T0-02 | CI 基础 | lint/test 可运行 | T0-01 |
| T0-03 | README 初版 | 文档结构清晰 | T0-01 |
| T0-04 | 任务看板 | TASKBOARD.md 可用 | T0-01 |

---

## MVP 必须任务（按阶段排列）

### Phase 0（基础设施）
```
T0-01 → T0-02 → T0-03 → T0-04
```

### Phase 1（推理核心）
```
T1-01 → T1-02 → T1-05 → T1-06 → T1-03 → T1-04 → T1-07
                ↓
            T1-08 → T1-09 → T1-10 → T1-11 → T1-12
```

### Phase 2（可观测性）
```
T2-01 → T2-02（可选）
        T2-03（可选）
        T2-04（可选）
        T2-05（可选）
```

### Phase 3（评测能力）
```
T3-01 → T3-02 → T3-03 → T3-04 → T3-05 → T3-06
```

### Phase 4（微调能力）
```
T4-01 → T4-02 → T4-05 → T4-06
              ↓
          T4-03（可选）
          T4-04（可选）
          T4-07（可选）
```

---

## 关键路径（MVP 完成最短路径）

```
T0-01 → T0-02 → T0-03 → T0-04 →
T1-01 → T1-02 → T1-05 → T1-06 → T1-03 → T1-04 →
T1-08 → T1-09 → T1-10 → T1-11 → T1-12 →
T3-01 → T3-02 → T3-03 → T3-04 → T3-05 →
T4-01 → T4-02 → T4-05 → T4-06
```

---

## 可选任务（不阻塞 MVP）

| 任务 ID | 任务 | 说明 |
|---------|------|------|
| T2-02 | Prometheus 部署 | metrics 存储 |
| T2-03 | Grafana dashboard | 可视化 |
| T2-04 | Langfuse SDK 埋点 | trace 上报 |
| T2-05 | gateway tracing | token 计量 |
| T4-03 | QLoRA 集成 | 4-bit 量化 |
| T4-04 | SFTTrainer 集成 | SFT 训练 |
| T4-07 | Unsloth 加速 | GPU 加速 |

---

## Codex 执行建议

1. **并行化**：Phase 2 和 Phase 3 可在 Phase 1 完成后并行
2. **MVP 优先**：先完成必须任务，可选任务后续按需引入
3. **验证串联**：T4-06 需要 T3-03 已完成，确保评测能力先就绪

---

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval
3. https://github.com/huggingface/peft — PEFT

Risk of Staleness:
- 任务粒度可能需要根据实际执行情况调整

Out of Scope Kept:
- 未写具体排期
- 未写人员分工
