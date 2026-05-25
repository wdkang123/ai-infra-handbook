Task ID: T172
Task Title: 搜集 router / model routing 官方资料与核心链接
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
搜集 AI Infra 中请求路由、模型路由资料包，包含术语边界、代表性实现、官方入口、核心能力、优先阅读链接。

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

### 与 AI Gateway 的关系
Router 通常是 AI Gateway 的内部组件，但也有独立 Router 实现。Router 更多关注"流量策略"，Gateway 更多关注"统一入口和管理"。

## 二、代表性开源/产品实现

| 实现 | 类型 | 官方入口 |
|------|------|---------|
| **NVIDIA llm-router** | 开源 | https://github.com/NVIDIA-AI-Blueprints/llm-router |
| **LiteLLM Proxy** | 开源 Router 功能 | https://github.com/BerriAI/litellm |
| **Portkey Gateway** | 开源 + 云 | https://github.com/Portkey-AI/gateway |
| **VLLM（分布式部署 Router）** | 开源 | https://github.com/vllm-project/vllm |
| **SGLang（Router 后端）** | 开源 | https://github.com/sgl-project/sglang |

## 三、官方主页 / GitHub / 文档

1. **NVIDIA llm-router**：https://github.com/NVIDIA-AI-Blueprints/llm-router — NVIDIA 官方 LLM 路由实现，支持模型选择策略
2. **LiteLLM Proxy**：https://github.com/BerriAI/litellm — 支持路由、限流、重试、fallback
3. **Portkey Gateway**：https://github.com/Portkey-AI/gateway — 包含智能路由功能
4. **vLLM（分布式推理）**：https://github.com/vllm-project/vllm — vLLM 的分布式部署和模型路由能力
5. **SGLang**：https://github.com/sgl-project/sglang — SGLang Runtime 的请求调度路由

## 四、核心路由策略

| 策略 | 说明 | 典型场景 |
|------|------|---------|
| **Simple Route** | 固定路由到某模型 | 单模型部署 |
| **Weighted Route** | 按权重比例分配流量 | 多版本并存、A/B test |
| **Cost-aware Route** | 根据请求复杂度分配 | 成本优化 |
| **Fallback Route** | 主模型失败时切备用 | 高可用保障 |
| **Canary Route** | 小比例新版本验证 | 新版本发布 |
| **Latency-based Route** | 优先路由到延迟最低实例 | 性能优化 |

## 五、精确优先阅读链接（6 个）

1. **NVIDIA llm-router GitHub**：https://github.com/NVIDIA-AI-Blueprints/llm-router
2. **LiteLLM Routing 文档**：https://docs.litellm.ai/docs/proxy_router
3. **Portkey Gateway GitHub**：https://github.com/Portkey-AI/gateway
4. **vLLM 分布式推理文档**：https://docs.vllm.ai/en/latest/distributedributed_serving.html
5. **SGLang Backend 文档**：https://docs.sglang.ai/backend/index.html
6. **Canary Routing CNCF Glossary**：https://glossary.cncf.io/canary-deployment/

Sources:
1. https://github.com/NVIDIA-AI-Blueprints/llm-router — NVIDIA LLM Router 主仓库
2. https://docs.litellm.ai/docs/proxy_router — LiteLLM 路由文档
3. https://github.com/Portkey-AI/gateway — Portkey Gateway 主仓库
4. https://docs.vllm.ai/en/latest/distributedributed_serving.html — vLLM 分布式服务文档
5. https://docs.sglang.ai/backend/index.html — SGLang 后端架构文档
6. https://glossary.cncf.io/canary-deployment/ — CNCF Canary Deployment 术语定义

Risk of Staleness:
- NVIDIA llm-router 更新活跃，具体策略以实际版本为准
- LiteLLM 作为活跃项目，API 变更较频繁
- vLLM 和 SGLang 的分布式部署方案持续演进

Out of Scope Kept:
- 未写完整章节
- 未写最终架构结论
- 未做各 Router 方案排名对比
