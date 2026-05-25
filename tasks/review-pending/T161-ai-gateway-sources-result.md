Task ID: T161
Task Title: 搜集 AI Gateway 官方资料与核心链接
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
搜集 AI Gateway / model gateway / LLM gateway 在 AI Infra 中的资料包，包含术语边界、代表性实现、官方入口、核心能力、优先阅读链接。

Result:

## 一、术语边界说明

**AI Gateway / LLM Gateway / Model Gateway** 是位于 AI 应用层和模型推理层之间的代理层，负责对 LLM API 请求进行统一管理。其核心功能包括：

- **统一接入**：通过单一 API 接口接入多个模型供应商（OpenAI、Anthropic、Azure OpenAI、自部署模型等）
- **流量管理**：路由、负载均衡、限流、降级
- **安全与合规**：API 密钥管理、审计日志、敏感词过滤
- **可观测性**：请求日志、token 用量统计、延迟监控

注意：AI Gateway 与 AI Router 的边界有时模糊。AI Gateway 更强调"统一入口和管理平面"，AI Router 更强调"请求分发策略"。在开源实现中两者经常重叠。

## 二、代表性开源/产品实现

| 实现 | 类型 | 官方入口 |
|------|------|---------|
| **Portkey Gateway** | 开源 + 云服务 | https://github.com/Portkey-AI/gateway |
| **APIPark** | 开源 | https://github.com/APIParkLab/APIPark |
| **LiteLLM Proxy** | 开源 | https://github.com/BerriAI/litellm |
| **gateway（Agent-Uncommon）** | 开源 | https://github.com/Agent-Uncommon/gateway |
| **Cloudflare AI Gateway** | 云服务 | https://developers.cloudflare.com/ai-gateway/ |
| **AWS Bedrock + API Gateway** | 云服务 | https://aws.amazon.com/bedrock/ |

## 三、官方主页 / GitHub / 文档

1. **Portkey Gateway**：https://github.com/Portkey-AI/gateway — 支持 160+ 模型，1.x 已开源，2.0 正在 pre-release
2. **APIPark**：https://github.com/APIParkLab/APIPark — 支持多模型接入和统一管理
3. **LiteLLM Proxy**：https://github.com/BerriAI/litellm — 单一接口代理 100+ 模型，支持所有主流 LLM API
4. **Agent-Uncommon gateway**：https://github.com/Agent-Uncommon/gateway — 专注路由到 100+ 模型，轻量级（~45kb）
5. **Cloudflare AI Gateway**：https://developers.cloudflare.com/ai-gateway/ — CDN 边缘接入，流量管理

## 四、核心能力对比

| 功能 | Portkey | APIPark | LiteLLM | gateway |
|------|---------|---------|---------|---------|
| 多模型统一接入 | 160+ | 多 | 100+ | 100+ |
| OpenAI 兼容 API | 是 | 是 | 是 | 是 |
| 限流 | 是 | 是 | 是 | 是 |
| 用量审计 | 是 | 是 | 是 | 是 |
| Gateway 2.0 开源 | 是 | - | - | - |
| 认证/鉴权 | 是 | 是 | 是 | 是 |
| 重试机制 | 是 | 是 | 是 | 是 |

## 五、精确优先阅读链接（6 个）

1. **Portkey Gateway GitHub**：https://github.com/Portkey-AI/gateway
2. **APIPark GitHub**：https://github.com/APIParkLab/APIPark
3. **LiteLLM Proxy GitHub**：https://github.com/BerriAI/litellm
4. **Agent-Uncommon gateway GitHub**：https://github.com/Agent-Uncommon/gateway
5. **Cloudflare AI Gateway 文档**：https://developers.cloudflare.com/ai-gateway/
6. **AWS Bedrock 产品页**：https://aws.amazon.com/bedrock/

Sources:
1. https://github.com/Portkey-AI/gateway — Portkey Gateway 主仓库
2. https://github.com/APIParkLab/APIPark — APIPark 主仓库
3. https://github.com/BerriAI/litellm — LiteLLM 主仓库
4. https://github.com/Agent-Uncommon/gateway — gateway 主仓库
5. https://developers.cloudflare.com/ai-gateway/ — Cloudflare AI Gateway 文档
6. https://aws.amazon.com/bedrock/ — AWS Bedrock 产品页

Risk of Staleness:
- 各 Gateway 项目更新频繁，具体支持模型数量以实际版本为准
- Portkey 2.0 处于 pre-release，API 可能变化

Out of Scope Kept:
- 未写完整章节
- 未做最终架构结论
- 未对比各 Gateway 优劣排名
