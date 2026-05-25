Task ID: T302
Title: ai-gateway MVP 目录与边界设计
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于已通过的 AI Gateway 资料包（T181）、Router 资料包（T183）、Cache 资料包（T182），定义 ai-gateway 模块的 MVP 边界和目录结构。

Result:

## 一、定位说明

**ai-gateway** 是 AI Infra 项目中负责**统一接入和流量管理**的模块。它的核心职责：

- **统一接入**：通过单一 API 接口接入多个下游推理服务（inference-service）或外部模型 API
- **流量管理**：路由策略（根据模型、成本、延迟选择下游）、限流、降级
- **安全与观测**：API 密钥管理、请求日志、token 用量统计

**ai-gateway 不做的事**：
- 实际模型推理（委托给 inference-service 或外部 API）
- 模型训练和微调（属于 finetune-demo）
- 模型评测（属于 eval-module）

## 二、目录结构（最小骨架）

```
ai-gateway/
├── README.md                    # 模块说明、快速启动
├── pyproject.toml               # Python 依赖定义
├── src/
│   └── ai_gateway/
│       ├── __init__.py
│       ├── proxy.py             # HTTP 代理核心，请求转发
│       ├── router.py            # 路由策略（模型选择、fallback）
│       ├── rate_limiter.py      # 限流实现
│       ├── auth.py              # API 密钥管理
│       ├── models.py            # 下游模型配置
│       └── metrics.py           # Prometheus metrics 封装
├── tests/
│   └── test_proxy.py            # 基本代理转发测试
└── examples/
    └── quickstart.py           # 快速启动示例（对接 vLLM）
```

## 三、核心接口

### HTTP API（对外入口）

| 端点 | 方法 | 说明 |
|------|------|------|
| `/v1/chat/completions` | POST | 聊天补全（透传至下游） |
| `/v1/completions` | POST | 文本补全（透传至下游） |
| `/v1/models` | GET | 列出已配置模型 |
| `/health` | GET | Gateway 健康状态 |
| `/metrics` | GET | Prometheus metrics |

### Python SDK 接口

```python
from ai_gateway import AIGateway

gateway = AIGateway()
gateway.add_model("vllm-local", base_url="http://localhost:8000/v1")
gateway.add_model("openai-gpt4", api_key="sk-...", base_url="https://api.openai.com/v1")

response = gateway.chat(model="vllm-local", messages=[...])
```

### CLI 接口

```bash
# 启动网关
ai-gateway serve --config config.yaml --port 8080

# 查看已配置模型
ai-gateway models list
```

## 四、核心功能边界

### 已包含（MVP 范围）
- **模型接入**：支持 OpenAI 兼容 API 和自定义后端 URL
- **请求路由**：根据 model name 路由到指定下游
- **Fallback**：下游失败时自动切换到备用模型
- **限流**：per-model RPS 限制
- **用量统计**：记录每个模型的请求数和 token 数

### 不包含（超出 MVP）
- **成本感知路由**：根据请求复杂度自动选择便宜/贵模型（需要更多上下文）
- **Semantic Cache**：需要与外部向量库配合，超出 MVP 范围
- **AI Safety / Guardrails**：内容过滤等安全功能
- **多租户认证**：复杂的 tenant 隔离

## 五、依赖关系

```
应用层（用户/Agent）
    ↓ HTTP 请求
ai-gateway（本案）
    ↓
├── inference-service（本地推理服务）
├── 外部模型 API（OpenAI / Anthropic / Azure）
└── Redis（限流计数器，可选）
```

- **下游依赖**：inference-service 提供本地推理能力；也支持直连外部模型 API
- **可选依赖**：Redis 用于分布式限流（单机版可不用）

## 六、边界说明

| 边界 | 说明 |
|------|------|
| vs inference-service | ai-gateway 做流量管理，inference-service 做实际推理。ai-gateway 可以调用 inference-service，也可以直连外部 API |
| vs eval-module | eval-module 通过 ai-gateway 发送推理请求进行评测，不需要知道下游模型细节 |
| vs finetune-demo | finetune-demo 负责训练，ai-gateway 负责部署后对外暴露推理 API |

## 七、最小可运行路径

**目标**：启动 ai-gateway，对接本地 inference-service（vLLM），验证请求透传成功。

```bash
# 1. 安装依赖
pip install ai-gateway

# 2. 启动 inference-service（已在 inference-service 模块中定义）
# inference-service serve --engine vllm --model Qwen/Qwen2.5-7B-Instruct --port 8000 &

# 3. 启动 ai-gateway（透传到本地 vLLM）
ai-gateway serve \
    --port 8080 \
    --models '{"vllm-local": {"base_url": "http://localhost:8000/v1"}}'

# 4. 通过 gateway 发送请求
curl http://localhost:8080/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{"model": "vllm-local", "messages": [{"role": "user", "content": "Hello via gateway"}]}'

# 5. 查看 metrics
curl http://localhost:8080/metrics
```

**预期输出**：与直接调用 inference-service 相同的响应，但通过 gateway 透传。

## 八、路由策略设计

```python
class Router:
    def route(self, model: str) -> str:
        """根据 model name 返回下游 base_url"""
        if model in self.models:
            return self.models[model]
        raise ModelNotFoundError(model)

    def route_with_fallback(self, primary: str, fallback: str) -> str:
        """优先用 primary，失败时用 fallback"""
        # 实际实现需考虑下游健康状态
        ...
```

Sources:
1. https://github.com/Portkey-AI/gateway — Portkey Gateway（参考架构）
2. https://github.com/BerriAI/litellm — LiteLLM（参考架构）
3. https://github.com/NVIDIA-AI-Blueprints/llm-router — NVIDIA LLM Router（参考）
4. https://docs.litellm.ai/docs/proxy_router — LiteLLM 路由文档

Risk of Staleness:
- 路由策略设计需随下游 API 变化迭代
- 各开源 gateway 的接口设计有所不同，本设计参考 Portkey/LiteLLM 共性

Out of Scope Kept:
- 未写多租户隔离和复杂权限体系
- 未写 Semantic Cache 实现
- 未写成本感知路由策略
