# LLM Evaluation

## 先把 Evaluation 放在什么位置理解

Evaluation 更适合先理解成：

> 系统已经能跑了之后，你如何判断它输出得好不好。

这句话里有两个重点：

1. 它关心的是输出质量。
2. 它通常建立在“请求已经能被系统执行”这件事之上。

所以 evaluation 和 inference、gateway、observability 都有关，但又不是同一层。

Inference 让模型能返回结果。

Gateway 让调用可以被治理。

Observability 让运行过程可解释。

Evaluation 让输出质量可判断。

缺了 evaluation，系统很容易停在“能回答”，但不知道回答是否值得信任。

## 为什么它是单独一条主线

一个系统跑通，不代表答案靠谱。

你完全可能遇到这种情况：

- 服务稳定
- 延迟正常
- metrics 也很好看
- request id 和 events 都完整
- 但模型回答质量就是不行

这时 observability 解决不了全部问题。

Observability 可以告诉你请求有没有成功、慢在哪里、是否 fallback、错误率是否上升；但它不能直接告诉你答案是否符合任务目标。

Evaluation 才是真正的下一层。

## Evaluation 最核心在回答什么

它主要在回答几类问题。

### 模型选型问题

哪一个模型更适合当前任务？

例如：

- 小模型是否足够
- 更贵模型是否带来明显收益
- 本地模型和远程模型差距在哪里
- streaming 体验好是否伴随质量下降

### 版本回归问题

新版本上线后，质量有没有变差？

例如：

- prompt 改动是否破坏原有行为
- adapter 导出后是否引入退化
- gateway 路由切换后输出是否一致
- judge 配置变化是否影响结果

### 场景边界问题

这个模型在什么任务上表现好，在什么任务上容易翻车？

例如：

- 简单事实问答可以
- 长上下文任务不稳
- JSON 格式容易错
- 多轮指令跟随退化

### 发布决策问题

这个 candidate 值不值得继续推进？

这不只看分数，还要看：

- delta 是否超过门槛
- 是否有关键样本退化
- 是否带来成本或延迟上升
- 是否需要人工复核

## Evaluation 常见的三种思路

### 标准 Benchmark

这是最容易形成结构化结果的一类。

优势：

- 可重复
- 可比较
- 任务和指标明确
- 适合回归检测

限制：

- 任务边界较固定
- 可能和真实业务有距离
- 容易被排行榜误读

### LLM-as-Judge

更适合开放式任务。

当“正确答案”很难写成规则时，让更强模型来做判断，会更灵活。

优势：

- 能处理开放式回答
- 可以输出 reason
- 适合人工复核前的初筛

限制：

- judge 本身可能有偏差
- prompt 变化会影响评分
- 成本和稳定性要考虑
- 不能把 judge 当成绝对真理

### Heuristic / Rule-based Eval

适合有明确标准答案或明确规则的任务。

例如：

- 输出必须是合法 JSON
- 必须包含某个字段
- 不能包含敏感词
- 数值必须在范围内
- exact match / regex match

优势是可解释性强，缺点是覆盖不了很多开放式质量问题。

## 一次 Eval Run 应该留下什么

真正有用的 evaluation，通常至少要留下：

- task
- model
- backend
- runner config
- judge config
- run metadata
- metrics
- sample outputs
- sample summary
- sample analysis
- result bundle
- history entry

这就是为什么当前仓库里的 `eval-module` 会特别强调 run、compare、history。

没有这些上下文，分数就很难被解释。

## Compare 为什么重要

单次 run 回答的是：

> 这次结果是什么？

Compare 回答的是：

> 这次结果相对 baseline 发生了什么变化？

真实发布判断通常不是看一个孤立分数，而是看：

- baseline 是谁
- candidate 是谁
- task 是否一致
- metrics 是否可比
- delta 是否超过门槛
- 是否有退化
- recommendation 是 promote、review 还是 block

所以 compare 是从 evaluation 走向 release decision 的中间层。

## Evaluation 和 Observability 的边界

两者关系很近，但不是包含关系。

| 问题 | 更靠近 |
| --- | --- |
| 请求有没有失败 | Observability |
| 哪个 upstream 慢 | Observability |
| fallback 是否发生 | Observability |
| 输出是否符合任务要求 | Evaluation |
| candidate 是否比 baseline 好 | Evaluation |
| 质量提升是否值得发布 | Evaluation + Observability |

很多真实决策要两者一起看。

例如：candidate 分数提升，但延迟翻倍、fallback 增多、输出 token 暴涨，这时就不能只看 evaluation 分数。

## 在当前仓库里怎么对应

当前 `eval-module` 的价值，不在于它已经是完整 benchmark 平台，而在于它把评测最重要的结构先收出来了：

- run
- compare
- result bundle
- history
- leaderboard
- sample analysis
- release recommendation

这会帮助你建立一个关键直觉：

> 评测不是一次性命令，而是一种可追踪、可比较、可沉淀的对象化流程。

## 学习时怎么练

建议按下面顺序：

1. 运行一个 eval task。
2. 查看 run JSON 和 run Markdown。
3. 找到 sample outputs。
4. 运行 compare。
5. 查看 comparison JSON 和 Markdown。
6. 查看 history。
7. 生成 leaderboard。
8. 写一段 release recommendation 的解释。

每一步都问：

- 这个产物回答什么问题？
- 它能否支撑发布判断？
- 如果三个月后回看，还能解释当时为什么这么判断吗？

## 学习时常见误区

### 有 Benchmark 分数就够了

不够。

你还需要知道那次分数是怎么来的，以及和上次有什么不同。

### Evaluation 只在大模型选型时才有用

也不对。

即使是同一个模型，不同 prompt、不同版本、不同部署方式，也都可能需要评测。

### 先把系统做完，评测以后再说

风险很大。

如果不早点建立评测习惯，后面系统一复杂，质量回归会更难追。

### LLM-as-Judge 可以完全替代人工

不能。

它可以提高效率，但仍然需要 sample、reason 和人工复核入口。

### Leaderboard 就是 Evaluation

不是。

Leaderboard 是展示层。Evaluation 的核心是任务、运行、比较、证据和判断。

## 这一章学完应该带走什么

Evaluation 是输出质量层。

它和 inference、gateway、observability 一起，才构成一条完整的 AI Infra 学习主线。

学完这一章，你应该从“看一个分数”转向“看一组可解释证据”。
