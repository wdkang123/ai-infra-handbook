# Blocker Escalation Map v1

## Task ID: T805
## Task Title: Cross-Project Integration Prep Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T801-T804 risk cut list，准备阻塞升级路径。

---

# Blocker Escalation Map v1

## 概述

本文档定义 MVP 实施过程中可能遇到的阻塞问题及其升级路径。

---

## 阻塞问题分类

| 类别 | 说明 | 示例 |
|------|------|------|
| 环境问题 | 硬件/软件环境不满足 | GPU 不足、CUDA 版本不对 |
| 依赖问题 | 外部依赖不可用 | HuggingFace 下载慢、lm-eval API 变更 |
| 集成问题 | 模块间集成失败 | API 格式不匹配、端口冲突 |
| 决策问题 | 需要架构决策 | 引擎选型、配置策略 |

---

## 环境问题

### GPU 显存不足

| 阶段 | 问题 | 处理方式 |
|------|------|---------|
| inference-service | vLLM OOM | 降低 gpu_memory_utilization，使用更小模型 |
| finetune-demo | 训练 OOM | 使用 QLoRA，降低 batch_size |
| 升级路径 | 无法解决 | → 采购更高显存 GPU 或使用量化 |

### CUDA 版本不匹配

| 问题 | 处理方式 |
|------|---------|
| CUDA 版本低 | 升级 CUDA 驱动 |
| 升级路径 | → 系统管理员处理 |

---

## 依赖问题

### HuggingFace 下载慢

| 处理方式 | 说明 |
|---------|------|
| 使用镜像 | 配置 HuggingFace 镜像站 |
| 预下载 | 提前下载模型到本地 |
| 升级路径 | → 网络管理员处理 |

### lm-eval API 变更

| 处理方式 | 说明 |
|---------|------|
| 锁定版本 | 使用稳定版本 v0.4.3 |
| 升级路径 | → 等待官方修复或降级版本 |

---

## 集成问题

### inference-service 与 ai-gateway API 不匹配

| 问题 | 原因 | 处理方式 |
|------|------|---------|
| 响应格式不一致 | vLLM 版本差异 | 升级 vLLM 或添加适配层 |
| 升级路径 | → 检查 vLLM 文档，确认 API 兼容性 |

### eval-module 调用 inference-service 失败

| 问题 | 原因 | 处理方式 |
|------|------|---------|
| Backend URL 配置错误 | 配置不一致 | 统一配置（参考 T805-shared-config-boundary） |
| 升级路径 | → 检查网络连通性 |

---

## 决策问题

### 需要 Codex 判断的决策

| 决策点 | 当前状态 | 阻塞影响 |
|--------|---------|---------|
| vLLM vs SGLang | 建议 vLLM | 等待决策才能继续 |
| Langfuse Cloud vs self-hosted | 建议 Cloud | 可先跳过 tracing |
| QLoRA vs LoRA | 建议 QLoRA | 影响 finetune-demo 配置 |

---

## 升级路径总览

```
遇到阻塞
    ↓
判断类别
    ├── 环境问题 → 系统管理员
    ├── 依赖问题 → 官方文档/社区
    ├── 集成问题 → Codex
    └── 决策问题 → Codex（必须）
```

---

## 升级触发条件

| 条件 | 说明 |
|------|------|
| 尝试 2 次仍无法解决 | 记录错误，开始升级流程 |
| 影响 MVP 必须任务 | 立即升级 |
| 需要外部资源 | 升级到资源 owner |

---

## 升级文档模板

```markdown
## Blocker Report

**日期**: YYYY-MM-DD
**模块**: xxx
**问题描述**: ...
**已尝试的解决方式**:
1. ...
2. ...

**错误日志**:
```
...
```

**需要的帮助**: ...
```

---

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval

Risk of Staleness:
- 阻塞处理方式可能因环境调整

Out of Scope Kept:
- 未写完整故障应急流程
