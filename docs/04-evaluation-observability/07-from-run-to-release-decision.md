# 从 Run 到发布决策

## 为什么评测最终要走到“决策”

Run 本身不是终点。

如果一次 run 最后只留下一个结果文件，但没有影响任何判断，它的学习价值和工程价值都会有限。

在真实系统里，评测最终通常要服务这些问题：

- 这个版本能不能继续推进
- 这个模型要不要替换现有主模型
- 这个 prompt / adapter 改动是否值得保留
- 质量变化和系统行为变化是否能一起解释
- 如果不发布，原因是什么
- 如果发布，需要保留哪些回滚证据

所以 evaluation 的终点不是“有分数”，而是“能支撑一次可解释的决策”。

## 一次 Run 之后，最常见的下一步是什么

最常见的不是“立刻上线”，而是比较。

也就是把这次 run 放进上下文里看：

- 和上一个版本比
- 和另一个模型比
- 和另一组 prompt 比
- 和另一个 adapter 比
- 和不同 judge 配置比

所以 `compare` 不是附属功能，而是从 run 走向决策的关键中间层。

单次 run 回答的是：

> 这次结果是什么？

Compare 回答的是：

> 这次结果相对另一个候选发生了什么变化？

Release decision 回答的是：

> 这种变化是否足以支持下一步动作？

这三个问题不能混在一起。

## 为什么单次分数不够支持决策

真正的发布决策通常不是在问：

- 这次分数是多少

而是在问：

- 它比上次好了吗
- 好在哪
- 差在哪
- 变化是否超过噪声
- 是否有关键样本退化
- 成本是否增加
- 延迟是否变差
- 错误率是否上升
- 这种变化是否值得发布

这就是为什么 evaluation 不能只剩一个数字。

它必须保留 enough context：

- task
- dataset 或 sample set
- runner config
- judge config
- baseline
- candidate
- metrics
- sample outputs
- sample analysis
- recommendation

没有上下文的分数，不能支撑可靠决策。

## 从 Run 到 Decision 的最小链路

可以把当前仓库里的最小链路理解成：

```text
Eval Task
  -> Baseline Run
  -> Candidate Run
  -> Compare Report
  -> History / Leaderboard
  -> Recommendation
  -> Release Decision
```

其中：

- run 是一次评测证据
- compare 是相对变化证据
- history 是时间维度证据
- leaderboard 是横向观察入口
- recommendation 是决策建议

当前项目没有完整 release platform，但它已经保留了足够的学习骨架，让你练习发布判断。

## 当前仓库提供了什么学习骨架

当前仓库已经把从 run 走向决策最重要的基础对象留下来了：

- task
- run result
- run history
- compare report
- min delta threshold
- sample outputs
- sample summary
- sample analysis
- leaderboard
- recommendation

这意味着你已经能开始练习一种更真实的思考方式：

不是只看“这次跑成没跑成”，而是开始看“这次结果对后续意味着什么”。

## Decision 应该包含哪些字段

一个比较扎实的发布判断，至少应该包含：

| 字段 | 要回答的问题 |
| --- | --- |
| baseline | 当前候选和谁比较 |
| candidate | 这次要不要推进的对象 |
| task | 比较是否在同一个任务上发生 |
| metric deltas | 指标变化多少 |
| threshold | 变化是否超过发布门槛 |
| regression | 是否有关键退化 |
| sample evidence | 样本级证据是否支持结论 |
| observability signals | 延迟、错误、fallback、cache 是否异常 |
| recommendation | 建议 approve、review 还是 block |
| rollback evidence | 如果发布后出问题，如何回退和解释 |

这些字段不一定都要在一个文件里，但决策时必须能找到。

## Observability 为什么会在这里重新出现

很多发布决策不是纯质量问题，也不是纯系统问题，而是两者一起看。

比如：

- 质量略有提升，但延迟大幅变差
- benchmark 分数没变，但错误率升高
- 主观效果更好，但 token 成本明显上涨
- candidate 分数更好，但 gateway 频繁 fallback
- 训练后模型表现提升，但输出长度暴涨
- streaming 更顺滑，但首 token 明显变慢

这时如果 evaluation 和 observability 是断开的，你就很难做稳决策。

Evaluation 告诉你“回答质量发生了什么变化”。

Observability 告诉你“系统运行过程中发生了什么变化”。

Release decision 必须把两者放在一起。

## 一个具体决策例子

假设你有两个 run：

- baseline：当前线上 prompt
- candidate：新 prompt

Compare report 显示：

- overall score +0.03
- instruction following +0.08
- factuality -0.02
- 关键样本中有 2 条回答变长但不更准确

同时 observability 显示：

- 平均输出 token 增加 35%
- TTFT 基本不变
- 总延迟增加

这时推荐动作不一定是 approve。

更合理的决策可能是：

- 不直接发布
- 要求 review factuality 退化样本
- 限制输出长度
- 重新跑一轮 candidate
- 如果成本可接受，再进入小流量验证

这就是“分数提升但不一定发布”的典型场景。

## 发布建议的几种状态

可以用这几种状态理解 recommendation：

| 状态 | 含义 | 下一步 |
| --- | --- | --- |
| `approve` | 候选明显更好且设置一致 | 可以进入更大样本、灰度或下一轮发布评审 |
| `review` | 结果基本持平、证据不足，或评测设置发生变化 | 人工复核样本、配置和风险 |
| `block` | 候选退化超过阈值 | 不发布，记录原因并补回归证据 |

真实团队还可能把 `review` 继续细分成 rerun、hold、manual review 等状态。当前仓库先使用 `approve / review / block`，目的是让学习者先把最小发布门禁跑通。

## 发布前检查清单

一次发布判断前，至少问：

- baseline 和 candidate 是否可比
- task 是否一致
- metric 是否一致
- judge 配置是否一致
- sample outputs 是否保留
- regression 是否检查
- run history 是否更新
- leaderboard 是否能解释候选位置
- request / serving / gateway 观测是否正常
- 训练产物是否有 lineage
- 发布后如何回滚
- 相关文档和证据是否更新

如果这些问题大多答不上来，就不应该急着发布。

## 和当前项目怎么练习

你可以这样练：

1. 运行 baseline eval。
2. 修改一个 mock 输出或配置，运行 candidate eval。
3. 生成 compare report。
4. 查看 recommendation。
5. 查看 run history 和 leaderboard。
6. 对照 sample analysis 写一段发布判断。
7. 如果 candidate 来自 finetune export，补充 lineage 说明。
8. 如果 candidate 需要通过 gateway 访问，补充 request id、metrics 或 events 证据。

最后用一段话回答：

```text
我建议：
原因是：
主要证据是：
主要风险是：
需要补充验证的是：
```

这比单纯贴分数有价值得多。

## 学习时常见误区

### “run 结果出来就算完成”

不够。

更完整的完成应该至少包括：比较、解释、沉淀。

### “发布决策只看 benchmark”

风险很大。

实际决策往往要把：

- 质量
- 延迟
- 稳定性
- 成本
- 失败路径
- 回滚能力

一起放进去看。

### “观察和评测是两条平行线”

也不对。

真正的发布判断，往往正是建立在两者汇合之后。

### “推荐动作可以完全自动化”

不要太早这么想。学习阶段更重要的是让推荐动作可解释。自动化可以帮你筛选，但最终仍要保留证据和人工复核入口。

### “只要分数提升，就应该发布”

不一定。分数提升可能伴随成本、延迟、失败率或关键样本退化。

## 这一章学完应该带走什么

Run 是起点，不是终点。

当你学会把 run、compare、history、leaderboard、sample analysis 和 observability 一起放进决策视角里看，你就已经开始从“会跑工具”走向“会做工程判断”了。

这也是 AI Infra 学习最重要的转折之一。
