Task ID: T702
Task Title: Observability / Evaluation Deep-Research Pack
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
继续收紧 evaluation/benchmark/leaderboard/arena 的入口与边界，补官方 release/changelog 入口。

Result:

# Eval/Benchmark Sources Index v5

## 数据集类

### 标准 Benchmark 数据集

| 数据集 | 描述 | 官方链接 | 更新入口 |
|--------|------|---------|---------|
| **MMLU** | 多任务语言理解，57个学科选择题 | https://arxiv.org/abs/2009.03300 | https://github.com/hendrycks/test |
| **GSM8K** | 小学数学应用题，8.5K 题 | https://arxiv.org/abs/2110.14168 | https://openai.com/index/grade-school-math/ |
| **HumanEval** | 代码生成评测，164 题 | https://arxiv.org/abs/2107.03374 | https://github.com/openai/human-eval |
| **MBPP** | Python 编程题，974 题 | https://github.com/mbpp | https://github.com/mbpp |
| **HellaSwag** | 常识推理选择题，10K 题 | https://arxiv.org/abs/1905.07830 | https://github.comrowanz/hellaswag |
| **TruthfulQA** | 真实性问答，817 题 | https://arxiv.org/abs/2109.07958 | https://github.com/sylinrl/TruthfulQA |

来源：各数据集官方页面

---

## 评测框架

### LM-Eval Harness

| 维度 | 内容 |
|------|------|
| **定位** | 标准 benchmark 评测工具 |
| **官方链接** | https://github.com/EleutherAI/lm-evaluation-harness |
| **文档** | https://github.com/EleutherAI/lm-evaluation-harness#lm-eval-harness |
| **支持 backend** | vLLM、SGLang、OpenAI API、HuggingFace Transformers |
| **Release** | https://github.com/EleutherAI/lm-evaluation-harness/releases |
| **边界说明** | 不含数据存储和版本对比，需自行实现 |

来源：https://github.com/EleutherAI/lm-evaluation-harness

### Stanford HELM

| 维度 | 内容 |
|------|------|
| **定位** | 综合评测框架，多场景覆盖 |
| **官方链接** | https://crfm.stanford.edu/helm/ |
| **文档** | https://crfm.stanford.edu/helm/ |
| **边界说明** | 偏学术研究，工程接入成本高 |

来源：https://crfm.stanford.edu/helm/

### BigCode Eval Harness

| 维度 | 内容 |
|------|------|
| **定位** | 代码模型专用评测，Pass@K |
| **官方链接** | https://github.com/bigcode-project/bigcode-eval-harness |
| **Release** | https://github.com/bigcode-project/bigcode-eval-harness/releases |

来源：https://github.com/bigcode-project/bigcode-eval-harness

---

## Leaderboard / Arena 类

### Open LLM Leaderboard

| 维度 | 内容 |
|------|------|
| **定位** | HuggingFace 托管的开源模型排行榜 |
| **官方链接** | https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard |
| **提交入口** | https://huggingface.co/leaderboard/open_llm |
| **边界说明** | 接收社区提交，展示 benchmark 分数 |

来源：https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard

### LMSYS Arena

| 维度 | 内容 |
|------|------|
| **定位** | 对战式模型评测，Elo 排名 |
| **官方链接** | https://chat.lmsys.org/?leaderboard |
| **Blog** | https://blog.lmsys.org/ |
| **边界说明** | 对战 + 展示，不是纯展示层，需要大量外部用户参与 |

来源：https://chat.lmsys.org/?leaderboard

### OpenCompass

| 维度 | 内容 |
|------|------|
| **定位** | 司南实验室评测体系 |
| **官方链接** | https://opencompass.org.cn/ |
| **GitHub** | https://github.com/InternLM/OpenCompass |

来源：https://opencompass.org.cn/

### FlagEval

| 维度 | 内容 |
|------|------|
| **定位** | 国产评测体系 |
| **官方链接** | https://flageval.baai.ac.cn/ |

来源：https://flageval.baai.ac.cn/

---

## 边界说明：Benchmark vs Leaderboard vs Arena

| 类型 | 本质 | 与本项目关系 |
|------|------|------------|
| **Benchmark** | 标准化测试题，产出分数 | eval-module 执行 |
| **Leaderboard** | 静态分数汇总排行 | 评测结果可提交 |
| **Arena** | 对战 + Elo 排名，动态 | 本项目不建设，需要外部用户 |

Arena 的对战性质决定了它需要大量外部用户参与评分，本质上是社区运营平台而非工程系统。

来源：https://chat.lmsys.org/?leaderboard

---

## 与本项目关系

| 类型 | 与 eval-module 关系 |
|------|------------------|
| LM-Eval Harness | 主要评测执行工具 |
| Stanford HELM | 仅作参考架构 |
| BigCode Eval | 可选（代码模型场景） |
| Open LLM Leaderboard | 评测结果可提交 |
| LMSYS Arena | 本项目不建设 |
| OpenCompass | 中文评测参考 |
| FlagEval | 中文评测参考 |

## 优先阅读链接

1. https://github.com/EleutherAI/lm-evaluation-harness — LM-Eval 快速开始
2. https://arxiv.org/abs/2009.03300 — MMLU 论文
3. https://arxiv.org/abs/2110.14168 — GSM8K 论文
4. https://arxiv.org/abs/2107.03374 — HumanEval 论文
5. https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard — Open LLM Leaderboard

Sources:
1. https://github.com/EleutherAI/lm-evaluation-harness — LM-Eval Harness
2. https://crfm.stanford.edu/helm/ — Stanford HELM
3. https://github.com/bigcode-project/bigcode-eval-harness — BigCode Eval
4. https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard — Open LLM Leaderboard
5. https://chat.lmsys.org/?leaderboard — LMSYS Arena
6. https://opencompass.org.cn/ — OpenCompass
7. https://flageval.baai.ac.cn/ — FlagEval

Risk of Staleness:
- lm-eval 版本更新快，API 兼容性需确认
- 各数据集版本可能变化

Out of Scope Kept:
- 未收录所有 benchmark 数据集
- 未写完整评测流程
- 未写内部 Leaderboard 建设方案
