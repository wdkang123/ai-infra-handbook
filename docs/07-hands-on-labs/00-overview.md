# 深度实战总览

这一组 lab 是为了把学习网站从“能读”推进到“能练”。

前面的章节会告诉你 AI Infra 有哪些层、每层为什么存在。  
这一组 lab 则要求你真的动手观察、修改、验证和复盘。

如果说前面的章节负责建立地图，那么 lab 负责训练动作。读者只有真正做过一次“观察现象、提出假设、运行命令、检查证据、写出结论”的循环，才会把 AI Infra 从概念变成工程直觉。

这里的 lab 不追求复杂，而追求闭环。每个 lab 都应该让你明确知道：

- 我在验证哪一层。
- 我用哪条命令触发行为。
- 我应该看哪些输出。
- 什么算通过。
- 什么情况说明还没理解。

## 使用方式

每个 lab 都按同一套结构组织：

- 学习目标
- 前置知识
- 代码入口
- 操作步骤
- 观察点
- 扩展任务
- 验收标准

## 高质量 Lab 的标准

这个学习站里的 lab 不应该只是“命令集合”。
一篇合格的 lab 至少要让读者完成四件事：

| 目标 | 读者应该留下什么 |
| --- | --- |
| 触发现象 | 能用命令稳定复现一次行为 |
| 观察证据 | 能指出 header、metrics、events、manifest 或 report 在哪里 |
| 解释原因 | 能说明这个现象属于哪一层、为什么这样设计 |
| 写出复盘 | 能把事实、判断、风险和下一步整理成一段文字 |

如果读者只是复制命令并看到 `200`，这个 lab 还没有完成。
真正完成的标志是：读者能离开命令，自己解释系统行为。

可以用这张质量检查表自检：

| 问题 | 好的回答应该包含 |
| --- | --- |
| 我触发了什么行为 | 具体请求、状态码、输出文件或事件 |
| 我看了哪些证据 | 至少两个证据面，例如 header + events |
| 我排除了什么误判 | 说明为什么不是另一层的问题 |
| 这个 lab 对应哪层系统 | serving、gateway、eval、finetune 或发布 |
| 如果放到生产会缺什么 | 真实后端、监控、权限、持久化、告警等差距 |

后续每个 lab 都应该朝这个标准靠齐。

建议你不要一次做完所有 lab。更好的节奏是：

1. 做一个 lab
2. 跑一次 `infra-check`
3. 对照 [示例输出与证据库](/13-output-gallery/00-overview) 看懂关键输出
4. 写下你观察到的系统行为
5. 再进入下一个 lab

## 做 lab 前的准备

开始前先确认三件事：

```bash
nvm use 22
PYTHON=.venv/bin/python make infra-dev-install
PYTHON=.venv/bin/python make infra-check
```

如果 `infra-check` 不通过，先不要进入具体 lab。因为 lab 的目标是训练系统行为，不是把时间消耗在基础环境上。

建议再准备一个记录文件，写下：

```text
今天做的 lab：
我预计观察的行为：
我预计会用到的命令：
我预计会看到的证据：
我完成后要回答的问题：
```

这个小准备会让 lab 更像工程练习，而不是照着命令复制。

## 做 Lab 时怎么记笔记

建议每个 lab 都写一份短复盘，而不是只保存终端历史。

可以使用这个结构：

```text
Lab 名称：
我触发的行为：
关键 request id / run id / export id：
我查看的证据：
我确认的事实：
我排除的误判：
我还不能确认：
如果进入生产还缺什么：
下一步改进：
```

这份笔记不需要很长，但它会逼你把“跑过了”变成“理解了”。
如果后续把项目放到 GitHub，这类复盘也可以演化成 issue、PR 描述或博客片段。

## Lab 列表

### Lab 1：Serving 可观测性

入口：[Serving 可观测性 Lab](/07-hands-on-labs/01-serving-observability-lab)

你会观察一次请求如何影响：

- `/v1/chat/completions`
- streaming SSE
- `/metrics`
- `x-request-id`
- engine adapter 错误语义

适合建立执行层直觉。

完成后你应该能说清：

- 为什么 `/health`、`/metrics`、`/events` 面向的是不同问题。
- 为什么 streaming 不是普通 JSON 响应的变体，而是一条事件流。
- 为什么 engine adapter 错误需要映射成结构化响应。
- 为什么 request id 是后续跨层排障的线索。

### Lab 2：Gateway 韧性

入口：[Gateway 韧性 Lab](/07-hands-on-labs/02-gateway-resilience-lab)

你会观察 gateway 如何处理：

- 鉴权失败
- 模型不存在
- 限流
- 下游 5xx
- fallback
- streaming error event
- cache 命中

适合建立治理层直觉。

完成后你应该能说清：

- 哪些失败在 gateway 入口就应该结束。
- 哪些失败需要继续查 upstream。
- fallback 成功为什么仍然值得记录。
- cache hit 为什么不能掩盖上游持续失败。
- streaming 已经开始后为什么不能随意切换 fallback。

### Lab 3：Eval 发布门禁

入口：[Eval 发布门禁 Lab](/07-hands-on-labs/03-eval-release-gate-lab)

你会把一次评测结果变成一个发布判断：

- 运行 benchmark
- 保存 run bundle
- 生成 comparison
- 设置 `min_delta`
- 避免不同 task 混比
- 复盘 history

适合建立质量闭环直觉。

完成后你应该能说清：

- run、compare、leaderboard 分别解决什么问题。
- sample analysis 为什么能补足总体分数。
- `min_delta` 和设置一致性为什么重要。
- release recommendation 为什么是建议而不是自动发布命令。

### Lab 4：Finetune 复现资产

入口：[Finetune 复现资产 Lab](/07-hands-on-labs/04-finetune-reproducibility-lab)

你会检查一次训练 run 是否留下足够资产：

- dataset summary
- training args
- metrics
- logs
- checkpoint
- artifacts manifest
- export manifest

适合建立训练工程资产直觉。

完成后你应该能说清：

- dataset summary 和 dataset registry 的区别。
- checkpoint index 为什么比目录名可靠。
- export manifest 如何追溯到 checkpoint 和 dataset。
- 训练产物进入 eval 前必须确认哪些来源信息。

### Lab 5：系统 Capstone

入口：[系统 Capstone 与验收 Rubric](/07-hands-on-labs/05-capstone-review-rubric)

你会把四层串起来，形成一份可以对外展示的系统解释：

- 执行层
- 治理层
- 质量层
- 训练层
- 失败路径
- 验收命令

适合在准备分享、写博客、做 GitHub README 前完成。

完成后你应该能说清：

- 四层系统如何连接。
- 一条成功路径如何被证据支撑。
- 一条失败路径如何被定位。
- 当前学习型实现和生产系统的差距。
- 如果继续推进，最值得补强哪一层。

### Lab 6：公开发布验收

入口：[公开发布验收 Lab](/07-hands-on-labs/06-public-release-readiness-lab)

你会从公开读者视角检查这个仓库是否已经准备好分享：

- 首页和 README 是否能说明定位
- 课程路线、两周计划、lab、自测是否互相连通
- 文档站是否能构建
- `infra-check`、`infra-smoke`、依赖安全审计是否通过
- 学习型边界是否写清楚

适合在上传 GitHub、配置 Pages、写公开介绍前完成。

完成后你应该能说清：

- 公开读者第一眼会看到什么。
- README、首页、学习路线和 lab 是否互相连通。
- public-check 覆盖了哪些风险。
- 还有哪些页面需要继续深化。

### 配套：示例输出与证据库

入口：[示例输出与证据库](/13-output-gallery/00-overview)

它不是一个额外 lab，而是每个 lab 后面的复盘工具：

- Serving / Gateway lab 后看 header、metrics、events 和 timeline
- Eval lab 后看 sample outputs、sample analysis、compare 和 leaderboard
- Finetune lab 后看 run manifest、checkpoint index、export manifest 和 registry report
- Capstone 前整理一份端到端复盘证据包

## Lab 难度和目标

| Lab | 难度 | 最核心训练 | 最容易忽略 |
| --- | --- | --- | --- |
| Serving 可观测性 | 入门 | 把请求和 metrics/events 对上 | 只看 body，不看事件 |
| Gateway 韧性 | 中等 | 区分入口失败、路由失败、上游失败 | fallback 成功也要复盘 |
| Eval 发布门禁 | 中等 | 从分数走向发布判断 | 忽略 sample analysis |
| Finetune 复现资产 | 中等 | 追踪训练 lineage | 只看 checkpoint |
| 系统 Capstone | 综合 | 把四层讲成一条故事 | 只讲概念，不展示证据 |
| 公开发布验收 | 综合 | 从读者视角检查项目 | 只看本地能不能跑 |

如果你做某个 lab 时觉得困难，不一定说明你不适合继续学。更可能是前置检查点还没有站稳。回到 [学习检查点](/00-overview/09-learning-checkpoints) 找对应薄弱处，会比硬做下去更有效。

## 推荐顺序

如果你是第一次做：

1. Lab 1
2. Lab 2
3. Lab 3
4. Lab 4
5. Lab 5
6. Lab 6
7. 示例输出与证据库

如果你已经有后端经验，但 AI Infra 经验不多：

1. Lab 2
2. Lab 1
3. Lab 3
4. Lab 5

如果你更关心模型迭代：

1. Lab 3
2. Lab 4
3. Lab 1
4. Lab 5
5. Lab 6

## 通用验收命令

每做完一个 lab，至少跑：

```bash
PYTHON=.venv/bin/python make infra-check
```

如果改到了跨服务链路，再跑：

```bash
PYTHON=.venv/bin/python make infra-smoke
```

这两个命令不是形式主义。它们能帮你确认：

- 文档没有断链
- 单元测试没有回退
- 四个项目的最小闭环仍然成立

如果你改了文档或准备公开分享，再跑：

```bash
PYTHON=.venv/bin/python make docs-quality
PYTHON=.venv/bin/python make public-check
```

`docs-quality` 更关注文档结构和链接；`public-check` 会把安全扫描、测试和站点构建一起跑一遍。公开仓库里，这两条命令是很有价值的护栏。

## 复盘模板

每做完一个 lab，可以用这个模板复盘：

```text
我今天改动或观察的是哪一层：

它的上游是谁：

它的下游是谁：

正常路径是什么：

失败路径是什么：

我用什么命令验证：

我看到哪些产物或指标变化：

如果要走向生产系统，下一步还缺什么：
```

真正的学习不只是“命令通过”，而是你能把这些问题回答清楚。

## 一份合格 lab 记录

可以用这个更具体的格式：

```text
Lab：

目标：

我运行的命令：

我看到的关键证据：
- header：
- events：
- metrics：
- JSON / manifest：

我确认了：

我还不能确认：

我遇到的失败：

我是怎么定位的：

下一步改进：
```

合格记录不需要很长，但必须有“我确认了”和“我还不能确认”。这能防止你把一次成功运行误认为完整理解。

## 常见误区

### 只追求跑完

跑完只是最低标准。Lab 的真正目标是让你能解释系统行为。

### 每个 lab 都从零开始

后面的 lab 会复用前面的证据意识。比如 Eval 发布门禁也需要你理解 run 的产物，Finetune 复现也会连接到后续 eval。

### 只记录成功路径

失败路径通常更能训练工程判断。特别是 Gateway 和 Eval，失败路径比成功路径更接近真实维护场景。

### 做完不写复盘

不写复盘，知识很容易留在短期记忆里。哪怕只写 5 行，也会让你下次更容易接上。

如果你做完 lab 后想进一步验收自己，可以进入 [学习自测总览](/10-assessments/00-overview)。  
那里会把系统地图、Serving、Gateway、Eval、Finetune 和 Capstone 拆成更具体的答题与演示任务。
