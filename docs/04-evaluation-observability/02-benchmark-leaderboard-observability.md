# Benchmark、Leaderboard、Observability

评测系统最容易被误解成一张排行榜。
很多人看到 benchmark 和 leaderboard，就会下意识以为：

> 跑一组题，得到一个分数，分数高的模型就更好。

这只说对了一小部分。
在真实 AI Infra 里，benchmark、leaderboard 和 observability 是三件相关但不同的事。

- Benchmark 解决“怎么测”
- Leaderboard 解决“怎么展示和比较”
- Observability 解决“为什么会这样、哪里出了问题”

如果只看 leaderboard，不看 benchmark 设计和运行观测，就很容易做出错误发布决策。

## Benchmark：测什么，怎么测

benchmark 是一组相对固定的任务、数据、指标和运行方式。
它的核心目标是让结果可比较、可复现、可解释。

一个 benchmark 至少要说清楚：

- 测的是什么能力
- 使用什么数据集
- 样本如何抽取
- prompt 模板是什么
- few-shot 设置是什么
- 指标怎么算
- 运行环境是什么
- 模型输出如何解析
- 失败样本如何处理

如果这些条件不清楚，分数就很难解释。

例如两个模型都跑 MMLU：

| 设置 | 模型 A | 模型 B |
| --- | --- | --- |
| prompt 模板 | 中文说明 | 英文说明 |
| few-shot | 0-shot | 5-shot |
| 样本数量 | 100 | 1000 |
| 输出解析 | 宽松匹配 | 严格匹配 |

最后模型 B 分数更高，并不能说明 B 一定更好。
因为测试条件已经不一致。

所以 benchmark 的第一原则不是“分数越多越好”，而是“条件必须可复盘”。

## Leaderboard：展示不是评测本身

leaderboard 是把结果摆在一起看。
它很有用，因为人需要快速比较：

- 哪个模型分数更高
- 哪个任务退化了
- 哪个模型最近一次表现最好
- 哪个后端更稳定
- 哪个配置更值得继续测

但 leaderboard 只是展示层。
它不自动保证评测可信。

一个漂亮的 leaderboard 可能隐藏很多问题：

- 结果来自不同 prompt 模板
- 运行时间相隔太久
- 数据集版本不同
- 样本数量不同
- 解析规则不同
- 某些失败样本被忽略
- 指标只看平均值，不看失败分布

所以 leaderboard 的价值取决于它背后的 benchmark 元数据是否完整。

## Observability：分数之外发生了什么

observability 解决的是：

> 分数变化背后，系统到底发生了什么？

评测不是离线数学题。
它往往会经过模型服务、gateway、数据加载、prompt 构造、输出解析、报告生成等很多环节。

如果分数下降，可能原因很多：

- 模型真的变差了
- prompt 模板改了
- 数据集版本变了
- 后端返回超时
- gateway fallback 到了另一个模型
- 输出解析变严格了
- sampling 参数变化
- 某类样本失败率上升
- 评测运行时服务不稳定

只看总分，很难区分这些原因。

所以评测系统需要观测信息：

- run id
- model name
- backend url
- task name
- prompt / few-shot 设置
- sample outputs
- latency
- error count
- request id
- comparison report
- sample analysis
- release recommendation

这些信息让 reviewer 能从“分数变了”继续追到“为什么变了”。

## 三者如何组合成发布判断

可以把一次模型发布评审理解成这样：

```text
Benchmark -> 产生 run result
Leaderboard -> 展示历史和横向比较
Observability -> 解释结果变化和失败原因
Release Gate -> 决定是否发布、阻断或重测
```

单独一个 benchmark 分数不应该直接决定发布。
更合理的判断应该包含：

- 关键任务是否通过最低阈值
- 相比 baseline 是否有显著退化
- 退化样本集中在哪类问题
- settings 是否一致
- 后端运行是否稳定
- 是否发生 fallback 或异常错误
- 样本级输出是否有明显质量问题

这就是为什么当前仓库里 `eval-module` 不只生成一个 accuracy 字段。
它还会保留 run bundle、comparison、history、leaderboard、sample outputs 和 sample analysis。

## 一个具体例子

假设候选模型的平均分从 0.74 下降到 0.72。

这时候不要立刻说：

```text
候选模型退化，不能发布。
```

你应该继续问：

1. baseline 和 candidate 是否使用相同 task？
2. few-shot 数量是否一致？
3. backend 是否一致？
4. prompt 模板是否一致？
5. 样本数量是否一致？
6. 哪些样本错了？
7. 错误集中在某个 subject 还是随机分布？
8. 是否有请求失败或解析失败？
9. 这 0.02 的下降是否超过阈值？

如果 settings 不一致，这次比较可能根本不能作为发布结论。
如果 settings 一致，而且退化集中在关键能力上，就可能需要 block。

这就是 evaluation observability 的价值。

## Benchmark 常见层次

不是所有 benchmark 都解决同一类问题。

| 类型 | 例子 | 主要价值 | 局限 |
| --- | --- | --- | --- |
| 通用能力 benchmark | MMLU、GSM8K 类任务 | 快速建立模型能力画像 | 不一定贴近业务 |
| 领域 benchmark | 法律、医疗、客服、代码等领域题 | 更贴近具体场景 | 数据维护成本高 |
| 回归 benchmark | 固定线上问题集 | 防止版本退化 | 容易过拟合 |
| 安全 benchmark | 越狱、敏感内容、拒答 | 检查风险边界 | 指标解释复杂 |
| 人工评审集 | reviewer 标注样本 | 更接近真实质量 | 成本高、主观性强 |

学习阶段先理解通用 benchmark 和回归 benchmark 就够了。
真实生产系统通常会逐步加入领域集、安全集和人工评审。

## Leaderboard 应该展示什么

一个有用的 leaderboard 不应该只有总分。
至少应该能让人看出：

- model
- task
- backend
- metric
- score
- sample count
- run time
- few-shot
- latest / best
- settings summary

更进一步，还可以展示：

- 任务分组
- 版本差异
- release recommendation
- regression count
- failed samples
- confidence / variance

当前仓库里的 leaderboard 是最小学习版。
它的价值不在于和真实平台一样完整，而在于让你看到：

> run history 可以被组织成可比较的视图。

## Observability 应该保留什么

评测观测信息最好从一开始就结构化保存。

至少包括：

| 信息 | 为什么重要 |
| --- | --- |
| run id | 复现和引用这次评测 |
| task | 知道测的是什么 |
| model | 知道被测对象 |
| backend | 判断服务路径是否变化 |
| settings | 判断比较是否公平 |
| sample outputs | 看具体错误 |
| summary | 快速了解整体表现 |
| comparison | 判断相对 baseline 的变化 |
| recommendation | 给发布流程一个自动建议 |
| artifacts path | 让 PR reviewer 能打开证据 |

如果这些信息只散落在终端输出里，很快就会丢。
所以当前项目会把它们写成 JSON / Markdown / history 文件。

## 和当前仓库怎么对应

`projects/eval-module` 现在提供的是学习型评测模块，核心能力包括：

- `run`
- `compare`
- `leaderboard`
- `list-runs`
- `list-comparisons`
- `list-tasks`
- run bundle
- comparison bundle
- sample outputs
- sample summary
- sample analysis
- run history
- release recommendation

你可以重点看：

- `projects/eval-module/src/eval_module/runner.py`
- `projects/eval-module/src/eval_module/results/store.py`
- `projects/eval-module/tests/test_runner.py`
- [Eval 发布门禁 Lab](/07-hands-on-labs/03-eval-release-gate-lab)
- [Eval 退化与发布阻断案例](/11-case-studies/05-eval-regression-release-gate)

这些内容会把“benchmark / leaderboard / observability”从概念变成可运行产物。

## 一个学习任务

你可以这样练习：

1. 运行一次 eval，生成 result JSON。
2. 用同一个 result 作为 baseline 和 candidate 跑 compare。
3. 修改一份 candidate 的指标，观察 recommendation 如何变化。
4. 生成 leaderboard。
5. 打开 sample outputs 和 sample analysis。
6. 写一段发布判断：应该 release、review 还是 block？

这个练习的重点不是模型分数，而是能否解释“为什么做这个发布判断”。

## 常见误区

### 误区 1：只看平均分

平均分可能掩盖关键样本退化。
尤其是生产系统里，某些错误虽然数量少，但影响很大。

### 误区 2：把 leaderboard 当真相

leaderboard 是视图，不是事实本身。
事实在 run artifact、settings、sample outputs 和 comparison report 里。

### 误区 3：忽略评测设置变化

prompt、few-shot、数据集、解析规则变化都可能影响结果。
如果 settings_changed，就要谨慎解释比较结论。

### 误区 4：没有样本级证据

没有 sample outputs，就很难知道分数为什么变。
真实评审一定要能下钻到样本。

## 学完这一页应该能回答

- benchmark 和 leaderboard 有什么区别？
- 为什么 leaderboard 不能替代评测过程？
- observability 在评测里解决什么问题？
- 为什么 settings_changed 会影响发布判断？
- 一个 release gate 应该看哪些信号？
- 当前 `eval-module` 生成了哪些可复盘产物？

## 下一步

继续读：

- [Run、Compare、History](/04-evaluation-observability/01-run-compare-history)
- [从 Run 到发布决策](/04-evaluation-observability/07-from-run-to-release-decision)
- [Benchmark 与生产质量不是一回事](/04-evaluation-observability/08-benchmark-vs-production-quality)
- [Eval 发布门禁 Lab](/07-hands-on-labs/03-eval-release-gate-lab)
