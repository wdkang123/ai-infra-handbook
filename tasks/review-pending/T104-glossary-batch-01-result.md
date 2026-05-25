Task ID: T104
Task Title: Glossary 第一批术语初稿
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
围绕 AI Infra 入门阶段，产出 10 个核心术语初稿，每个术语包含一句话定义、工程上下文意义、和项目的关系、易混淆点。

Result:

---

### Term 1: LLM Serving

**一句话定义**：将大语言模型部署为在线或离线服务，使其能够接收请求并返回生成结果的全套工程系统。

**工程上下文中的意义**：包括模型加载、请求调度、并行推理、资源管理、协议适配（OpenAI API 兼容）等能力。与训练不同，Serving 强调高吞吐、低延迟、资源复用，是 AI Infra 最直接面向用户的一层。

**和项目的关系**：作为 AI Infra 书的入口概念，定义清楚 LLM Serving 才能让读者理解 vLLM / SGLang 这类框架"解决的是什么问题"。

**易混淆点**：容易和"模型训练"混淆。Serving 不涉及梯度反向传播，核心是推理效率和资源调度，不是模型能力提升。

---

### Term 2: Throughput（吞吐量）

**一句话定义**：单位时间内系统完成处理的请求数量或生成的 token 数量。

**工程上下文中的意义**：在 LLM Serving 中通常指 tokens/second 或 requests/second，是评估推理框架性能的核心指标之一。高吞吐量意味着 GPU 资源被充分利用，单位算力成本更低。

**和项目的关系**：vLLM 和 SGLang 的核心宣传点都是"高吞吐量"，是本书对比各框架时的主要性能维度。

**易混淆点**：Throughput 和 Latency（延迟）往往需要权衡。追求极致吞吐量可能增加单个请求的排队等待；追求低延迟可能限制 batch size，降低整体吞吐。

---

### Term 3: Latency（延迟）

**一句话定义**：从请求发出到收到完整响应所经历的时间，通常以 P50/P99 毫秒计。

**工程上下文中的意义**：对交互式应用（聊天机器人、代码补全）至关重要，直接影响用户体验。LLM Serving 的延迟由 prefill 延迟（输入处理）和 decode 延迟（逐 token 生成）共同构成。

**和项目的关系**：SGLang 宣传 ITL（Inter-Token Latency）作为 SLO 目标，vLLM 也在 benchmark 中强调 P99 latency，是框架比较的必测指标。

**易混淆点**：Latency 有不同粒度——首 token 时间（TTFT）vs 整体响应时间，容易在不做区分的情况下被混用导致误解。

---

### Term 4: Token Throughput

**一句话定义**：系统每秒生成的 token 总数，是 LLM 推理中衡量吞吐量最常用的具体指标。

**工程上下文中的意义**：计算方式：并发请求数 × 每个请求的 token 生成速度。影响因素包括 batch size、模型大小、显存容量、attention 效率。优化手段有 continuous batching、tensor parallelism、paged attention 等。

**和项目的关系**：vLLM 和 SGLang 的 benchmark 报告中均以 token/s 作为核心数字，也是 Mooncake 等分布式架构优化的目标。

**易混淆点**：Token Throughput 不等于 Request Throughput——一个含 1000 token 输出的请求和含 10 token 输出的请求消耗算力差异巨大，但都只算 1 个 request。

---

### Term 5: KV Cache

**一句话定义**：Transformer 自回归解码过程中，存储已经计算过的 Key-Value 矩阵以避免重复注意力计算的高速显存缓存。

**工程上下文中的意义**：在自回归生成中，每个新 token 都需要 attend 到之前所有 token。如果没有 KV Cache，每次生成都要重新计算，造成 O(n²) 复杂度浪费。KV Cache 将历史 K/V 矩阵保存在显存中，新 token 只需计算一次新增的注意力。

**和项目的关系**：PagedAttention（vLLM）和 RadixAttention（SGLang）的核心都是优化 KV Cache 的管理——vLLM 通过分页减少显存碎片，SGLang 通过前缀共享减少重复缓存。

**易混淆点**：KV Cache 存储在 GPU 显存（VRAM）中，受限于显存大小。KV Cache 容量不足会导致 OOM 或必须丢弃缓存重新计算，两者都有显著性能代价。

---

### Term 6: Batching（批处理）

**一句话定义**：将多个独立请求合并为一个 GPU kernel 一起推理，以提升 GPU 利用率的技术。

**工程上下文中的意义**：GPU 并行度高，单请求推理往往只能利用一小部分算力。Batching 通过将多个请求拼成矩阵（将各自独立的 token 序列 padding 到相同长度）实现单次 kernel 调用处理多条请求，显著提升吞吐。

**和项目的关系**：vLLM 和 SGLang 都采用 batching 作为基础优化手段。

**易混淆点**：静态 batching（Static Batching）和动态 batching（Continuous Batching）差别很大——静态 batching 在请求到达时整批处理，可能因 padding 造成大量算力浪费；continuous batching 以单次生成 token 为粒度动态入队/出队，是生产环境的主流做法。

---

### Term 7: Continuous Batching

**一句话定义**：以单次 token 生成（iteration）作为调度粒度，在每个 step 动态将已完成推理的请求移出批次、插入新到达请求的 batching 策略。

**工程上下文中的意义**：相比静态 batching，continuous batching 解决了"短请求等待长请求"的调度低效问题，是 LLM Serving 实现高吞吐的关键机制。Orca 论文首次提出，vLLM 和 SGLang 都以此为核心调度器。

**和项目的关系**：vLLM 0.2+ 和 SGLang 均实现了 continuous batching，是两者吞吐性能优异的主要原因之一。

**易混淆点**：Continuous batching 不等于"一直做 batching"——它有明确的调度粒度（每生成一个 token 调度一次），实现复杂度高，调度开销在极短序列场景下不可忽视。

---

### Term 8: Prefill

**一句话定义**：LLM 推理的第一阶段，将输入 prompt 的所有 token 一次性通过模型计算出第一个 output token 的过程。

**工程上下文中的意义**：Prefill 阶段处理完整 prompt，计算量与输入序列长度成正比。长 prompt 的 prefill 是延迟的主要来源。由于可以充分并行，是 GPU 利用率最高的阶段。Prefill 和 Decode 阶段的特性差异是 PD 分离（Prefill-Decode Disaggregation）优化的基础。

**和项目的关系**：SGLang 的 Chunked Prefill 将过长 prefill 分块避免阻塞；PD 分离将 prefill 和 decode 部署在不同硬件上，都是围绕 prefill 特性的优化。

**易混淆点**：容易把 prefill 等同于"输入处理"。实际上 prefill 的输出是第一个 token（有时也叫"首次解码"），之后才是 decode 循环。不要把 prefill 误解为仅仅是"把 prompt 放进模型"。

---

### Term 9: Decode

**一句话定义**：LLM 推理的第二阶段，自回归地逐 token 生成输出序列的循环过程。

**工程上下文中的意义**：每个新 token 的生成都需要 attend 到 KV Cache 中所有已缓存的 token（来自 prefill 和之前的 decode step）。Decode 是延迟敏感的部分——因为是逐 token 串行生成，无法像 prefill 那样充分并行。Decode 阶段显存访问量大，是 batching 优化的主要受益阶段。

**和项目的关系**：Decode 是 vLLM PagedAttention 显存管理的核心场景；SGLang 的 Decode 优化依赖 RadixAttention 前缀共享减少重复计算。

**易混淆点**：Decode 不是"解码"（decoding），虽然中文常用"解码"指代它。Decode 阶段生成的是 token_id，需要经过 tokenizer 转换才是可读文本。

---

### Term 10: Router（请求路由）

**一句话定义**：在多模型或多副本部署场景下，将用户请求分发到合适推理实例的调度组件。

**工程上下文中的意义**：Router 可以基于负载（least-loaded）、基于模型版本（canary routing）、基于请求特征（prompt 长度、是否带附件）做智能路由。高级 Router 还支持多 LoRA 动态加载、多租户隔离。Router 是 AI Gateway 的核心组件，也是 disaggregated serving（分离式部署）中连接前端和推理集群的枢纽。

**和项目的关系**：SGLang 和 vLLM 都没有内置 Router，但它们提供的 OpenAI 兼容接口使 Router 层的实现更容易对接。Router 在 comparison-index 和 ai-gateway 章节中会深入讨论。

**易混淆点**：Router 不等于 Load Balancer（负载均衡器）。Load Balancer 通常只看机器负载，Router 可以感知请求内容、模型特性、KV Cache 状态做更智能的决策。

---

Sources:
1. vLLM 官方文档（https://docs.vllm.ai/）— PagedAttention / Scheduling 说明
2. SGLang 官方文档（https://docs.sglang.ai/）— RadixAttention / Continuous Batching 说明
3. Orca 论文（"Orca: A Distributed Serving System for Transformer-Based Generative Models"，OSDI 2022）— Continuous Batching 起源
4. PagedAttention 官方 blog（https://www.vllm.ai/）— KV Cache 分页管理概念
5. SGLang GitHub Issue #10813 — PD-Multiplexing 中 TTFT/ITL 定义
6. "How does LLM Serving Work" 技术博客（各框架 README 引用的背景材料）— Serving 概念梳理
7. LLM Serving 综述（vLLM / SGLang / TensorRT-LLM 各框架 README）— 术语一致性对照

Risk of Staleness:
- Continuous Batching 的具体实现细节（调度频率、padding 策略）各框架版本间有差异
- "Orca 论文首次提出 continuous batching"——如果后续有更早来源，Codex 需做文献调研纠正
- Router 在 disaggregated serving 中的具体形态（Agentic / Microservice / Sidecar）尚未收敛，术语解释偏重通用理解

Out of Scope Kept:
- 未扩展为完整章节（每个术语限制在 4 项结构内）
- 未做性能对比
- 未延伸训练侧术语

Need Codex Review On:
- Continuous Batching 的"Orca 首发"说法是否准确，Codex 需核实
- Router 在 Agentic AI 场景下的新语义（带 memory / tool-use）是否需要单独章节补充
- "易混淆点"中 decode ≠ 解码的说法在中文语境是否通行（中文社区常混用"解码"指代 decode），Codex 需确认用词规范
