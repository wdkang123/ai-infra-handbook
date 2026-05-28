# 04. Evaluation Observability

> 本页解决：系统跑完之后，如何知道输出质量和运行过程到底发生了什么。
> 读完能做：区分 evaluation 和 observability，并把 run、compare、events、metrics 放到一条证据链里。
> 关联代码：`projects/eval-module`、`projects/ai-gateway`、`projects/inference-service`。
> 验证命令：`PYTHON=.venv/bin/python make infra-smoke`。

这一组讲的是“系统跑完之后，你怎么知道它到底表现如何”。

它包含两条互相补充的线：

- evaluation：输出质量是否变好
- observability：运行过程发生了什么

很多 AI 项目失败，不是因为没有模型，也不是因为没有接口，而是因为缺少判断系统变化的证据。模型换了、prompt 改了、gateway 加了 fallback、训练换了数据集，如果没有评测和观测，团队只能靠感觉讨论“是不是更好”。

这一章要帮你建立的直觉是：

> AI Infra 不是只把请求跑通，还要把结果变成可比较、可复盘、可发布判断的证据。

![Evaluation 与 Observability 证据视图](/images/articles/evaluation-observability-overview.jpg)

*图：Evaluation 关注质量变化，Observability 关注运行过程；两者连起来，才有足够证据解释系统变化。*

## Evaluation 和 Observability 的区别

这两个词经常一起出现，但不要混成一个东西。

### Evaluation 问的是质量

Evaluation 关注的是：

- 回答是否正确
- 是否遵循指令
- 是否更安全
- 是否更稳定
- 新模型是否优于旧模型
- 某次 prompt 改动是否值得发布
- 训练后模型是否真的改善目标任务

它通常会产生 run、score、sample、judge reason、compare report、leaderboard 等对象。

### Observability 问的是运行过程

Observability 关注的是：

- 请求走到了哪里
- 哪个服务慢
- 哪个上游失败
- fallback 是否触发
- cache 是否命中
- 错误率是否上升
- 某个 request id 的链路是什么
- metrics、logs、traces 如何互相解释

它通常会产生 metrics、events、logs、trace、timeline、failure summary 等对象。

### 它们必须连起来

只做 evaluation，你可能知道新版本质量下降了，但不知道为什么。

只做 observability，你可能知道系统运行很稳，但不知道回答是否有用。

成熟的 AI 系统需要两者互补：质量变化要能追溯到运行证据，运行异常也要能影响发布判断。

## 为什么这一章是 AI Infra 的分水岭

很多学习项目到“接口能返回内容”就结束了。但真实 AI Infra 的难点常常从这里才开始：

- 模型回答变长了，是能力提升还是啰嗦？
- 平均分提高了，关键样本是否退化？
- 延迟降低了，是否因为 fallback 走了更短输出？
- cache 命中率提高了，是否把旧答案错误复用？
- 训练后输出更像目标风格，是否牺牲了事实性？

这些问题不能靠一次肉眼体验回答。你需要把一次变化拆成可比较对象，把运行过程拆成可追溯证据，再把两者放到同一张判断表里。

所以这一章训练的不是“会跑 eval 命令”，而是“能解释系统变化”。这是从 demo 走向工程系统的分水岭。

## 当前仓库如何体现这两条线

`projects/eval-module` 是评测侧的学习型项目。它保留了几类关键对象：

- task
- run
- result store
- compare report
- run history
- leaderboard
- sample analysis
- recommendation

`projects/inference-service` 和 `projects/ai-gateway` 则提供观测侧信号：

- health
- metrics
- events
- failure summary
- request timeline
- request id
- cache / fallback headers

这些项目放在一起，就是一个最小质量闭环：

```text
Serving/Gateway 产生运行证据
  -> Eval 产生质量证据
  -> Compare 形成发布建议
  -> Case study 复盘具体决策
  -> Release checklist 收住公开发布风险
```

这比单独一个分数更接近真实工程。

## 最小证据模型

一次靠谱的评测至少应该留下四层证据。

| 层级 | 代表对象 | 解决的问题 |
| --- | --- | --- |
| Task | task definition、dataset id、metric | 这次到底在测什么 |
| Run | run manifest、raw results、sample outputs | 这次是怎么跑出来的 |
| Compare | baseline、candidate、delta、threshold | 和谁比，变化是否有意义 |
| Decision | recommendation、risk note、follow-up | 接下来该发布、阻断还是补测 |

Observability 也有类似层次：

| 层级 | 代表对象 | 解决的问题 |
| --- | --- | --- |
| Request | request id、status、headers | 单次请求发生了什么 |
| Service | metrics、health、events | 服务整体是否异常 |
| Timeline | gateway timeline、inference timeline | 一次请求经过哪些阶段 |
| Summary | failure summary、cache/fallback stats | 一类问题是否正在聚集 |

当 evaluation 和 observability 放在一起，你就能从“结果变差”继续追问“它为什么变差”。

## 推荐阅读顺序

1. [Run、Compare、History](/04-evaluation-observability/01-run-compare-history)
2. [Benchmark、Leaderboard、Observability](/04-evaluation-observability/02-benchmark-leaderboard-observability)
3. [Tracing、Metrics、Logs](/04-evaluation-observability/03-observability-traces-metrics-logs)
4. [评测工具与展示面](/04-evaluation-observability/04-evaluation-tools-and-surfaces)
5. [LLM Evaluation](/04-evaluation-observability/05-llm-evaluation)
6. [Benchmark、Arena、Leaderboard](/04-evaluation-observability/06-benchmark-arena-leaderboard)
7. [从 Run 到发布决策](/04-evaluation-observability/07-from-run-to-release-decision)
8. [Benchmark 与生产质量不是一回事](/04-evaluation-observability/08-benchmark-vs-production-quality)
9. [Eval Regression Gate 示例](/04-evaluation-observability/09-eval-regression-gate-example)

建议先读 run / compare / history，因为这是最小可复盘单元；再读 benchmark 和 leaderboard；最后读 observability 与发布决策。

## 一个具体判断场景

假设你改了一个 prompt，然后 candidate run 的平均分比 baseline 高了 0.03。

直觉上这像是好事。但一个工程判断应该继续问：

1. 这个 delta 是否超过最小有效阈值？
2. 退化样本是否集中在关键任务？
3. candidate 是否和 baseline 使用同一个 task 和 dataset？
4. judge 配置有没有变化？
5. 运行期间是否有 fallback、cache 或 timeout？
6. 输出是否只是变长，导致 judge 更偏好？
7. 是否需要增加专门回归样本？

这些问题解释了为什么 compare report、sample analysis、settings changed、events 和 metrics 要同时存在。它们不是形式化文件，而是防止你被单一分数误导。

## 一次质量判断应该包含什么

一个靠谱的 AI 质量判断，通常不应该只有一句“分数提高了”。

至少应该说明：

- 评测任务是什么
- 数据样本是什么
- baseline 是谁
- candidate 是谁
- 指标怎么算
- 样本级结果是否可检查
- judge reason 是否可读
- 运行环境是否一致
- 是否存在配置变化
- 是否有 regression
- 推荐动作是什么

当前 `eval-module` 的 run bundle、compare report 和 leaderboard，就是在学习这些对象。

## 为什么 LLM Evaluation 特别难

LLM 输出不是简单分类标签。它可能：

- 同义表达很多
- 长答案里局部正确、局部错误
- 遵循格式但事实错误
- 语气很好但没有解决问题
- 对不同用户有不同可接受答案
- 在 benchmark 上好，在生产里差

所以评测系统不能只追求一个漂亮分数。它还要保留样本、reason、配置、任务定义和变更历史。

这也是为什么这一章强调“证据包”而不是“排行榜截图”。

## 评测结果的常见误读

| 看到的现象 | 可能的误读 | 更稳的解释方式 |
| --- | --- | --- |
| 平均分提高 | 可以发布 | 先看 threshold、关键样本、退化聚类 |
| Leaderboard 第一 | 模型最好 | 先看任务覆盖、样本来源、评测口径 |
| Judge reason 很自信 | 判断可靠 | 先检查 reason 是否可审查、是否有偏差 |
| 运行没有报错 | 质量没问题 | 运行稳定不等于回答有用 |
| Eval 退化很小 | 可以忽略 | 小退化如果集中在核心能力，可能必须阻断 |
| Sample 看起来都差不多 | 没必要分析 | LLM 输出差异常常藏在细节和格式里 |

这张表可以当作读 eval 报告时的自检清单。

## Observability 如何帮助 Evaluation

假设一次 eval 结果变差。原因可能是：

- 模型真的变差了
- prompt 被改坏了
- gateway 路由到了另一个上游
- cache 返回了旧结果
- 上游超时触发 fallback
- streaming 中途出错
- 数据集版本不一致
- judge 配置变了

如果没有 observability，所有问题都会被误以为是“模型质量问题”。

所以 request id、events、metrics、run manifest、dataset id 这些看起来偏工程的东西，最终都会影响质量判断。

## 如何把一次退化排查讲清楚

建议使用这个顺序：

```text
1. 先说变化：candidate 相比 baseline 发生了什么。
2. 再说范围：变化影响哪些 task、metric、sample。
3. 检查可比性：task、dataset、judge、settings 是否一致。
4. 查运行证据：request、fallback、cache、latency、error 是否异常。
5. 给出判断：发布、补测、阻断还是继续人工 review。
6. 留下后续：补哪些样本、改哪些阈值、加哪些观测。
```

这套叙述会让评测从“分数报告”变成“工程决策”。公开分享时，它也比展示一张 leaderboard 更有教学价值。

## 学完这一章应该能回答的问题

读完后，你应该能说明：

- run、history、compare report 分别解决什么问题
- benchmark、leaderboard、arena 为什么不是同一件事
- metrics、logs、traces 如何互相补充
- 为什么评测结果需要 sample-level evidence
- 为什么发布决策不能只看平均分
- 为什么观测异常会影响质量判断
- 为什么 benchmark 不等于生产质量
- 当前仓库的 eval-module 如何支持最小发布门禁

如果能回答这些，你就已经开始具备“模型发布判断”的工程视角。

## 最小实践路线

建议这样跑一遍：

1. 运行 eval task，生成一个 baseline run。
2. 修改一个配置或 mock 输出，生成 candidate run。
3. 用 compare 生成对比报告。
4. 查看 run history。
5. 生成 leaderboard。
6. 查看 sample analysis 和 recommendation。
7. 回到 gateway / serving 的 metrics 和 events，想象一次质量退化如何排查。

这比只看概念更有效，因为你会看到质量证据如何落成文件。

## 进一步实践：设计一个小型发布门禁

读完这一章后，可以自己设计一个最小 release gate：

```text
必须满足：
- task 一致
- dataset 一致
- candidate 平均分不低于 baseline
- 关键样本无 P0 退化
- settings_changed 为 false 或有明确解释
- sample_analysis 已人工抽查
- gateway / serving 运行证据无异常集中
```

这个门禁不需要复杂，但要能解释。真正有价值的是你能说清每条规则防什么风险。

## 常见误区

### 误区一：有 benchmark 分数就够了

不够。你还需要样本证据、任务定义、配置、compare、错误分析和发布建议。

### 误区二：Observability 只是线上运维才需要

学习阶段也需要。没有 request id、metrics 和 events，你连 demo 为什么失败都很难复盘。

### 误区三：LLM Judge 可以替代人工判断

LLM Judge 可以提高效率，但也会引入偏差。它应该产生可审查 reason，而不是变成不可解释的黑箱。

### 误区四：平均分提高就应该发布

平均分可能掩盖关键任务退化。发布决策要看 threshold、regression、样本和业务风险。

### 误区五：评测和训练是分开的

训练的 dataset、run、checkpoint 和 export 最终都需要进入评测闭环。否则你无法判断训练是否真的改进了目标能力。
