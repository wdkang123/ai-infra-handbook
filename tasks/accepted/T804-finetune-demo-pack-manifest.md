# finetune-demo Execution Prep Pack Manifest

## Task ID: T804
## Task Title: finetune-demo Execution Prep Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T304 MVP 设计、T713 决策 memo、T703 boundary matrix、T703 training map，准备 finetune-demo 实施前包。

---

# finetune-demo Execution Prep Pack Manifest

## 包概述

本包为 finetune-demo 模块的实施前准备包，8 个文件全部完成，从 repo layout、API contract、training config map、artifact flow、test plan、validation checklist、risk cut list 七个维度收束可执行输入。

## 已完成交付物

| 文件 | 内容 |
|------|------|
| T804-finetune-demo-repo-layout-v1.md | 目录结构设计 |
| T804-finetune-demo-api-contract-v1.md | 训练接口定义 |
| T804-finetune-demo-training-config-map-v1.md | LoRA/QLoRA/SFT 配置映射 |
| T804-finetune-demo-artifact-flow-v1.md | 训练产物流转 |
| T804-finetune-demo-test-plan-v1.md | 测试计划 |
| T804-finetune-demo-validation-checklist-v1.md | 验收清单 |
| T804-finetune-demo-risk-cut-list-v1.md | 风险裁剪清单 |

## 本包升级了什么

| 维度 | T304 MVP | T804（本包） |
|------|---------|-------------|
| 目录结构 | 骨架 | 完整可执行目录 |
| API 定义 | 简单列表 | 详细接口契约 |
| Training Config | 提到有 config | LoRA/QLoRA/SFT 配置映射 |
| Artifact Flow | 未提 | 完整产物流转 |
| 测试计划 | 无 | 单元+集成测试 |
| 验收清单 | 无 | 逐项可验证 |
| 风险清单 | 无 | 5 个风险及缓解 |

## 供 Codex 直接使用的输入

### 开箱即用
- **Repo Layout**：直接对应 `finetune-demo/` 目录结构
- **Training Config Map**：对应 LoRA/QLoRA/SFT 配置
- **Validation Checklist**：逐项验证清单

### 关键决策点（本包未解决，需要 Codex 判断）
1. **默认微调方法**：LoRA vs QLoRA
2. **Unsloth 引入时机**：GPU 兼容性确认后
3. **训练数据集**：格式和来源

## 关键链接

| 资源 | URL |
|------|-----|
| PEFT GitHub | https://github.com/huggingface/peft |
| TRL GitHub | https://github.com/huggingface/trl |
| Unsloth GitHub | https://github.com/unslothai/unsloth |

## 与其他包的关系

| 包 | 关系 |
|----|------|
| T801 inference-service | 加载 adapter 做推理 |
| T803 eval-module | 微调后 benchmark 评测 |
| T805 cross-project | 整体集成测试 |

## 整体完成度

| 专题包 | 文件数 | 完成度 |
|--------|--------|--------|
| T801 inference-service | 8 | 100% |
| T802 ai-gateway | 8 | 100% |
| T803 eval-module | 8 | 100% |
| T804 finetune-demo | 8 | 100% |

Sources:
1. https://github.com/huggingface/peft — PEFT
2. https://github.com/huggingface/trl — TRL
3. https://github.com/unslothai/unsloth — Unsloth
4. https://arxiv.org/abs/2305.14314 — QLoRA

Risk of Staleness:
- PEFT/TRL 版本更新可能改变 API

Out of Scope Kept:
- 未写代码实现
- 未写数据准备详细步骤
