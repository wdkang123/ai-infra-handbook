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

## 2. 先准备到什么程度

你不需要已经做过 AI Infra，但最好先具备下面这些基础。

| 基础 | 最低要求 | 不熟怎么办 |
| --- | --- | --- |
| Python | 能执行 `python -m module` | 先照命令跑，不急着读完源码 |
| HTTP | 知道 request、response、status code | 重点观察 `curl -i` 的响应头和状态码 |
| 终端 | 会进入目录、执行命令、看报错 | 把报错和当前目录一起记录下来 |
| 大模型 API | 知道 chat completion 的输入输出 | 先把它当成一个 HTTP 接口 |

如果这些基础都不稳，也可以开始。只是第一轮目标要更小：先跑通，不追求解释每一行代码。

## 3. 第一轮只走主线

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

## 4. 第一天怎么走

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

## 5. 第二轮才开始分模块深入

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

## 6. 什么时候算从 0 到 1 完成

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

## 7. 卡住时怎么处理

先判断卡在哪一类：

| 卡点 | 先看哪里 | 先做什么 |
| --- | --- | --- |
| 命令跑不起来 | [常见排障手册](/09-reference/04-troubleshooting) | 记录当前目录、命令、完整报错 |
| 不知道该跑什么 | [命令速查](/09-reference/01-command-cheatsheet) | 只选当前模块的一条命令 |
| 不知道产物在哪 | [产物与文件索引](/09-reference/03-artifacts-and-files) | 找到最新生成的 JSON 或 Markdown |
| 不知道改完测什么 | [验证矩阵](/09-reference/07-validation-matrix) | 先跑最小相关检查 |
| 概念和代码对不上 | [概念到代码索引](/09-reference/02-concept-to-code-index) | 从入口文件往下读 |

第一轮最常见的误区是急着“把所有东西都懂完”。这里更推荐你先把路径走通，再回来补细节。

## 8. 下一步

如果你准备正式开始，按这个顺序打开：

1. [什么是 AI Infra](/00-overview/01-what-is-ai-infra)
2. [学习路线图](/00-overview/02-learning-route)
3. [最小运行手册](/00-overview/03-runbook)
4. [第一次实操演练](/00-overview/04-first-walkthrough)
5. [示例输出与证据库](/13-output-gallery/00-overview)
6. [学习者工作簿](/14-workshop-kit/02-learner-workbook)
7. [两周学习计划](/00-overview/15-two-week-learning-plan)
