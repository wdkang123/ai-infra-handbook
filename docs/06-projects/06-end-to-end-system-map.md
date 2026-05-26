# 四个项目怎么连成系统

这个仓库不是四个彼此独立的 demo。

它更像一张最小 AI Infra 系统图：

- `inference-service` 负责模型服务执行。
- `ai-gateway` 负责平台入口治理。
- `eval-module` 负责质量判断和发布门禁。
- `finetune-demo` 负责训练资产和导出 lineage。

单看每个项目，你能知道“它自己干什么”。
但真正重要的是看它们合起来表达了什么系统。

## 最小系统地图

可以先用这张图理解：

```text
应用 / 调用方
  -> ai-gateway
     -> inference-service
        -> model backend

eval-module
  -> 评测 gateway 或 inference 的模型入口
  -> 生成 run / compare / leaderboard / release recommendation

finetune-demo
  -> 生成 dataset / run / checkpoint / export 资产
  -> 后续进入 eval-module 做质量判断
```

不是每个线上请求都会经过全部模块。
但这四个模块合起来，覆盖了 AI Infra 学习里最关键的四种能力：

- 服务
- 治理
- 评测
- 训练迭代

## 四层分别回答什么问题

| 层 | 项目 | 主要问题 |
| --- | --- | --- |
| 执行层 | `inference-service` | 模型请求怎么执行，普通响应和 streaming 怎么产出 |
| 治理层 | `ai-gateway` | 谁能调用，请求去哪里，失败后怎么治理 |
| 质量层 | `eval-module` | 结果怎么评测、比较、进入发布判断 |
| 训练资产层 | `finetune-demo` | 数据、run、checkpoint、export 如何追踪 |

这四层是学习坐标轴。
以后你看到新功能时，可以先问：它属于哪一层？

## 一条用户请求怎么走

用户请求通常走：

```text
client
  -> ai-gateway
  -> inference-service
  -> engine/backend
  -> inference-service
  -> ai-gateway
  -> client
```

其中：

- gateway 负责 auth、routing、rate limit、cache、fallback、request id。
- inference-service 负责模型校验、engine 调用、usage、streaming、执行层 events。
- 两层都暴露 health、metrics 和 request timeline。

如果请求失败，排查顺序通常是：

1. 从响应 header 拿 `x-request-id`。
2. 看 gateway timeline。
3. 看 inference timeline。
4. 对照 `/events/failures` 和 `/metrics`。
5. 判断是入口治理问题、上游问题，还是执行层问题。

这就是系统地图在排障里的价值。

## 一次模型发布怎么走

模型发布不是只看“模型能返回文本”。
更合理的路径是：

```text
candidate model / export
  -> eval run
  -> sample outputs / sample analysis
  -> compare with baseline
  -> release recommendation
  -> gateway route / canary
  -> production observability
```

这里 `eval-module` 是发布判断的中心：

- run 记录候选模型表现。
- compare 记录相对 baseline 的变化。
- leaderboard 展示历史表现。
- comparison index 记录发布判断历史。

gateway 则决定真实调用入口是否切换、canary 或 fallback。
inference-service 提供执行层 usage、events 和 metrics。
这三层必须一起看。

## 一次微调资产怎么走

微调路径更像：

```text
dataset
  -> finetune run
  -> checkpoint index
  -> export manifest
  -> eval run
  -> compare
  -> release decision
```

`finetune-demo` 不负责判断“模型是不是更好”。
它负责留下训练资产证据。

`eval-module` 不负责训练。
它负责判断训练产物是否值得进入下一步。

gateway 不负责训练或评测。
它负责把发布后的模型能力变成稳定平台入口。

这就是为什么训练、评测、网关不能混成一个脚本。

## 四层之间的关键连接点

| 连接 | 关键对象 |
| --- | --- |
| Gateway -> Inference | `x-request-id`、model routing、upstream model、streaming |
| Inference -> Eval | OpenAI-compatible API、model name、usage、sample outputs |
| Finetune -> Eval | export manifest、adapter hash、dataset id/version |
| Eval -> Gateway | release recommendation、candidate model、route/canary 决策 |
| Smoke -> 全链路 | serving snapshots、eval artifacts、finetune artifacts、evidence packet |

连接点比单个项目更重要。
真实系统的问题经常发生在连接处，而不是单个模块内部。

## 当前仓库为什么不用更多项目

真实世界当然还有更多系统：

- prompt registry
- feature store
- model registry
- vector database
- tracing backend
- dashboard
- deployment controller
- billing system
- policy engine

但学习阶段如果一开始全加进来，主线会散。

当前四个项目已经能表达最重要的闭环：

```text
serve -> govern -> evaluate -> improve -> serve again
```

等这条主线稳定，再加更多项目才不容易迷路。

## 怎么把文档和系统地图一起读

推荐顺序：

1. 读基础概念：Token、Context、Prefill、TTFT。
2. 回到 `inference-service` 看执行层。
3. 读 Gateway：auth、routing、rate limit、fallback。
4. 回到 `ai-gateway` 看治理层。
5. 读 Eval：run、compare、leaderboard、production quality。
6. 回到 `eval-module` 看质量层。
7. 读 Finetune：LoRA、artifact、history、when to finetune。
8. 回到 `finetune-demo` 看训练资产层。
9. 最后看 case studies，把四层串起来。

这个顺序不是唯一的，但非常适合第一次系统学习。

## 一个改动应该怎么定位

当你准备改代码或文档时，可以先问：

| 问题 | 可能层 |
| --- | --- |
| 请求怎么生成结果？ | inference-service |
| 请求为什么被拒绝或路由？ | ai-gateway |
| 模型是否比 baseline 好？ | eval-module |
| 训练产物从哪里来？ | finetune-demo |
| 哪条请求失败了？ | gateway + inference |
| 发布能不能过？ | eval + gateway |
| 训练产物能不能发布？ | finetune + eval |
| 公开前是否安全？ | scripts + docs + root checks |

这能帮助你避免把所有问题都塞到一个项目里。

## 常见误区

### “四个项目就是四个 demo”

不是。
它们是四种系统能力的最小表达。

### “Eval 只在训练后才需要”

不对。
评测也可以评估 prompt、serving backend、gateway route 和模型发布。

### “Gateway 和 inference 都有 API，所以边界不重要”

边界很重要。
一个是入口治理层，一个是推理执行层。

### “Finetune 产物生成了就算完成”

不够。
训练产物必须进入 eval 和 release decision。

### “Smoke 只是测试脚本”

不只是。
它是四层最小闭环是否仍然能跑的证据来源。

## 学完应该能回答

读完这一页后，你应该能回答：

1. 四个项目分别属于哪一层？
2. 一条用户请求如何穿过 gateway 和 inference？
3. 一个模型候选如何进入 eval 和 release decision？
4. 一个微调 export 如何追溯到 dataset 和 checkpoint？
5. 为什么真实系统问题经常发生在层与层的连接处？

## 继续阅读

- [文档与项目怎么联动](/06-projects/05-docs-and-projects-map)
- [质量与维护入口](/06-projects/07-quality-and-maintenance)
- [案例复盘总览](/11-case-studies/00-overview)
- [生产迁移路线总览](/12-production-migration/00-overview)
