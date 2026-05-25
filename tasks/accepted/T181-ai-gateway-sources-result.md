Task ID: T181
Task Title: 收紧 AI Gateway 资料包中的边界和无来源功能表
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 T161 结果和 T161-review 修订。删除无来源功能表，收紧实现名单，强化 gateway/router/云厂商入口的边界划分。

Result:

## 一、术语边界说明

**AI Gateway / LLM Gateway / Model Gateway** 是位于 AI 应用层和模型推理层之间的代理层，负责对 LLM API 请求进行统一管理。其核心功能包括：

- **统一接入**：通过单一 API 接口接入多个模型供应商（OpenAI、Anthropic、Azure OpenAI、自部署模型等）
- **流量管理**：路由、负载均衡、限流、降级
- **安全与合规**：API 密钥管理、审计日志、敏感词过滤
- **可观测性**：请求日志、token 用量统计、延迟监控

**边界划分**：
- **AI Gateway 平台**：独立产品，提供完整管理平面（Portkey、APIPark、Cloudflare AI Gateway）
- **AI Router 组件**：Gateway 内部或独立进程，根据策略分发请求（LiteLLM Proxy 内置路由、NVIDIA llm-router）
- **云厂商 AI 托管服务**：云厂商提供的内置 AI 能力，不属于通用 AI Gateway 范畴（AWS Bedrock 是模型托管，不等同于 AI Gateway）

## 二、代表性开源实现（Gateway 平台）

| 实现 | 类型 | 官方入口 |
|------|------|---------|
| **Portkey Gateway** | 开源 + 云 | https://github.com/Portkey-AI/gateway |
| **APIPark** | 开源 | https://github.com/APIParkLab/APIPark |
| **LiteLLM Proxy** | 开源 | https://github.com/BerriAI/litellm |
| **Cloudflare AI Gateway** | 云服务 | https://developers.cloudflare.com/ai-gateway/ |

注：`gateway（Agent-Uncommon）`属轻量级 Router 类实现，定位介于 Gateway 和 Router 之间，可作为 Router 参考。

## 三、官方主页 / GitHub / 文档

1. **Portkey Gateway**：https://github.com/Portkey-AI/gateway
2. **APIPark**：https://github.com/APIParkLab/APIPark
3. **LiteLLM Proxy**：https://github.com/BerriAI/litellm
4. **Cloudflare AI Gateway**：https://developers.cloudflare.com/ai-gateway/

注：AWS Bedrock 是云厂商 AI 模型托管服务，不是通用 AI Gateway，不与其他开源 Gateway 直接可比。

## 四、精确优先阅读链接（4 个）

1. **Portkey Gateway GitHub**：https://github.com/Portkey-AI/gateway
2. **APIPark GitHub**：https://github.com/APIParkLab/APIPark
3. **LiteLLM Proxy GitHub**：https://github.com/BerriAI/litellm
4. **Cloudflare AI Gateway 文档**：https://developers.cloudflare.com/ai-gateway/

Sources:
1. https://github.com/Portkey-AI/gateway — Portkey Gateway 主仓库
2. https://github.com/APIParkLab/APIPark — APIPark 主仓库
3. https://github.com/BerriAI/litellm — LiteLLM 主仓库
4. https://developers.cloudflare.com/ai-gateway/ — Cloudflare AI Gateway 文档

Risk of Staleness:
- 各 Gateway 项目更新频繁，具体支持模型数量以实际版本为准
- Portkey 2.0 处于 pre-release，API 可能变化

Out of Scope Kept:
- 未写完整章节
- 未做最终架构结论
- 未对比各 Gateway 优劣排名
