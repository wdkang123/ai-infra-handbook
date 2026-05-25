# vLLM

## 先把 vLLM 放在什么位置理解

vLLM 更适合先理解成“面向 LLM serving 的完整执行框架”。

它不是简单的模型包装器，也不是只提供一个 OpenAI 风格接口。  
它真正解决的是一组更底层的问题：

- 请求如何进入统一服务
- prompt 的 prefill 和 token 的 decode 怎么协调
- KV cache 如何高效管理
- 多个请求如何动态组成 batch
- streaming 如何在不拖垮吞吐的前提下工作

如果你把它只理解成“一个能 `serve` 模型的命令”，后面看很多设计都会觉得平平无奇。  
但如果你把它理解成“把高吞吐 LLM 服务系统化”的一条主线，它的重要性就会非常清楚。

## 为什么它在学习路径里很关键

对学习 AI Infra 来说，vLLM 的价值不只是“流行”，而是它能把很多抽象问题变成具体结构：

1. 你可以用它理解什么叫 serving framework，而不只是 HTTP API
2. 你可以借它理解 cache、batching、latency、throughput 之间的权衡
3. 你可以从它延伸到 gateway、observability、evaluation，而不是把推理层看成黑盒

所以在这套手册里，vLLM 更像是“推理服务的第一条主线”。

## 最值得先理解的三个点

### 1. PagedAttention 不是一个“优化小技巧”

它更像 vLLM 为什么成立的关键支点。  
你可以先把它理解成：为了让 KV cache 不再被连续大块内存布局拖垮，vLLM 用分页思路来管理缓存块。

学习时最重要的不是背实现细节，而是抓住两个直觉：

- KV cache 是推理服务的核心资源之一
- cache 的管理方式，会直接影响并发、吞吐和长上下文能力

### 2. Continuous batching 是系统行为，不是参数表

很多初学者会把 batch size 当成一个静态训练思维里的参数。  
但在 serving 里，更关键的是“请求在运行中如何动态进入和退出 batch”。

vLLM 值得学的地方就在这里：  
它让你看到，在线推理不是把一堆请求硬拼在一起，而是围绕 token 生成过程不断重组执行单元。

### 3. OpenAI-compatible API 只是最外层壳

大家常常先接触到的是 `/v1/chat/completions`。  
但对 AI Infra 学习来说，这层接口只是入口，不是重点。

真正重要的是：

- 接口后面如何映射到调度器
- streaming 和普通响应怎么共存
- metrics 怎么暴露
- prefix caching 何时能命中

## 学习时常见误区

### “vLLM 就是更快的模型推理”

不够准确。  
更好的说法是：vLLM 让“高效推理服务”变得更容易组织和落地。

它当然追求速度，但它真正厉害的是把速度、显存、服务接口、批处理、缓存这些问题放进了同一个框架里。

### “用了 vLLM 就不需要 gateway”

不对。  
vLLM 解决的是推理执行层问题；gateway 解决的是统一入口、鉴权、路由、限流、跨模型治理问题。

它们经常是上下游关系，而不是二选一关系。

### “vLLM 学会了就等于推理服务学完了”

也不对。  
vLLM 是极好的起点，但不是全部。  
后面你还要继续看：

- SGLang 在调度和结构化生成上的不同回答
- Triton 在通用服务容器层的价值
- TensorRT-LLM 在执行优化层的定位

## 在当前仓库里应该怎么对照着看

当前仓库没有直接把 vLLM 嵌进 `inference-service` 的真实执行路径里，而是故意先做了一个学习型骨架。  
这样做的目的，是让你先看清服务层结构，再决定什么时候把真实后端接进去。

你可以按这个顺序对照：

1. 先看 [inference-service 项目页](/06-projects/01-inference-service)
2. 再看 `projects/inference-service/src/inference_service/server.py`
3. 然后回到本章，问自己：
   - 如果把 mock executor 换成真实 vLLM，哪些层不需要改
   - 哪些层会开始需要考虑 streaming、metrics、prefix caching

这时你会更容易理解：  
为什么我们前面没有急着把所有代码做成“完全真实”，而是先把结构和边界拉出来。

## 最小实践建议

如果你后面开始逐步实操，vLLM 这一章最适合做的不是“跑通所有高级参数”，而是这三步：

1. 启动一个最小 vLLM 服务
2. 分别打一条普通请求和一条 `stream=true` 请求
3. 再回来看 TTFT、ITL、prefix caching 这些词到底在描述什么

只要这三步做完，vLLM 对你就不再只是一个名字，而会变成一套可感知的系统行为。

## 下一章建议怎么接

读完 vLLM 后，最自然的下一步是去看 [SGLang](/02-inference-serving/05-sglang)。

这不是为了做“谁更强”的比较，而是为了让你看到：  
面对同一类 serving 问题，不同框架会给出不同的组织方式。
