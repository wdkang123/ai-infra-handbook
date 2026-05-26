# 学习自测总览

这一组页面不是为了考试，而是为了回答一个更实用的问题：

> 我是不是已经能把这套 AI Infra 小系统讲清楚、跑清楚、改清楚、验证清楚？

很多学习项目会停在“我看完了”或“我跑通了”。但如果你准备把这个项目分享给别人、写成博客、录成视频、放到 GitHub 上，真正需要证明的是另一件事：你能不能把系统边界、正常路径、失败路径、输出证据和后续改进都讲明白。

自测章节就是这个阶段的验收工具。

## 什么时候开始自测

不要等到“全部学完”才开始自测。自测越早出现，学习路线越不容易散。

建议在这些节点做一次：

| 节点 | 自测目标 |
| --- | --- |
| 第一次实操后 | 确认系统地图和最小链路 |
| Serving/Gateway 学完后 | 确认请求路径和失败归因 |
| Eval/Finetune 学完后 | 确认质量判断和训练资产 |
| 做完 Lab 后 | 确认证据解释和复盘能力 |
| 公开分享前 | 确认 Capstone 和边界说明 |

自测不是为了给自己打分，而是为了找下一步最该补哪里。

## 自测要检查什么

这套自测不追求记忆题，而是检查 5 类能力。

### 1. 系统地图能力

你是否能不看文档画出：

- execution / serving 层
- gateway / platform 层
- evaluation / observability 层
- finetuning / training 层

并说明它们为什么要拆开。

如果只能背项目名，但说不清边界，就还停在 Level 1。

### 2. 请求链路能力

你是否能解释一次请求从 gateway 到 inference service 的路径：

- 谁做鉴权
- 谁做模型路由
- 谁返回 `x-request-id`
- 谁可能返回 `401 / 404 / 429 / 502`
- streaming 失败为什么不等于普通 JSON error
- request timeline 应该怎么查

这决定你是否真的理解“能跑”和“能排查”的差异。

### 3. 质量判断能力

你是否能说明：

- eval run 为什么不是终点
- compare 为什么要校验 task
- min_delta 为什么会影响发布建议
- leaderboard 为什么不能替代样本分析
- benchmark 为什么不等于生产质量

这决定你是否从“跑评测脚本”走向“做发布判断”。

### 4. 训练资产能力

你是否能解释：

- dataset registry 的作用
- run manifest 为什么重要
- checkpoint index 如何支持 export / resume
- export manifest 为什么要保留 lineage
- finetune 结果如何进入 eval

这决定你是否理解训练系统不是一个孤立命令，而是一条资产链。

### 5. 工程验证能力

你是否知道不同改动要跑什么验证：

- 只改文档时跑什么
- 改脚本时跑什么
- 改项目代码时跑什么
- 公开发布前跑什么
- 如何用输出证据说明结果可信

这决定你是否能把项目维护成可公开协作的仓库。

## 自测分级

每个主题都可以用同一套标准判断。

| 等级 | 表现 | 典型证据 |
| --- | --- | --- |
| Level 1 | 能复述名词，但解释不出系统边界 | 能列出项目名和概念名 |
| Level 2 | 能跑通命令，也知道主要文件在哪里 | 能贴出命令、路径和基本输出 |
| Level 3 | 能解释正常路径和失败路径，并能指出测试覆盖和输出证据 | 能讲清 status、headers、events、manifest |
| Level 4 | 能提出一个合理改进方案，并说明风险和验证方式 | 能写出改动范围、回归风险、验证命令和文档更新 |

公开分享时，建议至少达到 Level 3。

如果你能稳定达到 Level 4，这套项目就不只是“能跑”，而是开始变成你自己的工程作品。

## 怎么给自己评分

评分时不要只看回答是否“听起来对”。建议每题都问三件事：

1. 有没有说明边界。
2. 有没有指向代码或命令。
3. 有没有引用输出证据。

比如回答“Gateway 为什么存在”：

- Level 1：因为它是网关。
- Level 2：它能代理请求到 inference-service。
- Level 3：它处理鉴权、路由、限流、fallback、cache，并能用 headers/events/metrics 解释请求路径。
- Level 4：它还能说明如果要加入多租户配额或真实缓存，需要改哪些边界、补哪些测试和文档。

这个评分方式能防止你把“会说概念”误判成“会做工程判断”。

## 自测目录

- [系统地图自测](/10-assessments/01-system-map-check)
- [Serving 与 Gateway 自测](/10-assessments/02-serving-gateway-quiz)
- [Eval 与 Finetune 自测](/10-assessments/03-eval-finetune-quiz)
- [Capstone 答辩稿](/10-assessments/04-capstone-defense)
- [参考答案与讲解](/10-assessments/05-answer-key)
- [自动生成测评包](/10-assessments/06-generated-assessment-pack)
- [自动生成路线图包](/08-publication/05-generated-roadmap-pack)
- [自动生成首发运营包](/08-publication/13-generated-launch-pack)

如果说 [课程大纲](/00-overview/12-course-syllabus) 是学习路线，[深度实战](/07-hands-on-labs/00-overview) 是动手任务，[示例输出与证据库](/13-output-gallery/00-overview) 是证据解释，那么学习自测就是阶段验收。

## 手写自测和自动测评包怎么配合

手写自测适合深入理解固定主题；自动测评包适合检查当前课程结构是否整体可测。

| 类型 | 优势 | 适合场景 |
| --- | --- | --- |
| 手写自测 | 题目更细，讲解更深入 | 自学、专题复习 |
| 自动测评包 | 跟随课程目录更新，覆盖模块更全 | 带练、公开发布、PR review |
| Capstone | 跨模块整合 | 最终展示和公开演示 |

如果你是学习者，先做手写自测。
如果你是维护者或讲师，再生成自动测评包，检查整站是否可测。

## 推荐节奏

### 第一次学习

如果你正在从头学：

1. 学完模块 0 和模块 1 后，做 [系统地图自测](/10-assessments/01-system-map-check)。
2. 学完推理服务和平台治理后，做 [Serving 与 Gateway 自测](/10-assessments/02-serving-gateway-quiz)。
3. 学完评测和训练后，做 [Eval 与 Finetune 自测](/10-assessments/03-eval-finetune-quiz)。
4. 对照 [示例输出与证据库](/13-output-gallery/00-overview) 整理一份证据包。
5. 完成所有 lab 后，做 [Capstone 答辩稿](/10-assessments/04-capstone-defense)。
6. 准备带练或公开展示前，生成 [自动生成测评包](/10-assessments/06-generated-assessment-pack)。

### 第二次复习

如果你已经学过一遍，直接从 Capstone 开始。

答辩过程中卡住的地方，就是你下一轮最值得回补的地方。

### 带别人学习

如果你是讲师或带练者：

1. 先让学习者独立回答题目。
2. 再让他们指出对应代码和输出证据。
3. 最后让他们提出一个小改进任务。

不要一开始就公布答案。自测最重要的是暴露思考断点。

带练时可以让学习者用这个格式回答：

```text
我的判断：
我引用的代码或页面：
我引用的输出证据：
我仍然不确定：
```

这样讲师能很快判断：学习者是会背，还是已经能用证据说话。

### 准备 GitHub 公开分享

如果你准备公开仓库或写发布说明：

1. 先完成 Capstone。
2. 再生成测评包。
3. 把薄弱题目转成路线图 issue。
4. 用 release brief 或 launch pack 整理首发材料。

对应页面：

- [发布摘要生成器](/09-reference/09-release-brief)
- [自动生成路线图包](/08-publication/05-generated-roadmap-pack)
- [自动生成首发运营包](/08-publication/13-generated-launch-pack)

公开分享前，至少完成：

```text
系统地图自测：Level 3
Serving/Gateway 自测：Level 3
Eval/Finetune 自测：Level 3
Capstone：能讲 5 到 10 分钟
自动测评包：assessment_readiness 为 ready 或能解释 review 原因
```

## 如何回答才算扎实

一个扎实回答通常包含 4 个部分：

1. **概念边界**：这个对象属于哪一层，解决什么问题，不解决什么问题。
2. **代码位置**：当前仓库里哪个项目、哪个文件或哪条命令体现它。
3. **输出证据**：运行后应该看到什么 header、event、JSON、manifest 或报告。
4. **失败推理**：如果它坏了，可能出现什么状态码、错误、日志或测试失败。

例如，回答“为什么 request id 重要”时，不要只说“方便排查”。更好的回答是：

- request id 连接 gateway、inference、events 和 timeline
- 它能让一次失败请求从 response header 追到结构化事件
- 如果 request id 丢失，跨层排障会断线
- 当前测试和案例里都有 request id 相关路径

这就是从名词解释走向工程解释。

## 自测结果怎么回流

自测后不要只留下分数。更有价值的是把薄弱点转成下一步行动。

| 自测发现 | 下一步 |
| --- | --- |
| 系统边界说不清 | 回到项目学习总览和系统地图 |
| 请求路径说不清 | 做 Serving/Gateway 自测和请求失败案例 |
| Eval 判断说不清 | 做模型发布判断案例 |
| Finetune lineage 说不清 | 做训练产物复现案例 |
| 证据不会写 | 回到输出证据库和端到端证据包 |
| 公开展示讲不顺 | 回到 Capstone 和公开演示脚本 |

如果同一个问题反复卡住，它很适合变成 GitHub issue：补一页解释、补一个 lab、补一个案例或补一个 FAQ。

## 自测后的复盘模板

做完每组题后，建议写下：

```text
我最清楚的一层是：
我最容易混淆的一层是：
我能指出代码位置的问题是：
我能指出输出证据的问题是：
我目前只能背概念的问题是：
我下一步要回看的文档是：
我下一步要跑的命令是：
```

这份复盘会让学习不再停在“感觉会了”。

## 常见误区

### 误区一：自测就是背答案

不对。背答案只能证明你看过文档，不能证明你能排查、演示或改进系统。

### 误区二：命令跑通就不用自测

跑通命令只是 Level 2。公开分享时，更重要的是你能解释为什么这样跑、输出说明什么、失败时怎么查。

### 误区三：只做自己会的题

最值得做的是那些会卡住你的题。它们会直接暴露下一轮学习重点。

### 误区四：自测和贡献无关

恰好相反。好的 issue、PR 和 release note，都来自清楚的问题判断和证据说明。

### 误区五：Capstone 是最后才需要看的

可以提前看。Capstone 相当于整套项目的终局验收清单，越早知道终点，学习路径越清楚。
