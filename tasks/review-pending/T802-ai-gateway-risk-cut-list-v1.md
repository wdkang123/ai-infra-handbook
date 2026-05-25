# ai-gateway Risk Cut List v1

## Task ID: T802
## Task Title: ai-gateway Execution Prep Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T302 MVP 设计，准备 ai-gateway 实施前包。

---

# ai-gateway Risk Cut List v1

## 概述

本文档定义 ai-gateway 的主要风险和缓解措施，供 Codex 实施前参考。

---

## 风险清单

| 风险 ID | 风险描述 | 影响 | 概率 | 缓解措施 |
|---------|---------|------|------|---------|
| R-01 | 下游服务不可用导致 Gateway 502 | 高 | 中 | 实现健康检查和 fallback |
| R-02 | 限流算法实现复杂 | 中 | 中 | MVP 用固定窗口，后续升级 |
| R-03 | Token 计量不准确 | 中 | 低 | 下游必须返回 usage 字段 |
| R-04 | 多下游路由配置复杂 | 中 | 低 | MVP 单下游，后续扩展 |
| R-05 | Auth 密钥管理不安全 | 高 | 中 | MVP 用静态列表，生产用 Vault |
| R-06 | 流式响应超时处理 | 中 | 低 | 配置合理 timeout |

---

## 风险详解

### R-01：下游服务不可用

**风险描述**：下游 inference-service 不可用时，Gateway 返回 502。

**影响**：用户体验差，请求失败。

**缓解措施**：
- 实现下游健康检查
- 配置 fallback 下游（如有）
- 返回有意义的错误信息

**实现建议**：
```python
async def proxy_with_health_check(request, model):
    if not await is_downstream_healthy(model):
        if fallback := get_fallback(model):
            return await proxy_to(fallback, request)
        raise ServiceUnavailableError("Downstream unavailable")
    return await proxy_to(primary, request)
```

---

### R-02：限流算法实现复杂

**风险描述**：滑动窗口算法实现比固定窗口复杂。

**影响**：MVP 交付延期。

**缓解措施**：
- MVP 使用固定窗口算法
- 记录边界突发风险
- 后续迭代升级到滑动窗口

**固定窗口问题**：
- 窗口切换时可能允许 2x 请求
- 可接受（MVP 阶段）

---

### R-03：Token 计量不准确

**风险描述**：Token 用量从下游响应提取，下游可能不返回。

**影响**：成本计量不准确。

**缓解措施**：
- 要求下游必须返回 usage 字段
- 下游无 usage 时，记录警告日志
- 不因计量失败阻止请求

---

### R-04：多下游路由配置复杂

**风险描述**：多模型、多版本、多引擎的路由配置复杂。

**影响**：配置错误导致路由失败。

**缓解措施**：
- MVP 单一下游配置
- 配置验证和测试
- 使用 schema 验证 config.yaml

---

### R-05：Auth 密钥管理不安全

**风险描述**：API Key 明文存储在配置文件。

**影响**：密钥泄露。

**缓解措施**：
- MVP：使用环境变量引用
- 生产：集成 Vault 或云 KMS
- 不在日志中打印密钥

**配置改进**：
```yaml
auth:
  api_keys:
    - "${API_KEY_1}"
    - "${API_KEY_2}"
```

---

### R-06：流式响应超时处理

**风险描述**：流式响应时间过长，连接超时。

**影响**：客户端断开。

**缓解措施**：
- 配置合理的 timeout（MVP 300s）
- 流式请求单独处理 timeout
- 返回部分数据而非完全断开

---

## MVP 阶段必须规避的风险

| 风险 | 规避措施 |
|------|---------|
| 502 未处理 | 实现 fallback 或错误提示 |
| 密钥泄露 | 使用环境变量 |
| 计量阻塞 | 计量失败不阻止请求 |

---

## 风险决策点

| 决策点 | 选项 | 建议 |
|--------|------|------|
| 限流算法 | 固定窗口/滑动窗口/令牌桶 | 固定窗口（MVP） |
| Auth 方式 | API Key / JWT | API Key（MVP） |
| 下游数量 | 单下游 / 多下游 | 单下游（MVP） |
| Fallback | 有 / 无 | 无（MVP） |

---

Sources:
1. https://github.com/Portkey-AI/gateway — Portkey Gateway
2. https://github.com/BerriAI/litellm — LiteLLM

Risk of Staleness:
- 开源 gateway 实现可能有变化

Out of Scope Kept:
- 未写完整安全审计
- 未写成本计量方案
