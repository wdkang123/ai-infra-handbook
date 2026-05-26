# 示例输出与证据库总览

## 这一章解决什么问题

前面的章节已经讲了怎么跑服务、怎么做 lab、怎么读案例。

但一个公开学习网站还需要回答另一个很实际的问题：

> 我跑完命令以后，应该看到什么？这些输出说明了什么？哪些证据可以拿去复盘和分享？

这一章就是把命令输出、HTTP header、JSON 产物、Markdown 报告、事件 timeline、训练 manifest 集中整理成一组证据库。

它不是为了替代实操，而是让读者在实操后能更快判断：

- 我现在跑对了吗
- 这个输出属于哪一层
- 它能证明什么
- 它不能证明什么
- 如果失败，下一步应该找哪个证据
- 公开分享时应该展示哪些材料

## 为什么需要证据库

AI Infra 学习很容易卡在两个极端：

| 极端 | 表现 | 问题 |
| --- | --- | --- |
| 只看概念 | 知道 gateway、eval、finetune 是什么 | 不知道本地系统里证据长什么样 |
| 只跑命令 | 看到一堆 JSON 和日志 | 不知道这些输出和系统设计有什么关系 |

证据库要把这两件事接起来。

你可以把每个输出都当成一个工程证据：

| 输出 | 它证明什么 | 它不证明什么 |
| --- | --- | --- |
| `/health` | 服务是否启动、依赖是否可探测 | 模型质量好不好 |
| `/metrics` | 请求和 token 计数是否在变化 | latency 是否生产可用 |
| `/events/requests/{id}` | 一条请求经过了哪些阶段 | 所有历史请求都永久保存 |
| `sample_outputs.json` | 具体样本如何被打分 | 评测覆盖了真实业务 |
| `comparison_index.json` | 多次 comparison 的 verdict 分布 | 可以直接生产发布 |
| `checkpoint_index.json` | checkpoint 文件和 hash 是否可追踪 | 训练质量是否足够 |
| `export_manifest.json` | 导出资产从哪里来 | adapter 能否上线服务 |

证据不是装饰，它是学习、排障、发布判断和公开分享的共同语言。

## 证据质量分级

不是所有输出都同样有用。
可以按这四档判断证据质量：

| 档位 | 表现 | 是否适合公开复盘 |
| --- | --- | --- |
| 截图式证据 | 只有一张成功截图或一句“跑通了” | 不够 |
| 字段式证据 | 摘出了 status、header、metrics、artifact 路径 | 勉强可用 |
| 解释式证据 | 说明字段属于哪一层、能证明什么、不能证明什么 | 推荐 |
| 链路式证据 | 能把请求、事件、评测、训练产物或发布检查串起来 | 最好 |

公开学习站应尽量追求解释式和链路式证据。
这会让读者看到工程判断，而不是只看到运行结果。

## 证据库和普通日志有什么不同

普通日志通常是过程记录，可能很碎。

证据库更强调结构化理解：

- 这个输出属于哪一层
- 哪个字段最重要
- 哪个字段只能说明局部事实
- 哪个字段能和其他证据串起来
- 哪些输出适合放进 PR、release notes 或案例复盘

例如，一个 `x-request-id` 本身只是 header；但当它能连接 gateway response、gateway events、inference events 和 request timeline 时，它就变成了排障证据链的主线。

## 这一章怎么读

如果你还没跑过项目，先按下面顺序：

1. [从 0 到 1 学习路径](/00-overview/00-zero-to-one)
2. [最小运行手册](/00-overview/03-runbook)
3. [第一次实操演练](/00-overview/04-first-walkthrough)

如果你已经跑过一轮，可以按证据类型读：

| 你想看什么 | 读哪一页 |
| --- | --- |
| HTTP 响应、header、metrics、events | [Serving 与 Gateway 输出证据](/13-output-gallery/01-serving-gateway-evidence) |
| eval run、compare、leaderboard、sample analysis | [Eval 报告证据](/13-output-gallery/02-eval-report-evidence) |
| train、checkpoint、export、dataset registry | [Finetune 产物证据](/13-output-gallery/03-finetune-artifact-evidence) |
| 如何整理成一次可分享复盘 | [端到端复盘证据包](/13-output-gallery/04-end-to-end-review-packet) |
| 失败时按症状找证据 | [失败症状到证据地图](/13-output-gallery/05-failure-evidence-map) |
| 如何做公开演示 | [公开演示脚本](/13-output-gallery/06-public-demo-script) |
| 如何从 smoke 产物自动汇总证据 | [自动生成证据包](/13-output-gallery/07-generated-evidence-packet) |

## 证据应该怎么命名

公开分享时，不要只贴一段“命令成功了”。

更好的做法是把证据写成：

```text
层级：
命令：
关键输出：
我从输出里确认了：
我还不能确认：
下一步验证：
```

例如：

```text
层级：gateway 治理层
命令：curl -i /v1/chat/completions
关键输出：x-request-id、x-upstream-model、x-cache
我从输出里确认了：请求经过 gateway，路由到了 vllm-local，并且本次没有命中缓存
我还不能确认：真实模型质量、生产级 fallback 策略
下一步验证：查 /events/requests/{request_id}
```

这会让学习者从“跑通”进入“会解释”。

## 按系统层看证据

| 系统层 | 主要证据 | 典型问题 |
| --- | --- | --- |
| Serving | `/v1/models`、completion、usage、metrics、events | 模型服务是否处理了请求 |
| Gateway | status、headers、fallback/cache metrics、failure events | 请求是否被正确治理 |
| Eval | run、sample outputs、compare、leaderboard、recommendation | 输出质量是否可判断 |
| Finetune | dataset registry、run state、checkpoint index、export manifest | 训练资产是否可复现 |
| Publication | public-check、Actions、Pages 200、release notes | 公开发布是否可信 |

这张表可以帮助你在看到输出后先判断它属于哪一层。

## 按使用场景看证据

### 自学复盘

最少保留：

- 跑过的命令
- 关键输出
- 一个 request id
- 一个 eval 或 finetune 产物
- 一个卡点

### PR 说明

最少保留：

- 改动范围
- 验证命令
- 关键输出摘要
- 是否影响文档/脚本/API/CLI
- 是否通过 public-check

PR 里可以直接使用这个证据块：

```text
Evidence:
- scope: docs + eval lab
- validation: PYTHON=.venv/bin/python make docs-quality
- build: npm run docs:build
- key artifacts: results/lab_compare.json, results/lab_compare.md
- checked risk: no secrets, no private endpoint, no personal path
- remaining boundary: learning scaffold, not production eval platform
```

### 公开演示

最少展示：

- 系统地图
- 一条请求证据链
- 一份 eval compare
- 一份 finetune lineage
- 一次 public-check 或 Actions 结果

### Release notes

最少说明：

- 新增学习价值
- 影响哪些入口
- 跑过哪些验证
- 当前仍然不是生产平台
- 下一步路线图

## 公开分享前的脱敏规则

证据越完整，越要注意公开边界。
发布到 GitHub、博客、社交媒体或演示材料前，先检查：

| 风险 | 处理方式 |
| --- | --- |
| API key、token、cookie | 直接删除，不要只打码前几位 |
| 私有 endpoint、内网域名 | 改成 `http://localhost:8000` 或示例域名 |
| 个人本机路径 | 改成 `/path/to/ai-infra` |
| 公司内部模型名或数据集名 | 改成公开模型名或合成名称 |
| 用户输入样本 | 确认没有个人信息、业务数据或聊天记录 |
| 截图 | 检查浏览器地址栏、终端 prompt、账号信息 |
| 生成式图片 | 不要暗示真实公司或开源项目官方背书 |

脱敏的目标不是把内容删空，而是在保留学习价值的同时移除个人和私有信息。

## 和案例复盘的关系

[案例复盘](/11-case-studies/00-overview) 更像完整故事：

- 某个请求失败了，怎么排查
- 某个模型能不能发布，怎么判断
- 某个训练产物能不能复现，怎么追溯

本章更像证据词典：

- 每类输出长什么样
- 应该看哪个字段
- 字段能说明什么
- 字段不能说明什么

两者可以配合使用：

1. 先用本章看懂证据。
2. 再用案例章节把证据串成故事。
3. 最后用 [Capstone 答辩稿](/10-assessments/04-capstone-defense) 讲给别人听。

## 推荐完成标准

读完这一章后，你应该能做到：

- 看到 gateway header，能解释请求经过了哪层
- 看到 event timeline，能解释一次请求的生命周期
- 看到 eval sample analysis，能解释分数背后的样本问题
- 看到 finetune manifest，能追溯 dataset、run、checkpoint、export
- 能运行证据包生成器，把 smoke 产物汇总成 JSON / Markdown
- 失败时能先找证据，而不是直接猜原因
- 分享项目时能整理一份证据包，而不是只展示目录结构

## 证据复盘模板

每次跑完一个 lab，可以写：

```text
我跑的命令：
我得到的关键输出：
这个输出属于哪一层：
它能证明：
它不能证明：
我还需要补充的证据：
我下一步要看的页面：
```

这份模板可以直接放进 [学习者工作簿](/14-workshop-kit/02-learner-workbook)。

## 常见误区

### 只贴成功截图

截图能证明你运行过，但不能证明你理解了字段含义。

### 把 metrics 当成质量判断

Metrics 说明系统行为，不直接说明回答质量。

### 把 eval 分数当成发布结论

分数只是证据之一，还要看 compare、sample、observability 和风险。

### 把 manifest 当成普通文件清单

Manifest 的价值是 lineage 和复现，不只是列出路径。

### 失败时先猜原因

更好的方式是先找 status、headers、events、metrics、manifest 或 report。

## 下一步

建议先看：

1. [Serving 与 Gateway 输出证据](/13-output-gallery/01-serving-gateway-evidence)
2. [Eval 报告证据](/13-output-gallery/02-eval-report-evidence)
3. [Finetune 产物证据](/13-output-gallery/03-finetune-artifact-evidence)
4. [自动生成证据包](/13-output-gallery/07-generated-evidence-packet)
