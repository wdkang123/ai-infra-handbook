Task ID: T601
Task Title: Inference Core Zero-Touch Pack
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
收录推理核心术语：Continuous Batching、Paged Attention、KV Cache、Prefix Caching、Tensor Parallel、Pipeline Parallel、Speculative Decoding、Scheduler。

Result:

# Inference Glossary Batch 07

## G01：Continuous Batching

**定义**：一种动态批处理策略，在请求级别而非固定 batch size 级别进行调度，允许不同长度的请求在同一个 batch 中处理，显著提高 GPU 利用率。

**边界说明**：
- 与静态批处理（Static Batching）的区别是：静态 batching 要求同一 batch 内请求长度相同，continuous batching 允许动态加入/退出
- vLLM 和 SGLang 均原生支持
- 效果：显著提升吞吐量，但会增加延迟波动

**来源**：https://docs.vllm.ai/

---

## G02：Paged Attention

**定义**：一种类操作系统分页思想的注意力机制，将 KV Cache 分块管理，解决传统注意力机制中显存分配不连续的问题。

**边界说明**：
- 灵感来自操作系统分页（paging），vLLM 首先实现
- 允许 KV cache 不连续存储，减少显存碎片
- 与 OS page 的区别：Paged Attention 只管理 attention 计算中的 KV cache，不是通用内存管理

**来源**：https://docs.vllm.ai/

---

## G03：KV Cache

**定义**：在自回归生成过程中，缓存已计算过的 Key-Value 注意力矩阵，避免重复计算。

**边界说明**：
- 生成式 LLM 的核心优化手段
- 显存占用与 sequence length 成正比
- Paged Attention 解决的问题之一就是 KV cache 的显存碎片

**来源**：https://docs.vllm.ai/

---

## G04：Prefix Caching

**定义**：利用请求之间的共享前缀（系统提示、多轮对话上下文），缓存前缀的 KV cache，新请求复用已计算的前缀。

**边界说明**：
- 对多轮对话、System Prompt 重复使用的场景效果显著
- SGLang 的 RadixAttention 原生支持 prefix caching
- vLLM 部分支持

**来源**：https://sglang.readthedocs.io/

---

## G05：Tensor Parallel（张量并行）

**定义**：将模型权重按张量维度切分到多个 GPU，每个 GPU 负责部分权重的计算，最后通过 AllReduce 汇总结果。

**边界说明**：
- 与数据并行（Data Parallel）的区别：数据并行复制模型到多卡，张量并行切分模型
- 适合大模型单卡放不下的场景
- 需要 NVLink 或高速互联以减少通信开销

**来源**：https://docs.vllm.ai/en/latest/tensor_parallelism.html

---

## G06：Pipeline Parallel（流水线并行）

**定义**：将模型按层（layer）切分到多个 GPU，不同 GPU 负责不同层的计算，形成类似流水线的处理流程。

**边界说明**：
- 与 Tensor Parallel 的区别：流水线并行切分层，Tensor Parallel 切分单层内的张量
- 通信模式：只相邻 GPU 间通信，带宽要求低于张量并行
- 流水线并行存在"流水线气泡"（bubble）问题，需要调度优化

**来源**：https://docs.vllm.ai/

---

## G07：Speculative Decoding

**定义**：一种加速自回归生成的解码策略，用小模型快速生成多个候选 token，再用大模型验证，从而降低自回归步数。

**边界说明**：
- 核心思想：用推测执行减少顺序依赖
- 可以与 Draft Model（小模型）配合
- vLLM 和 TensorRT-LLM 均支持
- 适合批量生成场景，对话场景收益相对较小

**来源**：https://nvidia.github.io/TensorRT-LLM/

---

## G08：Scheduler（调度器）

**定义**：推理引擎中负责请求排队、batch 组成、资源分配的组件。

**边界说明**：
- 调度策略直接影响 GPU 利用率和请求延迟
- 常见策略：FCFS（先来先服务）、Shortest Job First（SJF）
- Continuous Batching 是调度策略的一种

**来源**：https://docs.vllm.ai/

---

## G09：RadixAttention

**定义**：SGLang 特有的注意力机制，在前缀树（radix tree）上管理 KV cache，支持高效的 prefix caching 和 reuse。

**边界说明**：
- 与标准 Paged Attention 的区别：RadixAttention 在 KV cache 管理中加入了前缀匹配和复用能力
- 对多轮对话、few-shot learning 等有重复前缀的场景有显著优势
- SGLang 独家实现

**来源**：https://sglang.readthedocs.io/

---

## G10：TensorRT-LLM Backend

**定义**：Triton Inference Server 的后端插件，专门用于运行 TensorRT-LLM 编译的模型。

**边界说明**：
- 需要先通过 `trtllm-build` 编译模型
- 提供动态批处理、Tensor Parallel 等能力
- 与 vLLM/SGLang 的区别：需要预编译，不支持动态加载模型

**来源**：https://nvidia.github.io/TensorRT-LLM/

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://sglang.readthedocs.io/ — SGLang
3. https://nvidia.github.io/TensorRT-LLM/ — TensorRT-LLM
4. https://docs.nvidia.com/deeplearning/triton-inference-server/ — Triton IS

Risk of Staleness:
- 各引擎术语实现可能随版本更新
- Speculative Decoding 和 Paged Attention 的具体行为因引擎而异

Out of Scope Kept:
- 未写完整推理优化指南
- 未写分布式训练相关术语
- 未写 benchmark 性能测试方法
