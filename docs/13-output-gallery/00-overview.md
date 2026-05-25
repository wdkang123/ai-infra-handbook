# 示例输出与证据库总览

## 这一章解决什么问题

前面的章节已经讲了怎么跑服务、怎么做 lab、怎么读案例。

但一个公开学习网站还需要回答另一个很实际的问题：

> 我跑完命令以后，应该看到什么？这些输出说明了什么？哪些证据可以拿去复盘和分享？

这一章就是把“命令输出、JSON 产物、Markdown 报告、事件 timeline、训练 manifest”集中整理成一组证据库。

它不是为了替代实操，而是让读者在实操后能更快判断：

- 我现在跑对了吗
- 这个输出属于哪一层
- 它能证明什么
- 它不能证明什么
- 如果失败，下一步应该找哪个证据

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

1. 先用本章看懂证据
2. 再用案例章节把证据串成故事
3. 最后用 [Capstone 答辩稿](/10-assessments/04-capstone-defense) 讲给别人听

## 推荐完成标准

读完这一章后，你应该能做到：

- 看到 gateway header，能解释请求经过了哪层
- 看到 event timeline，能解释一次请求的生命周期
- 看到 eval sample analysis，能解释分数背后的样本问题
- 看到 finetune manifest，能追溯 dataset、run、checkpoint、export
- 能运行证据包生成器，把 smoke 产物汇总成 JSON / Markdown
- 失败时能先找证据，而不是直接猜原因
- 分享项目时能整理一份“证据包”，而不是只展示目录结构

## 下一步

建议先看：

1. [Serving 与 Gateway 输出证据](/13-output-gallery/01-serving-gateway-evidence)
2. [Eval 报告证据](/13-output-gallery/02-eval-report-evidence)
3. [Finetune 产物证据](/13-output-gallery/03-finetune-artifact-evidence)
4. [自动生成证据包](/13-output-gallery/07-generated-evidence-packet)
