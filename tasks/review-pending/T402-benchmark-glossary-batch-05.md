Task ID: T402
Task Title: Evaluation / Benchmark Long-Run Pack v1
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 T312/T309，产出 8 个 benchmark/leaderboard 相关术语的 glossary。

Result:

# Benchmark / Leaderboard Glossary Batch 05

## 条目列表

---

### Accuracy

**定义**：准确率，模型预测正确答案的比例，是分类和知识评测任务中的核心指标。

**边界说明**：Accuracy 是通用评测指标，适用于有标准答案的选择题、判断题等任务；不适用于开放式生成或代码生成评测。

**来源**：https://github.com/EleutherAI/lm-evaluation-harness

---

### Pass@K

**定义**：K 次独立采样中至少有一次通过测试的比例，常用于代码模型评测（HumanEval、MBPP）。

**边界说明**：Pass@K 是代码模型评测的核心指标，K 值越大通过率越高但测试越宽松；区别于准确率等分类指标。

**来源**：https://github.com/bigcode-project/bigcode-eval-harness

---

### Elo

**定义**：人类盲评对战中，根据胜负关系计算的单打独斗评分，反映模型的相对强弱。

**边界说明**：Elo 是 Arena 场景下的评分机制，区别于 Benchmark 的绝对分数；Elo 分数只有在对战环境下才有意义。

**来源**：https://chat.lmsys.org/

---

### Benchmark

**定义**：在标准数据集上执行评测、输出量化分数的体系，代表模型在特定任务上的绝对能力。

**边界说明**：Benchmark 是评测执行和结果的统称，区别于纯展示的 Leaderboard；Benchmark 结果质量取决于评测工具版本和数据集版本。

**来源**：https://github.com/EleutherAI/lm-evaluation-harness

---

### Leaderboard

**定义**：聚合多个模型在 Benchmark 上分数的排名表，按分数排序展示模型相对位置。

**边界说明**：Leaderboard 是 Benchmark 结果的展示聚合层，自身不执行评测；不同 Leaderboard 选择的评测集和权重不同，跨榜比较需谨慎。

**来源**：https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard

---

### Arena

**定义**：基于人类盲评对战的评测方式，将两个模型的回答展示给人类评分者，根据胜负关系计算 Elo 评分。

**边界说明**：Arena 包含对战机制和结果展示两部分，区别于纯分数排名的 Leaderboard；Arena 反映人类主观偏好，与客观 Benchmark 分数维度不同。

**来源**：https://chat.lmsys.org/

---

### MMLU

**定义**：Massive Multitask Language Understanding，涵盖 57 个学科选择题的综合评测数据集，用于评估模型在广泛知识领域的能力。

**边界说明**：MMLU 是标准化 benchmark 数据集，区别于代码评测（HumanEval）或数学评测（GSM8K）；MMLU 分数反映模型的综合知识水平。

**来源**：https://github.com/EleutherAI/lm-evaluation-harness

---

### GSM8K

**定义**：Grade School Math 8K，包含约 8000 道初中数学题目的评测数据集，用于评估模型的数学推理能力。

**边界说明**：GSM8K 是数学推理 benchmark，区别于综合知识评测（MMLU）；GSM8K 答案需要多步推理过程，评测的是模型解题能力而非知识记忆。

**来源**：https://github.com/EleutherAI/lm-evaluation-harness

---

Sources:
1. https://github.com/EleutherAI/lm-evaluation-harness — LM-Eval Harness
2. https://github.com/bigcode-project/bigcode-eval-harness — BigCode Eval Harness
3. https://chat.lmsys.org/ — LMSYS Chatbot Arena
4. https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard — Open LLM Leaderboard

Risk of Staleness:
- 各 benchmark 数据集版本可能影响分数含义
- LMSYS Arena 按季度更新，Elo 排名变化较快
- LM-Eval Harness 版本更新可能影响 benchmark 兼容性

Out of Scope Kept:
- 未写扩展性背景介绍
- 未写排名评论文章
- 未写训练相关术语
