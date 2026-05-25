Task ID: T704
Task Title: Cross-Project Deep-Research Pack
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
把 Phase 进一步拆细，便于 Codex 后续拆任务。

Result:

# Build Order Roadmap v2

## 概述

本文档在 v1 基础上进一步细化推进路线，按阶段划分，先做什么、后做什么、哪些可以并行。

---

## 阶段 0：基础设施（前置）

| 任务 | 说明 | 验收条件 |
|------|------|---------|
| T0-01 | 建立项目仓库骨架 | 目录结构符合预期 |
| T0-02 | 建立 CI 基础 | lint / test 可运行 |
| T0-03 | 建立 README 初版 | 文档结构清晰 |
| T0-04 | 建立任务看板 | TASKBOARD.md 可用 |

---

## 阶段 1：推理核心（最早可验证）

| 任务 | 说明 | 验收条件 | 紧密度 |
|------|------|---------|---------|
| T1-01 | inference-service MVP 设计 | MVP 文档完成 | 必须 |
| T1-02 | vLLM 集成 | vLLM 服务可启动 | 必须 |
| T1-03 | OpenAI 兼容 API | /v1/chat/completions 可调用 | 必须 |
| T1-04 | ai-gateway MVP 设计 | MVP 文档完成 | 必须 |
| T1-05 | gateway 路由/鉴权/限流 | 基础功能可用 | 必须 |
| T1-06 | gateway → inference 串联 | 端到端推理可跑 | 必须 |
| T1-07 | 健康检查接口 | /health 返回正常 | 必须 |

**可并行**：T1-01 与 T1-04 可并行开发，通过接口 Mock 联调

---

## 阶段 2：可观测性（与阶段1可部分并行）

| 任务 | 说明 | 验收条件 | 紧密度 |
|------|------|---------|---------|
| T2-01 | vLLM /metrics 端点 | metrics 可抓取 | 必须 |
| T2-02 | Prometheus 部署 | metrics 存储可用 | 建议 |
| T2-03 | Grafana + vLLM dashboard | dashboard 可查看 | 建议 |
| T2-04 | Langfuse SDK 埋点 | trace 数据上报成功 | 建议 |
| T2-05 | gateway tracing | token 用量可统计 | 可选 |

**与阶段1关系**：T2-01 在 T1-02 完成后立即开始；T2-02/03/04 可与 T1 并行

---

## 阶段 3：评测能力（阶段1之后）

| 任务 | 说明 | 验收条件 | 紧密度 |
|------|------|---------|---------|
| T3-01 | eval-module MVP 设计 | MVP 文档完成 | 必须 |
| T3-02 | lm-eval 集成 | lm-eval 可运行 | 必须 |
| T3-03 | MMLU benchmark 可跑 | 分数正常返回 | 必须 |
| T3-04 | GSM8K benchmark 可跑 | 分数正常返回 | 必须 |
| T3-05 | 结果 JSON 持久化 | 文件保存成功 | 必须 |
| T3-06 | 历史结果对比 | 两个结果可对比 | 必须 |

**依赖关系**：T3 需要 T1（inference-service）完成

---

## 阶段 4：微调能力（阶段3之后或并行）

| 任务 | 说明 | 验收条件 | 紧密度 |
|------|------|---------|---------|
| T4-01 | finetune-demo MVP 设计 | MVP 文档完成 | 必须 |
| T4-02 | PEFT/LoRA 集成 | LoRA adapter 可训练 | 必须 |
| T4-03 | QLoRA 集成（可选） | 4-bit 量化可训练 | 建议 |
| T4-04 | trl SFTTrainer 集成 | SFT 可运行 | 可选（后续 DPO） |
| T4-05 | adapter 保存/加载 | adapter 持久化可用 | 必须 |
| T4-06 | 训练+评测串联 | 微调后 benchmark 可跑 | 必须 |
| T4-07 | Unsloth 加速（可选） | 加速效果可验证 | 按需 |

**可并行**：T4 与 T3 可并行开发，通过 Mock 接口联调

---

## 阶段 5：生产增强（后续迭代）

| 任务 | 说明 | 验收条件 | 紧密度 |
|------|------|---------|---------|
| T5-01 | SGLang 备选引擎 | SGLang 可用 | 可选 |
| T5-02 | Triton IS 集成 | 多模型编排可用 | 可选 |
| T5-03 | TensorRT-LLM | 编译模型可部署 | 可选 |
| T5-04 | Langfuse 结果上报 | 评测结果上报 Langfuse | 可选 |
| T5-05 | DPO 微调 | DPO 可运行 | 可选 |
| T5-06 | HumanEval benchmark | 代码评测可跑 | 可选 |

---

## 关键里程碑（v2 收紧）

| 里程碑 | 验收条件 | 对应任务 |
|--------|---------|---------|
| **M1：推理可跑** | vLLM 服务启动，/v1/chat/completions 返回结果 | T1-02/03 |
| **M2：gateway 串联** | 通过 gateway 调用 inference 返回结果 | T1-05/06 |
| **M3：metrics 可用** | Prometheus 可抓取 Grafana 能看到 | T2-01/02 |
| **M4：评测可跑** | lm-eval 跑通 MMLU，返回分数 | T3-02/03 |
| **M5：微调可跑** | LoRA 训练完成，adapter 保存成功 | T4-02/05 |
| **M6：训练+评测串联** | finetune 后跑 benchmark，对比基线 | T4-06 |

---

## 并行推进建议（v2）

| 组合 | 说明 |
|------|------|
| 推理核心 + 可观测性 | 阶段1 + 阶段2并行（T2-01 依赖 T1-02） |
| eval + finetune | 阶段3 + 阶段4并行（通过 Mock 接口） |
| inference-service + ai-gateway | 阶段1内并行 |

---

## 风险提示

- T5（生产增强）阶段的 Triton IS / TensorRT-LLM 引入会增加复杂度
- DPO（T5-05）需要高质量偏好数据，可能延后

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval
3. https://github.com/huggingface/peft — PEFT
4. https://langfuse.com/docs/observability/overview — Langfuse

Risk of Staleness:
- 各工具版本更新可能影响里程碑可行性

Out of Scope Kept:
- 未写代码实现
- 未写具体排期
- 未写人员分工
