Task ID: T702
Task Title: Observability / Evaluation Deep-Research Pack
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
梳理 LM-Eval/HELM/BigCode Eval 的稳定入口与更新线索。

Result:

# Eval Tooling Timeline v1

## 概述

本文档收录 LM-Eval Harness、Stanford HELM、BigCode Eval Harness 的关键更新线索和稳定入口。

---

## LM-Eval Harness

### 关键更新线索

| 时间 | 版本 | 关键更新 |
|------|------|---------|
| 2023 年 | v0.2.x | 早期稳定版，支持多种 benchmark |
| 2024 年初 | v0.3.x | vLLM backend 支持 |
| 2024 年中 | v0.4.x | API 较大变化，支持更多模型 |
| 2024 年末 | v0.4.3+ | 稳定版，bug 修复 |
| 2025 年初 | v0.5.x | 更多 backend 支持，性能改进 |

### 官方入口

| 维度 | 内容 |
|------|------|
| **GitHub** | https://github.com/EleutherAI/lm-evaluation-harness |
| **文档** | https://github.com/EleutherAI/lm-evaluation-harness#lm-eval-harness |
| **Release** | https://github.com/EleutherAI/lm-evaluation-harness/releases |
| **Discussions** | https://github.com/EleutherAI/lm-evaluation-harness/discussions |
| **任务列表** | https://github.com/EleutherAI/lm-evaluation-harness/tree/main/lm_eval/tasks |

### 边界说明

- v0.4 版本 API 有较大变化，使用时需确认版本
- 不含数据存储和版本对比，需要 eval-module 自己实现

来源：https://github.com/EleutherAI/lm-evaluation-harness

---

## Stanford HELM

### 关键更新线索

| 时间 | 版本 | 关键更新 |
|------|------|---------|
| 2022 年 | v1.0 | 首次发布，综合评测框架 |
| 2023 年 | v1.2 | 扩展评测场景 |
| 2024 年 | v1.4 | 改进 UI，更多模型支持 |

### 官方入口

| 维度 | 内容 |
|------|------|
| **官网** | https://crfm.stanford.edu/helm/ |
| **GitHub** | https://github.com/stanford-crfm/helm |
| **文档** | https://crfm.stanford.edu/helm/ |
| **Blog** | https://crfm.stanford.edu/helm/blog |

### 边界说明

- 偏学术研究，工程接入成本高
- 主要通过 Web 界面使用，API 支持有限

来源：https://crfm.stanford.edu/helm/

---

## BigCode Eval Harness

### 关键更新线索

| 时间 | 版本 | 关键更新 |
|------|------|---------|
| 2023 年 | 早期版本 | HumanEval 评测支持 |
| 2024 年 | v0.4.x | MBPP 支持，更多代码模型 |
| 2024 年末 | 最新版 | Pass@K 改进，更多 benchmark |

### 官方入口

| 维度 | 内容 |
|------|------|
| **GitHub** | https://github.com/bigcode-project/bigcode-eval-harness |
| **文档** | https://github.com/bigcode-project/bigcode-eval-harness |
| **Release** | https://github.com/bigcode-project/bigcode-eval-harness/releases |
| **Leaderboard** | https://huggingface.co/spaces/bigcode/bigcode-leaderboard |

### 边界说明

- 仅覆盖代码模型评测
- 与 lm-eval 有部分功能重叠

来源：https://github.com/bigcode-project/bigcode-eval-harness

---

## 更新监控建议

### 推荐方式

| 工具 | 用途 |
|------|------|
| **GitHub Releases Atom Feed** | 自动追踪 release 更新 |
| **GitHub Discussions** | 用户反馈和计划讨论 |

### 订阅链接

- LM-Eval：https://github.com/EleutherAI/lm-evaluation-harness/releases/atom
- HELM：https://github.com/stanford-crfm/helm/releases（如有）
- BigCode Eval：https://github.com/bigcode-project/bigcode-eval-harness/releases/atom

---

## 版本稳定性说明

| 工具 | 稳定性 | 说明 |
|------|--------|------|
| **LM-Eval** | 中等 | v0.4 有 API 变化，需要锁定版本 |
| **Stanford HELM** | 高 | 学术项目，API 稳定 |
| **BigCode Eval** | 中等 | 活跃开发中，可能有 API 变化 |

---

## 版本选择建议

| 场景 | 推荐版本 |
|------|---------|
| LM-Eval 生产使用 | v0.4.3（稳定） |
| LM-Eval 最新功能 | v0.5.x |
| BigCode Eval | 最新 release |

---

## 风险提示

- LM-Eval v0.4 之前和之后的 API 有较大差异，迁移需要注意
- 各工具的 benchmark 支持情况随版本变化
- BigCode Eval 和 LM-eval 功能有重叠，不需要同时使用

Sources:
1. https://github.com/EleutherAI/lm-evaluation-harness — LM-Eval Harness
2. https://crfm.stanford.edu/helm/ — Stanford HELM
3. https://github.com/bigcode-project/bigcode-eval-harness — BigCode Eval Harness
4. https://github.com/EleutherAI/lm-evaluation-harness/releases — LM-Eval Releases
5. https://huggingface.co/spaces/bigcode/bigcode-leaderboard — BigCode Leaderboard

Risk of Staleness:
- 各工具更新快，本文收录信息可能随时间变化

Out of Scope Kept:
- 未写完整评测流程
- 未写代码实现
