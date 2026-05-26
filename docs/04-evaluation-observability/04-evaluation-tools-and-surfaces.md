# 评测工具与展示面

很多初学者会把 benchmark、leaderboard、arena、harness、dashboard 全部混成“评测”。

这会带来一个问题：
看到一个排行榜，就误以为自己已经理解了评测过程。

更好的方式是把它们分层：

- 有些负责执行评测。
- 有些负责定义任务和规则。
- 有些负责比较结果。
- 有些负责展示结果。
- 有些负责人类偏好收集。

这页就是把这些层拆开。

## 先分清几类对象

| 对象 | 主要作用 | 更像哪一层 |
| --- | --- | --- |
| Evaluation Harness | 执行评测任务 | 执行层 |
| Benchmark | 定义任务、数据和规则 | 评测口径 |
| Run Bundle | 保存一次评测证据 | 证据层 |
| Compare | 比较 baseline/candidate | 判断层 |
| Leaderboard | 横向展示结果 | 展示层 |
| Arena | 人类偏好对战/盲评 | 偏好收集层 |
| Dashboard | 查询、筛选、趋势和 drill-down | 展示/运营层 |

这些东西都和 evaluation 有关，但不是同一个角色。

## Evaluation Harness：负责跑

Harness 负责真正执行评测任务。

它通常做：

- 加载 task
- 准备 prompt
- 调用模型
- 收集输出
- 计算指标
- 保存结果

你可以把 harness 理解成“评测执行引擎”。

它解决的是：

> 这次评测怎么跑出来？

但 harness 本身不一定负责：

- 长期 history
- 发布判断
- dashboard
- 结果解释
- 人工审核流程

这些是更上层的系统能力。

## Benchmark：定义测什么

Benchmark 更像一套被设计好的评测口径。

它定义：

- task
- dataset
- split
- metric
- prompt template
- few-shot 设置
- scoring rule
- judge rule

所以 benchmark 不是一个页面，也不是一个分数。
它是一套“如何比较”的规则。

如果 benchmark 版本变了，结果就不能和旧结果随便混看。

## Run Bundle：保留证据

一次 run 不能只留下一个分数。

它至少要留下：

- task
- model
- backend
- few-shot
- sample count
- raw output
- sample outputs
- sample summary
- sample analysis
- run manifest
- result file

run bundle 的价值是让分数能被解释。
没有 run bundle，leaderboard 上的数字就很难复盘。

当前仓库的 `eval-module` 已经把这层表达出来。

## Compare：从分数走向判断

Compare 解决的是：

> candidate 相比 baseline 是否值得进入下一步？

它不只是算 delta。
还要看：

- task 是否一致
- sample count 是否变化
- few-shot 是否变化
- metric delta
- min delta
- verdict
- release recommendation
- release reasons

Compare 是评测系统从“测量”走向“决策”的关键层。

## Leaderboard：展示，不是事实来源

Leaderboard 很有用。
它能帮助你横向看多个模型、多个 backend、多个 run。

但 leaderboard 应该从 run history 和 run artifacts 聚合，而不是手写分数。

它应该能追溯：

- best result file
- latest result file
- run count
- backend
- few-shot
- task

如果 leaderboard 不能跳回证据，它就容易变成漂亮但危险的展示页。

## Arena：偏好而不是标准答案

Arena 更像人类偏好收集。

它适合回答：

- 用户更喜欢哪种回答？
- 哪个模型在开放式交互中更受欢迎？
- 哪些回答风格更被接受？

它和标准 benchmark 不同：

- 更依赖真实交互。
- 更依赖主观偏好。
- 更容易受展示、样本和用户群影响。
- 更适合开放式任务。

Arena 很有价值，但不能直接替代受控 benchmark。

## Dashboard：视图，不是证据本身

Dashboard 适合做：

- 趋势展示
- 筛选
- 对比
- drill-down
- 发布复盘
- 运营监控

但 dashboard 不应该成为唯一事实来源。

更好的结构是：

```text
run artifacts / comparison artifacts / history
  -> index / leaderboard
  -> dashboard
```

这样 UI 可以迭代，证据不会丢。

## 工具选择不要先从品牌开始

选评测工具时，不要先问“哪个最流行”。先问自己要解决哪一层问题：

| 需求 | 更适合的方向 |
| --- | --- |
| 跑标准 benchmark | evaluation harness |
| 验证 prompt / RAG 输出 | prompt/app eval 工具 |
| 做发布前 baseline/candidate compare | 项目内 compare/report |
| 做可视化查询 | dashboard |
| 收集人类偏好 | arena/human review workflow |
| 做安全和 red teaming | red-team eval 工具 |

一个成熟系统往往会同时使用多种工具，但它们要接在同一条证据链上，而不是各自生成一堆孤立报告。

## CI 里应该放什么

不是所有 eval 都适合每次 CI 跑。

可以分三档：

| 档位 | 触发时机 | 内容 |
| --- | --- | --- |
| 快速回归 | 每个 PR | 小 golden set、schema/rule checks、核心 prompt |
| 中等评测 | 合并前或每日 | 更多样本、LLM-as-Judge、compare |
| 深度评测 | release 前 | 全量 benchmark、人工抽检、成本/延迟复盘 |

这样既能及时发现退化，又不会让每个 PR 都被昂贵评测拖死。

## 一个 dashboard 应该从哪里钻下去

如果后续做 dashboard，不建议只做总分表。

更有用的 drill-down 路径是：

```text
leaderboard
  -> task result
  -> run metadata
  -> sample outputs
  -> sample analysis
  -> comparison reasons
  -> release recommendation
```

当 reviewer 看到一个分数变化时，应该能一路点到“哪些样本变了、为什么变了、是否影响发布”。

## 当前仓库怎么对应

当前 `eval-module` 不是完整评测平台，但已经表达了关键骨架：

```text
run
  -> run bundle
  -> run_history.jsonl
  -> list-runs
  -> leaderboard

compare
  -> comparison bundle
  -> comparison_history.jsonl
  -> list-comparisons
```

相关文件：

```text
projects/eval-module/src/eval_module/main.py
projects/eval-module/src/eval_module/results/result_store.py
projects/eval-module/src/eval_module/runners/lm_eval_runner.py
```

这套结构让评测从一次性命令变成可追踪对象。

## 一个合理演进路线

如果以后要继续扩展评测系统，推荐顺序是：

1. 先保 run bundle 和 comparison bundle。
2. 扩展 runner adapter。
3. 扩展 task/benchmark config。
4. 引入 judge adapter。
5. 强化 release recommendation。
6. 从 JSON/Markdown index 接 dashboard。
7. 再考虑 arena 或 human preference import。

这个顺序能保住证据层。

## 常见误区

### “排行榜就是最可信结果”

不一定。
排行榜受任务集、版本、提交规则和展示方式影响。

### “Arena 和 benchmark 只是两种分数”

不对。
它们背后的数据来源、主观性和用途不同。

### “有 harness 就有评测平台”

不够。
平台还需要结果存储、history、compare、证据、展示和发布判断。

### “Dashboard 可以替代 artifact”

不建议。
dashboard 是视图，artifact 才是可复盘证据。

### “分数展示越多越专业”

不一定。
如果没有可比性和追溯性，更多分数只会制造噪音。

## 学完应该能回答

读完这一页后，你应该能回答：

1. harness、benchmark、leaderboard、arena 分别是什么？
2. 为什么 leaderboard 不能替代 run bundle？
3. Compare 在评测系统里为什么是判断层？
4. Dashboard 应该如何建立在 artifact 和 history 上？
5. 当前仓库的 `eval-module` 已经表达了哪些评测平台骨架？

## 继续阅读

- [LLM Evaluation](/04-evaluation-observability/05-llm-evaluation)
- [Run、Compare、History](/04-evaluation-observability/01-run-compare-history)
- [Benchmark、Leaderboard 与 Observability](/04-evaluation-observability/02-benchmark-leaderboard-observability)
- [Eval 评测系统迁移](/12-production-migration/03-eval-judge-dashboard-migration)
- [lm-evaluation-harness 官方接口文档](https://github.com/EleutherAI/lm-evaluation-harness/blob/main/docs/interface.md)
- [promptfoo 官方文档](https://www.promptfoo.dev/docs/intro/)
