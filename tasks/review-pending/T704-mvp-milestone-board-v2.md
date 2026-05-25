Task ID: T704
Task Title: Cross-Project Deep-Research Pack
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
把 Phase 进一步拆细，便于 Codex 后续拆任务。

Result:

# MVP Milestone Board v2

## 概述

本文档在 v1 基础上进一步细化里程碑，按阶段拆分成更细粒度的任务单元。

---

## 里程碑总览

| 阶段 | 里程碑 | 核心验收条件 |
|------|--------|------------|
| **Phase 0** | 基础设施就绪 | 仓库骨架 / CI / 文档 |
| **Phase 1** | 推理可跑 | vLLM + gateway + 串联 |
| **Phase 2** | 可观测性就绪 | metrics + traces（可选） |
| **Phase 3** | 评测可跑 | lm-eval + 结果持久化 |
| **Phase 4** | 微调可跑 | LoRA + 评测验证 |

---

## Phase 0：基础设施

| 任务 ID | 任务 | 验收条件 |
|---------|------|---------|
| T0-01 | 建立项目仓库骨架 | 目录结构符合预期 |
| T0-02 | 建立 CI 基础 | lint / test 可运行 |
| T0-03 | 建立 README 初版 | 文档结构清晰 |
| T0-04 | 建立任务看板 | TASKBOARD.md 可用 |

---

## Phase 1：推理核心

| 任务 ID | 任务 | 验收条件 |
|---------|------|---------|
| T1-01 | inference-service MVP 设计 | MVP 文档完成 |
| T1-02 | vLLM 集成 | vLLM 服务可启动 |
| T1-03 | OpenAI 兼容 API | /v1/chat/completions 可调用 |
| T1-04 | ai-gateway MVP 设计 | MVP 文档完成 |
| T1-05 | gateway 路由/鉴权/限流 | 基础功能可用 |
| T1-06 | gateway → inference 串联 | 端到端推理可跑 |
| T1-07 | 健康检查接口 | /health 返回正常 |

---

## Phase 2：可观测性

| 任务 ID | 任务 | 验收条件 | MVP 必须 |
|---------|------|---------|---------|
| T2-01 | vLLM /metrics 端点 | metrics 可抓取 | 是 |
| T2-02 | Prometheus 部署 | metrics 存储可用 | 否 |
| T2-03 | Grafana + vLLM dashboard | dashboard 可查看 | 否 |
| T2-04 | Langfuse SDK 埋点 | trace 数据上报成功 | 否 |
| T2-05 | gateway tracing | token 用量可统计 | 否 |

---

## Phase 3：评测能力

| 任务 ID | 任务 | 验收条件 |
|---------|------|---------|
| T3-01 | eval-module MVP 设计 | MVP 文档完成 |
| T3-02 | lm-eval 集成 | lm-eval 可运行 |
| T3-03 | MMLU benchmark 可跑 | 分数正常返回 |
| T3-04 | GSM8K benchmark 可跑 | 分数正常返回 |
| T3-05 | 结果 JSON 持久化 | 文件保存成功 |
| T3-06 | 历史结果对比 | 两个结果可对比 |

---

## Phase 4：微调能力

| 任务 ID | 任务 | 验收条件 | MVP 必须 |
|---------|------|---------|---------|
| T4-01 | finetune-demo MVP 设计 | MVP 文档完成 | 是 |
| T4-02 | PEFT/LoRA 集成 | LoRA adapter 可训练 | 是 |
| T4-03 | QLoRA 集成（可选） | 4-bit 量化可训练 | 否 |
| T4-04 | trl SFTTrainer 集成 | SFT 可运行 | 否 |
| T4-05 | adapter 保存/加载 | adapter 持久化可用 | 是 |
| T4-06 | 训练+评测串联 | 微调后 benchmark 可跑 | 是 |
| T4-07 | Unsloth 加速（可选） | 加速效果可验证 | 否 |

---

## 里程碑依赖关系

```
Phase 0（基础设施）
    ↓
Phase 1（推理核心）
    ↓ ↓ ← 可并行
Phase 2  Phase 3
  ↓         ↓
Phase 4（微调 + 评测串联）
```

---

## MVP 必须任务（精简版）

| 任务 ID | 任务 | 所属 Phase |
|---------|------|-----------|
| T0-01 ~ T0-04 | 基础设施 | Phase 0 |
| T1-01 ~ T1-07 | 推理核心 | Phase 1 |
| T2-01 | metrics 端点 | Phase 2 |
| T3-01 ~ T3-06 | 评测能力 | Phase 3 |
| T4-01, T4-02, T4-05, T4-06 | 微调能力（部分） | Phase 4 |

---

## 每个里程碑的 Codex 判断点

| 里程碑 | 需要 Codex 判断 |
|--------|---------------|
| Phase 1 | 默认 vLLM 还是 SGLang？ |
| Phase 2 | Langfuse self-hosted 还是云端？是否引入 Prometheus？ |
| Phase 3 | lm-eval 结果是否上报 Langfuse？ |
| Phase 4 | QLoRA 是否作为 MVP 默认？ |

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval
3. https://github.com/huggingface/peft — PEFT
4. https://langfuse.com/docs/observability/overview — Langfuse

Risk of Staleness:
- 里程碑粒度可能需要根据实际执行情况调整

Out of Scope Kept:
- 未写具体排期
- 未写人员分工
- 未写详细技术方案
