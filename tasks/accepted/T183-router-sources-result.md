Task ID: T183
Task Title: 收紧 router 资料包中的坏链接和实现边界
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 T172 结果和 T172-review 修订。修正坏链接，移除 vLLM/SGLang 从 router 实现名单，强化 router 与 backend/gateway 的边界。

Result:

## 一、术语边界说明

### Router / Model Router
在 AI Gateway 层或独立进程中，根据请求特征（如 model name、user id、prompt 内容、cost）将请求导向不同后端模型实例。是 AI Gateway 的核心组件之一。

### Model Routing（模型路由）
根据任务特征（如 prompt 长度、所需能力、延迟/成本预算）动态选择最合适的模型。常见策略包括：
- **Simple routing**：固定路由到指定模型
- **Cost-aware routing**：简单请求路由到小模型降低成本
- **Fallback routing**：主模型失败时路由到备用模型
- **Canary routing**：小比例流量导向新模型版本
- **Traffic split**：按比例拆分流量到不同模型

### 边界划分
- **Router / Model Router**：独立组件或 Gateway 内置模块，负责请求分发策略
- **Backend Inference Engine**（vLLM、SGLang）：被路由的目标，提供 LLM 推理能力，本身不做跨模型的请求分发
- **AI Gateway 平台**：完整解决方案，通常包含 Router 作为其组件之一

## 二、代表性 Router 实现

| 实现 | 类型 | 官方入口 |
|------|------|---------|
| **NVIDIA llm-router** | 开源独立 Router | https://github.com/NVIDIA-AI-Blueprints/llm-router |
| **LiteLLM Proxy** | 开源 Gateway（含路由） | https://github.com/BerriAI/litellm |
| **Portkey Gateway** | 开源 + 云 Gateway（含路由） | https://github.com/Portkey-AI/gateway |

注：vLLM、SGLang 是推理引擎，不是 Router。vLLM 的分布式部署支持多实例负载均衡，但这属于后端工程架构范畴，不是 Router 产品的请求分发策略。

## 三、被路由的后端推理引擎（参考）

| 引擎 | 说明 | 官方入口 |
|------|------|---------|
| **vLLM** | LLM 推理引擎，PagedAttention 优化 | https://github.com/vllm-project/vllm |
| **SGLang** | LLM 推理引擎，RadixAttention 优化 | https://github.com/sgl-project/sglang |

## 四、官方主页 / GitHub / 文档

1. **NVIDIA llm-router**：https://github.com/NVIDIA-AI-Blueprints/llm-router
2. **LiteLLM Proxy**：https://github.com/BerriAI/litellm
3. **Portkey Gateway**：https://github.com/Portkey-AI/gateway
4. **vLLM**：https://github.com/vllm-project/vllm
5. **SGLang**：https://github.com/sgl-project/sglang

## 五、精确优先阅读链接（5 个）

1. **NVIDIA llm-router GitHub**：https://github.com/NVIDIA-AI-Blueprints/llm-router
2. **LiteLLM Routing 文档**：https://docs.litellm.ai/docs/proxy_router
3. **Portkey Gateway GitHub**：https://github.com/Portkey-AI/gateway
4. **vLLM GitHub**：https://github.com/vllm-project/vllm
5. **SGLang GitHub**：https://github.com/sgl-project/sglang

Sources:
1. https://github.com/NVIDIA-AI-Blueprints/llm-router — NVIDIA LLM Router 主仓库
2. https://docs.litellm.ai/docs/proxy_router — LiteLLM 路由文档
3. https://github.com/Portkey-AI/gateway — Portkey Gateway 主仓库
4. https://github.com/vllm-project/vllm — vLLM 主仓库（被路由的后端）
5. https://github.com/sgl-project/sglang — SGLang 主仓库（被路由的后端）

Risk of Staleness:
- NVIDIA llm-router 更新活跃，具体策略以实际版本为准
- LiteLLM 作为活跃项目，API 变更较频繁

Out of Scope Kept:
- 未写完整章节
- 未写最终架构结论
- 未做 Router 方案排名对比
