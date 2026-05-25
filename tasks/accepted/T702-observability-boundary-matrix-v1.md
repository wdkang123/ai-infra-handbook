Task ID: T702
Task Title: Observability / Evaluation Deep-Research Pack
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
澄清 tracing/metrics/monitoring/prompt observability 的边界。

Result:

# Observability Boundary Matrix v1

## 边界一：Tracing vs Metrics vs Monitoring

### Tracing（调用链追踪）

| 属性 | 内容 |
|------|------|
| **定义** | 记录请求在分布式系统中的完整调用路径 |
| **粒度** | 请求级 / span 级 |
| **核心数据** | trace_id、span_id、父子关系、时间线 |
| **代表工具** | Jaeger、Zipkin、Langfuse、Phoenix |
| **边界说明** | 适合理解请求路径和延迟瓶颈，不擅长聚合统计 |

### Metrics（指标）

| 属性 | 内容 |
|------|------|
| **定义** | 数值型数据的聚合统计 |
| **粒度** | 时间窗口聚合（QPS、延迟百分位、GPU 利用率） |
| **核心数据** | counter、gauge、histogram |
| **代表工具** | Prometheus、Grafana、云监控 |
| **边界说明** | 适合告警和趋势监控，不擅长理解单请求路径 |

### Monitoring（监控）

| 属性 | 内容 |
|------|------|
| **定义** | metrics + alerting + dashboard 的综合能力 |
| **范围** | 包含 metrics 但不只是 metrics |
| **代表工具** | Grafana + Prometheus、Datadog、云监控 |
| **边界说明** | 监控是上层概念，包含 metrics、logging、tracing 的综合 |

### 边界澄清

- **Tracing 不等于 Monitoring**：Tracing 关注路径，Monitoring 关注聚合
- **Metrics 不等于 Monitoring**：Metrics 是数据，Monitoring 是能力
- **Langfuse** 主要是 Tracing + Metrics（LLM 专用），不完全是通用 Monitoring

来源：https://opentelemetry.io/docs/concepts/signals/traces/
来源：https://prometheus.io/

---

## 边界二：Prompt Observability

### Prompt Observability 定义

| 属性 | 内容 |
|------|------|
| **定义** | 对 LLM 应用的 prompt/response 进行记录、分析和版本管理 |
| **核心能力** | prompt 版本管理、输入输出记录、token 用量统计 |
| **代表工具** | Langfuse、PromptLayer、 Helicone |
| **边界说明** | 专用 LLM 可观测性格，不含通用 tracing |

### Prompt Observability vs General Tracing

| 维度 | Prompt Observability | General Tracing |
|------|---------------------|-----------------|
| **粒度** | prompt / response 级 | span / request 级 |
| **数据** | LLM 特有（prompt、response、token） | 通用（时间、属性） |
| **工具** | Langfuse | Jaeger、Zipkin |
| **与本项目关系** | inference-service / eval-module | 通用微服务 |

### 边界澄清

- **Langfuse** 是 Prompt Observability + Tracing + Metrics 的组合
- **OpenTelemetry** 是通用 Tracing 标准，不专门针对 LLM
- 两者可以结合：OTel 采集 + Langfuse 作为后端

来源：https://langfuse.com/docs/observability/overview

---

## 边界三：Langfuse vs Phoenix vs Grafana

### Langfuse

| 属性 | 内容 |
|------|------|
| **定位** | LLM 专用可观测性平台 |
| **核心能力** | Tracing + Metrics + Prompt 管理 + LLM-as-Judge |
| **优势** | LLM 原生，集成简单 |
| **劣势** | 通用 tracing 能力弱于 Jaeger，metrics 可视化弱于 Grafana |

### Phoenix

| 属性 | 内容 |
|------|------|
| **定位** | LLM trace 分析工具 |
| **核心能力** | Span 可视化、trace 分析、LLM-as-Judge |
| **优势** | Trace 分析深入 |
| **劣势** | 不含 metrics 可视化，self-hosted 能力有限 |

### Grafana / Prometheus

| 属性 | 内容 |
|------|------|
| **定位** | 通用监控可视化 |
| **核心能力** | Metrics 采集存储 + Dashboard + Alerting |
| **优势** | Metrics 能力强，生态成熟 |
| **劣势** | 不含 LLM 专用 tracing，需要额外配置 |

### 选择指引

| 场景 | 推荐组合 |
|------|---------|
| LLM tracing + metrics + prompt 管理 | Langfuse |
| LLM trace 深度分析 | Phoenix（补充） |
| 推理服务 metrics 可视化 | Prometheus + Grafana |
| 完整可观测性 | Langfuse + Prometheus + Grafana |

来源：https://langfuse.com/
来源：https://github.com/Arize-AI/phoenix
来源：https://grafana.com/

---

## 边界四：OTel 标准 vs 工具实现

### OpenTelemetry

| 属性 | 内容 |
|------|------|
| **定位** | CNCF 标准，提供采集规范和 SDK |
| **职责** | 数据采集接口，不直接存储和展示 |
| **数据后端** | Jaeger、Zipkin、Langfuse、Prometheus（均需单独部署） |
| **边界说明** | OTel 是"怎么采"，不是"存哪" |

### 常见混淆

| 混淆 | 事实 |
|------|------|
| "用 OTel 就能看到 traces" | OTel 只是 SDK，需要配合 Jaeger/Langfuse 等后端 |
| "OTel 可以替代 Prometheus" | OTel 主要管 traces，metrics 有专门的 OTel Metrics 但不成熟 |
| "OTel 和 Langfuse 是竞争关系" | OTel 是采集标准，Langfuse 可以作为 OTel 的后端 |

来源：https://opentelemetry.io/

---

## 边界五：Self-hosted vs Cloud

| 维度 | Self-hosted | Cloud |
|------|-------------|-------|
| **数据控制** | 完全自主 | 部分在第三方 |
| **运维复杂度** | 高（需维护服务器/DB） | 低（托管服务） |
| **成本** | 基础设施成本 | 订阅费用 |
| **适用** | 数据敏感场景 | 快速启动 |

来源：https://langfuse.com/docs/
来源：https://arize.com/

Sources:
1. https://opentelemetry.io/ — OpenTelemetry
2. https://langfuse.com/ — Langfuse
3. https://github.com/Arize-AI/phoenix — Phoenix
4. https://grafana.com/ — Grafana
5. https://prometheus.io/ — Prometheus

Risk of Staleness:
- 各工具版本更新可能改变边界

Out of Scope Kept:
- 未写代码实现
- 未写完整平台对比
