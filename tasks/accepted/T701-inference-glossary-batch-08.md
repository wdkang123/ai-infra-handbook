Task ID: T701
Task Title: Inference Engines Deep-Research Pack
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
收录 Serving Engine/Backend/Model Repository/Request Batching/Dynamic Batching/RadixAttention/Prefill/Decode 术语。

Result:

# Inference Glossary Batch 08

## S01：Serving Engine

**定义**：负责实际执行模型推理计算的核心组件，处理 CUDA kernel 调用、显存管理和张量计算。

**边界说明**：
- 与推理服务的区别：引擎只负责计算，不直接暴露 HTTP 接口
- vLLM/SGLang 既是引擎又内置服务层，可独立对外
- TensorRT-LLM 是纯引擎，需要服务包装

**来源**：https://docs.vllm.ai/

---

## S02：Backend

**定义**：Triton Inference Server 中实际执行推理计算的组件，负责加载模型、执行推理。

**边界说明**：
- Triton 支持多种 backend：TensorRT、ONNX Runtime、Python、TensorRT-LLM
- Backend 不等于推理引擎，但 TensorRT backend 使用 TensorRT 引擎
- Backend 需要在 config.pbtxt 中配置

**来源**：https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/backend_lib.html

---

## S03：Model Repository

**定义**：Triton Inference Server 中存储模型文件的目录结构，包含模型版本和配置文件。

**边界说明**：
- 目录结构：`model_repository/<model_name>/<version>/model.pt`
- 每个模型需要有 config.pbtxt 配置文件
- 支持动态模型加载（部分 backend）

**来源**：https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/model_repository.html

---

## S04：Request Batching（请求批处理）

**定义**：将多个推理请求打包成一个 batch 一起处理，提高 GPU 利用率。

**边界说明**：
- 与 Dynamic Batching 的区别：Request Batching 通常指静态 batch，即用户显式指定 batch size
- 优点：简单直接，GPU 利用率高
- 缺点：需要等待凑满 batch，延迟增加

**来源**：https://docs.vllm.ai/

---

## S05：Dynamic Batching（动态批处理）

**定义**：Triton Inference Server 的动态批处理策略，自动将多个请求凑成 batch 处理。

**边界说明**：
- 与 Static Batching 的区别：动态 batching 由 Triton 自动调度，无需用户指定
- 配置参数：max_batch_size、preferred_batch_size、delay_threshold
- vLLM/SGLang 的 Continuous Batching 与此概念相关但实现不同

**来源**：https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/model_configuration.html#dynamic-batcher

---

## S06：RadixAttention

**定义**：SGLang 特有的注意力机制，在前缀树（radix tree）上管理 KV cache，支持高效的 prefix caching 和 reuse。

**边界说明**：
- 与标准 Paged Attention 的区别：RadixAttention 在 KV cache 管理中加入了前缀匹配和复用能力
- 对多轮对话、few-shot learning 等有重复前缀的场景有显著优势
- SGLang 独家实现，vLLM 部分支持

**来源**：https://sglang.readthedocs.io/

---

## S07：Prefill

**定义**：自回归生成的第一阶段，对输入 prompt 进行完整的前向传播计算，生成第一个 token。

**边界说明**：
- 与 Decode 的区别：Prefill 处理整个输入序列，Decode 只生成一个 token
- Prefill 阶段计算量大，是延迟的主要来源之一
- 投机解码（Speculative Decoding）中会用小模型做 Prefill

**来源**：https://docs.vllm.ai/

---

## S08：Decode

**定义**：自回归生成的第二阶段，逐 token 生成响应，每次前向传播只计算一个新 token。

**边界说明**：
- 与 Prefill 的区别：Decode 每次只处理一个 token，是自回归生成的主要步骤
- Decode 阶段显存瓶颈主要是 KV cache
- Paged Attention 主要优化的是 Decode 阶段的显存管理

**来源**：https://docs.vllm.ai/

---

## S09：Continuous Batching

**定义**：一种动态批处理策略，在请求级别而非固定 batch size 级别进行调度，允许不同长度的请求在同一个 batch 中处理。

**边界说明**：
- 与 Static Batching 的区别：Continuous Batching 允许请求动态加入/退出 batch
- vLLM 和 SGLang 均原生支持
- 效果：显著提升吞吐量，但会增加延迟波动

**来源**：https://docs.vllm.ai/

---

## S10：Paged Attention

**定义**：一种类操作系统分页思想的注意力机制，将 KV Cache 分块管理，解决传统注意力机制中显存分配不连续的问题。

**边界说明**：
- 灵感来自操作系统分页（paging），vLLM 首先实现
- 允许 KV cache 不连续存储，减少显存碎片
- 与 OS page 的区别：Paged Attention 只管理 attention 计算中的 KV cache，不是通用内存管理

**来源**：https://docs.vllm.ai/

---

## S11：KV Cache

**定义**：在自回归生成过程中，缓存已计算过的 Key-Value 注意力矩阵，避免重复计算。

**边界说明**：
- 生成式 LLM 的核心优化手段
- 显存占用与 sequence length 成正比
- Paged Attention 解决的问题之一就是 KV cache 的显存碎片

**来源**：https://docs.vllm.ai/

---

## S12：Tensor Parallel（张量并行）

**定义**：将模型权重按张量维度切分到多个 GPU，每个 GPU 负责部分权重的计算，最后通过 AllReduce 汇总结果。

**边界说明**：
- 与数据并行（Data Parallel）的区别：数据并行复制模型到多卡，张量并行切分模型
- 适合大模型单卡放不下的场景
- 需要 NVLink 或高速互联以减少通信开销

**来源**：https://docs.vllm.ai/en/latest/tensor_parallelism.html

---

## S13：Speculative Decoding（投机解码）

**定义**：一种加速自回归生成的解码策略，用小模型快速生成多个候选 token，再用大模型验证，从而降低自回归步数。

**边界说明**：
- 核心思想：用推测执行减少顺序依赖
- 可以与 Draft Model（小模型）配合
- vLLM 和 TensorRT-LLM 均支持
- 适合批量生成场景，对话场景收益相对较小

**来源**：https://nvidia.github.io/TensorRT-LLM/

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://sglang.readthedocs.io/ — SGLang
3. https://docs.nvidia.com/deeplearning/triton-inference-server/ — Triton IS
4. https://nvidia.github.io/TensorRT-LLM/ — TensorRT-LLM

Risk of Staleness:
- 各引擎术语实现可能随版本更新

Out of Scope Kept:
- 未写完整推理优化指南
- 未写 benchmark 性能测试方法
