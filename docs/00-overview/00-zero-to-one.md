# 从 0 到 1 学习路径

## 1. 这页适合谁

如果你是第一次系统学习 AI Infra，不要先打开所有目录。

这页只解决一个问题：怎么从完全没跑过这个仓库，走到能独立讲清楚并跑通一条最小 AI Infra 闭环。

你最终要完成的不是“看完所有文章”，而是这 6 件事：

1. 说清楚 AI Infra 为什么要分成执行层、治理层、质量层、训练层
2. 在本地打开文档站
3. 跑通四个项目的最小验证
4. 完成一次请求、评测、训练、导出的实操链路
5. 能看懂关键输出证据，并整理一次复盘
6. 如果要分享给别人，能用工作簿、议程和模板组织一次共学

这里的“从 0 到 1”不是指把所有生产系统能力都做完。它更像给你建立一个可继续扩展的学习地基：你知道系统分层，知道每层的最小接口，知道出问题时先看哪类证据，也知道当前学习型实现和真实生产系统之间还差什么。

如果你以前只接触过调用大模型 API，这页会把你带到“平台和基础设施”的视角。你会开始关心：请求进入平台后谁负责鉴权，模型名为什么需要映射，评测结果为什么要进入发布判断，训练产物为什么必须可追溯。这些问题听起来没有“调 prompt”直观，但它们正是 AI Infra 的工程核心。

## 2. 先准备到什么程度

你不需要已经做过 AI Infra，但最好先具备下面这些基础。

| 基础 | 最低要求 | 不熟怎么办 |
| --- | --- | --- |
| Python | 能执行 `python -m module` | 先照命令跑，不急着读完源码 |
| HTTP | 知道 request、response、status code | 重点观察 `curl -i` 的响应头和状态码 |
| 终端 | 会进入目录、执行命令、看报错 | 把报错和当前目录一起记录下来 |
| 大模型 API | 知道 chat completion 的输入输出 | 先把它当成一个 HTTP 接口 |

如果这些基础都不稳，也可以开始。只是第一轮目标要更小：先跑通，不追求解释每一行代码。

## 3. 先建立正确预期

第一轮学习最容易被两种期待带偏。

第一种期待是“我应该马上接真实模型、真实 GPU、真实线上流量”。这会让你在环境、成本和复杂度里消耗太多精力，反而看不清系统边界。

第二种期待是“既然是学习项目，那代码只要能跑就行”。这也不够。学习项目可以不是生产平台，但它应该保留真实系统最关键的骨架：接口、错误路径、观测、测试、产物、history、manifest 和发布判断。

所以第一轮的标准应该是：

- 不追求生产规模，但追求边界清晰。
- 不追求真实模型效果，但追求请求链路可观察。
- 不追求完整训练框架，但追求训练资产可复盘。
- 不追求完美 benchmark，但追求评测判断可解释。
- 不追求看完所有页面，但追求能讲清一条端到端故事。

带着这个预期学习，你会更容易理解为什么仓库里既有文档站，也有四个小项目，还有一组检查脚本、证据包和共学模板。

## 4. 第一轮只走主线

第一轮学习按这个顺序走，不要中途跳去读所有参考页。

| 阶段 | 目标 | 入口 | 完成标志 |
| --- | --- | --- | --- |
| 0 | 建立系统地图 | [什么是 AI Infra](/00-overview/01-what-is-ai-infra) | 能说出四层分别负责什么 |
| 1 | 确认本地环境 | [最小运行手册](/00-overview/03-runbook) | `infra-check` 能跑起来 |
| 2 | 跑通第一次实操 | [第一次实操演练](/00-overview/04-first-walkthrough) | 四个项目都留下了可观察产物 |
| 3 | 回头看代码入口 | [文档与代码怎么对应](/00-overview/05-docs-to-code-map) | 能找到每个项目入口文件 |
| 4 | 做阶段自测 | [学习自测总览](/10-assessments/00-overview) | 能答出系统地图和 Serving/Gateway 基础题 |
| 5 | 做一组 Lab | [深度实战总览](/07-hands-on-labs/00-overview) | 能按任务观察、修改、验证 |
| 6 | 整理输出证据 | [示例输出与证据库](/13-output-gallery/00-overview) | 能解释 header、events、sample analysis 和 manifest |
| 7 | 整理学习记录 | [学习者工作簿](/14-workshop-kit/02-learner-workbook) | 能把命令、证据和卡点写成复盘 |
| 8 | 做最终复盘 | [系统 Capstone 与验收 Rubric](/07-hands-on-labs/05-capstone-review-rubric) | 能讲 5 分钟系统故事 |

这张表看起来像路线图，但真正要养成的是一个循环：

```text
读一页 -> 跑一条命令 -> 看一份证据 -> 回到一处代码 -> 写三句复盘
```

如果只读页面，你会觉得内容很多但不扎实。
如果只跑命令，你会得到一堆成功输出但不知道它们说明什么。
如果只看代码，你很容易把学习变成“源码漫游”。

把这五步连起来，学习就会变成可验证的工程过程。

## 5. 第一天怎么走

如果你今天只有 60 到 90 分钟，按下面节奏来。

### 先打开学习站

```bash
nvm use
npm install
npm run docs:dev
```

然后打开：

- [http://localhost:5173](http://localhost:5173)

### 再做最小验证

```bash
cd /path/to/ai-infra
PYTHON=.venv/bin/python make infra-test
PYTHON=.venv/bin/python make infra-smoke
```

这一步先不要纠结每个测试内部做了什么。你只需要确认：这个仓库的最小学习链路可以在你机器上跑起来。

### 最后写一个 5 行复盘

```text
今天我跑通了：
我看到的服务地址：
我看到的输出产物：
我还没理解的问题：
下一页要读：
```

这份复盘很重要。AI Infra 很容易变成“看了很多名词，但不知道自己学会了什么”。每天留一小段证据，会让学习路线稳很多。

### 第一天不要做什么

第一天建议克制一点，不要马上做这些事：

- 不要一上来就改大量代码。
- 不要同时打开所有模块。
- 不要急着接真实 API key 或线上模型。
- 不要因为一个概念没完全懂就停在原地。
- 不要把 `make infra-smoke` 的成功理解成“我已经掌握了系统”。

第一天的真正目标是建立信心和坐标：项目能跑起来，你知道主入口在哪里，也知道后面应该继续看哪些证据。

## 6. 第二轮才开始分模块深入

第一轮跑通之后，再按模块深入。

| 模块 | 你要回答的问题 | 建议入口 |
| --- | --- | --- |
| LLM 基础 | 请求为什么会变成 token 输出 | [LLM Fundamentals 总览](/01-llm-fundamentals/00-overview) |
| 推理服务 | 模型服务本体最小需要什么 | [inference-service](/06-projects/01-inference-service) |
| 平台治理 | gateway 为什么不是普通代理 | [ai-gateway](/06-projects/02-ai-gateway) |
| 评测观测 | 分数如何变成发布判断 | [eval-module](/06-projects/03-eval-module) |
| 训练资产 | 训练为什么要留下 manifest 和 history | [finetune-demo](/06-projects/04-finetune-demo) |

每个模块都按同一个节奏学：

1. 读一页概念
2. 跑一条命令
3. 看一个输出产物
4. 找到对应代码入口
5. 改一个很小的地方
6. 重新跑验证

### 每个模块都要留下一个“可讲述成果”

为了避免学习变成散点，建议每个模块都留下一个小成果。

| 模块 | 可讲述成果 | 为什么有用 |
| --- | --- | --- |
| LLM 基础 | 一张请求生命周期图 | 帮你把 token、context、TTFT 放进同一条链 |
| 推理服务 | 一次普通请求和一次 streaming 证据 | 帮你理解接口形状和输出方式 |
| Gateway | 一次成功请求、一条失败路径、一条 fallback/cache 证据 | 帮你理解平台治理不是普通代理 |
| Eval | 一次 run、一次 compare、一次 release recommendation | 帮你理解质量判断不只是分数 |
| Finetune | 一次 run manifest、checkpoint index、export manifest | 帮你理解训练是资产链路 |
| Capstone | 一份端到端复盘 | 帮你把所有模块串成完整故事 |

这些成果不一定要写成正式文章，可以先写进 [学习者工作簿](/14-workshop-kit/02-learner-workbook)。等你准备公开分享时，它们会自然变成 README、博客、issue 或演示稿的素材。

## 7. 怎么判断自己是在“真学”

真学不是感觉很努力，而是你能不断把模糊问题变成可验证问题。

下面是一些信号。

| 状态 | 看起来像 | 更好的下一步 |
| --- | --- | --- |
| 只停在概念 | “我知道 gateway 是网关” | 解释一次请求为什么要先经过 gateway |
| 只停在命令 | “这个命令通过了” | 打开输出 JSON 或 events 说明它验证了什么 |
| 只停在源码 | “我看了 server.py” | 说出哪个路由对应哪个输出证据 |
| 只停在结果 | “分数提升了” | 解释 baseline/candidate 是否可比 |
| 只停在训练 | “checkpoint 生成了” | 追溯 export manifest 到 dataset version |

每次学习结束时，都可以问自己三个问题：

1. 我今天确认了什么？
2. 我今天还不能确认什么？
3. 下一次我会用哪条命令或哪份证据继续确认？

如果这三个问题能答出来，哪怕只学了一页，也比泛泛看十页更扎实。

## 8. 什么时候算从 0 到 1 完成

不要用“我看完了多少页”衡量。用下面这张表判断。

| 能力 | 合格标准 | 自测入口 |
| --- | --- | --- |
| 系统地图 | 能解释四个项目为什么分层 | [系统地图自测](/10-assessments/01-system-map-check) |
| 请求链路 | 能解释 gateway 到 inference 的正常路径和失败路径 | [Serving 与 Gateway 自测](/10-assessments/02-serving-gateway-quiz) |
| 质量闭环 | 能解释 run、compare、leaderboard 的区别 | [Eval 与 Finetune 自测](/10-assessments/03-eval-finetune-quiz) |
| 训练资产 | 能从 export 追溯到 checkpoint、run、dataset | [Eval 与 Finetune 自测](/10-assessments/03-eval-finetune-quiz) |
| 工程复盘 | 能讲清楚一次变更该怎么验证 | [Capstone 答辩稿](/10-assessments/04-capstone-defense) |
| 输出证据 | 能把 header、events、JSON 和 manifest 串成证据包 | [示例输出与证据库](/13-output-gallery/00-overview) |
| 共学分享 | 能把学习过程组织成工作簿、议程和评审模板 | [共学与公开分享套件](/14-workshop-kit/00-overview) |

如果这些都能做到，你就已经完成这个仓库意义上的“从 0 到 1”：不是变成专家，而是已经建立了能继续自学和扩展的工程骨架。

## 9. 卡住时怎么处理

先判断卡在哪一类：

| 卡点 | 先看哪里 | 先做什么 |
| --- | --- | --- |
| 命令跑不起来 | [常见排障手册](/09-reference/04-troubleshooting) | 记录当前目录、命令、完整报错 |
| 不知道该跑什么 | [命令速查](/09-reference/01-command-cheatsheet) | 只选当前模块的一条命令 |
| 不知道产物在哪 | [产物与文件索引](/09-reference/03-artifacts-and-files) | 找到最新生成的 JSON 或 Markdown |
| 不知道改完测什么 | [验证矩阵](/09-reference/07-validation-matrix) | 先跑最小相关检查 |
| 概念和代码对不上 | [概念到代码索引](/09-reference/02-concept-to-code-index) | 从入口文件往下读 |

第一轮最常见的误区是急着“把所有东西都懂完”。这里更推荐你先把路径走通，再回来补细节。

### 卡住时的记录方式

不要只记录“报错了”。建议记录成下面这种格式：

```text
我正在做的任务：
我执行的命令：
我所在目录：
我预期看到：
我实际看到：
我已经确认：
我还没确认：
下一步准备看：
```

这个格式看起来多几行，但它会大幅降低排障难度。很多问题不是因为错误复杂，而是因为缺少当前目录、命令、预期结果和实际结果。

## 10. 如果你准备公开分享

如果你后面想把这个项目分享给别人，第一轮学习时就可以顺手积累素材。

建议保留：

- 第一次启动文档站的截图或记录。
- `infra-check` / `infra-smoke` 的结果。
- 一条 gateway 请求的 request id 和 events。
- 一次 eval compare 的 recommendation。
- 一次 finetune export manifest 的 lineage。
- 一段你自己写的“当前项目不是生产平台，但为什么适合学习”的说明。

这些素材会让公开分享更可信。读者不只是看到你整理了一个目录，而是看到你能用证据说明这个学习项目确实跑过、检查过、复盘过。

## 11. 下一步

如果你准备正式开始，按这个顺序打开：

1. [什么是 AI Infra](/00-overview/01-what-is-ai-infra)
2. [学习路线图](/00-overview/02-learning-route)
3. [最小运行手册](/00-overview/03-runbook)
4. [第一次实操演练](/00-overview/04-first-walkthrough)
5. [示例输出与证据库](/13-output-gallery/00-overview)
6. [学习者工作簿](/14-workshop-kit/02-learner-workbook)
7. [两周学习计划](/00-overview/15-two-week-learning-plan)
