# Capstone 答辩稿

这页把最终验收整理成一场 30 分钟答辩。

你可以自己录屏，也可以让别人按这页提问。答辩目标不是炫技，而是证明你已经能把这套学习型 AI Infra 系统讲清楚、跑清楚、解释清楚。

如果前面的学习像是在搭积木，Capstone 就是检查你能不能把积木搭成一座有结构的房子。

## 答辩要证明什么

这场答辩要证明 5 件事。

### 1. 你理解项目定位

你要说清楚：

- 这不是生产级 AI 平台
- 这也不是零散 demo
- 它是“文档站 + 可运行脚手架 + 最小联调链路”的学习手册
- 公开分享时，重点是让读者学会系统边界和证据闭环

如果你一上来就把项目包装成生产平台，答辩会偏掉。

### 2. 你理解四层系统

你要能解释：

- `inference-service` 为什么是执行层
- `ai-gateway` 为什么是治理层
- `eval-module` 为什么是质量层
- `finetune-demo` 为什么是训练资产层

并说明它们如何连成闭环。

### 3. 你能跑通并解释证据

只跑命令不够。你要能解释输出：

- `infra-check` 证明什么
- `infra-smoke` 证明什么
- gateway headers 说明什么
- eval compare report 如何支持发布建议
- finetune manifest 如何支持复现
- evidence packet 如何串起端到端证据

### 4. 你能解释失败路径

真实系统不会只有 happy path。

你至少要能解释：

- `401`
- `404`
- `429`
- `502`
- streaming 中途失败
- eval compare 拒绝比较
- export 因 checkpoint 不完整失败

### 5. 你能提出下一步改进

Capstone 不是终点。答辩最后要提出一个可验证的改进任务：

- 改哪一层
- 为什么改
- 风险是什么
- 要补哪些测试或文档
- 跑什么验证命令
- 如何展示输出证据

## 答辩材料

答辩前准备：

1. 一张四层系统图
2. 一次完整 `infra-check` 结果
3. 一次完整 `infra-smoke` 结果
4. 一次 gateway 请求演示
5. 一次 eval run / compare 产物
6. 一次 finetune run / export 产物
7. 一份端到端复盘证据包
8. 一份“从学习型实现走向生产系统”的升级计划
9. 一条你亲自设计的后续改进任务

证据包可以参考 [端到端复盘证据包](/13-output-gallery/04-end-to-end-review-packet)。

升级计划可以参考 [生产迁移路线总览](/12-production-migration/00-overview)，但要用你自己的语言说明为什么先迁移哪一层。

## 30 分钟流程

| 时间 | 内容 | 目标 |
| --- | --- | --- |
| 0-3 min | 项目定位 | 说明这不是生产平台，而是学习型 AI Infra 手册 |
| 3-8 min | 四层系统图 | 讲清执行层、治理层、质量层、训练层 |
| 8-13 min | 请求链路演示 | 从 gateway 到 inference-service 跑一次请求 |
| 13-17 min | 失败路径演示 | 展示 `401 / 404 / 429 / 502` 中至少两个 |
| 17-21 min | Eval 发布判断 | 展示 run、compare、min_delta、history |
| 21-25 min | Finetune 资产复现 | 展示 run、checkpoint、export、manifest |
| 25-27 min | 输出证据包 | 说明哪些证据支撑你的判断 |
| 27-29 min | 生产化差距 | 说明哪些地方仍是 mock 或教学实现 |
| 29-30 min | 下一步计划 | 给出一个可验证的改进任务 |

如果时间不够，宁可少展示命令，也要把“为什么这条证据有意义”讲清楚。

## 演示脚本

你可以按这个顺序演示：

```bash
PYTHON=.venv/bin/python make infra-check
PYTHON=.venv/bin/python make infra-smoke
```

然后打开：

- [四个项目怎么连成系统](/06-projects/06-end-to-end-system-map)
- [命令速查](/09-reference/01-command-cheatsheet)
- [API Surface 速查](/09-reference/05-api-surface)
- [CLI Surface 速查](/09-reference/06-cli-surface)
- [产物与文件索引](/09-reference/03-artifacts-and-files)
- [示例输出与证据库](/13-output-gallery/00-overview)
- [常见排障手册](/09-reference/04-troubleshooting)
- [生产迁移路线总览](/12-production-migration/00-overview)

最后展示一个你自己完成的 lab 复盘。

## 必答问题

请准备这些问题：

1. 为什么 gateway 和 inference-service 要拆开？
2. 为什么 streaming error 不能总是普通 JSON error？
3. 为什么 request id 对排障重要？
4. 为什么 cache 要按 token 或调用方隔离？
5. 为什么 eval compare 需要校验 task 一致性？
6. 为什么训练导出产物要有 manifest？
7. 为什么 smoke 不能替代单元测试？
8. 为什么这个项目现在仍然不能直接当生产平台？
9. 为什么公开分享时要展示证据包，而不是只展示命令通过？
10. 如果你只能下一步改一层，你会先改哪里，为什么？

回答时建议使用这个结构：

```text
我的结论是：
对应系统层是：
当前仓库证据是：
如果失败，排查顺序是：
后续改进可以是：
```

## 深挖追问

如果你是带练者，可以继续追问：

| 主题 | 追问 |
| --- | --- |
| Serving | 如果 TTFT 变慢，你会先看 prefill、queue、gateway 还是 client？ |
| Gateway | Fallback 成功是否一定代表系统健康？ |
| Eval | 平均分提升但关键样本退化，应该怎么发布？ |
| Finetune | Export manifest 缺 base model，会影响什么？ |
| Observability | Metrics 正常但单个用户失败，应该看什么？ |
| Publication | 公开仓库为什么要跑安全扫描？ |

这些追问的目标不是难倒学习者，而是检查他们是否能跨层推理。

## Rubric

| 维度 | Level 1 | Level 2 | Level 3 | Level 4 |
| --- | --- | --- | --- | --- |
| 系统地图 | 能列出项目名 | 能说出四层职责 | 能解释上下游关系 | 能指出生产化差距并给迁移顺序 |
| 请求链路 | 能跑命令 | 能解释普通请求 | 能解释 streaming 和错误 | 能设计新的观测指标或失败证据 |
| Gateway 治理 | 知道鉴权和路由 | 能触发常见错误 | 能解释 fallback/cache/限流 | 能提出风险控制方案 |
| Eval 判断 | 能运行 run | 能运行 compare | 能解释 min_delta 和 task 校验 | 能设计发布门禁 |
| Finetune 资产 | 能运行 train | 能运行 export | 能解释 checkpoint/export/manifest | 能设计 lineage 或版本策略 |
| 工程验证 | 会跑测试 | 知道每类测试作用 | 能定位失败原因 | 能补测试并说明覆盖面 |
| 公开协作 | 知道仓库入口 | 能提 issue | 能按 PR template 说明验证 | 能把薄弱点转成路线图任务 |

建议公开展示时达到：

- 大部分维度 Level 3
- 至少一个维度 Level 4

如果只是自己学习，Level 2 到 Level 3 的跃迁最重要。

## 常见失败表现

| 表现 | 说明 |
| --- | --- |
| 只展示命令成功 | 没有解释证据含义 |
| 把所有错误都归因到模型 | 系统层次没分清 |
| 讲不清 eval compare | 质量判断还没有形成 |
| 讲不清 manifest | 训练资产链还没建立 |
| 没有失败路径 | 公开项目容易显得像演示脚本 |
| 没有下一步计划 | 学习成果无法继续推进 |

这些失败表现不是坏事，它们正好告诉你下一轮该补哪里。

## 答辩后复盘

答辩结束后写下：

```text
我讲得最清楚的是：
我讲得最模糊的是：
别人最容易问倒我的问题是：
我缺少哪类输出证据：
我下一步要补的文档或代码是：
我会用什么命令验证：
这件事能否变成一个 GitHub issue：
```

这份复盘比答辩本身更重要。

它会把“我感觉还可以”变成下一轮可执行的改进。

## 和公开分享怎么连接

如果你准备发到 GitHub、写文章或录视频，Capstone 可以直接变成内容结构：

- 开头讲项目定位
- 中间讲四层系统图
- 演示请求链路和失败路径
- 展示 eval / finetune 证据
- 解释安全和公开检查
- 最后给路线图

这样公开分享就不是单纯展示页面，而是在展示一套可复盘的学习系统。
