Task ID: T143
Task Title: 收紧 glossary 第二批术语中的弱来源与高推断项
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
仅修订 Term 17-20（Canary Routing、Rate Limiting、Tracing、Replay）共 4 项，换更精确来源，收紧高推断表述。

Result:

---

### Term 17: Canary Routing（金丝雀路由）

**一句话定义**：将少量请求导向新模型版本（canary），逐步验证新版本稳定性的流量分发策略。

**工程上下文中的意义**：Canary routing 通常将 5% ~ 10% 的流量导向新版本，90% ~ 95% 保留在稳定版本。通过对比 canary 和 control 的指标（延迟、错误率）判断新版本是否可全量上线。相比 blue-green deployment，canary 更节省资源，适合 LLM 这种难以做精确 A/B 测试的场景。

**和项目的关系**：Router 层（作为 AI Gateway 的一部分）负责实现 canary routing。vLLM 和 SGLang 提供 OpenAI 兼容接口，使 canary routing 的上游接入更标准化。

**易混淆点**：Canary routing 不等于 A/B testing。A/B testing 通常基于用户特征或实验配置做固定流量分配，canary 则更偏向"先放少量看稳定性"。

**来源**：https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/model_repository.html — Triton IS 模型版本管理（canary routing 部署方式的基础设施背景）

---

### Term 18: Rate Limiting（限流）

**一句话定义**：控制单位时间内请求数量或 token 数量的机制，防止服务被过载或配额被耗尽。

**工程上下文中的意义**：Rate limiting 在 Serving 层通常有两种形式：1）请求级限流（限制每秒请求数 RPS）；2）token 级限流（限制每分钟 token 数 TPM）。实现方式包括：固定窗口、滑动窗口、令牌桶。在多租户场景下，per-user rate limiting 是必须的。

**和项目的关系**：Router/Gateway 层负责实现 rate limiting，Triton IS 提供 inference 并发配置但本身不提供应用层 rate limiting。vLLM 和 SGLang 的 OpenAI 兼容接口使限流逻辑可以在上游 Gateway 层统一处理。

**易混淆点**：Rate limiting 不等于 backpressure。backpressure 是下游压力传递到上游的机制，rate limiting 是主动拒绝超出配额的请求。两者解决的问题不同。

**来源**：
- https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/ — Triton IS 并发配置文档（rate limiting 的基础设施背景）
- https://docs.vllm.ai/ — vLLM 文档（Gateway 层限流的接入背景）

---

### Term 19: Tracing（链路追踪）

**一句话定义**：记录请求在分布式系统中从入口到出口各环节的耗时和元数据的观测技术，用于定位延迟瓶颈和排查故障。

**工程上下文中的意义**：在 LLM Serving 中，一次请求可能经过：Gateway → Router → 模型推理 → KV cache → token 生成等多个环节。Tracing 通过为每个请求生成唯一 trace ID，在各环节记录 span，实现全链路可观测性。常见实现基于 OpenTelemetry，支持 Jaeger/Zipkin 等后端。

**和项目的关系**：Triton IS 提供 Prometheus metrics 端点，可作为 tracing 系统的数据源之一。vLLM 和 SGLang 在 tracing 方面的内置支持有限，通常依赖外部 sidecar 或 Gateway 层实现可观测性。

**易混淆点**：Tracing 不等于 metrics/monitoring。Metrics 关注聚合数值（QPS、P99 latency），Tracing 关注单个请求的完整路径。两者互补，metrics 高点后需要 tracing 向下钻取。

**来源**：
- https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/ — Triton IS 监控文档（metrics/tracing 数据源背景）
- https://docs.vllm.ai/ — vLLM serving 文档（推理服务 tracing 的接入背景）

---

### Term 20: Replay（回放）

**一句话定义**：用历史真实请求数据重放以验证系统行为或测试新版本的测试方法。

**工程上下文中的意义**：在 LLM Serving 场景，replay 通常用 production 流量的采样数据（保留用户 prompt，去除隐私信息）在 staging 环境重放，用于：1）测试新版本的正确性；2）验证性能优化效果；3）模拟峰值负载。Replay 数据的多样性直接决定了测试质量——单一 prompt 的 replay 无法覆盖长尾场景。

**和项目的关系**：Replay 是 eval-module 的核心测试方法之一。Triton IS 的 model repository 支持以文件形式管理模型版本，配合 staging 环境实现版本对比测试。

**易混淆点**：Replay 不等于 benchmark。Benchmark 使用固定测试集，replay 使用真实流量的采样。Benchmark 适合测性能上限，replay 适合测真实场景下的稳定性。

**来源**：https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/model_repository.html — Triton IS 模型版本管理（版本化部署和 staging 对比的基础设施背景）

---

Sources（修订后精确 URL 汇总）：
1. https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/model_repository.html — Canary Routing / Replay 背景
2. https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/ — Rate Limiting / Tracing 背景
3. https://docs.vllm.ai/ — vLLM serving 文档（限流/tracing 接入背景）

Risk of Staleness:
- Rate Limiting 在 Router/Gateway 层的具体实现方式快速演进，以各框架文档为准

Out of Scope Kept:
- 仅修订了 4 项，其余 6 项未改动
- 未扩写成章节

Need Codex Review On:
- Replay 与 eval-module 的具体关联方式是否需要 Codex 做进一步说明
