Task ID: T502
Task Title: Eval/Benchmark Long-Run Pack v2
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 T401/T402/T404，产出更完整的 eval/benchmark sources-index v3。

Result:

# Eval/Benchmark Sources Index v3

## 数据集类

### 标准 Benchmark 数据集

| 数据集 | 描述 | 官方链接 | 优先级 |
|--------|------|---------|--------|
| **MMLU** | 多任务语言理解，57个学科选择题 | https://arxiv.org/abs/2009.03300 | 高 |
| **GSM8K** | 小学数学应用题，8.5K 题 | https://arxiv.org/abs/2110.14168 | 高 |
| **HumanEval** | 代码生成评测，164 题 | https://arxiv.org/abs/2107.03374 | 高 |
| **MBPP** | Python 编程题，974 题 | https://github.com/mbpp | 中 |
| **HellaSwag** | 常识推理选择题，10K 题 | https://arxiv.org/abs/1905.07830 | 中 |
| **TruthfulQA** | 真实性问答，817 题 | https://arxiv.org/abs/2109.07958 | 中 |

### 评测框架

| 框架 | 描述 | 官方链接 | 边界说明 |
|------|------|---------|---------|
| **LM-Eval Harness** | 标准 benchmark 评测工具，支持 vLLM/SGLang backend | https://github.com/EleutherAI/lm-evaluation-harness | 不含数据存储和版本对比，需自行实现 |
| **Stanford HELM** | 综合评测框架，覆盖多场景 | https://crfm.stanford.edu/helm/ | 偏学术研究，工程接入成本高 |
| **BigCode Eval Harness** | 代码模型评测专用，Pass@K | https://github.com/bigcode-project/bigcode-eval-harness | 仅覆盖代码模型评测 |

## Leaderboard / Arena 类

### 公开排行榜

| 平台 | 描述 | 官方链接 | 与本项目关系 |
|------|------|---------|------------|
| **Open LLM Leaderboard** | HuggingFace 托管的开源模型排行榜 | https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard | 评测结果可选择性提交 |
| **LMSYS Arena** | 对战式模型评测，Elo 排名 | https://chat.lmsys.org/?leaderboard | 对战 + 展示，不是纯展示层 |
| **OpenCompass** | 司南实验室评测体系 | https://opencompass.org.cn/ | 支持自定义数据集 |
| **FlagEval** | 国产评测体系 | https://flageval.baai.ac.cn/ | 中文模型评测参考 |

### Arena 说明

Arena（对战竞技场）的本质是对战 + 展示：

- **对战**：用户提交两个模型回复，系统随机发给评估者盲测
- **Elo 排名**：基于对战结果计算，动态更新
- **展示**：公开排名页面，供社区参考

边界说明：Arena 不等于 Leaderboard。Leaderboard 是静态 benchmark 分数汇总，Arena 是对战式动态排名。本项目不建设 Arena，但评测结果可对接外部 Arena。

来源：https://chat.lmsys.org/?leaderboard

## 与本项目关系

| 类型 | 与 eval-module 关系 |
|------|------------------|
| LM-Eval Harness | eval-module 的主要评测执行层 |
| Stanford HELM | 仅作参考架构，不直接集成 |
| BigCode Eval Harness | 可选集成（仅代码模型场景） |
| Open LLM Leaderboard | 评测结果可提交 |
| LMSYS Arena | 本项目不建设，但可对接 |
| OpenCompass | 中文评测参考 |

## 优先阅读链接

1. https://github.com/EleutherAI/lm-evaluation-harness — LM-Eval 快速上手
2. https://arxiv.org/abs/2009.03300 — MMLU 论文
3. https://arxiv.org/abs/2110.14168 — GSM8K 论文
4. https://arxiv.org/abs/2107.03374 — HumanEval 论文

## 风险与边界

- lm-eval 的 benchmark 覆盖持续更新，v0.4 版本接口有变化
- 各数据集版本可能影响历史评测结果可比性
- Arena 对战平台需要外部用户参与，本项目不建设

Sources:
1. https://github.com/EleutherAI/lm-evaluation-harness — LM-Eval Harness
2. https://crfm.stanford.edu/helm/ — Stanford HELM
3. https://github.com/bigcode-project/bigcode-eval-harness — BigCode Eval Harness
4. https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard — Open LLM Leaderboard
5. https://chat.lmsys.org/?leaderboard — LMSYS Arena
6. https://opencompass.org.cn/ — OpenCompass
7. https://flageval.baai.ac.cn/ — FlagEval

Risk of Staleness:
- lm-eval 版本更新快，API 兼容性需确认
- 各 benchmark 数据集版本可能变化
- Arena/Leaderboard 平台可能有更新

Out of Scope Kept:
- 未收录所有 benchmark 数据集
- 未写完整评测流程
- 未写内部 Leaderboard 建设方案
