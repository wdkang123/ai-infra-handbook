# End-to-End Scenario Map v1

## Task ID: T805
## Task Title: Cross-Project Integration Prep Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T714 依赖矩阵，准备端到端场景映射。

---

# End-to-End Scenario Map v1

## 概述

本文档定义四个核心模块的端到端用户场景，覆盖从推理到评测到微调的完整链路。

---

## 场景总览

| 场景 ID | 场景名称 | 涉及模块 | 优先级 |
|---------|---------|---------|--------|
| E2E-01 | 基础推理请求 | gateway → inference | P0 |
| E2E-02 | 微调后推理请求 | finetune → inference | P0 |
| E2E-03 | 微调后评测 | finetune → inference → eval | P0 |
| E2E-04 | Benchmark 对比 | eval → inference | P0 |
| E2E-05 | 多模型路由 | gateway → inference | P1 |

---

## E2E-01：基础推理请求

### 场景描述

用户通过 ai-gateway 发送推理请求，ai-gateway 路由到 inference-service（vLLM）。

### 完整链路

```
用户
  ↓
ai-gateway（鉴权/限流）
  ↓
inference-service（vLLM）
  ↓
响应返回
```

### 关键验证点

| 验证点 | 预期结果 |
|--------|---------|
| 鉴权 | 无效 token 返回 401 |
| 限流 | 超出 RPM 返回 429 |
| 推理 | 正常响应 |
| 延迟 | < 1s（0.5B 模型） |

---

## E2E-02：微调后推理请求

### 场景描述

用户加载微调后的 adapter，通过 inference-service 提供推理服务。

### 完整链路

```
用户
  ↓
ai-gateway
  ↓
inference-service（加载 LoRA adapter）
  ↓
微调后推理响应
```

### 关键验证点

| 验证点 | 预期结果 |
|--------|---------|
| Adapter 加载 | 服务正常启动 |
| 推理 | 响应正常 |
| 效果 | 与 base model 有差异 |

---

## E2E-03：微调后评测

### 场景描述

使用 finetune-demo 训练 LoRA adapter，训练完成后加载到 inference-service，通过 eval-module 运行 benchmark 评测效果。

### 完整链路

```
finetune-demo（训练 LoRA）
  ↓
adapter 产物
  ↓
inference-service（加载 adapter）
  ↓
eval-module（lm-eval backend）
  ↓
评测结果
```

### 关键验证点

| 验证点 | 预期结果 |
|--------|---------|
| 训练完成 | adapter 产物存在 |
| Adapter 加载 | 服务正常 |
| 评测完成 | accuracy 分数 |
| 对比 | 与 base model 可对比 |

---

## E2E-04：Benchmark 对比

### 场景描述

使用 eval-module 对 base model 和微调后模型分别运行 benchmark，对比效果。

### 完整链路

```
eval-module
  ↓
inference-service（base model）
  ↓
base 结果
  ↓
inference-service（微调 model）
  ↓
微调结果
  ↓
对比
```

### 关键验证点

| 验证点 | 预期结果 |
|--------|---------|
| Base 结果 | accuracy 分数 |
| 微调结果 | accuracy 分数 |
| 对比 | diff 计算正确 |

---

## E2E-05：多模型路由（增强）

### 场景描述

ai-gateway 支持配置多个后端，根据 model 参数路由到不同 inference-service。

### 完整链路

```
用户（model=vllm-7b）
  ↓
ai-gateway（路由）
  ↓
inference-service（7B 模型）

用户（model=vllm-3b）
  ↓
ai-gateway（路由）
  ↓
inference-service（3B 模型）
```

### 关键验证点

| 验证点 | 预期结果 |
|--------|---------|
| 路由正确 | 7B 请求到 7B 服务 |
| 模型切换 | 3B 请求到 3B 服务 |
| 未知模型 | 返回 404 |

---

## MVP 必须场景

| 场景 | MVP 必须 | 说明 |
|------|---------|------|
| E2E-01 基础推理 | 是 | 最基本链路 |
| E2E-02 微调后推理 | 是 | 验证微调产物可用 |
| E2E-03 微调后评测 | 是 | 验证微调效果 |
| E2E-04 Benchmark 对比 | 是 | 验证评测链路 |
| E2E-05 多模型路由 | 否 | 增强功能 |

---

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval
3. https://github.com/huggingface/peft — PEFT

Risk of Staleness:
- 场景可能因业务需求调整

Out of Scope Kept:
- 未写完整自动化 E2E 测试
