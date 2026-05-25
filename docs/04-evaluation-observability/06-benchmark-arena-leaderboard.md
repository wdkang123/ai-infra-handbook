# Benchmark、Arena、Leaderboard

## 为什么这三个词值得拆开

因为它们经常一起出现，但它们不是同一类东西。

如果你把它们混在一起，后面就很容易：

- 把排行榜当成评测过程本身
- 把人类偏好对战结果当成客观 benchmark 分数
- 误以为“展示面”就是“执行机制”

## Benchmark 是什么

benchmark 更像一套评测规则和任务集合。

它定义的是：

- 测什么
- 怎么测
- 用什么指标看

所以 benchmark 的重点是“执行与口径”。

## Arena 是什么

arena 更像一种对战式的人类偏好评测形态。

它和 benchmark 最大的不同，不在于有没有分数，而在于它更依赖：

- 对战
- 人类选择
- 相对偏好

所以 arena 更像“交互式偏好比较”，而不是固定答案式 benchmark。

## Leaderboard 是什么

leaderboard 是展示层。  
它把各种结果汇总起来，形成：

- 排名
- 对比
- 外部可阅读的结果面

所以 leaderboard 很重要，但它通常不是底层执行器。

## 三者之间最重要的边界

### Benchmark 更关心绝对任务表现

比如准确率、pass@k、某套题上的综合分。

### Arena 更关心相对偏好

也就是人在同题对战时更愿意选谁。

### Leaderboard 更关心结果可比较和可展示

它本身不一定说明底层评测过程的所有细节，但它方便你快速看到整体格局。

## 为什么这个边界对学习很重要

因为你以后会经常看到类似说法：

- 某模型 benchmark 分高
- 某模型在 arena 更受欢迎
- 某排行榜上某模型名次更高

如果没有边界意识，你就会把这些话都当成同一种结论。  
但更稳的做法是先问：

- 这是标准任务能力吗
- 这是人类偏好吗
- 还是只是某种展示汇总结果

## 在当前仓库里怎么对应

当前仓库的 `eval-module` 更接近：

- run 执行
- compare
- bundle
- history
- 从 history 聚合出来的最小 leaderboard

也就是说，它先保留 benchmark 执行和结果沉淀层，再提供一个很薄的 leaderboard 展示层。

这很合理，因为对学习来说，更重要的是先理解：

- 怎么跑
- 怎么比
- 怎么留下上下文

而不是先做一个漂亮排行榜页面。

当前最小 leaderboard 的重点不是视觉呈现，而是让你看到这条依赖关系：

```text
run -> run_history.jsonl -> leaderboard.json / leaderboard.md
```

如果没有 run 和 history，leaderboard 就会失去可追溯性。

当前最小 leaderboard 也会保留 backend 和 few-shot 维度，并生成 `backend_groups` / `fewshot_groups`。这不是为了做复杂 dashboard，而是提醒你：不同评测后端或提示设置下的分数，应该先分开看，再决定是否能横向比较。

## 学习时常见误区

### “排行榜高就一定最适合我”

不一定。  
排行榜结果一定要结合任务场景来看。

### “Arena 比 benchmark 更真实，所以 benchmark 不重要”

也不对。  
两者解决的是不同问题，一个更偏标准任务能力，一个更偏人类偏好。

### “只要能看 leaderboard，就不需要理解底层评测”

风险很大。  
因为 leaderboard 的可信度，仍然依赖底层 benchmark 或 arena 的执行质量。

## 这一章学完应该带走什么

你最应该带走的是这条分层：

- benchmark：怎么测
- arena：怎么比偏好
- leaderboard：怎么展示结果

把这三层分开之后，你后面看任何公开评测页面，都会更容易判断自己到底在看什么。
