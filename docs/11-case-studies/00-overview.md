# 案例复盘总览

这一章把前面的概念、项目和 lab 重新组织成几个接近真实工程场景的案例。

前面的章节更像“学零件”：

- 什么是 gateway
- 什么是 run bundle
- 什么是 checkpoint index
- 什么是 request timeline

案例复盘则更像“看一次完整工作流”：

- 一个请求失败了，怎么定位
- 一个候选模型想发布，怎么判断
- 一次训练产物要复现，怎么追溯
- 一次 fallback/cache 成功响应背后是否隐藏平台风险
- 一次 eval 轻微退化是否应该阻断发布

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

## 这章训练什么能力

这章最想训练的是三种能力：

| 能力 | 你应该能做到 |
| --- | --- |
| 定位 | 从一个现象回到具体层、具体 request、具体 artifact |
| 判断 | 用证据而不是感觉判断是否可发布、可复现、可继续排查 |
| 讲述 | 把一次工程过程讲成别人听得懂的系统故事 |
| 阻断 | 在证据不足或风险集中时，知道为什么不能继续发布 |

## 建议复盘格式

每做完一个案例，可以按这个格式复盘：

```text
现象：

第一条证据：

我怀疑的系统层：

我排除掉的原因：

最终判断：

还缺哪些生产级能力：
```

如果你能稳定写出这类复盘，说明你已经不只是会跑命令，而是在形成 AI Infra 工程判断力。

配套页面：

- [端到端复盘证据包](/13-output-gallery/04-end-to-end-review-packet)
- [失败症状到证据地图](/13-output-gallery/05-failure-evidence-map)
