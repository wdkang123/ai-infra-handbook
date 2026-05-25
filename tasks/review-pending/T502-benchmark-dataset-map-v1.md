Task ID: T502
Task Title: Eval/Benchmark Long-Run Pack v2
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
收录常用 benchmark 数据集的分类、评测维度和来源。

Result:

# Benchmark Dataset Map v1

## 概述

本文档收录 AI Infra 项目相关的常用 benchmark 数据集，按评测维度分类，说明各数据集的用途和来源。

---

## 通用语言理解

### MMLU（Massive Multitask Language Understanding）

| 维度 | 内容 |
|------|------|
| **规模** | 57 个学科，15,908 题 |
| **题型** | 选择题（4选1） |
| **评测维度** | 语言理解、领域知识 |
| **主要用途** | 模型通用能力评估 |
| **来源** | https://arxiv.org/abs/2009.03300 |

### HellaSwag

| 维度 | 内容 |
|------|------|
| **规模** | 10,042 题 |
| **题型** | 选择题（情境推理） |
| **评测维度** | 常识推理 |
| **主要用途** | 评估模型的常识推理能力 |
| **来源** | https://arxiv.org/abs/1905.07830 |

### TruthfulQA

| 维度 | 内容 |
|------|------|
| **规模** | 817 题 |
| **题型** | 问答题 |
| **评测维度** | 回复真实性、避免幻觉 |
| **主要用途** | 评估模型的信息真实性 |
| **来源** | https://arxiv.org/abs/2109.07958 |

---

## 数学推理

### GSM8K（Grade School Math 8K）

| 维度 | 内容 |
|------|------|
| **规模** | 8,500 题 |
| **题型** | 数学应用题（含推理过程） |
| **评测维度** | 数学推理能力 |
| **主要用途** | 评估模型的数学问题解决能力 |
| **来源** | https://arxiv.org/abs/2110.14168 |

### MATH

| 维度 | 内容 |
|------|------|
| **规模** | 12,500 题 |
| **题型** | 数学竞赛题（含 LaTeX） |
| **评测维度** | 高级数学推理 |
| **主要用途** | 评估竞赛级数学能力 |
| **来源** | https://arxiv.org/abs/2103.14074 |

---

## 代码生成

### HumanEval

| 维度 | 内容 |
|------|------|
| **规模** | 164 题 |
| **题型** | Python 函数生成（docstring 描述） |
| **评测维度** | 代码生成、函数补全 |
| **主要指标** | Pass@1, Pass@10, Pass@K |
| **来源** | https://arxiv.org/abs/2107.03374 |

### MBPP（Mostly Basic Python Problems）

| 维度 | 内容 |
|------|------|
| **规模** | 974 题 |
| **题型** | Python 编程题 |
| **评测维度** | Python 编码能力 |
| **主要指标** | Pass@1 |
| **来源** | https://github.com/mbpp |

### APPS（Automated Programming Progress Standard）

| 维度 | 内容 |
|------|------|
| **规模** | 5,000 题（入门到竞赛级） |
| **题型** | 代码生成（多语言） |
| **评测维度** | 编程能力 |
| **主要指标** | Pass@K |
| **来源** | https://github.com/THUDM/CodeGPT |

---

## 评测维度总览

| 评测维度 | 数据集 | 优先级 |
|---------|--------|--------|
| 通用语言理解 | MMLU, HellaSwag | 高 |
| 数学推理 | GSM8K, MATH | 高 |
| 代码生成 | HumanEval, MBPP | 高（代码模型） |
| 回复真实性 | TruthfulQA | 中 |

---

## 数据集选择决策树

```
输入：模型类型
    │
    ├── 通用语言模型
    │     → MMLU（必测）
    │     → HellaSwag（推荐）
    │     → TruthfulQA（可选）
    │
    ├── 数学能力重要
    │     → GSM8K（必测）
    │     → MATH（推荐，数学专项）
    │
    └── 代码模型
          → HumanEval（必测）
          → MBPP（推荐）
          → APPS（可选，深度代码能力）
```

---

## 与 lm-eval 的对应关系

| 数据集 | lm-eval task name | 说明 |
|--------|------------------|------|
| MMLU | `mmlu` | 需指定 `--tasks mmlu` |
| GSM8K | `gsm8k` | 需指定 `--tasks gsm8k` |
| HumanEval | `humaneval` | 需安装额外依赖 |
| MBPP | `mbpp` | 需指定 `--tasks mbpp` |
| HellaSwag | `hellaswag` | 需指定 `--tasks hellaswag` |
| TruthfulQA | `truthfulqa_mc1` | 需指定 `--tasks truthfulqa_mc1` |

来源：https://github.com/EleutherAI/lm-evaluation-harness

---

## 风险与边界

- 各数据集版本可能更新（如 MMLU 有多个版本）
- lm-eval 的 task name 可能随版本变化
- MATH 数据集评测需要 LaTeX 解析支持

Sources:
1. https://arxiv.org/abs/2009.03300 — MMLU
2. https://arxiv.org/abs/2110.14168 — GSM8K
3. https://arxiv.org/abs/2107.03374 — HumanEval
4. https://github.com/mbpp — MBPP
5. https://arxiv.org/abs/1905.07830 — HellaSwag
6. https://arxiv.org/abs/2109.07958 — TruthfulQA
7. https://arxiv.org/abs/2103.14074 — MATH
8. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval

Risk of Staleness:
- 各数据集版本可能更新
- lm-eval task name 映射可能有变化

Out of Scope Kept:
- 未收录所有数据集
- 未写完整评测流程
- 未写自定义数据集导入方法
