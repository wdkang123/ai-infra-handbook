# eval-module Execution Prep Pack Manifest

## Task ID: T803
## Task Title: eval-module Execution Prep Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T303 MVP 设计、T205 Evaluation 章节、T702 boundary matrix、T702 tooling timeline，准备 eval-module 实施前包。

---

# eval-module Execution Prep Pack Manifest

## 包概述

本包为 eval-module 模块的实施前准备包，8 个文件全部完成，从 repo layout、API contract、runner map、config surface、test plan、validation checklist、risk cut list 七个维度收束可执行输入。

## 已完成交付物

| 文件 | 内容 |
|------|------|
| T803-eval-module-repo-layout-v1.md | 目录结构设计 |
| T803-eval-module-api-contract-v1.md | 评测接口定义 |
| T803-eval-module-runner-map-v1.md | lm-eval runner 映射 |
| T803-eval-module-config-surface-v1.md | 配置项清单 |
| T803-eval-module-test-plan-v1.md | 测试计划 |
| T803-eval-module-validation-checklist-v1.md | 验收清单 |
| T803-eval-module-risk-cut-list-v1.md | 风险裁剪清单 |

## 本包升级了什么

| 维度 | T303 MVP | T803（本包） |
|------|---------|-------------|
| 目录结构 | 骨架 | 完整可执行目录 |
| API 定义 | 简单列表 | 详细接口契约 |
| Runner 映射 | 提到 lm-eval | lm-eval runner 详细映射 |
| 配置项 | 未提 | 完整 config surface |
| 测试计划 | 无 | 单元+集成测试 |
| 验收清单 | 无 | 逐项可验证 |
| 风险清单 | 无 | 5 个风险及缓解 |

## 供 Codex 直接使用的输入

### 开箱即用
- **Repo Layout**：直接对应 `src/eval_module/` 目录结构
- **Runner Map**：对应 lm-eval 集成
- **Validation Checklist**：逐项验证清单

### 关键决策点（本包未解决，需要 Codex 判断）
1. **默认 benchmark**：MMLU vs GSM8K vs HumanEval
2. **评测结果存储**：JSON 文件 vs 数据库
3. **历史对比**：是否需要版本对比功能

## 关键链接

| 资源 | URL |
|------|-----|
| lm-eval GitHub | https://github.com/EleutherAI/lm-evaluation-harness |
| Stanford HELM | https://crfm.stanford.edu/helm/ |
| BigCode Eval | https://github.com/bigcode-project/bigcode-eval-harness |

## 与其他包的关系

| 包 | 关系 |
|----|------|
| T801 inference-service | 下游被调用（lm-eval backend） |
| T802 ai-gateway | 可选调用方 |
| T804 finetune-demo | 微调后模型评测 |
| T805 cross-project | 整体集成测试 |

## 整体完成度

| 专题包 | 文件数 | 完成度 |
|--------|--------|--------|
| T801 inference-service | 8 | 100% |
| T802 ai-gateway | 8 | 100% |
| T803 eval-module | 8 | 100% |

Sources:
1. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval
2. https://crfm.stanford.edu/helm/ — Stanford HELM
3. https://github.com/bigcode-project/bigcode-eval-harness — BigCode Eval

Risk of Staleness:
- lm-eval 版本更新可能改变 API

Out of Scope Kept:
- 未写代码实现
- 未写评测结果数据库
- 未写 LLM-as-Judge 实现
