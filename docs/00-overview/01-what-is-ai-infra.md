# 什么是 AI Infra

> 本页解决：AI Infra 到底包含哪些系统边界，以及为什么它不是“把模型 API 包起来”。
> 读完能做：画出 inference-service、ai-gateway、eval-module、finetune-demo 四层学习地图。
> 关联代码：`projects/inference-service`、`projects/ai-gateway`、`projects/eval-module`、`projects/finetune-demo`。
> 验证命令：`PYTHON=.venv/bin/python make quickstart`。

AI Infra 不是单一组件，也不是“把模型跑起来”这么简单。

如果从工程视角看，它更像一整套围绕模型能力建立的基础设施：模型如何接入、如何提供推理服务、请求如何被治理、输出如何被评测、运行过程如何被观测、训练产物如何被管理，以及这些能力如何进入真实产品和平台。

对学习者来说，一个更实用的定义是：

> AI Infra = 围绕模型能力交付、运行、治理、评估和迭代的一组工程系统。

这个定义里有几个关键词：

- **交付**：模型能力要从 demo 变成可调用服务。
- **运行**：服务要处理延迟、吞吐、并发、显存、失败和成本。
- **治理**：调用方、模型名、限流、fallback、cache、权限都要可管理。
- **评估**：结果不能只靠感觉，需要 run、compare、sample、history 和发布判断。
- **迭代**：prompt、数据、训练、模型版本和反馈要进入持续改进闭环。

这也是整个仓库后续所有章节反复展开的主线。

![AI Infra 系统关系图](/images/articles/what-is-ai-infra.jpg)

*图：AI Infra 的难点不是单个组件，而是交付、运行、治理、评估和迭代如何连接成一套系统。*

## 为什么 AI Infra 重要

模型本身再强，如果不能稳定接入、低成本运行、被观测、被评估、被治理，就很难真正支撑业务。

AI Infra 的价值通常体现在几件事上：

- 让模型能力从 demo 变成可运行服务
- 让推理成本、延迟、吞吐变成可优化对象
- 让接入方式、权限、路由、限流、缓存有统一治理层
- 让效果评估、日志观测、故障排查形成闭环
- 让训练和微调产物能被追踪、复现和评测
- 让“用模型”升级成“运营模型系统”

如果没有 AI Infra，很多项目会卡在一个很尴尬的状态：单次演示很好看，但一旦进入多人使用、持续迭代或公开维护，就会暴露出大量工程问题。

## 从一次请求看 AI Infra

可以先从一条请求理解。

一个用户调用模型时，表面上只是：

```text
User -> API -> Model -> Answer
```

但工程系统里会发生更多事情：

```text
Client
  -> Gateway auth / rate limit / routing
  -> Model service
  -> Tokenization / prefill / decode / streaming
  -> Metrics / events / request timeline
  -> Eval run / compare / release decision
  -> Training data / checkpoint / export / next candidate
```

这条链路里，每一段都可能成为问题来源：

- token 过长导致延迟变高
- gateway 路由到错误上游
- upstream 失败触发 fallback
- streaming 中途断开
- eval run 和 baseline 不可比
- finetune export 缺少 lineage
- public repo accidentally 提交了敏感信息

AI Infra 学习的核心，就是学会把这些问题放回正确的系统层里。

## 四层学习地图

从本仓库的学习路径上看，AI Infra 可以拆成四层。

| 层次 | 核心问题 | 当前项目 |
| --- | --- | --- |
| 模型运行层 | 模型如何被服务出来 | `inference-service` |
| 平台治理层 | 请求如何被鉴权、路由、限流、缓存和 fallback | `ai-gateway` |
| 质量闭环层 | 输出如何被评测、观测、比较和用于发布判断 | `eval-module` |
| 训练迭代层 | 数据、run、checkpoint、export 如何形成可复盘资产 | `finetune-demo` |

真正难的地方往往不是“知道有哪些组件”，而是理解这些层之间的关系：

- 推理服务决定模型能否稳定跑起来
- AI Gateway 决定能力能否被规范化使用
- 评测和观测决定系统能否持续优化
- 训练和微调决定能力能否根据场景演进

这四层分开学习，是为了让边界清楚；最终合起来，才是一条完整 AI Infra 闭环。

## 每一层解决什么问题

### 模型运行层

这一层更靠近模型执行。

它关心：

- 模型如何加载
- 请求如何变成 token
- prefill / decode 如何发生
- KV Cache 如何影响显存和并发
- streaming 如何返回
- TTFT / ITL / throughput 如何观察
- engine error 如何映射

对应学习模块：

- [LLM Fundamentals](/01-llm-fundamentals/00-overview)
- [Inference Serving](/02-inference-serving/00-overview)
- [inference-service](/06-projects/01-inference-service)

### 平台治理层

这一层更靠近调用入口。

它关心：

- 谁能调用
- 外部模型名如何映射到内部 target
- 请求如何限流
- 上游失败时是否 fallback
- response cache 如何隔离
- request id 如何串联排查
- metrics 和 events 如何保留平台证据

对应学习模块：

- [AI Gateway Platform](/03-ai-gateway-platform/00-overview)
- [ai-gateway](/06-projects/02-ai-gateway)

### 质量闭环层

这一层让模型输出不再只靠感觉判断。

它关心：

- task 如何定义
- run 如何保存
- baseline 和 candidate 如何比较
- sample outputs 如何审查
- leaderboard 如何辅助观察
- observability 如何解释质量变化
- release decision 如何形成

对应学习模块：

- [Evaluation Observability](/04-evaluation-observability/00-overview)
- [eval-module](/06-projects/03-eval-module)

### 训练迭代层

这一层让模型能力可以被持续改进。

它关心：

- dataset 如何登记
- run 如何复现
- checkpoint 如何索引
- export 如何追溯来源
- history 如何支持横向观察
- 训练结果如何进入 eval

对应学习模块：

- [Finetuning Training](/05-finetuning-training/00-overview)
- [finetune-demo](/06-projects/04-finetune-demo)

## 常见组件怎么放进地图

如果按工程落地理解，常见组件大致包括：

| 类型 | 例子 | 更接近哪一层 |
| --- | --- | --- |
| 推理服务 | vLLM、SGLang、Triton | 模型运行层 |
| 优化执行 | TensorRT-LLM、KV Cache、prefix caching | 模型运行层 |
| 网关与路由 | AI Gateway、Router、Fallback、Rate limit | 平台治理层 |
| 观测与评测 | metrics、logs、traces、benchmark、leaderboard | 质量闭环层 |
| 训练与微调 | LoRA、QLoRA、PEFT、Unsloth、TRL | 训练迭代层 |
| 支撑能力 | 配置、权限、成本、发布、回滚、CI | 跨层支撑 |

重点不在于记住工具名单，而在于知道每类组件解决什么问题、放在系统的哪一层。

## 关键指标

AI Infra 里最常见的指标可以分几类。

### 性能指标

- TTFT：首 token 延迟
- ITL：token 间延迟
- throughput：单位时间生成量
- queue time：排队等待
- total latency：请求总耗时

### 资源指标

- GPU 利用率
- 显存占用
- CPU / 内存
- 网络带宽
- KV Cache 占用

### 平台指标

- 请求数
- 错误率
- fallback 次数
- cache 命中率
- rate limit 命中
- upstream health

### 质量指标

- task score
- regression count
- sample pass/fail
- judge reason
- compare delta
- release recommendation

### 训练指标

- dataset version
- run status
- checkpoint completeness
- export status
- lineage completeness

这些指标不是孤立的。发布一个模型或配置时，往往要同时看质量、性能、稳定性和成本。

## 当前仓库和 AI Infra 的关系

这一章是整个仓库的总入口，对应后续四条项目线：

- `projects/inference-service/`：理解模型如何稳定提供推理能力
- `projects/ai-gateway/`：理解请求治理、模型接入和平台抽象
- `projects/eval-module/`：理解质量闭环如何建立
- `projects/finetune-demo/`：理解模型能力如何迭代

它的作用不是把所有细节讲完，而是先建立整体地图，避免后续学习碎片化。

你也可以把这四条线暂时记成四个问题：

1. 模型怎么被服务出来？
2. 请求怎么被治理起来？
3. 结果怎么被判断和比较？
4. 能力怎么被继续迭代？

后面整套手册其实都在反复回答这四个问题。

## 最小实践任务

读完这一页后，建议做 4 个小任务：

1. 画出一张 AI Infra 分层图，标出推理、网关、评测、训练四层。
2. 为仓库中的四个项目分别写一句“它解决什么问题”。
3. 选一条请求链路，标出 request id、status、headers、events 这些证据会出现在哪里。
4. 挑一个工具名，例如 vLLM、SGLang、Unsloth 或 Triton，说明它更接近哪一层。

如果你能做完，后面阅读会轻松很多。

## 常见误区

### 把 AI Infra 误解成只会部署模型

部署只是其中一部分。AI Infra 还包括治理、观测、评测、训练、发布和维护。

### 只研究模型效果，不研究运行稳定性

效果重要，但如果系统不可观测、不可排障、不可复现，就很难进入真实使用。

### 只看单组件能力，不看系统链路

工具很重要，但工具一定要放进链路里理解。

### 把文档学习和项目实践割裂开

这个仓库的设计正好相反：文档讲地图，项目保边界，输出证据证明系统行为。

### 一开始就追求大而全

学习阶段先把最小闭环跑通，再逐步替换真实后端，会更稳。

## 这章读完之后，下一步最适合看什么

如果你现在还处在“先把系统地图建立起来”的阶段，下一步最推荐是：

1. [学习路线图](/00-overview/02-learning-route)
2. [最小运行手册](/00-overview/03-runbook)
3. [第一次实操演练](/00-overview/04-first-walkthrough)

如果你已经明确自己更想先看哪条线，可以直接去：

- [推理服务](/02-inference-serving/00-overview)
- [AI Gateway Platform](/03-ai-gateway-platform/00-overview)
- [Evaluation Observability](/04-evaluation-observability/00-overview)
- [Finetuning Training](/05-finetuning-training/00-overview)

如果你准备按目标选择路线，继续看：

- [按目标选择学习路径](/00-overview/07-choose-your-path)
