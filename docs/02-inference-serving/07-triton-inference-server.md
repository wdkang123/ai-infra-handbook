# Triton Inference Server

Triton Inference Server 更适合先理解成：

> 通用推理服务容器。

它不是某个 LLM 专用生成引擎。
这点非常重要。

很多人第一次看到 Triton，会直接把它和 vLLM、SGLang 放在同一层比较：

```text
vLLM vs SGLang vs Triton
```

但更准确的分层是：

- vLLM / SGLang：更接近 LLM 专用执行框架。
- Triton：更接近统一模型服务容器。
- TensorRT-LLM：更接近底层 LLM 执行优化层。

Triton 的核心价值不是“自己最会生成 token”，而是“把不同模型、不同后端、不同版本统一托管起来”。

## 它在系统里处在哪一层

可以把 Triton 放在这里：

```text
client / app
  -> ai-gateway
  -> model service layer
  -> Triton Inference Server
     -> backend A
     -> backend B
     -> TensorRT-LLM backend
     -> Python backend
```

它更像模型服务托管层。
它可以承载多种 backend，而不是只服务一种 LLM。

## 为什么 Triton 在工程里重要

真实系统通常不会只有一种模型。

你可能同时有：

- LLM
- embedding model
- reranker
- classifier
- OCR model
- vision model
- speech model
- small utility model

它们可能来自不同框架：

- PyTorch
- ONNX
- TensorRT
- Python custom backend
- TensorRT-LLM

这时，Triton 的价值就出现了：
它让模型服务不再是一堆散落脚本，而是进入统一托管、统一配置、统一暴露的结构。

## Model Repository 是什么

Triton 里很有代表性的概念是 model repository。

它表达的是：

> 模型不是一个孤立权重文件，而是一个有目录结构、版本和配置的服务对象。

一个模型服务通常需要：

- 模型文件
- 版本目录
- config
- 输入输出定义
- backend 类型
- instance group
- batching 配置
- version policy

这会帮助你建立一个工程直觉：

线上模型不是“把权重放上去”就完了。
它需要被服务系统正式管理。

## Backend 抽象为什么重要

Triton 的 backend 抽象告诉你：

> 服务容器不一定亲自执行推理，它可以把推理委托给不同 backend。

这和 AI Infra 的分层非常一致：

- gateway 管入口治理
- model service container 管托管和暴露
- backend 管具体执行
- optimizer/runtime 管底层性能

如果你以后接触更复杂推理系统，这种 backend 思维会非常有用。

## Dynamic Batching 与实例管理

Triton 也会处理服务层资源组织问题，例如：

- dynamic batching
- model instance count
- version loading
- model warmup
- backend execution

这些能力提醒你：
服务容器不是透明代理，它也会影响吞吐和延迟。

不过 Triton 的 batching 和 vLLM/SGLang 针对 LLM token 生成过程的调度不是完全同一种问题。
LLM serving 里 prefill/decode、KV Cache、streaming 会带来更特殊的复杂度。

## 它和 vLLM / SGLang 怎么比较

不要先问谁更强。
先问：

> 我现在要解决的是 LLM 专用执行问题，还是多模型统一托管问题？

如果你要快速服务一个 LLM，并关注：

- KV Cache
- continuous batching
- streaming
- prefix caching

vLLM / SGLang 这条主线更直接。

如果你要统一托管多类模型，并关注：

- 模型仓库
- backend 抽象
- 模型版本
- 多模型部署
- 通用 inference serving

Triton 的主线更明显。

## 它和 TensorRT-LLM 的关系

Triton 和 TensorRT-LLM 经常一起出现，因为它们可以形成分层组合：

```text
Triton
  -> TensorRT-LLM backend
     -> optimized LLM execution
```

Triton 更像服务容器。
TensorRT-LLM 更像底层执行优化。

这组关系能帮助你理解：一个推理系统可以由多个层次拼出来，而不是一个框架包打天下。

## 当前仓库怎么对应

当前仓库没有直接接 Triton。
这不是缺失，而是刻意控制学习复杂度。

当前系统先表达：

- `inference-service`：服务边界
- `ai-gateway`：平台入口
- `eval-module`：质量判断
- `finetune-demo`：训练资产

等这些边界清楚后，再看 Triton，你会更容易理解：

- 为什么模型要有 repository 和版本
- 为什么服务容器和执行 backend 可以分开
- 为什么 gateway 和 Triton 不是同一层

## 一个具体迁移想象

如果后续要把当前学习系统接向 Triton，可以想象这样的路径：

```text
ai-gateway
  -> inference-service
     -> Triton endpoint
        -> backend model
```

迁移时仍然要保留：

- OpenAI-compatible API 或稳定 adapter
- request id
- health
- metrics
- events
- error mapping
- eval 入口

Triton 可以进入执行/托管层，但不应该让外部学习边界全部重写。

## 常见误区

### “Triton 本身就是最快的 LLM 引擎”

不准确。
Triton 是服务容器，具体性能很大程度取决于 backend。

### “Triton 和 vLLM 是同一层二选一”

不完全是。
vLLM 更偏 LLM runtime，Triton 更偏通用服务容器。

### “用了 Triton 就不用 gateway”

不对。
Triton 管模型服务托管，gateway 管入口治理、鉴权、限流和平台路由。

### “Triton 只适合 LLM”

不对。
它本来就是通用推理服务容器，多模型多后端才是重要主线。

## 学完应该能回答

读完这一页后，你应该能回答：

1. Triton 和 vLLM/SGLang 分别更像哪一层？
2. Model repository 为什么是工程对象？
3. Backend 抽象解决什么问题？
4. Triton 和 TensorRT-LLM 为什么常组合出现？
5. 当前仓库未来接 Triton 时应该保留哪些学习边界？

## 继续阅读

- [TensorRT-LLM](/02-inference-serving/08-tensorrt-llm)
- [Triton 与 TensorRT-LLM](/02-inference-serving/02-triton-tensorrt-llm)
- [服务选型与取舍](/02-inference-serving/03-serving-tradeoffs)
- [Serving 后端迁移](/12-production-migration/01-serving-backend-migration)
