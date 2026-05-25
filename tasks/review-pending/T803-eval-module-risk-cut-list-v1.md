# eval-module Risk Cut List v1

## Task ID: T803
## Task Title: eval-module Execution Prep Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T303 MVP 设计，准备 eval-module 实施前包。

---

# eval-module Risk Cut List v1

## 概述

本文档定义 eval-module 的主要风险和缓解措施，供 Codex 实施前参考。

---

## 风险清单

| 风险 ID | 风险描述 | 影响 | 概率 | 缓解措施 |
|---------|---------|------|------|---------|
| R-01 | lm-eval API 变更导致集成失败 | 高 | 中 | 锁定版本；Mock 测试 |
| R-02 | benchmark 结果不可比（配置漂移） | 高 | 中 | 统一配置；记录版本 |
| R-03 | vLLM backend 调用失败 | 中 | 中 | 检查 inference-service 健康 |
| R-04 | 数据集下载失败 | 低 | 低 | 预下载；本地缓存 |
| R-05 | 评测时间过长 | 中 | 低 | 小规模样本测试先跑 |

---

## 风险详解

### R-01：lm-eval API 变更

**风险描述**：lm-eval v0.4 版本 API 有较大变化。

**影响**：eval-module 调用 lm-eval 的代码需要适配。

**缓解措施**：
- 锁定 `lm-eval>=0.4.0,<0.5.0`
- 使用官方 stable API
- 单元测试 Mock lm-eval

**版本建议**：
- 生产使用：`0.4.3`（稳定）
- 最新功能：`0.5.x`

来源：https://github.com/EleutherAI/lm-evaluation-harness

---

### R-02：benchmark 结果不可比

**风险描述**：不同评测配置（few-shot 数、数据集版本）导致结果不可比。

**影响**：历史评测结果对比失效。

**缓解措施**：
- 统一 `num_fewshot` 默认值
- 记录 lm-eval 版本
- 记录数据集版本

**MVP 配置**：
```yaml
datasets:
  mmlu:
    num_fewshot: 5
  gsm8k:
    num_fewshot: 5
```

---

### R-03：vLLM backend 调用失败

**风险描述**：inference-service 不可用或响应格式不符。

**影响**：评测失败。

**缓解措施**：
- 评测前检查 inference-service 健康
- 使用 timeout 防止挂起
- 记录详细错误日志

**健康检查**：
```bash
curl http://localhost:8000/health
```

---

### R-04：数据集下载失败

**风险描述**：MMLU/GSM8K 数据集下载失败。

**影响**：评测无法运行。

**缓解措施**：
- lm-eval 自动缓存数据集
- 预先下载到本地
- 使用 `--download` 单独下载

---

### R-05：评测时间过长

**风险描述**：完整 MMLU 评测可能需要数小时。

**影响**：开发迭代慢。

**缓解措施**：
- MVP 阶段用 `--limit` 限制样本数
- 验证流程后再跑完整评测
- 使用并行评测（后续）

---

## MVP 阶段必须规避的风险

| 风险 | 规避措施 |
|------|---------|
| API 变更 | 锁定版本 |
| 结果不可比 | 统一配置 |
| 评测挂起 | 健康检查 + timeout |

---

## 风险决策点

| 决策点 | 选项 | 建议 |
|--------|------|------|
| lm-eval 版本 | 0.4.3 / 0.5.x | 0.4.3（稳定） |
| num_fewshot 默认 | 0 / 5 | 5 |
| 评测并发 | 单任务 / 多任务 | 单任务（MVP） |

---

Sources:
1. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval

Risk of Staleness:
- lm-eval 版本更新可能改变风险

Out of Scope Kept:
- 未写完整应急预案
