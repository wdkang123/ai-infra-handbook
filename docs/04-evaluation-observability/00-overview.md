# 04. Evaluation Observability

这一组讲的是“系统跑完之后，你怎么知道它到底表现如何”。

它包含两条互相补充的线：

- evaluation：输出质量是否变好
- observability：运行过程发生了什么

很多 AI 项目失败，不是因为没有模型，也不是因为没有接口，而是因为缺少判断系统变化的证据。模型换了、prompt 改了、gateway 加了 fallback、训练换了数据集，如果没有评测和观测，团队只能靠感觉讨论“是不是更好”。

这一章要帮你建立的直觉是：

> AI Infra 不是只把请求跑通，还要把结果变成可比较、可复盘、可发布判断的证据。

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

## 推荐阅读顺序

1. [Run、Compare、History](/04-evaluation-observability/01-run-compare-history)
2. [Benchmark、Leaderboard、Observability](/04-evaluation-observability/02-benchmark-leaderboard-observability)
3. [Tracing、Metrics、Logs](/04-evaluation-observability/03-observability-traces-metrics-logs)
4. [评测工具与展示面](/04-evaluation-observability/04-evaluation-tools-and-surfaces)
5. [LLM Evaluation](/04-evaluation-observability/05-llm-evaluation)
6. [Benchmark、Arena、Leaderboard](/04-evaluation-observability/06-benchmark-arena-leaderboard)
7. [从 Run 到发布决策](/04-evaluation-observability/07-from-run-to-release-decision)
8. [Benchmark 与生产质量不是一回事](/04-evaluation-observability/08-benchmark-vs-production-quality)

建议先读 run / compare / history，因为这是最小可复盘单元；再读 benchmark 和 leaderboard；最后读 observability 与发布决策。

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
