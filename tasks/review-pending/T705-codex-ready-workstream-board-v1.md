Task ID: T705
Task Title: Execution Decomposition Pack
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
把后续实施拆成若干工作流，便于 Codex 继续分发。

Result:

# Codex Ready Workstream Board v1

## 概述

本文档把后续实施拆成若干工作流，便于 Codex 继续分发。每个工作流是可以独立分发的任务束。

---

## 工作流总览

| 工作流 | 名称 | 包含任务数 | 紧密度 |
|--------|------|-----------|--------|
| W1 | 推理核心工作流 | T1-01 ~ T1-07 | 必须 |
| W2 | 可观测性工作流 | T2-01 ~ T2-05 | 建议 |
| W3 | 评测能力工作流 | T3-01 ~ T3-06 | 必须 |
| W4 | 微调能力工作流 | T4-01 ~ T4-07 | 必须 |

---

## W1：推理核心工作流

### 包含任务

| 任务 ID | 任务 | 验收条件 |
|---------|------|---------|
| T1-01 | inference-service MVP 设计 | MVP 文档完成 |
| T1-02 | vLLM 集成 | vLLM 服务可启动 |
| T1-03 | OpenAI 兼容 API | /v1/chat/completions 可调用 |
| T1-04 | ai-gateway MVP 设计 | MVP 文档完成 |
| T1-05 | gateway 路由/鉴权/限流 | 基础功能可用 |
| T1-06 | gateway → inference 串联 | 端到端推理可跑 |
| T1-07 | 健康检查接口 | /health 返回正常 |

### Codex 判断点

1. **默认引擎**：vLLM 还是 SGLang？
2. **Langfuse**：self-hosted 还是云端？

---

## W2：可观测性工作流

### 包含任务

| 任务 ID | 任务 | 验收条件 | MVP 必须 |
|---------|------|---------|---------|
| T2-01 | vLLM /metrics 端点 | metrics 可抓取 | 是 |
| T2-02 | Prometheus 部署 | metrics 存储可用 | 否 |
| T2-03 | Grafana + vLLM dashboard | dashboard 可查看 | 否 |
| T2-04 | Langfuse SDK 埋点 | trace 数据上报成功 | 否 |
| T2-05 | gateway tracing | token 用量可统计 | 否 |

### Codex 判断点

1. **Prometheus/Grafana**：是否在 MVP 引入？
2. **Langfuse Cloud**：是否使用云端版本？

---

## W3：评测能力工作流

### 包含任务

| 任务 ID | 任务 | 验收条件 |
|---------|------|---------|
| T3-01 | eval-module MVP 设计 | MVP 文档完成 |
| T3-02 | lm-eval 集成 | lm-eval 可运行 |
| T3-03 | MMLU benchmark 可跑 | 分数正常返回 |
| T3-04 | GSM8K benchmark 可跑 | 分数正常返回 |
| T3-05 | 结果 JSON 持久化 | 文件保存成功 |
| T3-06 | 历史结果对比 | 两个结果可对比 |

### Codex 判断点

1. **lm-eval 版本**：使用哪个稳定版本？
2. **评测结果上报**：是否上报 Langfuse？

---

## W4：微调能力工作流

### 包含任务

| 任务 ID | 任务 | 验收条件 | MVP 必须 |
|---------|------|---------|---------|
| T4-01 | finetune-demo MVP 设计 | MVP 文档完成 | 是 |
| T4-02 | PEFT/LoRA 集成 | LoRA adapter 可训练 | 是 |
| T4-03 | QLoRA 集成（可选） | 4-bit 量化可训练 | 否 |
| T4-04 | trl SFTTrainer 集成 | SFT 可运行 | 否 |
| T4-05 | adapter 保存/加载 | adapter 持久化可用 | 是 |
| T4-06 | 训练+评测串联 | 微调后 benchmark 可跑 | 是 |
| T4-07 | Unsloth 加速（可选） | 加速效果可验证 | 否 |

### Codex 判断点

1. **QLoRA**：是否作为 MVP 默认微调方法？
2. **Unsloth**：GPU 是否兼容（Ampere/Hopper）？

---

## 工作流分发建议

| 工作流 | 优先级 | 可并行 | 说明 |
|--------|--------|-------|------|
| W1 | P0（必须） | — | 推理是基础 |
| W3 | P0（必须） | W1 之后 | 评测依赖推理 |
| W4 | P0（必须） | W1 之后 | 微调依赖推理 |
| W2 | P1（建议） | W1 并行 | 可观测性辅助优化 |

---

## Codex 判断点汇总

| 判断点 | 工作流 | 紧迫度 |
|--------|--------|-------|
| vLLM vs SGLang | W1 | 高 |
| Langfuse Cloud vs self-hosted | W1/W2 | 高 |
| Prometheus/Grafana 引入 | W2 | 中 |
| QLoRA 作为 MVP 默认 | W4 | 高 |
| Unsloth GPU 兼容性 | W4 | 中 |
| 评测结果是否上报 Langfuse | W3 | 中 |

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval
3. https://github.com/huggingface/peft — PEFT

Risk of Staleness:
- 工作流粒度可能需要根据实际执行情况调整

Out of Scope Kept:
- 未写具体排期
- 未写人员分工
