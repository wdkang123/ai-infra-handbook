Task ID: T402
Task Title: Evaluation / Benchmark Long-Run Pack v1
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 T306-v1，产出 eval/benchmark sources-index v2，补齐更稳定的精确优先阅读链接。

Result:

# Evaluation / Benchmark Sources Index v2

## 一、Evaluation 框架

### 官方入口

| 工具 | 官方入口 |
|------|---------|
| **LM-Eval Harness** | https://github.com/EleutherAI/lm-evaluation-harness |
| **BigCode Evaluation Harness** | https://github.com/bigcode-project/bigcode-eval-harness |
| **Stanford HELM** | https://crfm.stanford.edu/helm/ |
| **Agenta** | https://github.com/agenta-ai/agenta |

### 边界说明
Evaluation 框架提供评测工具和评测流程，输出模型在特定任务上的量化分数。不同框架覆盖的评测集和接口不同。

### 精确优先阅读链接（5 个）

1. **LM-Eval Harness GitHub** — https://github.com/EleutherAI/lm-evaluation-harness — 标准 benchmark 评测工具，支持多种标准数据集
2. **BigCode Evaluation Harness GitHub** — https://github.com/bigcode-project/bigcode-eval-harness — 代码模型专用评测工具
3. **Stanford HELM 官网** — https://crfm.stanford.edu/helm/ — 全面评测框架，多场景覆盖
4. **Agenta GitHub** — https://github.com/agenta-ai/agenta — 开源 LLMOps，含评测能力
5. **LM-Eval Harness 文档** — https://github.com/EleutherAI/lm-evaluation-harness?tab=readme-ov-file#supported-models — 支持的模型和任务列表

---

## 二、Benchmark / Leaderboard / Arena

### 官方入口

| 工具 | 官方入口 |
|------|---------|
| **Open LLM Leaderboard** | https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard |
| **LMSYS Chatbot Arena** | https://chat.lmsys.org/ |
| **Stanford HELM** | https://crfm.stanford.edu/helm/ |
| **BigCode Leaderboard** | https://huggingface.co/spaces/bigcode/bigcode-leaderboard |

### 边界说明
Benchmark/Leaderboard/Arena 是评测结果的展示层。Leaderboard 聚合分数排名，Arena 通过人类对战展示相对强弱，展示层本身不执行评测，依赖底层 Evaluation 框架提供数据。

### 精确优先阅读链接（6 个）

1. **Open LLM Leaderboard** — https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard — Hugging Face 官方开源模型排行榜
2. **LMSYS Chatbot Arena** — https://chat.lmsys.org/ — 基于人类盲评的模型对战排名
3. **Stanford HELM** — https://crfm.stanford.edu/helm/ — 评测框架兼结果展示
4. **BigCode Leaderboard** — https://huggingface.co/spaces/bigcode/bigcode-leaderboard — 代码模型专项排行榜
5. **EleutherAI LM-Eval Harness** — https://github.com/EleutherAI/lm-evaluation-harness — 多数 benchmark 的底层工具
6. **BigCode Evaluation Harness** — https://github.com/bigcode-project/bigcode-eval-harness — 代码模型 benchmark 底层工具

---

## 三、关键数据集

### 官方入口

| 数据集 | 官方入口 |
|--------|---------|
| **MMLU** | https://github.com/EleutherAI/lm-evaluation-harness |
| **GSM8K** | https://github.com/EleutherAI/lm-evaluation-harness |
| **HumanEval** | https://github.com/openai/human-eval |
| **MBPP** | https://github.com/bigcode-project/bigcode-eval-harness |

### 精确优先阅读链接（4 个）

1. **MMLU / GSM8K 评测入口** — https://github.com/EleutherAI/lm-evaluation-harness — 通过 lm-eval 工具运行
2. **HumanEval 数据集** — https://github.com/openai/human-eval — OpenAI 代码评测数据集
3. **BigCode Eval Harness 文档** — https://github.com/bigcode-project/bigcode-eval-harness — MBPP 等代码数据集评测说明
4. **MMLU 数据集说明** — https://arxiv.org/abs/2009.03300 — MMLU 论文（理解评测维度参考）

Sources:
1. https://github.com/EleutherAI/lm-evaluation-harness — LM-Eval Harness 主仓库
2. https://github.com/bigcode-project/bigcode-eval-harness — BigCode Eval Harness
3. https://crfm.stanford.edu/helm/ — Stanford HELM 官网
4. https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard — Open LLM Leaderboard
5. https://chat.lmsys.org/ — LMSYS Chatbot Arena
6. https://github.com/openai/human-eval — HumanEval 数据集

Risk of Staleness:
- LMSYS Arena 和 Open LLM Leaderboard 按季度更新，排名变化较快
- LM-Eval Harness 版本更新可能影响 benchmark 兼容性
- 各 benchmark 数据集版本可能影响结果可比性

Out of Scope Kept:
- 未写完整评测手册
- 未做排名结论
- 未写分布式训练相关
