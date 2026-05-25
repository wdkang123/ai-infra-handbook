# 01. LLM Fundamentals

这一组内容解决的是“你后面在看推理、网关、评测、微调时，到底在围绕什么对象工作”。

如果基础概念没站稳，后面的工程词会很容易变成一堆零散术语。所以这一组不是为了背定义，而是为了建立几个最重要的直觉：

- 模型到底在处理什么
- token 为什么会变成一切工程问题的共同单位
- context 为什么既是能力边界，也是成本边界
- prefill / decode 为什么会直接影响服务性能
- TTFT / ITL / throughput 为什么会变成你后面反复看到的核心指标

推荐阅读顺序：

1. [模型、Token、Context](/01-llm-fundamentals/01-model-token-context)
2. [Prefill、Decode、KV Cache](/01-llm-fundamentals/02-prefill-decode-kv-cache)
3. [TTFT、ITL、吞吐](/01-llm-fundamentals/03-ttft-itl-throughput)
4. [从请求到首个 Token](/01-llm-fundamentals/04-from-request-to-first-token)

学这一组时，不用一上来追求特别精确的论文级表述。更重要的是先形成工程直觉：后面的服务层、平台层、评测层，其实都在围绕这些基础变量做取舍。
