# 外部模型名与内部目标映射

Gateway 最容易被低估的一件事，是模型名设计。

很多人第一次看模型调用时，会默认认为：

- 用户请求里的 `model`
- gateway 配置里的模型名
- 下游 serving runtime 的模型名
- provider 里的 deployment id

都应该是同一个字符串。

在 demo 里这样做没问题。
但在平台里，“名字”不是小事，它决定外部 API 是否稳定，也决定内部实现能不能演进。

## 先分清三种名字

| 名字 | 面向谁 | 例子 | 主要作用 |
| --- | --- | --- | --- |
| 外部模型名 | 调用方、业务应用、评测系统 | `gpt-learning` | 稳定 API 契约 |
| Gateway 内部模型名 | 平台配置、路由规则 | `vllm-local` | 选择候选 upstream |
| 下游目标模型名 | inference-service、provider、runtime | `Qwen/Qwen2.5-0.5B-Instruct` | 真正执行请求 |

这三者可以相同，但不应该被迫相同。
平台层的价值之一，就是把它们解耦。

## 外部模型名是什么

外部模型名是平台对调用方承诺的名字。

它应该尽量稳定、可理解、可治理。
调用方不应该因为你内部从 mock 换到 vLLM，或者从一个 provider 切到另一个 provider，就被迫改代码。

例如对外可以暴露：

```text
ai-infra-chat
ai-infra-fast
ai-infra-eval
```

这些名字表达的是平台能力，而不是某个具体后端实现。

## 内部目标是什么

内部目标回答的是：

> gateway 最终要把请求发到哪里？

它可能包含：

- upstream 服务地址
- 下游模型名
- provider deployment id
- fallback 候选
- canary 目标
- health 状态
- 权重或优先级

这些信息对调用方不应该全部暴露。
调用方只需要知道“我请求哪个平台模型”，不应该知道“今天内部跑在哪个 provider 的哪个 deployment”。

## 为什么映射层重要

映射层让平台同时具备两种能力：

1. 对外保持稳定。
2. 对内保持灵活。

没有这层映射，你会遇到很多麻烦。

### 场景一：替换后端

你把后端从 mock inference 换成 vLLM。
如果外部模型名直接等于下游模型名，所有调用方都可能要改。

有映射层后，外部仍然请求：

```text
ai-infra-chat
```

内部 target 可以从：

```text
mock-local
```

切到：

```text
Qwen/Qwen2.5-0.5B-Instruct
```

调用方无感。

### 场景二：增加 fallback

主上游失败后，gateway 可以把同一个外部模型名路由到备用 upstream。
调用方仍然只知道自己请求的是同一个平台模型。

这时响应 header 或 events 可以告诉维护者：

- 实际走了哪个 upstream
- 是否使用 fallback
- fallback 是否成功

稳定接口和排障信息可以同时存在。

### 场景三：做 canary

你想把 5% 流量切到新模型。
如果业务方直接绑定下游模型名，canary 会变成应用层改造。

有 gateway 映射后，平台可以在内部做：

```text
ai-infra-chat -> 95% old target, 5% new target
```

调用方仍然请求同一个外部名字。

### 场景四：接评测和发布门禁

eval-module 不应该绑定某个临时下游地址。
它更应该评测平台暴露的稳定模型入口。

这样发布判断才接近真实调用路径。
否则你可能评测的是一个后端，线上走的是另一个入口。

## 映射层应该保留哪些信息

一个更真实的 gateway 模型配置，通常会逐步包含：

| 字段 | 作用 |
| --- | --- |
| external model name | 对外 API 名字 |
| target model | 下游真实模型或 provider deployment |
| upstream base url | 下游服务地址 |
| fallback list | 主目标失败后的候选 |
| timeout | 单次请求最大等待 |
| health status | 当前 upstream 是否可用 |
| owner / tenant policy | 谁能调用 |
| cost metadata | 成本或预算治理 |
| rollout metadata | canary、版本、权重 |

当前仓库只实现了其中一部分，但结构方向已经对了。

## 当前仓库怎么表达

相关文件：

```text
projects/ai-gateway/configs/models.yaml
projects/ai-gateway/src/ai_gateway/config.py
projects/ai-gateway/src/ai_gateway/router.py
projects/ai-gateway/src/ai_gateway/server.py
```

当前路径是：

```text
client model name
  -> gateway route_model_candidates
  -> configured upstream model
  -> downstream chat completion
```

`/v1/models` 会展示：

- 外部模型 id
- target model
- fallback list
- fallback count
- upstream health

chat completion 响应会通过 header 暴露：

- `x-upstream-model`
- `x-fallback-used`
- `x-request-id`
- `x-cache`

这些字段帮助读者区分“我请求的模型名”和“平台实际走的目标”。

## 为什么 `/v1/models` 也重要

模型发现接口不是装饰。

它让调用方先知道：

- 平台允许请求哪些模型
- 每个模型是否有 fallback
- 当前 upstream 大致是否健康
- 外部模型名和 target model 是否一致

在学习项目里，这能帮助读者直接观察 gateway 的平台抽象。
在真实平台里，它还可以接权限、计费、文档和 SDK。

## 映射错误会造成什么

模型名映射问题通常表现为：

| 症状 | 可能原因 |
| --- | --- |
| 404 Model not found | 外部模型名没有配置 |
| 请求到了错误模型 | target model 配置错误 |
| fallback 没生效 | fallback list 或 routing 逻辑错误 |
| eval 结果和线上不一致 | eval 没走同一个外部入口 |
| 权限绕过 | 直接暴露了内部 target |
| 迁移成本高 | 调用方绑定了 provider/deployment 名 |

所以模型名不是“字符串细节”，而是平台稳定性的基础。

## 一个健康的设计原则

可以用这句话自查：

> 外部名字表达平台承诺，内部目标表达执行选择。

外部名字应该稳定。
内部目标可以演进。

当你发现业务代码里到处写着 provider deployment id、vLLM 内部模型路径或临时测试模型名时，就说明平台抽象可能太薄。

## 与评测、训练、发布的关系

模型名映射不只影响 gateway。

### 对 Eval

评测应该尽量评测平台入口，而不是只评测某个孤立后端。
这样 compare 和 release recommendation 才能反映真实调用路径。

### 对 Finetune

微调导出的 adapter 将来可能成为某个 target model 的来源。
但对外模型名可以继续保持稳定。

### 对 发布

发布一个新模型版本时，不一定要改变外部模型名。
你可以先更新内部 target，再通过 run/compare/history 和 gateway events 观察结果。

这就是模型名映射的长期价值：它让发布变成平台内部可控动作，而不是调用方大迁移。

## 常见误区

### “模型名只是字符串”

不是。
它是平台 API 契约的一部分。

### “外部模型名和内部 target 一样最简单”

短期简单，长期会让后端迁移、fallback、canary 和发布变得更难。

### “只有大平台才需要映射层”

不对。
学习项目也应该先建立这个边界，否则后续接真实 backend 时会混乱。

### “`/v1/models` 只用来列模型”

不只是列表。
它也是模型发现、平台元信息和健康状态的入口。

### “Eval 直接打后端更真实”

不一定。
如果真实用户走 gateway，评测也应该理解 gateway 路由、fallback 和模型名映射。

## 学完应该能回答

读完这一页后，你应该能回答：

1. 外部模型名、gateway 内部模型名、下游 target model 有什么区别？
2. 为什么 gateway 不应该简单透传所有下游模型名？
3. 模型名映射如何支持 fallback、canary 和后端迁移？
4. `/v1/models` 在当前仓库里展示了哪些平台信息？
5. 为什么 eval 和发布判断也会受模型名映射影响？

## 继续阅读

- [平台层与模型服务层边界](/03-ai-gateway-platform/05-platform-vs-model-service)
- [Gateway Router、Fallback 与 Cache](/03-ai-gateway-platform/03-gateway-router-fallback-cache)
- [Run、Compare、History](/04-evaluation-observability/01-run-compare-history)
- [从 Demo Gateway 到真实平台层](/03-ai-gateway-platform/07-from-demo-gateway-to-real-platform)
