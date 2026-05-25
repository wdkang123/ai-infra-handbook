# Benchmark、Leaderboard、Observability

## Benchmark 是什么

benchmark 更像“用一组固定任务去测一个系统”的过程。  
它关心的是测法、任务、结果是否可重复。

## Leaderboard 是什么

leaderboard 更像“把很多结果摆在一起看”的展示层。  
它本身不等于评测过程。

所以一个常见误区是把 benchmark 和 leaderboard 混成同一件事。  
更好的理解方式是：

- benchmark：测
- leaderboard：展示

## Observability 在这里解决什么

observability 解决的是“分数之外的运行信息”。  
比如：

- 请求量
- 失败率
- 延迟
- 追踪上下文

它的价值在于：  
就算结果变差了，你也不一定知道问题出在哪；但如果评测结果和观测信息同时存在，排查会快很多。

## 对当前仓库的意义

当前仓库里的 `eval-module` 还不是完整评测平台，但它已经把最关键的结构收出来了：

- run
- compare
- bundle
- history
- 从 history 生成的最小 leaderboard
- backend/few-shot 过滤和分组

这就是后面继续长成 benchmark / leaderboard / observability 体系的骨架。
