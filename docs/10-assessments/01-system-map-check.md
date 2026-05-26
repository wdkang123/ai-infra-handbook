# 系统地图自测

这页检查你是否真正理解这个仓库为什么分成四个项目，以及这些项目之间的边界。

系统地图不是画给好看的。它解决的是一个很实际的问题：

> 当某个请求失败、某个评测退化、某个训练产物不可复现时，你能不能判断应该先查哪一层？

如果系统地图不清楚，后面所有排障都会变成猜。

## 自测前准备

先打开这些页面：

- [什么是 AI Infra](/00-overview/01-what-is-ai-infra)
- [项目学习总览](/06-projects/00-projects-overview)
- [四个项目怎么连成系统](/06-projects/06-end-to-end-system-map)
- [文档与代码怎么对应](/00-overview/05-docs-to-code-map)
- [API Surface 速查](/09-reference/05-api-surface)
- [CLI Surface 速查](/09-reference/06-cli-surface)

然后在不看答案的情况下，用一张纸或一个文档写出：

```text
执行层：
治理层：
质量层：
训练层：

每一层的输入：
每一层的输出：
每一层最重要的失败路径：
每一层对应的项目：
每一层对应的验证命令：
```

先写自己的版本，再回来看题目。

## 四层系统地图

当前仓库的四层可以这样理解：

| 层次 | 项目 | 核心问题 | 关键证据 |
| --- | --- | --- | --- |
| 执行层 | `inference-service` | 模型服务如何接收请求并返回结果 | `/health`、`/v1/models`、completion、metrics、events |
| 治理层 | `ai-gateway` | 请求如何被鉴权、路由、限流、cache、fallback | status code、headers、upstream health、timeline |
| 质量层 | `eval-module` | 输出质量如何被评测、比较和沉淀 | run、compare、history、leaderboard、sample analysis |
| 训练层 | `finetune-demo` | 训练过程如何留下可复盘资产 | dataset registry、run state、checkpoint index、export manifest |

注意：这不是唯一可能的生产架构，但它是这个学习站刻意保留的最小系统地图。

## 题目 A：四层边界

请回答：

1. `inference-service` 解决的核心问题是什么？
2. `ai-gateway` 为什么不能只理解成 HTTP proxy？
3. `eval-module` 为什么属于质量闭环，而不是普通脚本？
4. `finetune-demo` 为什么强调 run、checkpoint、export，而不是只强调训练命令？
5. Serving 层和 Gateway 层都可能有 `/metrics`，它们统计的问题有什么不同？
6. Evaluation 和 Observability 为什么不能混成一个词？
7. 训练产物为什么最终要回到 eval，而不是训练完就结束？
8. 哪些东西属于学习型实现，哪些边界未来迁移到生产系统时仍然应该保留？

回答时尽量用“它负责什么 / 不负责什么”的格式。

## 题目 B：失败归因

请解释下面问题优先查哪一层。

| 现象 | 优先层 | 你要说明的理由 |
| --- | --- | --- |
| 请求没有认证头，返回 `401` | Gateway | 鉴权发生在平台入口 |
| 请求模型名不存在，返回 `404` | Gateway 或 Serving | 要区分外部模型名路由失败和下游模型校验失败 |
| 请求触发 `429` | Gateway | 限流属于平台治理 |
| Gateway 返回 `502` | Gateway + Upstream | 可能是上游失败或所有 fallback 失败 |
| Inference `/health` 正常，但 eval compare 失败 | Eval | compare 的 task / metric / threshold 可能不一致 |
| Export 失败，提示 checkpoint 不完整 | Finetune | checkpoint index 或 manifest 不满足导出要求 |
| Pages 发布失败 | Publication / CI | 文档构建、路径、workflow 或依赖可能有问题 |

不要只写状态码。要写出你会查的接口、文件或命令。

## 题目 C：代码定位

请在项目里找到这些入口，并写出它们的职责：

| 目标 | 你要找到什么 | 应该能解释什么 |
| --- | --- | --- |
| inference API | chat completion 的 HTTP 入口 | 请求如何进入执行层 |
| inference engine | mock engine 或 OpenAI-compatible adapter | 外部契约和内部执行如何分离 |
| gateway proxy | 接收外部请求并转发到 upstream 的逻辑 | 鉴权后请求如何进入下游 |
| gateway routing | 外部模型名映射到内部 target 的逻辑 | 为什么外部模型名要稳定 |
| eval runner | 执行一次评测 run 的逻辑 | run 如何形成结果对象 |
| eval comparison | 比较两个 run 的逻辑 | 为什么 task 和 metric 要一致 |
| finetune trainer | 生成训练 run 资产的逻辑 | run state 和 history 如何形成 |
| finetune export | 从 checkpoint 生成 export 资产的逻辑 | export manifest 如何保留 lineage |

要求不是背路径，而是能解释“为什么这个文件在这里”。

## 题目 D：系统行为推理

### 场景 1：Gateway 正常，但 inference-service 没启动

请说明：

- gateway `/health` 怎么变化
- chat completion 可能返回什么错误
- `/events/failures` 会出现什么信号
- smoke 测试中哪类步骤会失败
- 这是否说明 gateway 自己坏了

好的回答应该能区分“入口服务还活着”和“下游不可用”。

### 场景 2：Inference-service 正常，但请求里没有认证头

请说明：

- 错误来自 gateway 还是 inference-service
- HTTP status 应该是什么
- 这类失败是否应该计入 upstream failure
- 为什么这类错误不应该打到下游模型服务

好的回答应该能说明鉴权是在平台入口完成的。

### 场景 3：两次 eval run task 不同，却被拿来 compare

请说明：

- 为什么系统应该拒绝比较
- 如果不拒绝，会带来什么误导
- compare report 应该保留哪些上下文
- 这和发布决策有什么关系

好的回答应该能说明“分数可比性”不是天然存在的。

### 场景 4：Finetune run 成功，但 checkpoint 不完整

请说明：

- 为什么 export 应该失败
- checkpoint index 解决了什么问题
- export manifest 应该引用哪些来源
- 如果强行导出，后续 eval 会遇到什么风险

好的回答应该能把训练资产和质量闭环连起来。

## 题目 E：画一张自己的系统图

请用自己的语言画一张图，至少包含：

```text
Client
  -> Gateway
  -> Inference Service
  -> Eval Module
  -> Finetune Demo
  -> Eval Module
  -> Release Decision
```

并在每条边上标注：

- 输入是什么
- 输出是什么
- 失败时看哪里
- 哪个文件或接口能提供证据

如果你能把每条边说清楚，说明系统地图已经不只是概念图了。

## 通过标准

你可以认为自己通过了这页自测，如果你能做到：

- 不看文档画出四层结构
- 给每个项目说出一个正常路径和一个失败路径
- 找到每个项目的核心入口和测试文件
- 解释为什么 smoke 是跨项目验收，而不是单元测试替代品
- 说明某个状态码更可能来自哪一层
- 用 request id、events、manifest 或 report 作为证据

达到这些标准，后面做 Capstone 会轻松很多。

## 常见扣分点

| 表现 | 问题 |
| --- | --- |
| 只列项目名 | 没有说明职责边界 |
| 把 Gateway 和 Serving 混在一起 | 排障时会找错位置 |
| 把 Eval 当成脚本 | 看不到发布判断和历史比较 |
| 把 Finetune 当成训练命令 | 看不到 dataset/run/checkpoint/export 资产链 |
| 只说“跑测试” | 没说明哪类测试证明什么 |
| 只看 happy path | 公开项目最容易在失败路径上暴露薄弱点 |

## 复盘问题

做完后写下：

```text
我最清楚的一层是：
我最容易混淆的一层是：
我最能指出代码证据的问题是：
我最缺输出证据的问题是：
我下一步应该回看哪一页：
我下一步应该跑哪条命令：
```

这份复盘可以直接变成下一轮学习计划或 GitHub issue。
