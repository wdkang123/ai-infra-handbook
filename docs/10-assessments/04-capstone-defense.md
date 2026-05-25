# Capstone 答辩稿

这页把最终验收整理成一场 30 分钟答辩。  
你可以自己录屏，也可以让别人按这页提问。

答辩目标不是炫技，而是证明你已经能把这套学习型 AI Infra 系统讲清楚。

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

## 演示脚本

你可以按这个顺序演示：

```bash
PYTHON=.venv/bin/python make infra-check
PYTHON=.venv/bin/python make infra-smoke
```

然后打开：

- [四个项目怎么连成系统](/06-projects/06-end-to-end-system-map)
- [命令速查](/09-reference/01-command-cheatsheet)
- [产物与文件索引](/09-reference/03-artifacts-and-files)
- [示例输出与证据库](/13-output-gallery/00-overview)
- [常见排障手册](/09-reference/04-troubleshooting)
- [生产迁移路线总览](/12-production-migration/00-overview)

最后展示一个你自己完成的 lab 复盘。

## Rubric

| 维度 | Level 1 | Level 2 | Level 3 | Level 4 |
| --- | --- | --- | --- | --- |
| 系统地图 | 能列出项目名 | 能说出四层职责 | 能解释上下游关系 | 能指出生产化差距 |
| 请求链路 | 能跑命令 | 能解释普通请求 | 能解释 streaming 和错误 | 能设计新的观测指标 |
| Gateway 治理 | 知道鉴权和路由 | 能触发常见错误 | 能解释 fallback/cache/限流 | 能提出风险控制方案 |
| Eval 判断 | 能运行 run | 能运行 compare | 能解释 min_delta 和 task 校验 | 能设计发布门禁 |
| Finetune 资产 | 能运行 train | 能运行 export | 能解释 checkpoint/export/manifest | 能设计 lineage 或版本策略 |
| 工程验证 | 会跑测试 | 知道每类测试作用 | 能定位失败原因 | 能补测试并说明覆盖面 |

建议公开展示时达到：

- 大部分维度 Level 3
- 至少一个维度 Level 4

## 答辩后复盘

答辩结束后写下：

```text
我讲得最清楚的是：
我讲得最模糊的是：
别人最容易问倒我的问题是：
我下一步要补的文档或代码是：
我会用什么命令验证：
```

这份复盘比答辩本身更重要。  
它会把“我感觉还可以”变成下一轮可执行的改进。
