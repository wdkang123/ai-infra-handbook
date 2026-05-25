# 02. Inference Serving

这一组内容讲的是“模型服务本体”这一层。  
也就是：真正把模型挂出来对外提供推理能力的那一段。

你后面会看到很多名字，比如：

- vLLM
- SGLang
- Triton Inference Server
- TensorRT-LLM

它们不是简单的“谁更高级”，而是各自站在不同工程位置上解决问题。

推荐阅读顺序：

1. [vLLM 与 SGLang](/02-inference-serving/01-vllm-sglang)
2. [Triton 与 TensorRT-LLM](/02-inference-serving/02-triton-tensorrt-llm)
3. [服务选型与取舍](/02-inference-serving/03-serving-tradeoffs)
4. [vLLM](/02-inference-serving/04-vllm)
5. [SGLang](/02-inference-serving/05-sglang)
6. [Cache 与 Prefix Caching](/02-inference-serving/06-cache-prefix-caching)
7. [Triton Inference Server](/02-inference-serving/07-triton-inference-server)
8. [TensorRT-LLM](/02-inference-serving/08-tensorrt-llm)
9. [Streaming、Batching、Metrics](/02-inference-serving/09-streaming-batching-metrics)
10. [从学习型服务到真实 Serving Stack](/02-inference-serving/10-from-learning-service-to-real-serving-stack)

如果你想边读边看实际可运行代码，最好同步配合：

- [inference-service 项目页](/06-projects/01-inference-service)
