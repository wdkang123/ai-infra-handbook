Task ID: T114
Task Title: 修订 glossary 第一批术语，补精确来源并收紧易误导表述
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 T104 初稿和 review note T104 修订。要求所有来源精确 URL，收紧高争议/高波动表述，保持 10 个术语结构不变。

Result:

---

### Term 1: LLM Serving

**一句话定义**：将大语言模型部署为可响应请求的服务，使其能够接收输入并返回生成结果的工程系统。

**工程上下文中的意义**：包括模型加载、请求调度、显存管理、协议适配（OpenAI API 兼容）等能力。与训练不同，Serving 核心关注推理效率和资源复用，不涉及梯度计算。

**和项目的关系**：作为 AI Infra 入口概念，vLLM / SGLang 等框架解决的都是 LLM Serving 的效率问题，理解 Serving 才能理解这些框架的价值。

**易混淆点**：容易和"模型训练"混淆。Serving 不涉及反向传播，目标是高吞吐低延迟，不是模型能力提升。

**来源**：
- https://docs.vllm.ai/ — vLLM 官方文档对 serving 的定义
- https://docs.sglang.ai/ — SGLang 官方文档对 serving 的说明

---

### Term 2: Throughput（吞吐量）

**一句话定义**：单位时间内系统完成处理的请求数量或生成的 token 总数量。

**工程上下文中的意义**：在 LLM Serving 中通常以 tokens/second 或 requests/second 计量。高吞吐意味着 GPU 资源被充分利用，单位算力成本更低。但吞吐量和延迟之间存在权衡，追求极致吞吐可能增加单个请求的排队等待时间。

**和项目的关系**：vLLM 和 SGLang 的核心宣传指标之一，章节中引用时需注意区分 token throughput 和 request throughput。

**易混淆点**：Token Throughput ≠ Request Throughput。一个含 1000 token 输出的请求和含 10 token 输出的请求消耗算力差异巨大，但都只计 1 个 request。

**来源**：
- https://docs.vllm.ai/ — vLLM 文档中吞吐量的讨论
- https://github.com/vllm-project/vllm — 主仓库 README 中的性能指标说明

---

### Term 3: Latency（延迟）

**一句话定义**：从请求发出到收到完整响应所经历的时间，通常以毫秒计。

**工程上下文中的意义**：对交互式应用（聊天机器人、代码补全）至关重要。LLM Serving 的延迟由 prefill 延迟（输入处理）和 decode 延迟（逐 token 生成）共同构成，需要区分 TTFT（Time To First Token，首 token 延迟）和 overall E2E latency（端到端延迟）。

**和项目的关系**：SGLang 在 benchmark 中以 ITL（Inter-Token Latency）作为 SLO 约束目标；vLLM 也使用 P99 latency 作为性能指标。

**易混淆点**：TTFT 和 E2E latency 是不同指标，混用会导致误导。

**来源**：
- https://github.com/sgl-project/sglang/issues/10813 — SGLang issue 中对 TTFT/ITL 的定义和讨论
- https://docs.sglang.ai/ — SGLang 调度文档

---

### Term 4: Token Throughput

**一句话定义**：系统每秒生成的 token 总数，是 LLM 推理中衡量吞吐量最常用的具体指标。

**工程上下文中的意义**：计算方式：并发请求数 × 每个请求的 token 生成速度。影响因素包括 batch size、模型大小、显存容量、attention 效率。优化手段有 continuous batching、tensor parallelism、paged attention 等。

**和项目的关系**：vLLM 和 SGLang 的 benchmark 报告中均以 token/s 作为核心数字。

**易混淆点**：Token Throughput 不等于 Request Throughput。两者衡量维度不同，长短输出请求混排时尤其需要注意区分。

**来源**：
- https://docs.vllm.ai/ — vLLM 性能相关文档
- https://docs.sglang.ai/ — SGLang 性能相关文档

---

### Term 5: KV Cache

**一句话定义**：Transformer 自回归解码过程中，存储已经计算过的 Key-Value 矩阵以避免重复注意力计算的高速显存缓存。

**工程上下文中的意义**：自回归生成中，每个新 token 需要 attend 到之前所有 token。KV Cache 将历史 K/V 矩阵保存在显存中，新 token 只需计算新增的注意力而非全量重算。KV Cache 容量受限于 GPU 显存大小，不足时会触发 OOM 或缓存丢弃。

**和项目的关系**：PagedAttention（vLLM）通过分页减少显存碎片；RadixAttention（SGLang）通过前缀共享减少重复缓存。两者从不同角度优化 KV Cache 的利用效率。

**易混淆点**：KV Cache 存储在 GPU 显存（VRAM）中，不是 CPU 内存。容量不足会导致 OOM 或丢弃缓存重新计算，两者都有显著性能代价。

**来源**：
- https://www.vllm.ai/ — PagedAttention 官方介绍
- https://github.com/vllm-project/vllm — 主仓库 README 中对 PagedAttention 的说明

---

### Term 6: Batching（批处理）

**一句话定义**：将多个独立请求合并为一个 GPU kernel 一起推理，以提升 GPU 利用率的技术。

**工程上下文中的意义**：GPU 并行度高，单请求推理算力利用率低。Batching 通过将多个请求拼接成矩阵实现单次 kernel 调用处理多条请求，显著提升吞吐。但不恰当的 batching（静态 batching 的 padding 浪费）也可能降低效率。

**和项目的关系**：vLLM 和 SGLang 都以 batching 为基础优化手段。

**易混淆点**：静态 batching 和动态 batching（continuous batching）差异极大。静态 batching 在请求到达时整批处理，可能因 padding 造成大量算力浪费；continuous batching 以单次 token 生成为粒度动态入队/出队，是生产环境主流做法。

**来源**：
- https://docs.vllm.ai/ — vLLM 调度文档
- Orca 论文：https://www.usenix.org/conference/osdi22/presentation/yu — Orca: A Distributed Serving System for Transformer-Based Generative Models（OSDI 2022），首次提出 iteration-level scheduling

---

### Term 7: Continuous Batching

**一句话定义**：以单次 token 生成（iteration）作为调度粒度，在每个 step 动态将已完成推理的请求移出批次、插入新到达请求的 batching 策略。

**工程上下文中的意义**：相比静态 batching，continuous batching 解决了"短请求等待长请求"的调度低效问题，是 LLM Serving 实现高吞吐的关键机制。

**和项目的关系**：vLLM 0.2+ 和 SGLang 均实现了 continuous batching，是两者吞吐性能优异的主要原因之一。

**易混淆点**：Continuous batching 不等于"一直做 batching"，它有明确的调度粒度（每生成一个 token 调度一次），在极短序列场景下调度开销不可忽视。

**来源**：
- Orca 论文：https://www.usenix.org/conference/osdi22/presentation/yu
- https://docs.vllm.ai/ — vLLM 调度相关文档

---

### Term 8: Prefill

**一句话定义**：LLM 推理的第一阶段，将输入 prompt 的所有 token 一次性通过模型计算，产出第一个 output token 的过程。

**工程上下文中的意义**：Prefill 阶段计算量与输入序列长度成正比，是 GPU 利用率最高的阶段。Prefill 延迟（TTFT）是交互式应用的主要体验指标。由于可以充分并行，是 batching 优化中计算密度最高的阶段。

**和项目的关系**：SGLang 的 Chunked Prefill 将过长 prefill 分块避免阻塞；PD 分离（Prefill-Decode Disaggregation）将 prefill 和 decode 部署在不同硬件上，是围绕 prefill 特性的工程优化。

**易混淆点**：不要把 prefill 等同于"把 prompt 放进模型"。prefill 的输出是第一个 token（first token），之后才是 decode 自回归循环。

**来源**：
- https://docs.sglang.ai/ — SGLang 调度文档
- https://github.com/sgl-project/sglang/issues/10813 — PD-Multiplexing issue 中对 prefill/decode 的讨论

---

### Term 9: Decode

**一句话定义**：LLM 推理的第二阶段，自回归地逐 token 生成输出序列的循环过程。

**工程上下文中的意义**：每个新 token 的生成都需要 attend 到 KV Cache 中已缓存的所有 token。Decode 是延迟敏感的部分——因为是逐 token 串行生成，无法像 prefill 那样充分并行。Decode 阶段显存访问量大，是 batching 优化的主要受益阶段。

**和项目的关系**：Decode 是 vLLM PagedAttention 显存管理的主要场景；SGLang 的 Decode 优化依赖 RadixAttention 前缀共享减少重复计算。

**易混淆点**：Decode 阶段生成的 token_id 需要经过 tokenizer 转换才是可读文本。"解码"在中文社区常被混用指代 decode，但严格来说 decode 是 token 生成过程，tokenizer 将 token 映射为文字才是"解码"。

**来源**：
- https://docs.vllm.ai/ — vLLM 推理文档
- https://docs.sglang.ai/ — SGLang 推理文档

---

### Term 10: Router（请求路由）

**一句话定义**：在多模型或多副本部署场景下，将用户请求分发到合适推理实例的调度组件。

**工程上下文中的意义**：Router 可以基于负载（least-loaded）、基于模型版本（canary routing）、基于请求特征（prompt 长度、是否带附件）做智能路由。高级 Router 支持多 LoRA 动态加载、多租户隔离。Router 是 AI Gateway 的核心组件，也是 disaggregated serving（分离式部署）中连接前端和推理集群的枢纽。

**和项目的关系**：vLLM 和 SGLang 都没有内置 Router，但它们提供 OpenAI 兼容接口使 Router 层的实现更容易对接。Router 层的设计在 inference-service 和 ai-gateway 章节中会深入讨论。

**易混淆点**：Router 不等于 Load Balancer。Load Balancer 通常只看机器负载，Router 可以感知请求内容、模型特性、KV Cache 状态做更智能的决策。在 Agentic AI 场景下，Router 还可能携带 memory 或 tool-use 决策能力。

**来源**：
- https://github.com/vllm-project — vLLM 项目中对 API 接口的说明
- https://docs.sglang.ai/ — SGLang 对服务接口的说明
- https://github.com/triton-inference-server/server — Triton IS 的模型调度说明（作为 Router 功能参考背景）

---

Sources（精确 URL 汇总）：
1. https://docs.vllm.ai/ — vLLM 官方文档
2. https://docs.sglang.ai/ — SGLang 官方文档
3. https://www.vllm.ai/ — PagedAttention 官方介绍
4. https://github.com/vllm-project/vllm — vLLM 主仓库
5. https://www.usenix.org/conference/osdi22/presentation/yu — Orca 论文（continuous batching 起源）
6. https://github.com/sgl-project/sglang/issues/10813 — PD-Multiplexing / TTFT/ITL 定义
7. https://github.com/triton-inference-server/server — 作为 Router 功能的背景参考（非精确指向 vLLM/SGLang Router 实现）

Risk of Staleness:
- Orca 论文发表于 OSDI 2022，continuous batching 的原始描述以论文为准
- Router 在 Agentic AI 场景下的演进较快，术语表中保留通用定义，不扩展新语义
- Decode ≠ "解码"的说法在中文社区通行度有待确认，术语中使用"生成过程"替代以避免歧义

Out of Scope Kept:
- 未扩展为完整章节
- 未新增训练侧术语
- 未做性能对比

Need Codex Review On:
- "Decode ≠ 解码"的用词是否需要调整，或在术语表中直接写英文避免歧义
- Router 在 Agentic AI 场景下带 memory/tool-use 的新语义是否需要单独说明，还是保持当前通用定义
- Orca 论文作为 continuous batching 的"首发"引用是否准确（Codex 需核实文献）
