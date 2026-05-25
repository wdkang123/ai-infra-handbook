# Codex Review Focus Map v1

## Task ID: T705
## Task Title: Execution Decomposition Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
把后续实施拆成若干工作流，便于 Codex 继续分发。

---

# Codex Review Focus Map v1

## 概述

本文档指引 Codex 在审查各模块时需要重点关注的方向。

---

## 审查重点总览

| 模块 | 重点关注 | 高风险点 |
|------|---------|---------|
| inference-service | 引擎选型 / API 兼容性 / 版本锁定 | GPU 显存 / 版本兼容性 |
| ai-gateway | 路由稳定性 / 鉴权安全 / 限流策略 | 并发压力 / 超时处理 |
| eval-module | lm-eval 版本 / 结果一致性 | benchmark 配置漂移 |
| finetune-demo | LoRA 配置 / adapter 管理 | 超参数敏感 / 训练不稳定 |
| 跨模块 | 接口契约 / trace_id 传递 | 集成失败 / 数据不一致 |

---

## inference-service 审查重点

### 引擎选型
- [ ] vLLM vs SGLang 决策是否明确
- [ ] 版本是否锁定
- [ ] 备选引擎是否规划

### API 兼容性
- [ ] OpenAI 格式完全兼容
- [ ] 流式输出格式正确
- [ ] 错误响应格式一致

### 资源管理
- [ ] GPU 显存分配策略
- [ ] 模型冷启动时间
- [ ] 并发请求处理

### 高风险点
- R-01：引擎版本不兼容
- R-02：GPU 显存不足

---

## ai-gateway 审查重点

### 路由稳定性
- [ ] 后端故障时路由策略
- [ ] 重试机制
- [ ] 超时配置

### 鉴权安全
- [ ] Token 验证强度
- [ ] 密钥管理
- [ ] 越权访问防护

### 限流策略
- [ ] QPS 限制算法
- [ ] 限流粒度（用户/租户/全局）
- [ ] 限流响应头

### 高风险点
- R-03：多引擎切换复杂度
- R-12：接口契约缺失

---

## eval-module 审查重点

### lm-eval 集成
- [ ] lm-eval 版本锁定
- [ ] 调用方式正确
- [ ] 结果解析正确

### Benchmark 配置
- [ ] MMLU 配置是否标准
- [ ] GSM8K 配置是否标准
- [ ] 数据集缓存策略

### 结果管理
- [ ] JSON schema 是否稳定
- [ ] 历史结果存储策略
- [ ] 对比算法正确性

### 高风险点
- R-07：lm-eval API 变更
- R-10：benchmark 结果不可比

---

## finetune-demo 审查重点

### LoRA 配置
- [ ] rank/alpha 默认值合理
- [ ] target_modules 配置正确
- [ ] 学习率调度

### Adapter 管理
- [ ] 保存路径规范
- [ ] 加载机制稳定
- [ ] 多 adapter 切换

### 串联验证
- [ ] 微调后模型评测流程
- [ ] 评测结果与微调参数关联
- [ ] 训练曲线可视化

### 高风险点
- R-02：GPU 显存不足
- R-11：LoRA 超参数敏感
- R-09：DPO 数据成本（后续）

---

## 跨模块审查重点

### 接口契约
- [ ] 各模块接口文档完整
- [ ] 请求/响应格式一致
- [ ] 错误码规范统一

### trace_id 传递
- [ ] Langfuse trace 如何串联
- [ ] gateway → inference trace 连续性
- [ ] eval-module trace 独立性

### 数据流向
- [ ] 评测结果数据流向
- [ ] 训练 metrics 数据流向
- [ ] 审计日志完整性

### 高风险点
- R-12：接口契约缺失
- R-08：Langfuse 运维复杂度

---

## Codex 决策点追踪

| 决策点 | 当前状态 | 需要确认 |
|--------|---------|---------|
| vLLM vs SGLang | vLLM 优先 | 默认引擎版本 |
| Langfuse 模式 | 云端优先 | self-hosted 条件 |
| QLoRA 默认 | 标准 LoRA | QLoRA 引入时机 |
| Unsloth 启用 | 暂不启用 | GPU 兼容性 |
| Prometheus 引入 | MVP 不引入 | 引入条件 |

---

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval
3. https://github.com/huggingface/peft — PEFT

Risk of Staleness:
- 审查重点可能因实际执行问题调整

Out of Scope Kept:
- 未写详细审查清单
- 未写审查自动化
