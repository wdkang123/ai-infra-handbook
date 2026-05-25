# 学习检查点

## 为什么要有这页

因为学这种工程手册时，很容易出现两种错觉：

- 看了很多页，感觉好像懂了
- 跑了很多命令，又不确定自己到底有没有真正掌握

这页不是考试，而是帮你快速判断：  
你现在大概已经站到哪一层了。

如果你想做更正式的阶段验收，可以继续看 [学习自测总览](/10-assessments/00-overview)。  
这里偏快速定位，自测页偏完整答题、演示和复盘。

## 检查点 1：系统地图

如果你已经能不看文档，自己说出这四层分别在解决什么问题，说明第一层已经站稳了：

1. 推理服务层
2. 平台治理层
3. 质量闭环层
4. 训练迭代层

如果你现在还总把它们混在一起，最该回去看的是：

- [什么是 AI Infra](/00-overview/01-what-is-ai-infra)
- [项目学习总览](/06-projects/00-projects-overview)
- [四个项目怎么连成系统](/06-projects/06-end-to-end-system-map)

## 检查点 2：最小联调闭环

如果你已经能跑通：

- `make infra-test`
- `make infra-smoke`

并且大概知道 smoke 在验证什么，说明你已经不只是“看文档”，而是进入了最小实操层。

如果这一步还不稳，最该回去看的是：

- [最小运行手册](/00-overview/03-runbook)
- [第一次实操演练](/00-overview/04-first-walkthrough)

## 检查点 3：请求生命周期

如果你已经能大概说清楚一条请求是怎么经过：

- `ai-gateway`
- `inference-service`
- ordinary response / streaming
- `x-request-id`
- `/metrics`

那说明你已经开始建立系统执行直觉了。

如果这一步还不稳，最该回去看的是：

- [从请求到首个 Token](/01-llm-fundamentals/04-from-request-to-first-token)
- [Streaming、Batching、Metrics](/02-inference-serving/09-streaming-batching-metrics)
- [ai-gateway](/06-projects/02-ai-gateway)
- [inference-service](/06-projects/01-inference-service)
- [Serving 与 Gateway 输出证据](/13-output-gallery/01-serving-gateway-evidence)

## 检查点 4：平台层边界

如果你已经能比较稳定地区分：

- 哪些问题属于 gateway
- 哪些问题属于 inference-service

那说明你已经抓住了非常关键的一条边界。

如果还不稳，最该回去看的是：

- [平台层与模型服务层边界](/03-ai-gateway-platform/05-platform-vs-model-service)
- [外部模型名与内部目标映射](/03-ai-gateway-platform/06-model-name-to-target-mapping)

## 检查点 5：评测不是一个分数

如果你已经不再把 eval 理解成“跑一次命令拿一个结果”，而开始理解：

- run
- compare
- bundle
- history

那说明你已经开始建立质量闭环意识了。

如果这一步还不稳，最该回去看的是：

- [Run、Compare、History](/04-evaluation-observability/01-run-compare-history)
- [从 Run 到发布决策](/04-evaluation-observability/07-from-run-to-release-decision)
- [eval-module](/06-projects/03-eval-module)
- [Eval 报告证据](/13-output-gallery/02-eval-report-evidence)

## 检查点 6：训练是资产，不只是命令

如果你已经开始把训练看成：

- run
- checkpoint
- export
- manifest
- history

而不是只看 `train` 命令有没有执行成功，说明你已经抓住训练工程的关键感觉了。

如果这一步还不稳，最该回去看的是：

- [训练产物、Checkpoint、Export](/05-finetuning-training/02-run-artifacts-export)
- [实验追踪、History、复现](/05-finetuning-training/06-experiment-tracking-history-reproducibility)
- [finetune-demo](/06-projects/04-finetune-demo)
- [Finetune 产物证据](/13-output-gallery/03-finetune-artifact-evidence)

## 检查点 7：能公开讲清当前阶段

如果你已经能说明：

- 当前项目已经具备哪些学习能力
- 哪些地方仍然是学习型实现
- 为什么它适合分享但不等于生产平台
- 公开前应该跑哪些验证命令

那说明你已经可以把这个仓库当成一个完整学习作品来介绍。

如果这一步还不稳，最该回去看的是：

- [项目成熟度地图](/00-overview/14-project-maturity-map)
- [两周学习计划](/00-overview/15-two-week-learning-plan)
- [公开发布验收 Lab](/07-hands-on-labs/06-public-release-readiness-lab)
- [公开演示脚本](/13-output-gallery/06-public-demo-script)

## 检查点 8：能整理输出证据包

如果你已经能把一次运行整理成：

- request id 和 header
- metrics 和 event timeline
- eval sample analysis
- finetune manifest / checkpoint / export
- 已确认和未确认的结论

那说明你已经从“看到输出”进入“能解释输出”的阶段。

如果这一步还不稳，最该回去看的是：

- [示例输出与证据库](/13-output-gallery/00-overview)
- [端到端复盘证据包](/13-output-gallery/04-end-to-end-review-packet)
- [失败症状到证据地图](/13-output-gallery/05-failure-evidence-map)

## 检查点 9：能用案例讲工程判断

如果你已经能选一个案例，讲清：

- 现象是什么
- 证据按什么顺序收集
- 哪些层被排除
- 最终判断为什么成立
- 这个学习型实现离生产系统还差什么

那说明你已经从“会用项目”进入“能讲工程判断”的阶段。

如果这一步还不稳，最该回去看的是：

- [案例复盘总览](/11-case-studies/00-overview)
- [请求失败排查案例](/11-case-studies/01-request-incident-walkthrough)
- [模型发布判断案例](/11-case-studies/02-model-release-decision-walkthrough)
- [训练产物复现案例](/11-case-studies/03-finetune-to-eval-asset-lineage)

## 检查点 10：能组织一次共学或公开分享

如果你已经能准备：

- 一份学习者工作簿
- 一份 90 分钟或半天议程
- 一份复盘或评审模板
- 一组适合 first-time contributor 的任务
- 一份 GitHub 首发检查计划

那说明你已经从“自己学懂”进入“能帮助别人一起学”的阶段。

如果这一步还不稳，最该回去看的是：

- [共学与公开分享套件](/14-workshop-kit/00-overview)
- [讲师与带练指南](/14-workshop-kit/01-facilitator-guide)
- [学习小组议程](/14-workshop-kit/03-study-group-agenda)
- [贡献者协作手册](/14-workshop-kit/05-contribution-playbook)
- [GitHub 发布计划](/14-workshop-kit/06-github-release-plan)

## 这页怎么用最合适

最好的用法不是一次全看，而是：

1. 学一条主线
2. 回来对照一次
3. 看自己卡在哪个检查点
4. 再回对应章节补

这样会比盲目继续往下翻更有效。

## 这一页学完应该带走什么

真正的学习进展，不只是“看了多少页”，而是你能不能更稳定地回答一类问题。  
这些检查点，就是帮你判断这个稳定度的。
