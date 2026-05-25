# 评测工具与展示面

## 为什么要把“工具”和“展示面”分开

因为很多初学者会把 benchmark、leaderboard、arena、harness 全混成“评测”。

但更好的理解方式是：

- 有些东西负责真正去跑
- 有些东西负责组织结果
- 有些东西负责把结果展示出来

如果你不把这几层分开，后面一看排行榜就容易误以为“这就是评测本身”。

## 先把几类东西分出来

### 1. Evaluation Harness

这类工具负责真正执行评测任务。  
比如给模型喂标准任务集，收集结果，再算出 accuracy、pass@k 之类的指标。

学习时你可以把它们理解成“执行引擎”。

### 2. Benchmark

benchmark 更像“被设计好的一套评测任务和规则”。  
它定义的是测什么、怎么测、用什么口径看结果。

所以 benchmark 不是一个页面，而是一套评测过程。

### 3. Leaderboard

leaderboard 是展示层。  
它把很多 benchmark 结果摆在一起，方便横向比较。

所以 leaderboard 最大的价值是“可比较”，而不是“替代了评测过程”。

### 4. Arena

arena 更像人类盲评或交互式对比场景。  
它和标准 benchmark 的最大不同，是它更依赖真实交互和主观偏好，而不是固定标准答案。

## 为什么这个边界很重要

因为你后面会不断看到这样的说法：

- 某模型在 leaderboard 上分更高
- 某模型在 arena 更受欢迎
- 某 harness 支持更多任务

如果你没有分层意识，就会把这些话混成一件事。  
但实际上它们可能分别在讨论：

- 结果展示
- 人类偏好
- 评测执行能力

## 在当前仓库里对应到什么

当前仓库的 `eval-module` 还不是完整 benchmark 平台，但它已经把最重要的结构搭出来了：

- run
- compare
- result bundle
- history
- 最小 leaderboard JSON/Markdown
- leaderboard backend/few-shot 分组

这意味着它更像“评测执行和结果管理骨架”。  
现在的 leaderboard 也只是站在 history 上的展示对象。你以后如果要往 dashboard 方向长，应该继续在这个骨架之上加展示层，而不是反过来。

## 学习时常见误区

### “排行榜就是最可信结果”

不一定。  
排行榜当然有用，但它会受任务集选择、版本更新、提交流程、展示规则影响。

### “Arena 和 benchmark 只是两种分数”

也不对。  
它们背后的评测逻辑、数据来源和主观性程度都不一样。

### “有了 harness 就自动有平台”

不对。  
harness 更像执行层。  
要变成真正的平台，你还需要：

- 结果存储
- history
- compare
- 可追踪的 run metadata
- 展示与解释界面

## 推荐的学习顺序

1. 先理解 harness 是怎么执行一次 run 的
2. 再理解 benchmark 为什么是一套规则，而不是一个页面
3. 再理解 leaderboard / arena 为什么属于展示与比较层

这样你以后再看外部世界里各种“评测榜单”，就更容易判断自己到底在看什么。
