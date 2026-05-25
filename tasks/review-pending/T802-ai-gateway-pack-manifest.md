# ai-gateway Execution Prep Pack Manifest

## Task ID: T802
## Task Title: ai-gateway Execution Prep Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T302 MVP 设计、T181/T203 AI Gateway 资料，准备 ai-gateway 实施前包。

---

# ai-gateway Execution Prep Pack Manifest

## 包概述

本包为 ai-gateway 模块的实施前准备包，8 个文件全部完成，从 repo layout、API contract、middleware map、config surface、test plan、validation checklist、risk cut list 七个维度收束可执行输入。

## 已完成交付物

| 文件 | 内容 |
|------|------|
| T802-ai-gateway-repo-layout-v1.md | 目录结构设计 |
| T802-ai-gateway-api-contract-v1.md | 代理 API 接口定义 |
| T802-ai-gateway-middleware-map-v1.md | 中间件（鉴权/限流/计量）设计 |
| T802-ai-gateway-config-surface-v1.md | 配置项清单 |
| T802-ai-gateway-test-plan-v1.md | 测试计划 |
| T802-ai-gateway-validation-checklist-v1.md | 验收清单 |
| T802-ai-gateway-risk-cut-list-v1.md | 风险裁剪清单 |

## 本包升级了什么

| 维度 | T302 MVP | T802（本包） |
|------|---------|-------------|
| 目录结构 | 骨架 | 完整可执行目录 |
| API 定义 | 简单列表 | 详细接口契约 |
| Middleware | 提到有 middleware | 独立 middleware map |
| 配置项 | 提到有 config | 完整 config surface |
| 测试计划 | 无 | 单元+集成+端到端 |
| 验收清单 | 无 | 逐项可验证 |
| 风险清单 | 无 | 5 个风险及缓解 |

## 供 Codex 直接使用的输入

### 开箱即用
- **Repo Layout**：直接对应 `src/ai_gateway/` 目录结构
- **Middleware Map**：对应鉴权/限流/计量实现
- **Validation Checklist**：逐项验证清单

### 关键决策点（本包未解决，需要 Codex 判断）
1. **限流算法**：令牌桶 vs 滑动窗口
2. **鉴权方式**：API Key vs JWT
3. **多后端路由**：是否在 MVP 引入

## 关键链接

| 资源 | URL |
|------|-----|
| Portkey Gateway | https://github.com/Portkey-AI/gateway |
| LiteLLM Proxy | https://github.com/BerriAI/litellm |
| APIPark | https://github.com/APIParkLab/APIPark |

## 与其他包的关系

| 包 | 关系 |
|----|------|
| T801 inference-service | 下游被调用 |
| T803 eval-module | 可选调用方 |
| T804 finetune-demo | 可选调用方 |
| T805 cross-project | 整体集成测试 |

## 整体完成度

| 专题包 | 文件数 | 完成度 |
|--------|--------|--------|
| T801 inference-service | 8 | 100% |
| T802 ai-gateway | 8 | 100% |

Sources:
1. https://github.com/Portkey-AI/gateway — Portkey Gateway
2. https://github.com/BerriAI/litellm — LiteLLM
3. https://github.com/APIParkLab/APIPark — APIPark

Risk of Staleness:
- 开源 gateway 更新快，具体 API 以实际版本为准

Out of Scope Kept:
- 未写代码实现
- 未写多租户设计
- 未写 Semantic Cache
