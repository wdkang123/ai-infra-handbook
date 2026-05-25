Task ID: T702
Task Title: Observability / Evaluation Deep-Research Pack
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
澄清 evaluation/benchmark/leaderboard/arena 的边界。

Result:

# Eval/Benchmark Boundary Matrix v1

## 边界一：Evaluation vs Benchmark

### Evaluation（评测）

| 属性 | 内容 |
|------|------|
| **定义** | 评估模型能力的过程，包含 benchmark 但不限于 benchmark |
| **范围** | Benchmark + 人工评估 + LLM-as-Judge + 主观评测 |
| **边界说明** | 评测是上层概念，benchmark 是其中一种手段 |

### Benchmark（基准测试）

| 属性 | 内容 |
|------|------|
| **定义** | 在标准化数据集上运行模型，产出量化分数 |
| **范围** | 数据集 + 评测脚本 + 分数计算 |
| **代表** | MMLU、GSM8K、HumanEval |
| **边界说明** | Benchmark 是评测的一种手段，不是评测全部 |

### 关系澄清

```
Evaluation（评测）
    ├── Benchmark（标准数据集测试）→ lm-eval 执行
    ├── LLM-as-Judge（模型评估）→ Langfuse / 外部 Judge
    ├── Heuristic Eval（规则评估）→ eval-module 内置
    └── 人工评估（主观）→ 外部
```

来源：https://github.com/EleutherAI/lm-evaluation-harness

---

## 边界二：Benchmark vs Leaderboard

### Benchmark（基准测试）

| 属性 | 内容 |
|------|------|
| **本质** | 测试题库 + 评分标准 |
| **输出** | 量化分数（accuracy、Pass@K 等） |
| **例子** | MMLU（57 学科选择题）、GSM8K（数学题） |
| **与本项目关系** | eval-module 执行，数据来自各 benchmark 官方 |

### Leaderboard（排行榜）

| 属性 | 内容 |
|------|------|
| **本质** | 模型分数的汇总展示 |
| **输出** | 排名 + 分数 |
| **例子** | Open LLM Leaderboard、HuggingFace 排行榜 |
| **与本项目关系** | 可提交评测结果，但不需要自己建设 |

### 关系澄清

- **Benchmark 是分数来源，Leaderboard 是分数展示**
- Benchmark 可以独立存在（本地跑分）
- Leaderboard 需要汇总多个模型/多个 benchmark 的结果

来源：https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard

---

## 边界三：Leaderboard vs Arena

### Leaderboard（排行榜）

| 属性 | 内容 |
|------|------|
| **本质** | 静态分数汇总排行 |
| **评分方式** | 固定 benchmark 跑分 |
| **更新频率** | 按提交更新，不实时 |
| **例子** | Open LLM Leaderboard、OpenCompass |
| **边界说明** | 不需要外部用户参与评分 |

### Arena（对战竞技场）

| 属性 | 内容 |
|------|------|
| **本质** | 用户对战式评分 |
| **评分方式** | 随机对战 + 用户投票 + Elo 排名 |
| **更新频率** | 实时（依赖对战数据） |
| **例子** | LMSYS Arena、Chatbot Arena |
| **边界说明** | 需要大量外部用户持续参与，本质是社区运营平台 |

### 关系澄清

| 维度 | Leaderboard | Arena |
|------|-------------|-------|
| **评分来源** | 固定数据集 | 用户对战投票 |
| **外部依赖** | 无（自己跑分） | 需要大量外部用户 |
| **建设难度** | 低（汇总数据） | 高（需要用户运营） |
| **与本项目关系** | 可提交 | 不建设 |

来源：https://chat.lmsys.org/?leaderboard

---

## 边界四：LM-Eval vs HELM vs BigCode Eval

### LM-Eval Harness

| 属性 | 内容 |
|------|------|
| **定位** | 标准 benchmark 评测工具 |
| **执行方式** | Python API + CLI |
| **下游对接** | vLLM、SGLang、OpenAI API 等 |
| **数据存储** | 不含，需自行实现 |
| **边界说明** | 专注执行，不含评测结果管理 |

### Stanford HELM

| 属性 | 内容 |
|------|------|
| **定位** | 综合评测框架 |
| **执行方式** | Web 界面 + API |
| **下游对接** | 多种推理服务 |
| **数据存储** | 含部分（结果展示） |
| **边界说明** | 偏学术，API 接入成本高 |

### BigCode Eval Harness

| 属性 | 内容 |
|------|------|
| **定位** | 代码模型专用评测 |
| **执行方式** | Python API + CLI |
| **下游对接** | 多种代码模型 |
| **数据存储** | 不含，需自行实现 |
| **边界说明** | 仅覆盖 HumanEval、MBPP 等代码 benchmark |

### 选择指引

| 场景 | 推荐工具 |
|------|---------|
| 通用 benchmark 评测 | LM-Eval Harness |
| 学术研究 / 多场景综合 | Stanford HELM（参考） |
| 代码模型评测 | BigCode Eval Harness |

来源：https://github.com/EleutherAI/lm-evaluation-harness
来源：https://crfm.stanford.edu/helm/
来源：https://github.com/bigcode-project/bigcode-eval-harness

---

## 边界五：eval-module 与评测框架的关系

### eval-module 的职责

| 属性 | 内容 |
|------|------|
| **定位** | 评测任务管理层 |
| **核心能力** | 评测任务编排、结果记录、版本对比 |
| **与 lm-eval 关系** | 调用 lm-eval API 执行评测 |
| **边界说明** | eval-module 不直接跑 benchmark，而是调用 lm-eval |

### 分工澄清

```
eval-module（任务管理）
    ↓ 调用
lm-eval（评测执行）← inference-service（vLLM/SGLang）
    ↓
评测结果 → eval-module 持久化
```

eval-module 与 lm-eval 是调用关系，不是替代关系。

来源：https://github.com/EleutherAI/lm-evaluation-harness

---

## 常见混淆总结

| 混淆 | 事实 |
|------|------|
| "Benchmark 和 Evaluation 是一样的" | Benchmark 是评测的一种手段 |
| "Leaderboard 就是 Arena" | Leaderboard 是静态排行，Arena 是对战竞技场 |
| "lm-eval 可以替代 eval-module" | lm-eval 管执行，eval-module 管任务管理 |
| "本项目需要建设 Arena" | 不建设，Arena 需要大量外部用户参与 |

Sources:
1. https://github.com/EleutherAI/lm-evaluation-harness — LM-Eval Harness
2. https://crfm.stanford.edu/helm/ — Stanford HELM
3. https://github.com/bigcode-project/bigcode-eval-harness — BigCode Eval
4. https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard — Open LLM Leaderboard
5. https://chat.lmsys.org/?leaderboard — LMSYS Arena

Risk of Staleness:
- 各工具版本更新可能改变边界

Out of Scope Kept:
- 未写代码实现
- 未写评测结果数据库设计
