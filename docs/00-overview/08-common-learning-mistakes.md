# 常见学习误区

## 为什么这一页要放在总览里

AI Infra 很容易出现一种表面上的“很努力”，但实际上学习路径并不高效。

这通常不是因为你不认真，而是因为这个领域天然容易让人：

- 一下看太多组件
- 一下追太多框架
- 一下想把代码做得特别真实
- 一下把模型、平台、评测、训练混在一起
- 一下被 benchmark、工具名和架构图带着走

所以先把常见误区点出来，反而会更省时间。

这页不是给你增加心理负担，而是帮你避开几个最容易浪费时间的弯路。

## 误区一：一开始就想把所有源码看完

这通常不是最高效的起点。

AI Infra 项目里的代码如果脱离上下文直接读，很容易像“复杂实现细节的堆叠”。你会看到 server、runtime、router、store、manifest、tests，但不知道它们为什么被这样拆开。

更好的方式通常是：

1. 先跑起来
2. 看输出物
3. 画系统地图
4. 再带着问题回看关键文件

例如，先跑一次 gateway 请求，看到 `x-request-id`、`x-cache`、`x-upstream-model`，再去看 gateway 代码，理解会更快。

推荐入口：

- [第一次实操演练](/00-overview/04-first-walkthrough)
- [API Surface 速查](/09-reference/05-api-surface)
- [概念到代码索引](/09-reference/02-concept-to-code-index)

## 误区二：一开始就追求生产级真实实现

这也是最常见的坑之一。

当前仓库里很多模块是学习型实现，不是完整生产系统。这不是弱，而是刻意控制复杂度。

如果你太早把目标变成：

- 全部真实后端
- 全部真实训练
- 全部真实平台策略
- 全部接上外部服务
- 一次性做完 dashboard、auth、billing、tenant、deployment

学习成本会陡增。

更稳的方式是：

1. 先保住接口和边界
2. 再保住观测和证据
3. 再替换某一层内部实现
4. 最后再做跨层生产化

推荐入口：

- [生产迁移路线总览](/12-production-migration/00-overview)
- [项目成熟度地图](/00-overview/14-project-maturity-map)

## 误区三：把 gateway 和 inference-service 混在一起看

这会让你很难建立系统边界。

更稳的做法是先明确：

- `inference-service` 更像执行层
- `ai-gateway` 更像治理层

两者都可能有 `/health`、`/metrics`、`/events`，但它们回答的问题不同：

- inference-service 关注模型服务是否能处理请求
- ai-gateway 关注请求是否被正确鉴权、路由、限流、cache 和 fallback

如果这条边界不清楚，看到 `502` 时你可能不知道该先查 gateway、upstream health、fallback，还是 inference engine。

推荐入口：

- [平台层与模型服务层边界](/03-ai-gateway-platform/05-platform-vs-model-service)
- [系统地图自测](/10-assessments/01-system-map-check)

## 误区四：只看 benchmark，不看上下文

Benchmark 很重要，但它不是全部。

更完整的判断通常要一起看：

- benchmark
- run / compare
- sample outputs
- observability
- 成本与延迟
- 失败路径
- 发布风险

如果只看单个分数，很容易把“某个榜单表现”误当成最终结论。

一个模型或 prompt 是否值得发布，还要问：

- 它和谁比较
- task 是否一致
- 指标是否一致
- 关键样本是否退化
- latency 和 cost 是否可接受
- gateway 是否发生 fallback
- 训练产物是否能追溯来源

推荐入口：

- [从 Run 到发布决策](/04-evaluation-observability/07-from-run-to-release-decision)
- [Benchmark 与生产质量不是一回事](/04-evaluation-observability/08-benchmark-vs-production-quality)

## 误区五：一上来就决定必须微调

训练当然重要，但不是每个问题都应该先走微调。

很多时候更该先问：

- prompt / workflow 是否已经稳定
- 是否更像知识接入问题
- 是否应该先做 RAG 或工具调用
- 是否已经有最小评测路径
- 数据是否足够干净
- 训练后如何判断变好

如果评测路径还没有建立，微调后的结果很容易变成“感觉更好了”。

推荐入口：

- [什么时候该微调](/05-finetuning-training/07-when-to-finetune)
- [数据集、Run、Checkpoint](/05-finetuning-training/04-datasets-runs-checkpoints)

## 误区六：只读文档，不回代码

这也不够。

这套仓库不是纯文档站。最好的节奏通常是：

- 文档给你地图
- 代码给你当前实现
- 命令和结果给你反馈
- 测试告诉你哪些行为被保护
- 输出证据帮助你复盘

三者一起看，理解会长得更快。

推荐入口：

- [文档与代码怎么对应](/00-overview/05-docs-to-code-map)
- [项目学习总览](/06-projects/00-projects-overview)

## 误区七：跑通一次就停

第一次跑通只是起点。

更有价值的下一步通常是：

- 选一条主线
- 改一个小点
- 再跑一轮
- 观察结果变化
- 写一段复盘

比如：

- 改一个 mock 输出，观察 eval compare 怎么变
- 改一个 gateway 限流配置，观察 `429`
- 改一个 manifest 字段，观察 export history
- 改一个文档链接，跑 docs-quality

推荐入口：

- [第一次跑完之后学什么](/00-overview/06-after-first-walkthrough)
- [学习自测总览](/10-assessments/00-overview)

## 误区八：只看 happy path

AI Infra 的学习价值很大一部分在失败路径。

你需要主动观察：

- `401`
- `404`
- `429`
- `502`
- streaming error event
- compare 拒绝比较
- export 失败
- public-check 发现安全问题

如果只看“请求成功返回文本”，很难理解平台、评测和维护为什么重要。

推荐入口：

- [失败症状到证据地图](/13-output-gallery/05-failure-evidence-map)
- [常见排障手册](/09-reference/04-troubleshooting)

## 误区九：把公开发布当成最后一步才考虑

公开发布不是最后随手 push 一下。

如果你准备把项目传到 GitHub，应该尽早养成这些习惯：

- 不提交真实 `.env`
- 示例值只用 placeholder
- 文档里不放个人路径
- 每次大改后跑 `public-check`
- 变更写入 changelog
- PR 说明验证结果

这样后面公开时不会突然大规模返工。

推荐入口：

- [公开仓库卫生规范](/08-publication/06-public-repo-hygiene)
- [GitHub 入口与协作地图](/08-publication/14-github-entrypoints)

## 误区十：把 AI 当成替你完成学习的人

AI 可以帮你写代码、改文档、查报错、生成草稿，但它不能替你建立系统判断。

更好的用法是：

- 先用这套手册建立地图
- 用 AI 帮你细化某一页或某个函数
- 自己运行验证命令
- 自己解释输出证据
- 自己决定下一步改哪里

如果你只是让 AI 不断生成内容，而不跑、不看、不复盘，项目会变厚，但你的理解不会同步变厚。

## 如何判断自己走偏了

如果出现这些信号，可以停下来调整：

- 看了很多工具，但说不清它们属于哪一层
- 跑了很多命令，但说不清输出证明什么
- 改了很多文件，但不知道该跑哪些验证
- benchmark 看了很多，但不能做发布判断
- 训练跑了，但不知道数据和 export 来源
- 准备公开了，却还没跑安全检查

调整方式通常很简单：

1. 回到系统地图。
2. 选一条主线。
3. 做一个小任务。
4. 跑验证。
5. 写复盘。

## 这一页学完应该带走什么

AI Infra 学习最重要的不是一开始学得多快，而是路径要稳。

避开这些常见误区之后，你后面再继续深入，速度反而会更快。
