# 案例复盘总览

这一章把前面的概念、项目和 lab 重新组织成几个接近真实工程场景的案例。

前面的章节更像学零件：

- 什么是 gateway
- 什么是 run bundle
- 什么是 checkpoint index
- 什么是 request timeline

案例复盘则更像看一次完整工作流：

- 一个请求失败了，怎么定位
- 一个候选模型想发布，怎么判断
- 一次训练产物要复现，怎么追溯
- 一次 fallback/cache 成功响应背后是否隐藏平台风险
- 一次 eval 轻微退化是否应该阻断发布

案例的价值不是告诉你标准答案，而是训练你用证据做工程判断。

## 案例和教程的区别

教程通常按顺序告诉你做什么：

```text
第一步运行命令，第二步查看输出，第三步得到结果。
```

案例更接近真实工程：

```text
先看到一个现象。
再根据证据提出假设。
然后排除错误方向。
最后给出判断和下一步。
```

所以读案例时，不要只找“最后答案”。更重要的是看作者为什么这样判断。一个好的案例应该让你看到：

- 第一条证据为什么重要
- 哪些原因被排除了
- 哪些证据还不够
- 当前学习系统和生产系统之间差了什么
- 后续应该沉淀成什么任务

这类训练会让你从“照着命令跑”走向“能处理不完整信息”。

## 什么时候读这一章

建议在你至少完成这些内容之后再看：

- [第一次实操演练](/00-overview/04-first-walkthrough)
- [四个项目怎么连成系统](/06-projects/06-end-to-end-system-map)
- [Serving 可观测性 Lab](/07-hands-on-labs/01-serving-observability-lab)
- [Gateway 韧性 Lab](/07-hands-on-labs/02-gateway-resilience-lab)
- [Eval 发布门禁 Lab](/07-hands-on-labs/03-eval-release-gate-lab)
- [Finetune 复现资产 Lab](/07-hands-on-labs/04-finetune-reproducibility-lab)
- [示例输出与证据库](/13-output-gallery/00-overview)

如果你还没有跑过命令，也可以先浏览，但不要急着背结论。

这些案例的价值在于把命令、日志、事件、产物和判断串起来。

如果你对某个输出字段不熟，可以先去证据库查它属于哪一层、能证明什么、不能证明什么。

## 读每个案例时的三遍法

建议每个案例至少读三遍。

### 第一遍：看现象

只看开头和最终判断，先知道这是哪类问题。

你要回答：

- 用户或维护者最初看到什么？
- 这个现象属于请求、发布、训练还是平台治理？
- 如果你自己遇到，第一反应会怀疑哪里？

### 第二遍：看证据链

沿着文中的证据一步步走。

你要回答：

- 第一条证据是什么？
- 它把怀疑范围缩小到了哪一层？
- 哪条证据排除了错误方向？
- 哪条证据支撑最终判断？

### 第三遍：看迁移价值

最后看它如何迁移到真实系统。

你要回答：

- 当前 demo 里哪些证据在生产系统仍然需要？
- 生产里还缺哪些能力？
- 这个案例可以拆成什么 GitHub issue 或改进任务？

这样读案例，收获会比只看结论大很多。

## 案例列表

### 案例 1：请求失败排查

入口：[请求失败排查案例](/11-case-studies/01-request-incident-walkthrough)

你会从一个 `502` 或 `401` 现象出发，沿着：

- response header
- request id
- gateway `/events/failures`
- gateway request timeline
- inference request timeline
- metrics

逐步判断问题属于调用方、gateway 还是 inference-service。

训练重点：

- 不要只看 status
- 用 request id 串证据
- 区分入口错误和下游错误

### 案例 2：模型发布判断

入口：[模型发布判断案例](/11-case-studies/02-model-release-decision-walkthrough)

你会从一次候选模型评测结果出发，沿着：

- eval run
- sample outputs
- sample analysis
- comparison report
- release recommendation
- leaderboard / run index

判断候选模型是否值得进入下一步发布。

训练重点：

- 不要只看平均分
- 看 task、metric、min_delta 和样本
- 结合 observability 和发布风险

### 案例 3：训练产物复现

入口：[训练产物复现案例](/11-case-studies/03-finetune-to-eval-asset-lineage)

你会从一个 export artifact 出发，向前追溯：

- export manifest
- run manifest
- checkpoint index
- dataset summary
- dataset registry
- run history

确认这个导出产物能否被解释、被复现、被评测。

训练重点：

- checkpoint 和 export 不是同一件事
- dataset/run/checkpoint/export 要形成 lineage
- 没有来源的训练产物很难进入发布判断

### 案例 4：Gateway Fallback 与缓存复盘

入口：[Gateway Fallback 与缓存复盘案例](/11-case-studies/04-gateway-fallback-cache-incident)

你会从一个表面成功的请求出发，沿着：

- `x-fallback-used`
- `x-cache`
- gateway request timeline
- failure summary
- cache token 隔离
- fallback 成本、质量和延迟风险

判断这次成功是正常降级，还是掩盖了上游健康问题。

训练重点：

- 成功响应也可能隐藏平台风险
- fallback 必须被观测
- cache 必须考虑隔离和过期

### 案例 5：Eval 退化与发布阻断

入口：[Eval 退化与发布阻断案例](/11-case-studies/05-eval-regression-release-gate)

你会从一次 candidate 评测轻微退化出发，沿着：

- comparison report
- settings changed
- sample outputs
- sample analysis
- failed sample 聚类
- release recommendation

判断应该继续 review、补测，还是直接阻断发布。

训练重点：

- 轻微退化也可能很重要
- settings changed 会影响可比性
- release gate 的价值是保护主线质量

## 这章训练什么能力

这章最想训练的是几种能力：

| 能力 | 你应该能做到 |
| --- | --- |
| 定位 | 从一个现象回到具体层、具体 request、具体 artifact |
| 判断 | 用证据而不是感觉判断是否可发布、可复现、可继续排查 |
| 讲述 | 把一次工程过程讲成别人听得懂的系统故事 |
| 阻断 | 在证据不足或风险集中时，知道为什么不能继续发布 |
| 复盘 | 把失败、原因、证据、修复和后续任务沉淀下来 |

这些能力比记住某个工具参数更重要。

## 案例里的证据优先级

不是所有证据都同样强。

| 证据类型 | 强项 | 局限 |
| --- | --- | --- |
| HTTP status | 快速判断入口结果 | 不能解释完整原因 |
| Header | 暴露 request id、cache、fallback | 容易被忽略，且不含完整上下文 |
| Events | 记录结构化过程 | 需要理解字段语义 |
| Metrics | 看趋势和聚合 | 很难解释单个样本细节 |
| Timeline | 解释请求经过哪些阶段 | 依赖 request id 串联 |
| Manifest | 说明产物来源 | 不能直接说明质量好坏 |
| Compare report | 说明候选和基线差异 | 依赖 task 和 dataset 可比 |
| Sample analysis | 解释具体退化或改善 | 需要人工判断和领域理解 |

读案例时可以不断问：这条证据能证明什么，不能证明什么。这个问题比“字段是什么意思”更关键。

## 建议复盘格式

每做完一个案例，可以按这个格式复盘：

```text
现象：

第一条证据：

我怀疑的系统层：

我排除掉的原因：

最终判断：

还缺哪些生产级能力：

后续可以变成什么 issue：
```

如果你能稳定写出这类复盘，说明你已经不只是会跑命令，而是在形成 AI Infra 工程判断力。

## 一个更完整的复盘模板

如果你准备公开分享，可以把复盘写得更完整：

```text
# 案例标题

## 背景
这个案例发生在哪一层，为什么值得看。

## 现象
用户、维护者或发布负责人最初看到什么。

## 第一条证据
从哪里看到，说明了什么。

## 假设
我最初怀疑哪些原因。

## 排除过程
哪些证据排除了哪些假设。

## 最终判断
当前最合理的解释是什么。

## 当前系统边界
学习型实现里已经能看到什么，生产级还缺什么。

## 后续任务
可以变成哪些 issue、lab、测试或文档改进。
```

这份模板也适合贡献者新增案例时使用。

## 如何把案例讲给别人听

公开分享时，一个案例可以按这个顺序讲：

1. 先讲现象，不急着给答案。
2. 展示第一条证据。
3. 说明为什么怀疑某一层。
4. 用第二条证据排除一个错误方向。
5. 展示最终判断。
6. 说明当前学习系统和真实生产系统之间还差什么。
7. 给出一个后续改进任务。

这样案例就不是流水账，而是一个可复用的工程故事。

## 演示案例时的节奏

公开演示时，不建议一上来展示一堆 JSON。更好的节奏是：

1. 用一句话说明现象。
2. 只展示第一条证据。
3. 停下来问听众会怀疑哪里。
4. 再展示第二条证据。
5. 解释为什么某个方向被排除。
6. 给出最终判断。
7. 回到系统图说明它属于哪一层。

这样听众会参与推理，而不是被动看你滚动日志。

## 和证据库、自测、Capstone 的关系

配套页面：

- [示例输出与证据库](/13-output-gallery/00-overview)
- [失败症状到证据地图](/13-output-gallery/05-failure-evidence-map)
- [端到端复盘证据包](/13-output-gallery/04-end-to-end-review-packet)
- [学习自测总览](/10-assessments/00-overview)
- [Capstone 答辩稿](/10-assessments/04-capstone-defense)

建议顺序：

1. 用证据库看懂字段。
2. 用案例复盘看懂故事。
3. 用自测检查自己能不能解释。
4. 用 Capstone 讲给别人听。

## 常见误区

### 只看结论

案例的重点不是结论，而是从现象到证据再到判断的过程。

### 所有失败都归因到模型

很多失败来自 gateway、配置、cache、fallback、eval 设置或训练 lineage。

### 成功响应就不需要复盘

Fallback/cache 案例正好说明：表面成功也可能隐藏风险。

### 案例只能人工写

自动证据包和 smoke 输出可以作为案例素材，但最终还需要人写清判断。

## 下一步

建议按顺序阅读：

1. [请求失败排查案例](/11-case-studies/01-request-incident-walkthrough)
2. [模型发布判断案例](/11-case-studies/02-model-release-decision-walkthrough)
3. [训练产物复现案例](/11-case-studies/03-finetune-to-eval-asset-lineage)
4. [Gateway Fallback 与缓存复盘案例](/11-case-studies/04-gateway-fallback-cache-incident)
5. [Eval 退化与发布阻断案例](/11-case-studies/05-eval-regression-release-gate)
