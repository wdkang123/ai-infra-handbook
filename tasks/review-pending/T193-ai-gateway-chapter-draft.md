Task ID: T193
Task Title: 产出 AI Gateway 章节初稿
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 T181/T182/T183 收紧版资料包，产出 AI Gateway 章节初稿，使用完整 10 节结构。

Result:

# AI Gateway

## 1. 这是什么

AI Gateway（LLM Gateway / Model Gateway）是位于 AI 应用层和模型推理层之间的代理层，负责对 LLM API 请求进行统一管理。其核心功能包括：

- **统一接入**：通过单一 API 接口接入多个模型供应商（OpenAI、Anthropic、Azure OpenAI、自部署模型等）
- **流量管理**：路由、负载均衡、限流、降级
- **安全与合规**：API 密钥管理、审计日志、敏感词过滤
- **可观测性**：请求日志、token 用量统计、延迟监控

**边界划分**：
- **AI Gateway 平台**：独立产品，提供完整管理平面（Portkey、APIPark、Cloudflare AI Gateway）
- **AI Router 组件**：Gateway 内部或独立进程，根据策略分发请求（LiteLLM Proxy 内置路由、NVIDIA llm-router）
- **云厂商 AI 托管服务**：云厂商提供的内置 AI 能力，不属于通用 AI Gateway 范畴（AWS Bedrock 是模型托管，不等同于 AI Gateway）

## 2. 为什么重要

在 AI Infra 架构中，AI Gateway 的价值在于：

1. **统一入口简化集成**：应用层只需对接一个端点，无需为每个模型供应商单独开发适配代码
2. **流量治理标准化**：限流、路由、降级在网关层统一实现，下游推理服务专注于推理本身
3. **多模型成本优化**：根据请求特征动态路由到不同成本的模型，优化整体 token 消耗

## 3. 核心原理

### 请求代理与转发
AI Gateway 接收外部请求后，根据配置将请求透传或转换后转发到下游模型实例。核心是 HTTP 代理逻辑，需要处理请求/响应的格式转换（如 OpenAI API → 内部格式）。

来源：https://github.com/Portkey-AI/gateway

### 路由策略
路由策略决定请求被发送到哪个下游模型。常见策略：
- **Simple routing**：固定模型路由
- **Fallback routing**：主模型失败时切换备用模型
- **Weighted routing**：按比例分配流量到不同版本
- **Canary routing**：小比例流量导向新版本

来源：https://docs.litellm.ai/docs/proxy_router

### 限流机制
限流防止单个用户或全局消耗超出配额。常见实现：令牌桶、滑动窗口。AI Gateway 通常在路由层或单独限流层实现。

来源：https://github.com/BerriAI/litellm

## 4. 常见方案 / 组件

- **Portkey Gateway**：开源 + 云，160+ 模型支持，提供完整管理平面
- **APIPark**：开源，支持多模型接入和统一管理
- **LiteLLM Proxy**：开源，单一接口代理 100+ 模型，支持所有主流 LLM API
- **Cloudflare AI Gateway**：云服务，CDN 边缘接入，与 Cloudflare 安全产品集成
- **NVIDIA llm-router**：开源独立 Router 组件，支持模型选择策略

来源：https://github.com/Portkey-AI/gateway
来源：https://github.com/BerriAI/litellm
来源：https://github.com/NVIDIA-AI-Blueprints/llm-router

## 5. 关键指标

- **RPS（Requests Per Second）**：网关每秒处理的请求数，反映吞吐量
- **Token 用量**：每个模型的 token 消耗，用于成本核算
- **P99 Latency**：端到端延迟，Gateway 调度开销通常 < 10ms
- **错误率**：下游失败导致的 HTTP 错误比例
- **限流命中率**：触发限流的请求比例

来源：https://github.com/Portkey-AI/gateway

## 6. 常见误区

1. **"AI Gateway 就是 Router"**：Router 是 Gateway 的核心组件之一，但 Gateway 还包含认证、限流、审计等能力
2. **"用了 Gateway 就不需要 inference-service"**：Gateway 负责请求代理，不执行实际推理，仍需下游推理引擎
3. **"所有模型都适合通过 Gateway 接入"**：对延迟极度敏感的场景（如实时 Agent），Gateway 的透传开销可能不理想

## 7. 与项目关系

在 AI Infra 学习路径中，AI Gateway 帮助理解：

- 对外 API 统一入口的设计（ai-gateway 模块的核心参考）
- 请求代理、路由策略、限流在工程层面的实现方式
- 与 eval-module 的关系：eval-module 通过 ai-gateway 发送推理请求，不需要感知下游模型细节

## 8. 最小实践任务

**目标**：使用 LiteLLM Proxy 快速启动一个 AI Gateway，对接本地 vLLM 推理服务，验证请求透传成功。

**注意**：以下为提案接口，不是仓库现有实现。

```bash
# 提案接口：安装（实际不存在 pip install ai-gateway）
# pip install ai-gateway

# 提案接口：启动 gateway（LiteLLM 内置 gateway 功能，此处作为 ai-gateway 模块的参考）
litellm --config config.yaml

# 其中 config.yaml 提案配置格式：
# model_list:
#   - model_name: vllm-local
#     litellm_params:
#       model: openai/qwen
#       api_base: http://localhost:8000/v1
#       rpm: 10
# proxy_config:
#   latency_threshold: 2
```

实际执行可用已开源的 LiteLLM：
```bash
pip install litellm
litellm --model openai/qwen --api_base http://localhost:8000/v1 --port 4000
```

来源：https://docs.litellm.ai/docs/proxy_router

## 9. 输出物

- AI Gateway 服务运行中（提案端口 4000）
- 可通过 `curl` 调用 `/v1/chat/completions` 透传到下游 vLLM
- 限流生效（rpm 限制）

## 10. 延伸阅读

1. https://github.com/Portkey-AI/gateway — Portkey Gateway（参考架构）
2. https://github.com/BerriAI/litellm — LiteLLM（参考架构）
3. https://github.com/APIParkLab/APIPark — APIPark
4. https://developers.cloudflare.com/ai-gateway/ — Cloudflare AI Gateway
5. https://github.com/NVIDIA-AI-Blueprints/llm-router — NVIDIA LLM Router
6. https://docs.litellm.ai/docs/proxy_router — LiteLLM 路由文档

Sources:
1. https://github.com/Portkey-AI/gateway — Portkey Gateway
2. https://github.com/BerriAI/litellm — LiteLLM
3. https://docs.litellm.ai/docs/proxy_router — LiteLLM 路由文档
4. https://github.com/APIParkLab/APIPark — APIPark
5. https://developers.cloudflare.com/ai-gateway/ — Cloudflare AI Gateway
6. https://github.com/NVIDIA-AI-Blueprints/llm-router — NVIDIA LLM Router

Risk of Staleness:
- 各开源 Gateway 更新频繁，具体 API 以实际版本为准
- LiteLLM 的 config 格式在 major 版本升级时可能变化

Out of Scope Kept:
- 未写完整 Gateway 产品手册
- 未做 Gateway 优劣排名
- 未写多租户隔离设计

Need Codex Review On:
- 最小实践是否应完全基于开源工具（LiteLLM）而非提案接口
