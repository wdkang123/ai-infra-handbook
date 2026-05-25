Task ID: T704
Task Title: Cross-Project Deep-Research Pack
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
列出8到12个推进风险，按技术、资料、实现、验证四类整理。

Result:

# Risk Register v2

## 概述

本文档在 v1 基础上更新推进风险，按技术、资料、实现、验证四类整理。

---

## 技术风险

### R-01：推理引擎版本不兼容

| 维度 | 内容 |
|------|------|
| **风险** | vLLM/SGLang 版本更新导致 API 不兼容 |
| **影响** | 需要修改 inference-service 代码 |
| **缓解措施** | 锁定版本，做好变更记录 |
| **来源** | https://docs.vllm.ai/ |

### R-02：GPU 显存不足

| 维度 | 内容 |
|------|------|
| **风险** | LoRA/QLoRA 训练显存需求超出实际硬件 |
| **影响** | 无法完成训练，或需要降级配置 |
| **缓解措施** | 先评估硬件环境，再确定微调方法 |
| **来源** | https://arxiv.org/abs/2305.14314 |

### R-03：多引擎切换复杂度

| 维度 | 内容 |
|------|------|
| **风险** | 同时支持 vLLM/SGLang/Triton 增加接口复杂度 |
| **影响** | gateway 需要适配多种接口 |
| **缓解措施** | MVP 只支持一种引擎，后续按需扩展 |
| **来源** | https://docs.vllm.ai/ |

---

## 资料风险

### R-04：文档时效性

| 维度 | 内容 |
|------|------|
| **风险** | Langfuse/lm-eval/PEFT 等工具更新快，文档可能过时 |
| **影响** | 实际接入时发现接口与文档不符 |
| **缓解措施** | 以实际安装版本和官方 GitHub 为准 |
| **来源** | https://github.com/EleutherAI/lm-evaluation-harness |

### R-05：TensorRT-LLM 编译依赖特定环境

| 维度 | 内容 |
|------|------|
| **风险** | TensorRT-LLM 需要特定 GPU 型号和驱动版本 |
| **影响** | 在非 NVIDIA 环境下无法编译和运行 |
| **缓解措施** | 确认硬件环境后再决定是否引入 TensorRT-LLM |
| **来源** | https://nvidia.github.io/TensorRT-LLM/ |

### R-06：OTel 日志信号不稳定

| 维度 | 内容 |
|------|------|
| **风险** | OpenTelemetry Logs 信号仍为草案，生产使用有风险 |
| **影响** | 日志采集方案可能需要调整 |
| **缓解措施** | 日志方案暂缓，优先 traces 和 metrics |
| **来源** | https://opentelemetry.io/ |

---

## 实现风险

### R-07：lm-eval API 变更

| 维度 | 内容 |
|------|------|
| **风险** | lm-eval v0.4 版本 API 有较大变化 |
| **影响** | eval-module 调用 lm-eval 的代码需要适配 |
| **缓解措施** | 使用稳定的 lm-eval 版本，做好版本锁定 |
| **来源** | https://github.com/EleutherAI/lm-evaluation-harness |

### R-08：Langfuse self-hosted 运维复杂度

| 维度 | 内容 |
|------|------|
| **风险** | self-hosted Langfuse 需要额外运维（数据库 / 存储） |
| **影响** | 增加部署复杂度 |
| **缓解措施** | MVP 阶段可用 Langfuse 云端 |
| **来源** | https://langfuse.com/docs/ |

### R-09：DPO 偏好数据获取成本

| 维度 | 内容 |
|------|------|
| **风险** | DPO 需要高质量偏好数据集，标注成本高 |
| **影响** | DPO 无法在 MVP 阶段落地 |
| **缓解措施** | MVP 只做 SFT，DPO 后续按需评估 |
| **来源** | https://arxiv.org/abs/2305.18290 |

---

## 验证风险

### R-10：benchmark 结果不可比

| 维度 | 内容 |
|------|------|
| **风险** | 不同版本 lm-eval 或不同评测配置导致结果不可比 |
| **影响** | 历史评测结果对比失效 |
| **缓解措施** | 统一 lm-eval 版本和评测配置 |
| **来源** | https://github.com/EleutherAI/lm-evaluation-harness |

### R-11：LoRA 超参数敏感

| 维度 | 内容 |
|------|------|
| **风险** | LoRA 的 rank/alpha 对效果影响大，需要大量实验调优 |
| **影响** | 训练效果不佳，难以达到预期 |
| **缓解措施** | 参考已有最佳实践，从默认参数开始 |
| **来源** | https://arxiv.org/abs/2106.09685 |

### R-12：多模块集成接口契约缺失

| 维度 | 内容 |
|------|------|
| **风险** | 各模块独立开发，接口对接时发现不匹配 |
| **影响** | 需要返工或临时适配 |
| **缓解措施** | 开发前先确定接口草案，定期集成验证 |
| **来源** | — |

---

## 风险矩阵（v2 更新）

| 风险 | 类型 | 概率 | 影响 | 优先级 |
|------|------|------|------|-------|
| R-01 引擎版本不兼容 | 技术 | 中 | 中 | 中 |
| R-02 GPU 显存不足 | 技术 | 高 | 高 | 高 |
| R-03 多引擎切换复杂度 | 技术 | 低 | 中 | 低 |
| R-04 文档时效性 | 资料 | 高 | 中 | 中 |
| R-05 TRT-LLM 环境依赖 | 资料 | 中 | 高 | 中 |
| R-06 OTel Logs 不稳定 | 资料 | 低 | 中 | 低 |
| R-07 lm-eval API 变更 | 实现 | 中 | 高 | 高 |
| R-08 Langfuse 运维 | 实现 | 中 | 中 | 中 |
| R-09 DPO 数据成本 | 实现 | 高 | 高 | 高 |
| R-10 结果不可比 | 验证 | 中 | 中 | 中 |
| R-11 LoRA 超参数敏感 | 验证 | 高 | 中 | 中 |
| R-12 接口契约缺失 | 验证 | 中 | 高 | 高 |

---

## 高优先级风险（需要 Codex 关注）

| 风险 | 说明 |
|------|------|
| R-02 GPU 显存不足 | 可能导致训练无法进行 |
| R-07 lm-eval API 变更 | 可能导致评测失败 |
| R-09 DPO 数据成本 | 可能影响后续迭代计划 |
| R-12 接口契约缺失 | 可能导致返工 |

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval
3. https://arxiv.org/abs/2305.14314 — QLoRA
4. https://arxiv.org/abs/2305.18290 — DPO
5. https://nvidia.github.io/TensorRT-LLM/ — TensorRT-LLM
6. https://opentelemetry.io/ — OpenTelemetry
7. https://langfuse.com/docs/ — Langfuse

Risk of Staleness:
- 各工具版本更新可能引入新的风险

Out of Scope Kept:
- 未写具体缓解措施执行方案
- 未写风险应对预案
