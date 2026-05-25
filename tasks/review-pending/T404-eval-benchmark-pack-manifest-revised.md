Task ID: T404
Task Title: Evaluation / Benchmark Long-Run Pack v1 收紧修订
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 T402-review，修订 T402 包的 3 个文件：manifest、sources-index-v2、tooling-notes。

Result:

# T402 包修订说明

## 本次修订内容

本次修订针对 T402-pack-v1 中的 3 个文件做局部收紧：

### 1. T404-eval-benchmark-sources-index-v2-revised.md

**修订点**：修正"Benchmark / Leaderboard / Arena"边界描述。

**原问题**：边界说明中把三者一概称为"展示层"，与 T312 章节中刚刚收正的边界矛盾。

**修订后**：
- **Benchmark**：执行+结果体系，包含评测执行和结果两部分
- **Leaderboard**：聚合层，是 Benchmark 结果的展示聚合
- **Arena**：对战+展示，包含对战机制和结果展示两部分

### 2. T404-eval-module-tooling-notes-v1-revised.md

**修订点**：删除数量型营销表述。

**原问题**：
- "50+ 场景"（描述 Stanford HELM）
- "70+"（描述 LM-Eval Harness 数据集覆盖）

**修订后**：改为中性工程描述，保留真正有用的定位信息。

### 3. T404-eval-benchmark-pack-manifest-revised.md

本文件，说明本次修订点和剩余开放问题。

## 本包完成状态

| 文件 | 状态 |
|------|------|
| T404-eval-benchmark-pack-manifest-revised.md | 本文件 |
| T404-eval-benchmark-sources-index-v2-revised.md | 已修订 |
| T404-eval-module-tooling-notes-v1-revised.md | 已修订 |

## 修订后仍需 Codex 判断的点

1. eval-module 的评测工具选型（LM-Eval Harness 作为主要工具是否合适）
2. 评测结果持久化方案（文件 vs 数据库）
3. LLM-as-Judge 的 Judge 模型选型
4. BigCode Eval Harness 的集成优先级

## 与其他包的关系

- **T501（Observability Pack v2）**：eval-module 的评测结果可上报 Langfuse，与 observability 协作
- **T503（Finetuning Pack v2）**：finetune-demo 训练产物由 eval-module 评测，形成训练→评测闭环

Sources:
1. https://github.com/EleutherAI/lm-evaluation-harness — LM-Eval Harness
2. https://crfm.stanford.edu/helm/ — Stanford HELM
3. https://github.com/bigcode-project/bigcode-eval-harness — BigCode Eval Harness
