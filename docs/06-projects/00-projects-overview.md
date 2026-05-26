# 项目学习总览

这套学习站不是只放文档，也不是只放几个孤立 demo。它的核心设计是：

> 用文档讲清楚概念，用项目保留可运行边界，用测试和输出证据证明这些边界真的存在。

当前最重要的 4 个项目分别对应 AI Infra 的 4 种能力：

1. `inference-service`：模型服务本体
2. `ai-gateway`：平台治理和代理层
3. `eval-module`：评测、对比和发布判断层
4. `finetune-demo`：训练、产物和能力迭代层

它们不是四个并列 demo，而是一条从请求到质量闭环的学习路径。

```text
inference-service
  -> ai-gateway
  -> eval-module
  -> finetune-demo
  -> back to eval and release decision
```

如果你把这四层关系看清楚，后面再接触更复杂的生产系统时，就不太容易把组件边界混在一起。

## 四个项目分别解决什么问题

### inference-service：模型怎么被服务出来

`inference-service` 代表模型服务本体。

它关心的是：

- 请求如何进入模型服务
- 模型列表如何暴露
- chat completion 如何返回
- streaming 如何表达
- metrics 如何记录
- engine error 如何映射
- request id 如何贯穿
- structured events 如何保留请求证据

它不追求真实 GPU 推理，而是先把 serving API 和观测边界讲清楚。

配套阅读：

- [Inference Serving](/02-inference-serving/00-overview)
- [inference-service 项目页](/06-projects/01-inference-service)

### ai-gateway：调用怎么被治理

`ai-gateway` 代表平台层。

它关心的是：

- 谁能调用
- 外部模型名如何映射到内部目标
- 请求如何路由
- 失败时是否 fallback
- 重复请求是否 cache
- 上游健康如何聚合
- streaming 代理如何处理
- metrics、events、failure summary 如何记录

它不执行模型，但它决定模型调用如何被组织和治理。

配套阅读：

- [AI Gateway Platform](/03-ai-gateway-platform/00-overview)
- [ai-gateway 项目页](/06-projects/02-ai-gateway)

### eval-module：结果怎么被判断

`eval-module` 代表质量判断层。

它关心的是：

- task 如何定义
- run 如何保存
- baseline 和 candidate 如何比较
- history 如何记录
- leaderboard 如何生成
- sample analysis 如何解释结果
- recommendation 如何进入发布判断

它的重点不是做一个华丽 dashboard，而是先把“可比较证据”变成稳定产物。

配套阅读：

- [Evaluation Observability](/04-evaluation-observability/00-overview)
- [eval-module 项目页](/06-projects/03-eval-module)

### finetune-demo：能力怎么被训练迭代

`finetune-demo` 代表训练与产物层。

它关心的是：

- dataset 如何校验和登记
- run 如何记录
- checkpoint 如何索引
- export 如何追踪来源
- history 如何保留
- 多次数据变化如何 diff
- 训练产物如何进入后续 eval

它不直接追求重训练，而是先让训练资产关系清楚。

配套阅读：

- [Finetuning Training](/05-finetuning-training/00-overview)
- [finetune-demo 项目页](/06-projects/04-finetune-demo)

## 推荐学习顺序

第一次系统学习，建议按下面顺序：

1. [inference-service](/06-projects/01-inference-service)
2. [ai-gateway](/06-projects/02-ai-gateway)
3. [eval-module](/06-projects/03-eval-module)
4. [finetune-demo](/06-projects/04-finetune-demo)

这个顺序对应的是：

1. 先看执行层
2. 再看治理层
3. 再看质量闭环
4. 最后看训练迭代

它不是唯一顺序，但对第一次接触这套仓库来说最稳。

如果你已经准备动手，优先从 [第一次实操演练](/00-overview/04-first-walkthrough) 进入。那条路径会把四个项目以最小成本串起来。

## 四个项目如何连成一个系统故事

可以用一个具体故事理解：

1. 用户发起一次 chat completion 请求。
2. Gateway 做鉴权、路由、cache 和 fallback。
3. Inference service 返回模型响应，并记录 metrics/events。
4. Eval module 用固定任务评测某个模型或配置。
5. Compare report 判断 candidate 是否优于 baseline。
6. Finetune demo 产生新的 export 产物。
7. 这个 export 再进入 eval，形成新的发布判断。

这就是一个最小 AI Infra 闭环：

```text
Serve
  -> Govern
  -> Observe
  -> Evaluate
  -> Train
  -> Evaluate again
  -> Release or reject
```

每个项目只做一部分，所以边界清楚；但它们加起来，能让你看到真实平台的骨架。

## 每个项目最适合解决哪类困惑

### 如果你最困惑的是“请求到底怎么产生结果”

先看 [inference-service](/06-projects/01-inference-service)。

重点观察 `/v1/chat/completions`、streaming、metrics、events 和 engine 边界。

### 如果你最困惑的是“为什么还要多一层 Gateway”

先看 [ai-gateway](/06-projects/02-ai-gateway)。

重点观察 auth、routing、fallback、cache、upstream health 和 request timeline。

### 如果你最困惑的是“跑完之后怎么判断结果好不好”

先看 [eval-module](/06-projects/03-eval-module)。

重点观察 run bundle、compare、history、leaderboard、sample analysis 和 recommendation。

### 如果你最困惑的是“训练为什么会留下这么多产物”

先看 [finetune-demo](/06-projects/04-finetune-demo)。

重点观察 dataset registry、run state、checkpoint index、export manifest 和 history。

## 项目和文档的对应方式

这套站点有三层入口：

- 概念页：解释为什么需要某个能力
- 项目页：解释当前代码怎么实现这个能力
- 参考页：整理 API、CLI、文件、验证命令和排障路径

如果你读概念觉得抽象，就去项目页看代码边界。

如果你读项目页不知道命令，就去参考页看：

- [命令速查](/09-reference/01-command-cheatsheet)
- [API Surface](/09-reference/05-api-surface)
- [CLI Surface](/09-reference/06-cli-surface)
- [Artifacts and Files](/09-reference/03-artifacts-and-files)
- [验证矩阵](/09-reference/07-validation-matrix)

如果你想看四个项目更细的联动关系，再继续读：

- [文档与项目怎么联动](/06-projects/05-docs-and-projects-map)
- [四个项目怎么连成系统](/06-projects/06-end-to-end-system-map)
- [质量与维护入口](/06-projects/07-quality-and-maintenance)

## 为什么这些项目看起来都偏“小”

这是有意的。

学习型项目如果一开始就做成完整生产系统，会带来几个问题：

- 依赖太重，读者跑不起来
- 代码太多，边界看不清
- 真正要学的系统对象被框架细节淹没
- 本地验证成本太高
- 公共仓库维护压力过大

所以当前项目选择了“最小但完整”的路线：每个项目都保留真实系统会需要的边界和证据，但内部实现尽量轻。

这不是降低目标，而是先把学习路径铺稳。

## 如何判断自己学明白了

你可以用下面几个问题自测：

- 能否画出四个项目之间的调用和证据关系
- 能否说明 serving 和 gateway 的边界
- 能否解释 eval run 和 training run 的区别
- 能否找到某个 API 对应的测试
- 能否说清一个 request id 如何帮助排查
- 能否解释一个 export manifest 为什么需要 lineage
- 能否知道文档改动、代码改动分别该跑哪些验证

如果这些问题能回答，这套项目就不只是“看过”，而是开始变成你的系统地图。

## 常见误区

### 误区一：四个项目是四个互不相关的 demo

不是。它们分别站在 serving、gateway、evaluation、training 四个层次，共同构成最小闭环。

### 误区二：Mock 代表没有学习价值

Mock 只是不执行真实大模型。接口、边界、错误、事件、manifest、history 这些工程对象依然是真实系统会需要的。

### 误区三：先学完整生产系统更好

对第一次系统学习不一定。先学清楚边界，再逐步迁移真实后端，通常更稳。

### 误区四：项目越多越好

项目数量不是目标。每个项目能否解释一个清晰系统问题，才是学习价值。

### 误区五：文档和代码可以分开维护

这个仓库的设计正好相反：文档讲概念，代码保边界，检查命令和输出证据证明它们没有脱节。
