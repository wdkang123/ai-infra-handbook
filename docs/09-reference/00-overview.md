# 参考资料总览

这一组页面用于快速查找。

学习路径页面适合从头学，lab 适合动手练，参考资料适合在你卡住时直接定位：

- 我要跑哪个命令
- 这个概念对应哪个文件
- 某个输出文件是什么意思
- 某个错误应该先看哪里
- 跑完命令后哪些输出可以作为复盘证据
- 公开发布前还缺哪一步检查

参考资料不是替代教程，而是把教程、代码、命令和证据连接起来。

## 参考资料的正确心智模型

参考资料更像“地图索引”，不是第二套教程。

当你已经知道自己卡在哪一类问题时，它很有用：

- 卡在命令，就查命令速查。
- 卡在代码位置，就查概念到代码索引。
- 卡在输出含义，就查产物与文件索引。
- 卡在错误归因，就查排障手册。
- 卡在发布前跑什么，就查验证矩阵。

如果你还不知道自己卡在哪里，先回到学习路线或检查点。参考资料适合定位，不适合替代学习主线。

## 什么时候使用参考资料

### 第一次学习时

第一次学习不建议从这里开始。

更好的路径是：

1. [从 0 到 1 学习路径](/00-overview/00-zero-to-one)
2. [第一次实操演练](/00-overview/04-first-walkthrough)
3. [第一次跑完之后学什么](/00-overview/06-after-first-walkthrough)
4. 再回到参考资料查命令、文件和排障方式

如果一开始就看参考资料，很容易看到很多入口，但不知道它们为什么存在。

### 跑命令卡住时

优先看：

- [命令速查](/09-reference/01-command-cheatsheet)
- [验证矩阵](/09-reference/07-validation-matrix)
- [常见排障手册](/09-reference/04-troubleshooting)

这三页分别回答：

- 命令是什么
- 什么场景该跑什么
- 失败后先查哪里

建议记录这三项：

```text
我运行的命令：
我预期它验证：
我实际看到：
```

只记录命令本身不够。很多问题来自“命令跑了，但不知道它应该验证什么”。

### 看代码迷路时

优先看：

- [概念到代码索引](/09-reference/02-concept-to-code-index)
- [API Surface 速查](/09-reference/05-api-surface)
- [CLI Surface 速查](/09-reference/06-cli-surface)

这三页会把抽象概念拉回具体文件、接口和命令。

看代码时最好只带一个问题进去。比如“fallback 在哪里发生”，不要变成“我要读完整个 gateway 项目”。参考资料的作用是把问题缩小到 1 到 3 个入口文件。

### 看输出看不懂时

优先看：

- [产物与文件索引](/09-reference/03-artifacts-and-files)
- [示例输出与证据库](/13-output-gallery/00-overview)
- [端到端复盘证据包](/13-output-gallery/04-end-to-end-review-packet)

这三页会解释 JSON、Markdown、manifest、history、report 和 evidence packet 的意义。

输出文件的阅读顺序通常是：

```text
先看 summary
  -> 再看 manifest / index
  -> 再看样本或 timeline
  -> 最后看原始 JSONL / 详细事件
```

不要一开始就打开最长的原始文件。先用 summary 判断方向，再展开细节。

### 准备公开发布或共学时

优先看：

- [学习站清单生成器](/09-reference/08-learning-inventory)
- [发布摘要生成器](/09-reference/09-release-brief)
- [课程目录生成器](/09-reference/10-course-catalog)
- [自动生成共学包](/14-workshop-kit/07-generated-workshop-packet)
- [自动生成测评包](/10-assessments/06-generated-assessment-pack)
- [自动生成路线图包](/08-publication/05-generated-roadmap-pack)
- [自动生成首发运营包](/08-publication/13-generated-launch-pack)

这些页面帮助你把学习站从“内容集合”整理成可发布、可带练、可维护的公开项目。

公开前参考资料最重要的价值是复核一致性：README、首页、课程目录、共学包、测评包、证据包、release brief 和 launch pack 是否在讲同一套系统。

## 页面列表

| 页面 | 解决的问题 | 最适合的使用时机 |
| --- | --- | --- |
| [命令速查](/09-reference/01-command-cheatsheet) | 常用 make、pytest、脚本命令怎么跑 | 准备验证或复现实验 |
| [概念到代码索引](/09-reference/02-concept-to-code-index) | 概念对应哪些项目和文件 | 读文档后想看代码 |
| [产物与文件索引](/09-reference/03-artifacts-and-files) | 输出文件、manifest、history 是什么 | 跑完命令后解释结果 |
| [常见排障手册](/09-reference/04-troubleshooting) | 常见失败先查哪里 | 命令或服务失败时 |
| [API Surface 速查](/09-reference/05-api-surface) | HTTP 接口属于哪层、看哪些字段 | 调试 serving/gateway |
| [CLI Surface 速查](/09-reference/06-cli-surface) | eval/finetune/script CLI 怎么用 | 调试命令行工具 |
| [验证矩阵](/09-reference/07-validation-matrix) | 不同改动该跑哪些检查 | 开 PR 或发布前 |
| [学习站清单生成器](/09-reference/08-learning-inventory) | 文档站结构如何自动汇总 | 维护课程地图 |
| [发布摘要生成器](/09-reference/09-release-brief) | 发布前证据如何汇总 | 准备 release 或 PR 复盘 |
| [课程目录生成器](/09-reference/10-course-catalog) | 如何组织可带练课程 | 准备 workshop |
| [示例输出与证据库](/13-output-gallery/00-overview) | 输出证据如何解释 | 准备展示或复盘 |

## 速查路线

### 我只想确认本地是否健康

1. [命令速查](/09-reference/01-command-cheatsheet)
2. [验证矩阵](/09-reference/07-validation-matrix)
3. [常见排障手册](/09-reference/04-troubleshooting)

最小命令通常是：

```bash
PYTHON=.venv/bin/python make infra-check
```

### 我想解释一个 HTTP 请求

1. [API Surface 速查](/09-reference/05-api-surface)
2. [Serving 与 Gateway 输出证据](/13-output-gallery/01-serving-gateway-evidence)
3. [请求失败排查案例](/11-case-studies/01-request-incident-walkthrough)

重点不是背接口列表，而是能把 status、headers、events 和 metrics 串起来。

### 我想解释一次 eval

1. [CLI Surface 速查](/09-reference/06-cli-surface)
2. [产物与文件索引](/09-reference/03-artifacts-and-files)
3. [模型发布判断案例](/11-case-studies/02-model-release-decision-walkthrough)

重点是 run、sample analysis、compare、leaderboard 和 history 的关系。

### 我想解释一次 finetune

1. [产物与文件索引](/09-reference/03-artifacts-and-files)
2. [Finetune 产物证据](/13-output-gallery/03-finetune-artifact-evidence)
3. [训练产物复现案例](/11-case-studies/03-finetune-to-eval-asset-lineage)

重点是 dataset、checkpoint、manifest、export 和 history 的 lineage。

## 参考资料如何和项目配合

可以把参考资料理解成一张“系统索引网”：

```text
概念页
  -> 项目代码
  -> 命令
  -> 输出文件
  -> 验证矩阵
  -> 排障手册
  -> 证据库
```

例如你在读 Gateway：

1. 概念页告诉你为什么需要鉴权、路由、fallback。
2. API Surface 告诉你有哪些 HTTP 入口和 headers。
3. 命令速查告诉你怎么启动或检查。
4. 排障手册告诉你 `401 / 429 / 502` 怎么判断。
5. 输出证据库告诉你怎么把结果放进复盘。

这样读者不需要在文档和项目之间来回猜。

## 参考资料和生成包的关系

生成包页面也属于参考资料的一部分，但它们解决的是“自动汇总”问题：

| 生成包 | 汇总对象 | 最适合用途 |
| --- | --- | --- |
| learning inventory | 文档站结构 | 检查页面和路线是否完整 |
| course catalog | 课程模块 | 组织学习路线和 workshop |
| release brief | 发布证据 | 判断是否适合公开展示 |
| workshop packet | 共学活动 | 带练和学习小组 |
| assessment pack | 测评题与评分 | 验收学习效果 |
| roadmap pack | issue 种子 | 把薄弱点转成路线图 |
| launch pack | release notes 和首发任务 | GitHub 首发运营 |

这些生成包不是为了炫技，而是为了让公开学习项目可以持续维护。每次内容变厚，都可以重新生成这些包，看结构是否仍然一致。

## 推荐查找路径

### 我不知道下一步学什么

先看：

- [第一次跑完之后学什么](/00-overview/06-after-first-walkthrough)
- [选择你的学习路径](/00-overview/07-choose-your-path)
- [课程大纲](/00-overview/12-course-syllabus)

### 我知道概念，但不知道代码在哪

先看：

- [概念到代码索引](/09-reference/02-concept-to-code-index)
- [文档与代码怎么对应](/00-overview/05-docs-to-code-map)
- [项目学习总览](/06-projects/00-projects-overview)

### 我知道命令，但不知道输出什么意思

先看：

- [产物与文件索引](/09-reference/03-artifacts-and-files)
- [示例输出与证据库](/13-output-gallery/00-overview)
- [学习自测总览](/10-assessments/00-overview)

### 我准备提交改动

先看：

- [验证矩阵](/09-reference/07-validation-matrix)
- [贡献者协作手册](/14-workshop-kit/05-contribution-playbook)
- [GitHub 入口与协作地图](/08-publication/14-github-entrypoints)

### 我准备公开发布

先看：

- [公开仓库卫生检查](/08-publication/06-public-repo-hygiene)
- [GitHub Pages 发布](/08-publication/01-github-pages)
- [v0.1 首发发布手册](/08-publication/10-v0-1-release-playbook)
- [自动生成首发运营包](/08-publication/13-generated-launch-pack)

## 参考资料的维护原则

每个条目尽量包含：

- 入口命令或文件路径
- 它解决的问题
- 应该观察的结果
- 相关学习页面
- 需要跑的验证命令
- 常见失败和排查方向

如果新增了接口、CLI、输出文件、脚本或 workflow，也要同步考虑是否更新参考资料。

可以把维护动作写成一个小 checklist：

```text
我新增或修改了：
- 接口：
- CLI：
- 输出文件：
- workflow：
- 文档页面：

我需要同步检查：
- 命令速查：
- API / CLI Surface：
- 产物索引：
- 验证矩阵：
- 证据库：
- README 或首页：
```

这能避免“代码已经变了，但参考资料还在讲旧行为”。

## 公开分享时怎么用

如果你要把项目展示给别人，参考资料可以放在演示后半段：

1. 先讲系统地图。
2. 再跑一次核心命令。
3. 然后打开参考资料，说明读者卡住时怎么自助定位。
4. 最后打开证据库，说明输出如何复盘。

这样分享不只是“我演示成功了”，而是“你也知道失败时该怎么办”。

## 常见误区

### 误区一：参考资料越多越好

不一定。参考资料的价值不是数量，而是能否快速把问题定位到命令、代码、输出或验证路径。

### 误区二：参考资料可以不维护

一旦接口、命令或输出文件变化，参考资料如果不更新，会比没有更误导。

### 误区三：参考资料就是附录

在公开项目里，参考资料是读者自助学习和贡献的入口，不只是附录。

### 误区四：只给命令，不解释证据

命令只是动作，证据才是学习和复盘的材料。
