# Benchmark、Arena、Leaderboard

## 为什么这三个词值得拆开

Benchmark、arena、leaderboard 经常一起出现，但它们不是同一类东西。

如果你把它们混在一起，后面就很容易：

- 把排行榜当成评测过程本身
- 把人类偏好对战结果当成客观 benchmark 分数
- 误以为展示面就是执行机制
- 看到一个排名就直接做选型结论

更稳的分层是：

- Benchmark：怎么测
- Arena：怎么比较偏好
- Leaderboard：怎么展示结果

这三个东西可以互相连接，但不能互相替代。

## Benchmark 是什么

Benchmark 更像一套评测规则和任务集合。

它定义的是：

- 测什么
- 怎么测
- 用什么数据
- 用什么指标
- 如何重复执行
- 如何比较不同候选

所以 benchmark 的重点是执行与口径。

一个 benchmark 如果没有任务定义、数据来源、指标规则和运行配置，分数就很难被解释。

## Benchmark 的价值

Benchmark 的价值是让质量判断变得可重复。

它能帮助你回答：

- 同一模型在不同任务上表现如何
- 新 prompt 是否比旧 prompt 好
- 新 adapter 是否引入回归
- 模型升级是否改善目标任务
- 某次变更是否值得进入下一步 review

但 benchmark 不是万能的。

它往往覆盖固定任务，不一定代表所有真实用户场景。

## Arena 是什么

Arena 更像一种对战式的人类偏好评测形态。

它和 benchmark 最大的不同，不在于有没有分数，而在于它更依赖：

- 对战
- 人类选择
- 相对偏好
- 多轮比较
- 统计汇总

所以 arena 更像交互式偏好比较，而不是固定答案式 benchmark。

## Arena 的价值和限制

Arena 的价值是能捕捉一些难以写成规则的主观偏好：

- 哪个回答更有帮助
- 哪个回答更自然
- 哪个回答更符合用户期望
- 哪个模型在开放式对话里更受欢迎

但 arena 也有明显限制：

- 参与者群体会影响结果
- 问题分布会影响结果
- 偏好不等于事实正确
- 人类选择可能受风格影响
- 排名变化不一定代表任务能力变化

所以 arena 结果适合参考，但不应该单独成为工程发布依据。

## Leaderboard 是什么

Leaderboard 是展示层。

它把各种结果汇总起来，形成：

- 排名
- 对比
- 分组
- 趋势
- 外部可阅读的结果面

Leaderboard 很重要，但它通常不是底层执行器。

如果没有 run、history、benchmark 或 arena 的可靠数据，leaderboard 就只是漂亮表格。

## 三者之间最重要的边界

| 对象 | 重点 | 常见输出 | 最大风险 |
| --- | --- | --- | --- |
| Benchmark | 固定任务表现 | score、metrics、sample outputs | 任务和真实场景不匹配 |
| Arena | 相对偏好 | win rate、rating、pairwise result | 偏好被风格和样本分布影响 |
| Leaderboard | 展示汇总 | ranking、table、groups | 忽略底层评测口径 |

把这张表记住，后面看公开评测结果会清醒很多。

## 为什么这个边界对学习重要

你以后会经常看到类似说法：

- 某模型 benchmark 分高
- 某模型在 arena 更受欢迎
- 某排行榜上某模型名次更高

如果没有边界意识，你就会把这些话都当成同一种结论。

更稳的做法是先问：

- 这是标准任务能力吗？
- 这是人类偏好吗？
- 这是某个展示面的汇总吗？
- 底层任务和我的场景是否一致？
- 是否有 sample-level evidence？
- 是否有运行配置和历史记录？

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
- 怎么从 history 生成可读展示

而不是先做一个漂亮排行榜页面。

当前最小 leaderboard 的重点不是视觉呈现，而是让你看到这条依赖关系：

```text
run -> run_history.jsonl -> leaderboard.json / leaderboard.md
```

如果没有 run 和 history，leaderboard 就会失去可追溯性。

## Backend 和 Few-shot 为什么要分组

当前最小 leaderboard 会保留 backend 和 few-shot 维度，并生成 `backend_groups` / `fewshot_groups`。

这不是为了做复杂 dashboard，而是提醒你：

- 不同评测后端的分数不要轻易混看
- 不同 few-shot 设置下的分数不要轻易横比
- 同一 task 下也要注意配置上下文

Leaderboard 的可信度来自上下文，而不是来自排序本身。

## 如何阅读一个 Leaderboard

看到 leaderboard 时，建议按顺序问：

1. 这些结果来自哪些 run？
2. task 是否一致？
3. backend 是否一致？
4. few-shot 是否一致？
5. metric 是否一致？
6. 是否能追溯到 sample outputs？
7. 是否有 run metadata？
8. 是否只是 latest，还是 best？
9. 是否有 regression 说明？
10. 是否能支撑发布判断？

如果这些问题答不上来，leaderboard 只能作为粗略浏览，不能作为强决策依据。

## Benchmark、Arena 和生产质量

Benchmark 和 arena 都不能直接等于生产质量。

生产质量还会受到：

- 用户分布
- 流量模式
- latency
- cost
- safety
- fallback
- cache
- 长上下文
- 真实 prompt
- 数据新鲜度
- UI 交互

所以公开榜单能帮助你建立候选集，但不能替代本项目里的 run、compare、sample analysis 和 release decision。

## 学习时常见误区

### 排行榜高就一定最适合我

不一定。

排行榜结果一定要结合任务场景来看。

### Arena 比 Benchmark 更真实，所以 Benchmark 不重要

也不对。

两者解决的是不同问题，一个更偏标准任务能力，一个更偏人类偏好。

### 只要能看 Leaderboard，就不需要理解底层评测

风险很大。

Leaderboard 的可信度，仍然依赖底层 benchmark 或 arena 的执行质量。

### Best result 一定比 latest result 更适合发布

不一定。

Best 可能来自旧配置、旧数据或不可复现的 run。Latest 也可能代表当前真实状态。两者都要有上下文。

### 一个综合分可以代表所有能力

不能。

综合分会掩盖任务差异、样本退化和业务风险。

## 这一章学完应该带走什么

你最应该带走的是这条分层：

- benchmark：怎么测
- arena：怎么比偏好
- leaderboard：怎么展示结果

把这三层分开之后，你后面看任何公开评测页面，都会更容易判断自己到底在看什么。

对当前仓库来说，最重要的是先把 run、compare、history 和 leaderboard 的证据链讲清楚，再考虑更复杂的展示面。
