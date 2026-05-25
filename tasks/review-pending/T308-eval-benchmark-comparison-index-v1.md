Task ID: T308
Task Title: 产出 evaluation / benchmark comparison-index v1
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 T205/T306，产出 evaluation/benchmark comparison-index v1，比较 LM-Eval Harness、Stanford HELM、BigCode Eval Harness、LMSYS Chatbot Arena、Open LLM Leaderboard 五个对象。

Result:

# Evaluation / Benchmark Comparison Index v1

## 比较对象

- LM-Eval Harness
- Stanford HELM
- BigCode Eval Harness
- LMSYS Chatbot Arena
- Open LLM Leaderboard

## 定位比较

| 对象 | 定位 | 来源 |
|------|------|------|
| **LM-Eval Harness** | 标准 benchmark 评测工具，执行模型能力评测并输出量化分数 | https://github.com/EleutherAI/lm-evaluation-harness |
| **Stanford HELM** | 全面评测框架，执行评测并提供结果展示，覆盖多场景 | https://crfm.stanford.edu/helm/ |
| **BigCode Eval Harness** | 代码模型专用评测工具，评测 HumanEval、MBPP 等代码任务 | https://github.com/bigcode-project/bigcode-eval-harness |
| **LMSYS Chatbot Arena** | 基于人类盲评的对战排名平台，通过 Elo 评分展示模型相对能力 | https://chat.lmsys.org/ |
| **Open LLM Leaderboard** | Hugging Face 官方的开源模型排行榜，展示标准 benchmark 结果 | https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard |

## 所处层级比较

| 对象 | 所处层级 | 说明 | 来源 |
|------|---------|------|------|
| **LM-Eval Harness** | 工具/框架层 | 执行 benchmark 评测的工具，输出原始分数 | https://github.com/EleutherAI/lm-evaluation-harness |
| **Stanford HELM** | 框架 + 展示层 | 评测框架兼结果展示，多场景覆盖 | https://crfm.stanford.edu/helm/ |
| **BigCode Eval Harness** | 工具/框架层 | 代码评测专用工具，输出 Pass@K 等指标 | https://github.com/bigcode-project/bigcode-eval-harness |
| **LMSYS Chatbot Arena** | 展示层 | 人类盲评对战平台，输出 Elo 评分排名 | https://chat.lmsys.org/ |
| **Open LLM Leaderboard** | 展示层 | 聚合 benchmark 结果的排行榜 | https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard |

层级关系：
```
框架层：LM-Eval Harness / Stanford HELM / BigCode Eval Harness（执行评测）
    ↓
展示层：LMSYS Chatbot Arena / Open LLM Leaderboard（呈现结果）
```

## 典型使用场景

| 对象 | 典型使用场景 | 来源 |
|------|-------------|------|
| **LM-Eval Harness** | 在标准数据集（MMLU、GSM8K 等）上评测模型能力 | https://github.com/EleutherAI/lm-evaluation-harness |
| **Stanford HELM** | 全面评测模型在多场景下的综合表现 | https://crfm.stanford.edu/helm/ |
| **BigCode Eval Harness** | 评测代码模型的 HumanEval、MBBP 等任务 | https://github.com/bigcode-project/bigcode-eval-harness |
| **LMSYS Chatbot Arena** | 通过人类盲评对战了解模型相对强弱 | https://chat.lmsys.org/ |
| **Open LLM Leaderboard** | 查看开源模型在标准 benchmark 上的排名 | https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard |

## 与本项目关系

| 对象 | 与本项目关系 |
|------|------------|
| **LM-Eval Harness** | eval-module 评测工具的首选，可与 vLLM backend 对接 |
| **Stanford HELM** | 作为全面评测框架参考，了解评测维度设计 |
| **BigCode Eval Harness** | 若涉及代码模型评测，可作为专用工具 |
| **LMSYS Chatbot Arena** | 作为模型选型的参考排名，不直接集成 |
| **Open LLM Leaderboard** | 作为模型基础能力选型的参考，不直接集成 |

Sources:
1. https://github.com/EleutherAI/lm-evaluation-harness — LM-Eval Harness 主仓库
2. https://crfm.stanford.edu/helm/ — Stanford HELM 官网
3. https://github.com/bigcode-project/bigcode-eval-harness — BigCode Eval Harness 主仓库
4. https://chat.lmsys.org/ — LMSYS Chatbot Arena
5. https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard — Open LLM Leaderboard

Risk of Staleness:
- LMSYS Arena 和 Open LLM Leaderboard 按季度更新，排名变化较快
- LM-Eval Harness 版本更新可能影响 benchmark 兼容性
- 各 benchmark 数据集版本可能影响结果可比性

Out of Scope Kept:
- 未写完整评测手册
- 未做 leaderboard 分析文章
- 未写分布式训练相关

Need Codex Review On:
- eval-module 中具体使用哪个评测工具（以实际实现为准）
