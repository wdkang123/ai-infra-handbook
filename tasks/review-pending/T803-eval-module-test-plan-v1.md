# eval-module Test Plan v1

## Task ID: T803
## Task Title: eval-module Execution Prep Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T303 MVP 设计，准备 eval-module 实施前包。

---

# eval-module Test Plan v1

## 概述

本文档定义 eval-module 的测试计划，覆盖单元测试、集成测试、端到端测试。

---

## 测试分层

| 测试类型 | 覆盖范围 | Mock 程度 |
|---------|---------|----------|
| 单元测试 | Runner、数据集加载、结果解析 | 完全 Mock lm-eval |
| 集成测试 | Runner + inference-service | Mock lm-eval API |
| 端到端测试 | 完整评测链路 | 无 Mock |

---

## 单元测试

### Runner

#### LmEvalRunner

| 测试用例 | 输入 | 预期输出 |
|---------|------|---------|
| `test_run_returns_eval_result` | Mock lm-eval 返回 | EvalResult 实例 |
| `test_run_with_fewshot` | num_fewshot=5 | fewshot 参数传递 |
| `test_list_tasks` | — | 任务列表非空 |
| `test_invalid_task` | 无效 task | 抛出 ValueError |

#### BaseRunner

| 测试用例 | 输入 | 预期输出 |
|---------|------|---------|
| `test_abstract_methods` | 实例化 BaseRunner | 抛出 TypeError |

### Result Store

| 测试用例 | 输入 | 预期输出 |
|---------|------|---------|
| `test_save_json` | 有效 EvalResult | 文件创建成功 |
| `test_load_json` | 已有 JSON 文件 | EvalResult 实例 |
| `test_load_nonexistent` | 无效路径 | 抛出 FileNotFoundError |

### Comparator

| 测试用例 | 输入 | 预期输出 |
|---------|------|---------|
| `test_compare_accuracy_delta` | 两个结果 | diff 计算正确 |
| `test_compare_same_results` | 相同结果 | diff = 0 |
| `test_compare_improvement` | candidate > baseline | 正向 diff |

---

## 集成测试

### Runner + Mock lm-eval

| 测试用例 | 输入 | Mock 方式 | 预期输出 |
|---------|------|----------|---------|
| `test_run_mmlu` | MMLU task | Mock API | accuracy 非空 |
| `test_run_gsm8k` | GSM8K task | Mock API | accuracy 非空 |
| `test_run_multiple_tasks` | [mmlu, gsm8k] | Mock API | 两个结果 |

---

## 端到端测试

### 完整评测链路

```bash
# 1. 启动 inference-service（如未启动）
# inference-service serve --engine vllm --model Qwen/Qwen2.5-0.5B-Instruct &

# 2. 运行 MMLU 评测
eval-module run \
    --backend lm-eval \
    --task mmlu \
    --model Qwen/Qwen2.5-0.5B-Instruct \
    --num-fewshot 5 \
    --output ./results/mmlu_result.json

# 3. 查看结果
cat ./results/mmlu_result.json

# 4. 运行 GSM8K 评测
eval-module run \
    --backend lm-eval \
    --task gsm8k \
    --model Qwen/Qwen2.5-0.5B-Instruct \
    --output ./results/gsm8k_result.json

# 5. 对比结果
eval-module compare \
    --baseline ./results/mmlu_result.json \
    --candidate ./results/gsm8k_result.json
```

### 预期输出

| 步骤 | 预期结果 |
|------|---------|
| MMLU 评测 | `{"task": "mmlu", "accuracy": 0.65, ...}` |
| GSM8K 评测 | `{"task": "gsm8k", "accuracy": 0.50, ...}` |

---

## 测试工具建议

| 工具 | 用途 |
|------|------|
| `pytest` | 测试框架 |
| `pytest-asyncio` | 异步测试 |
| `pytest-cov` | 覆盖率 |
| `pytest-mock` | Mock 工具 |

---

## 测试覆盖率目标

| 模块 | 目标覆盖率 |
|------|----------|
| `runners/` | 90% |
| `results/` | 85% |
| `datasets/` | 80% |
| `evaluator.py` | 85% |
| **总体** | **85%** |

---

Sources:
1. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval
2. https://pytest.org/ — pytest

Risk of Staleness:
- 测试命令可能因 lm-eval 版本变化

Out of Scope Kept:
- 未写压力测试
