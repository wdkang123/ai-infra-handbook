Task ID: T153
Task Title: 收紧 glossary 第二批术语中的弱来源与高推断项
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 T143 结果和 T143-review-round-2 修订。只修 Canary Routing、Tracing、Replay 共 3 项，换更直接来源，收回过强推断。

Result:

---

### Term 17: Canary Routing（金丝雀路由）

**一句话定义**：将少量请求导向新模型版本（canary），逐步验证新版本稳定性的流量分发策略。

**工程上下文中的意义**：Canary routing 通常将 5% ~ 10% 的流量导向新版本，90% ~ 95% 保留在稳定版本。通过对比 canary 和 control 的指标（延迟、错误率）判断新版本是否可全量上线。相比 blue-green deployment，canary 更节省资源，适合 LLM 这种难以做精确 A/B 测试的场景。

**和项目的关系**：Router 层（作为 AI Gateway 的一部分）负责实现 canary routing。vLLM 和 SGLang 提供 OpenAI 兼容接口，使 canary routing 的上游接入更标准化。

**易混淆点**：Canary routing 不等于 A/B testing。A/B testing 通常基于用户特征或实验配置做固定流量分配，canary 则更偏向"先放少量看稳定性"。

**来源**：Canary routing 作为软件工程通用部署策略，可参考 CNCF Glossary：https://glossary.cncf.io/canary-deployment/（云原生部署模式通用术语，非厂商特定）

---

### Term 19: Tracing（链路追踪）

**一句话定义**：记录请求在分布式系统中从入口到出口各环节的耗时和元数据的观测技术，用于定位延迟瓶颈和排查故障。

**工程上下文中的意义**：在 LLM Serving 中，一次请求可能经过：Gateway → Router → 模型推理 → KV cache → token 生成等多个环节。Tracing 通过为每个请求生成唯一 trace ID，在各环节记录 span，实现全链路可观测性。常见实现基于 OpenTelemetry，支持 Jaeger/Zipkin 等后端。

**和项目的关系**：Triton IS 提供 Prometheus metrics 端点，可作为 tracing 系统的数据源之一。vLLM 和 SGLang 在 tracing 方面的内置支持有限，通常依赖外部 sidecar 或 Gateway 层实现可观测性。

**易混淆点**：Tracing 不等于 metrics/monitoring。Metrics 关注聚合数值（QPS、P99 latency），Tracing 关注单个请求的完整路径。两者互补，metrics 高点后需要 tracing 向下钻取。

**来源**：OpenTelemetry 官方定义：https://opentelemetry.io/docs/concepts/observability-primer/#distributed-traces（OpenTelemetry 为 CNCF 项目，是 tracing 领域的主要标准）

---

### Term 20: Replay（回放）

**一句话定义**：用历史真实请求数据重放以验证系统行为或测试新版本的测试方法。

**工程上下文中的意义**：在 LLM Serving 场景，replay 通常用 production 流量的采样数据（保留用户 prompt，去除隐私信息）在 staging 环境重放，用于：1）测试新版本的正确性；2）验证性能优化效果；3）模拟峰值负载。Replay 数据的多样性直接决定了测试质量——单一 prompt 的 replay 无法覆盖长尾场景。

**和项目的关系**：Replay 可用于 eval-module 的测试流程，配合 staging 环境和版本化模型实现回归验证。

**易混淆点**：Replay 不等于 benchmark。Benchmark 使用固定测试集，replay 使用真实流量的采样。Benchmark 适合测性能上限，replay 适合测真实场景下的稳定性。

**来源**：Replay 作为测试工程通用概念，可参考 Google SRE Book（Production Testing 章节）：https://sre.google/sre-book/production-testing/（工程实践通用方法，非特定工具文档）

---

Sources（修订后精确 URL 汇总）：
1. https://glossary.cncf.io/canary-deployment/ — Canary Routing 通用术语定义
2. https://opentelemetry.io/docs/concepts/observability-primer/#distributed-traces — OpenTelemetry Tracing 定义
3. https://sre.google/sre-book/production-testing/ — Replay/生产测试工程实践

Risk of Staleness:
- CNCF Glossary 和 OpenTelemetry 为行业标准文档，稳定性较高
- Google SRE Book 概念更新周期较长

Out of Scope Kept:
- 仅修订了 3 项，其余项未改动
- 未扩写成章节

Need Codex Review On:
- CNCF Glossary 作为来源是否足够权威（还是需要更特定的厂商文档）
