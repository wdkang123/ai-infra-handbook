Task ID: T133
Task Title: Glossary 第二批术语初稿
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
围绕推理服务与平台治理，产出 10 个核心术语初稿，每个术语含一句话定义、工程上下文意义、和项目的关系、易混淆点。

Result:

---

### Term 11: TTFT（Time To First Token）

**一句话定义**：从请求发出到模型产出第一个 token 所经历的时间，是 LLM 交互式应用的首要体验指标。

**工程上下文中的意义**：TTFT 主要受 prefill 阶段（输入 prompt 的计算）影响，也受请求调度队列等待时间影响。对话式应用中，用户感知到的"响应快慢"很大程度上就是 TTFT。优化手段包括：减少 prefill 计算量（ quantization、KV cache 压缩）、chunked prefill 避免长 prompt 阻塞、PD 分离将 prefill 和 decode 部署在不同硬件上。

**和项目的关系**：SGLang 在 benchmark 中明确以 ITL（Inter-Token Latency）和 TTFT 作为 SLO 约束目标；vLLM 通过 paged attention 减少 prefill 阶段的显存管理开销。

**易混淆点**：TTFT 和整体 E2E latency 是不同指标。TTFT 短不代表整体响应快——一个长输出请求的 E2E latency 可能很高，但 TTFT 依然很快。

**来源**：https://github.com/sgl-project/sglang/issues/10813

---

### Term 12: ITL（Inter-Token Latency）

**一句话定义**：模型在生成阶段相邻两个 token 之间的时间间隔，是衡量生成流畅度的指标。

**工程上下文中的意义**：ITL 直接影响用户感知"打字速度"。ITL 的 P99 值比平均值更重要，因为尾部延迟决定了最坏情况下的体验。对流式输出（streaming）场景，ITL 是核心指标。

**和项目的关系**：SGLang 在 benchmark 中将 ITL 作为 SLO 目标（目标 ITL ≤ 60ms），用于评估 PD-Multiplexing 的调度效果。

**易混淆点**：ITL 和 TTFT 容易在 benchmark 中混用。TTFT 衡量的是"开始速度"，ITL 衡量的是"生成速度"，两者共同构成整体延迟体验。

**来源**：https://github.com/sgl-project/sglang/issues/10813

---

### Term 13: Prefix Caching（前缀缓存）

**一句话定义**：将多个请求共享的输入前缀（system prompt、few-shot examples 等）的 KV cache 缓存起来，避免重复计算的技术。

**工程上下文中的意义**：在多轮对话或结构化 prompt 场景中，多个请求经常共享相同的前缀。前缀缓存通过识别共享前缀，只计算一次，显著减少重复计算和显存占用。实现上通常依赖 Radix Tree 等数据结构管理缓存。

**和项目的关系**：SGLang 的 RadixAttention 是前缀缓存的具体实现，在多轮对话和 Agent 场景下效果显著。vLLM 的 prefix caching 在特定场景下也有实现。

**易混淆点**：前缀缓存不等于 KV cache。前缀缓存是 KV cache 的一种利用模式——通过识别共享前缀来复用已有的 cache，而不是新建独立的 cache。

**来源**：https://docs.sglang.ai/ — SGLang 文档中 RadixAttention 的描述

---

### Term 14: Tensor Parallelism（张量并行）

**一句话定义**：将模型的单层权重矩阵按行/列切分到多个 GPU 上并行计算，以突破单卡显存和算力限制的技术。

**工程上下文中的意义**：Transformer 的矩阵乘法（`Y = XW`）中，当 `W` 过大无法放入单卡时，可将 `W` 切分到 N 个 GPU 并行计算，最后汇总结果。Tensor Parallelism（TP）通常需要高速互联（NVLink）以避免通信开销。常见配置为 TP=2/4/8。TP 通信在每次 Transformer 层内发生，是延迟敏感场景的瓶颈之一。

**和项目的关系**：vLLM 和 SGLang 都支持 Tensor Parallelism。SGLang 在 DeepSeek 部署中结合 Expert Parallelism 使用，vLLM 通过 PyTorch 的 FSDP 风格的 TP 实现。

**易混淆点**：Tensor Parallelism 不等于 Data Parallelism。前者将同一层的权重切分到多卡，后者将不同请求放到不同卡上独立处理。

**来源**：
- https://docs.vllm.ai/ — vLLM 并行推理文档
- https://docs.sglang.ai/ — SGLang 并行推理文档

---

### Term 15: Data Parallelism（数据并行）

**一句话定义**：将不同请求或不同数据样本分配到不同 GPU 独立处理，每个 GPU 持有完整模型副本，是分布式训练和 Serving 中最常用的横向扩展方式。

**工程上下文中的意义**：Data Parallelism（DP）下，每个 GPU 有完整模型副本，无模型权重通信只有梯度同步（训练场景）或请求分发（Serving 场景）。DP 是最简单的 scale-out 策略，适合高吞吐场景。缺点是每个 GPU 都需要完整模型大小的显存，当模型过大无法放入单卡时需要结合 TP/PP 使用。

**和项目的关系**：SGLang 在 v0.4 中引入了 Data Parallelism Attention（DP Attention）用于 DeepSeek 系列，通过 DP 方式共享 KV Head 避免在每个 TP Worker 中重复计算。

**易混淆点**：DP 和 TP 的组合（TP+DP）容易混淆。在 MoE（Mixture-of-Experts）模型中，DP 和 EP（Expert Parallelism）也需要区分——EP 将不同 expert 放在不同 GPU，DP 复制完整模型。

**来源**：https://lmsys.org/blog/2024-12-04-sglang-v0-4/ — SGLang v0.4 blog 中 DP Attention 的说明

---

### Term 16: Model Repository（模型仓库）

**一句话定义**：以文件系统目录结构组织的模型存储方式，Triton IS 通过读取仓库中的 `config.pbtxt` 和模型权重文件来加载和管理模型。

**工程上下文中的意义**：Model Repository 定义了模型的版本（`/version/` 子目录）、配置（`config.pbtxt`）、输入输出格式、后端类型等。Triton IS 支持同时从多个仓库加载模型。生产部署中，模型仓库通常挂载为 NFS 或对象存储。

**和项目的关系**：Triton IS 使用 Model Repository 作为模型管理的基础抽象；vLLM/SGLang 主要通过 Hugging Face 模型 ID 直接加载，不使用 Triton 的模型仓库模式。

**易混淆点**：Model Repository 不等于模型文件存储——它是一套包含配置和版本管理的模型部署规范，不仅仅是"模型文件放在哪个目录"。

**来源**：https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/model_repository.html

---

### Term 17: Canary Routing（金丝雀路由）

**一句话定义**：将少量请求导向新模型版本（canary），逐步验证新版本稳定性的流量分发策略。

**工程上下文中的意义**：Canary routing 通常将 5% ~ 10% 的流量导向新版本，90% ~ 95% 保留在稳定版本。通过对比 canary 和 control 的指标（延迟、错误率）判断新版本是否可全量上线。相比 blue-green deployment，canary 更节省资源，适合 LLM 这种难以做精确 A/B 测试的场景。

**和项目的关系**：Router 层（作为 ai-gateway 的一部分）负责实现 canary routing。vLLM 和 SGLang 本身不实现路由，但它们的 OpenAI 兼容接口使 Router 实现更容易。

**易混淆点**：Canary routing 不等于 A/B testing。A/B testing 通常基于用户特征或实验配置做固定流量分配，canary 则更偏向"先放少量看稳定性"。

**来源**：https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/model_repository.html — Triton IS 的模型版本管理说明（作为 canary routing 的基础设施背景）

---

### Term 18: Rate Limiting（限流）

**一句话定义**：控制单位时间内请求数量或 token 数量的机制，防止服务被过载或配额被耗尽。

**工程上下文中的意义**：Rate limiting 在 Serving 层通常有两种形式：1）请求级限流（限制每秒请求数 RPS）；2）token 级限流（限制每分钟 token 数 TPM）。实现方式包括：固定窗口、滑动窗口、令牌桶。在多租户场景下，per-user rate limiting 是必须的。

**和项目的关系**：vLLM 和 SGLang 都没有内置完整的 rate limiting 功能，但它们的 OpenAI 兼容接口使限流可以在 Router/Gateway 层实现。Triton IS 本身不提供应用层 rate limiting。

**易混淆点**：Rate limiting 不等于 backpressure。backpressure 是下游压力传递到上游的机制，rate limiting 是主动拒绝超出配额的请求。两者解决的问题不同。

**来源**：
- https://docs.vllm.ai/ — vLLM serving 相关文档
- https://github.com/vllm-project/vllm — vLLM 项目中限流相关的 issue 或设计讨论

---

### Term 19: Tracing（链路追踪）

**一句话定义**：记录请求在分布式系统中从入口到出口各环节的耗时和元数据的观测技术，用于定位延迟瓶颈和排查故障。

**工程上下文中的意义**：在 LLM Serving 中，一次请求可能经过：Gateway → Router → 模型推理 → KV cache → token 生成等多个环节。Tracing 通过为每个请求生成唯一 trace ID，在各环节记录 span，实现全链路可观测性。常见实现基于 OpenTelemetry，支持 Jaeger/Zipkin 等后端。

**和项目的关系**：Triton IS 提供 Prometheus metrics 端点，是 tracing 的数据源之一。vLLM 和 SGLang 在 tracing 方面的内置支持有限，通常依赖外部 sidecar 或 Gateway 层实现。

**易混淆点**：Tracing 不等于 metrics/monitoring。Metrics 关注聚合数值（QPS、P99 latency），Tracing 关注单个请求的完整路径。两者互补，metrics 高点后需要 tracing 向下钻取。

**来源**：https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/ — Triton IS 监控文档

---

### Term 20: Replay（回放）

**一句话定义**：用历史真实请求数据重放以验证系统行为或测试新版本的测试方法。

**工程上下文中的意义**：在 LLM Serving 场景，replay 通常用 production 流量的采样数据（保留用户 prompt，去除隐私信息）在 staging 环境重放，用于：1）测试新版本的正确性；2）验证性能优化效果；3）模拟峰值负载。Replay 数据的多样性直接决定了测试质量——单一 prompt 的 replay 无法覆盖长尾场景。

**和项目的关系**：Triton IS 的 model repository 支持以文件形式管理模型版本，配合 staging 环境实现回放测试；vLLM 和 SGLang 的 benchmark 目录通常有标准测试集，但不提供生产流量 replay 功能。

**易混淆点**：Replay 不等于 benchmark。Benchmark 使用固定测试集，replay 使用真实流量的采样。Benchmark 适合测性能上限，replay 适合测真实场景下的稳定性。

**来源**：https://github.com/triton-inference-server/server — Triton IS 模型版本管理（replay 测试的基础设施背景）

---

Sources（精确 URL 汇总）：
1. https://github.com/sgl-project/sglang/issues/10813 — TTFT / ITL 定义
2. https://docs.sglang.ai/ — SGLang 文档（Prefix Caching / RadixAttention）
3. https://docs.vllm.ai/ — vLLM 并行推理文档
4. https://lmsys.org/blog/2024-12-04-sglang-v0-4/ — SGLang v0.4 DP Attention
5. https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/model_repository.html — Model Repository
6. https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/ — Triton IS 监控文档

Risk of Staleness:
- ITL SLO 目标（≤60ms）来自 SGLang PD-Multiplexing issue，为实验性场景的具体数值，不适合作为通用目标引用
- DP Attention 描述基于 SGLang v0.4 blog，其他框架实现细节可能有差异

Out of Scope Kept:
- 未扩写成完整章节
- 未做性能对比
- 未延伸到训练侧术语

Need Codex Review On:
- ITL 的 SLO 目标值（≤60ms）是否适合作为通用推荐值写入术语表
- Replay 在 AI Infra 项目中的具体实践方式（evals / staging 测试）是否需要 Codex 做进一步说明
