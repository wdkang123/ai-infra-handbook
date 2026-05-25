# Long Plan Phase 03

目标：把 MiniMax 从“微任务审稿模式”切换到“长跑专题包模式”，提升长时间无人值守时的 API 吞吐效率。

## 为什么切换

当前模式的问题不是质量差，而是任务过碎：

- 单个任务通常只修一两处
- 单次执行只产一个很小的交付物
- MiniMax 很快就结束，无法充分利用长时间运行窗口

这更适合白天人工盯着快速来回，不适合夜间或长时间批处理。

## 新模式核心

改成“专题包”推进：

- 每个专题包围绕一个主题
- 每包包含 3 到 6 个交付物
- 单次运行目标时长从几分钟提升到几十分钟甚至更久
- Codex 仍然负责最终审阅和收口

## 三类最适合的专题包

### 1. Observability Pack

可包含：

- sources-index v2
- comparison-index v2
- glossary batch
- project mapping
- minimal practice catalog

### 2. Evaluation / Benchmark Pack

可包含：

- sources-index v2
- comparison-index v2
- glossary batch
- benchmark / leaderboard 章节收口
- eval-module 工具映射

### 3. Finetuning Pack

可包含：

- comparison-index v2
- glossary batch
- finetune-demo 训练路径说明
- minimal practice catalog
- 方法 / 框架 / 工具边界收口

## 协作节奏

白天：

- 继续做小修订和高判断成本审阅

夜间 / 长跑：

- 只发专题包
- 一次 1 到 3 个包
- 每包 3 到 6 个交付物

## 当前推荐的第一批长跑包

1. Observability Long-Run Pack
2. Evaluation / Benchmark Long-Run Pack
3. Finetuning Long-Run Pack
