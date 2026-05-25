Task ID: T313
Task Title: 产出 observability / evaluation glossary batch 03
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 T204/T205/T306/T307，产出 10 个 observability/evaluation 相关术语的 glossary。

Result:

# Observability / Evaluation Glossary Batch 03

## 条目列表

---

### Trace

**定义**：单个请求从发起到完成的完整调用链，每个环节记录为一个 span。

**边界说明**：Trace 关注请求的完整路径，区别于聚合指标（metrics）；OpenTelemetry 是 Trace 采集的标准协议。

**来源**：https://opentelemetry.io/docs/concepts/observability-primer/#distributed-traces

---

### Span

**定义**：Trace 中的单个操作单元，记录一个环节的开始时间、结束时间和属性信息（如模型名称、延迟）。

**边界说明**：Span 是 Trace 的子单元，多个 Span 构成完整 Trace；Span 的顺序和嵌套关系反映调用依赖。

**来源**：https://opentelemetry.io/docs/concepts/observability-primer/#distributed-traces

---

### OpenTelemetry

**定义**：CNCF 标准的 traces/metrics 日志数据采集规范和 SDK，提供统一的数据采集接口，不直接提供存储和展示层。

**边界说明**：OpenTelemetry 是规范层和采集层，数据可接入多种后端（Jaeger、Prometheus、Grafana 等）；区别于 Langfuse 等端到端可观测性平台。

**来源**：https://opentelemetry.io/

---

### LLM-as-Judge

**定义**：用强模型评估弱模型输出质量的方法，适合无法用规则定义正确答案的开放式任务。

**边界说明**：LLM-as-Judge 是 Evaluation 的一种方法，区别于基于规则的 Heuristic Eval；其评估质量受 judge 模型本身能力影响。

**来源**：https://langfuse.com/docs/observability/overview

---

### Replay（回放）

**定义**：用真实历史请求重放，验证新版本模型在相同输入下的输出质量变化。

**边界说明**：Replay 属于 Evaluation 范畴，区别于 Benchmark 在标准数据集上的评测；Replay 使用生产流量，更贴近实际场景。

**来源**：https://crfm.stanford.edu/helm/

---

### Pass@K

**定义**：K 次独立采样中至少有一次通过测试的比例，常用于代码模型评测（HumanEval、MBPP）。

**边界说明**：Pass@K 是代码模型评测的核心指标，K 值越大通过率越高但测试更宽松；区别于准确率等分类指标。

**来源**：https://github.com/bigcode-project/bigcode-eval-harness

---

### Elo

**定义**：人类盲评对战中，根据胜负关系计算的单打独斗评分，反映模型的相对强弱。

**边界说明**：Elo 是 Arena 场景下的评分机制，区别于 Benchmark 的绝对分数；Elo 分数只有在对战环境下才有意义。

**来源**：https://chat.lmsys.org/

---

### Leaderboard

**定义**：聚合多个模型在 Benchmark 上分数的排名表，按总分或单项分数排序。

**边界说明**：Leaderboard 是 Benchmark 结果的展示聚合层，自身不执行评测；不同 Leaderboard 选择的评测集和权重不同，排名不可直接跨榜比较。

**来源**：https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard

---

### Arena

**定义**：基于人类盲评对战的评测方式，将两个模型的回答展示给人类评分者，根据胜负关系计算 Elo 评分。

**边界说明**：Arena 包含对战机制和结果展示两部分，区别于纯展示的 Leaderboard；Arena 反映人类主观偏好，与客观 Benchmark 分数维度不同。

**来源**：https://chat.lmsys.org/

---

### Benchmark

**定义**：在标准数据集（MMLU、GSM8K、HumanEval 等）上执行评测、输出量化分数的体系，代表模型在特定任务上的绝对能力。

**边界说明**：Benchmark 包含评测执行和结果两部分，区别于纯展示的 Leaderboard；Benchmark 结果质量取决于评测工具版本和数据集版本。

**来源**：https://github.com/EleutherAI/lm-evaluation-harness

---

Sources:
1. https://opentelemetry.io/ — OpenTelemetry 官网
2. https://opentelemetry.io/docs/concepts/observability-primer/#distributed-traces — OTel tracing 概念
3. https://langfuse.com/docs/observability/overview — Langfuse 文档
4. https://crfm.stanford.edu/helm/ — Stanford HELM
5. https://github.com/bigcode-project/bigcode-eval-harness — BigCode Eval Harness
6. https://chat.lmsys.org/ — LMSYS Chatbot Arena
7. https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard — Open LLM Leaderboard
8. https://github.com/EleutherAI/lm-evaluation-harness — LM-Eval Harness

Risk of Staleness:
- OpenTelemetry 为 CNCF 标准，稳定性较高
- Arena Elo 和 Leaderboard 排名随时间变化较快
- LM-Eval Harness 版本更新可能影响 Benchmark 定义

Out of Scope Kept:
- 未写扩展性背景介绍
- 未做术语排名或概念演化史
- 未写训练相关术语
