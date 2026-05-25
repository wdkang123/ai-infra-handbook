Task ID: T124
Title: 收紧 glossary 中 Router 术语的高波动表述并补精确来源
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
仅修订 Router 术语一项，删除 Agentic AI 扩展表述，用精确 URL 替换模糊组织页来源。

Result:

### Term 10: Router（请求路由）

**一句话定义**：在多模型或多副本部署场景下，将用户请求分发到合适推理实例的调度组件。

**工程上下文中的意义**：Router 可以基于负载（least-loaded）、基于模型版本（canary routing）、基于请求特征（prompt 长度、是否带附件）做智能路由。Router 是 AI Gateway 的核心组件，也是 disaggregated serving（分离式部署）中连接前端和推理集群的枢纽。

**和项目的关系**：vLLM 和 SGLang 都没有内置 Router，但它们提供 OpenAI 兼容接口使 Router 层的实现更容易对接。Router 层的设计在 inference-service 和 ai-gateway 章节中会深入讨论。

**易混淆点**：Router 不等于 Load Balancer。Load Balancer 通常只看机器负载，Router 可以感知请求内容、模型特性、KV Cache 状态做更智能的决策。

**来源**：
- https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html — vLLM OpenAI 兼容接口文档（Router 作为服务层上游的接入点）
- https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/model_repository.html — NVIDIA Triton IS 模型仓库文档（作为 Router 在推理服务架构中角色的参考背景）

Sources:
1. https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html — vLLM OpenAI 兼容接口
2. https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/model_repository.html — Triton IS 模型仓库（Router 功能参考背景）

Risk of Staleness:
- Router 作为独立组件在快速演进，精确定义以各框架文档为准

Out of Scope Kept:
- 未扩展 Agentic AI 场景下的 memory/tool-use 语义
- 未重写其余 9 项

Need Codex Review On:
- Router 在 Agentic AI 场景下的新语义是否需要在 glossary 中单独说明，还是保持当前通用定义
