Task ID: T164
Task Title: 产出 gateway / cache / router sources-index v1
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 T181（AI Gateway）、T182（Cache）、T183（Router）收紧版，产出 sources-index v1，按三组分组建索引。

Result:

## AI Gateway

### 官方入口

- Portkey Gateway：https://github.com/Portkey-AI/gateway
- APIPark：https://github.com/APIParkLab/APIPark
- LiteLLM Proxy：https://github.com/BerriAI/litellm
- Cloudflare AI Gateway：https://developers.cloudflare.com/ai-gateway/

### 边界说明
AI Gateway 是统一接入多模型供应商的代理层，负责流量管理、安全、观测。Router 是其内部组件或独立进程。云厂商托管服务（如 AWS Bedrock）不属于通用 AI Gateway 范畴。

### 优先阅读链接（4 个）

1. **Portkey Gateway GitHub** — https://github.com/Portkey-AI/gateway
2. **APIPark GitHub** — https://github.com/APIParkLab/APIPark
3. **LiteLLM Proxy GitHub** — https://github.com/BerriAI/litellm
4. **Cloudflare AI Gateway 文档** — https://developers.cloudflare.com/ai-gateway/

---

## Cache / Prefix Caching / Semantic Cache

### 官方入口

- vLLM（PagedAttention）：https://github.com/vllm-project/vllm
- SGLang（RadixAttention）：https://github.com/sgl-project/sglang
- LMCache：https://github.com/LMCache/LMCache
- GPTCache：https://github.com/zilliztech/GPTCache
- Redis Vector：https://redis.io/docs/interact/vector-embeddings/

### 边界说明
KV Cache 是底层数据结构，Prefix Caching 是引擎层共享前缀 KV 块，Semantic Cache 是应用层向量相似度匹配。三者分层：应用层 → Prefix Caching → KV Cache。

### 优先阅读链接（5 个）

1. **vLLM GitHub** — https://github.com/vllm-project/vllm
2. **SGLang RadixAttention 文档** — https://docs.sglang.ai/backend/index.html
3. **LMCache GitHub** — https://github.com/LMCache/LMCache
4. **GPTCache GitHub** — https://github.com/zilliztech/GPTCache
5. **Redis Vector 文档** — https://redis.io/docs/interact/vector-embeddings/

---

## Router / Model Routing

### 官方入口

- NVIDIA llm-router：https://github.com/NVIDIA-AI-Blueprints/llm-router
- LiteLLM Proxy（路由功能）：https://github.com/BerriAI/litellm
- Portkey Gateway（路由功能）：https://github.com/Portkey-AI/gateway

### 边界说明
Router 根据请求特征分发到后端模型实例，是 AI Gateway 的核心组件之一。vLLM/SGLang 是被路由的后端推理引擎，本身不是 Router。

### 优先阅读链接（3 个）

1. **NVIDIA llm-router GitHub** — https://github.com/NVIDIA-AI-Blueprints/llm-router
2. **LiteLLM Routing 文档** — https://docs.litellm.ai/docs/proxy_router
3. **Portkey Gateway GitHub** — https://github.com/Portkey-AI/gateway

Sources:
1. https://github.com/Portkey-AI/gateway — Portkey Gateway
2. https://github.com/APIParkLab/APIPark — APIPark
3. https://github.com/BerriAI/litellm — LiteLLM
4. https://developers.cloudflare.com/ai-gateway/ — Cloudflare AI Gateway
5. https://github.com/vllm-project/vllm — vLLM
6. https://docs.sglang.ai/backend/index.html — SGLang RadixAttention
7. https://github.com/LMCache/LMCache — LMCache
8. https://github.com/zilliztech/GPTCache — GPTCache
9. https://redis.io/docs/interact/vector-embeddings/ — Redis Vector
10. https://github.com/NVIDIA-AI-Blueprints/llm-router — NVIDIA LLM Router
11. https://docs.litellm.ai/docs/proxy_router — LiteLLM Routing

Risk of Staleness:
- 各开源项目更新频繁，具体版本以实际为准

Out of Scope Kept:
- 未扩写成章节
- 未做优劣排名
- 未写架构结论
