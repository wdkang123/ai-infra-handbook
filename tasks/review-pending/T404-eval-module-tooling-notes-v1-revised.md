Task ID: T404
Task Title: Evaluation / Benchmark Long-Run Pack v1 收紧修订
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 T402-review，删除 tool notes 中的数量型营销表述（"50+ 场景"、"70+"）。

Result:

# Eval Module Tooling Notes v1（修订版）

## 概述

本文档说明 eval-module 与三个主要评测工具（LM-Eval Harness、Stanford HELM、BigCode Eval Harness）的可能关系，为工具选型提供工程级参考，不输出最终实现结论。

## LM-Eval Harness

### 工具特征
- **定位**：标准 benchmark 评测工具
- **评测方式**：在标准数据集（MMLU、GSM8K、HumanEval 等）上运行模型，输出量化分数
- **接入方式**：Python API + CLI
- **下游对接**：支持 vLLM、SGLang 等推理引擎作为 backend

### 与 eval-module 的可能关系
- **直接集成**：eval-module 可调用 lm-eval 的 Python API，在标准数据集上运行评测
- **接口对应**：lm-eval 的 `--model vllm` + `--tasks mmlu` 与 eval-module 的 `evaluate(dataset="mmlu")` 接口概念对应
- **局限**：lm-eval 不包含评测结果持久化和版本对比能力，这部分需要 eval-module 自己实现

来源：https://github.com/EleutherAI/lm-evaluation-harness

## Stanford HELM

### 工具特征
- **定位**：全面评测框架
- **评测方式**：覆盖多场景综合评测，执行完整评测并展示结果
- **接入方式**：主要是 Web 界面和 API
- **下游对接**：支持多种推理服务和模型

### 与 eval-module 的可能关系
- **参考架构**：HELM 的评测维度和组织方式可作为 eval-module 设计评测场景的参考
- **不做直接集成**：HELM 偏学术研究性质，作为工具集成到本项目的工程成本较高
- **替代方案**：用 lm-eval 的多任务评测能力可以覆盖 HELM 的核心场景

来源：https://crfm.stanford.edu/helm/

## BigCode Eval Harness

### 工具特征
- **定位**：代码模型专用评测工具
- **评测方式**：HumanEval、MBPP 等代码任务，执行 Pass@K 评测
- **接入方式**：Python API + CLI
- **下游对接**：支持多种代码模型和推理服务

### 与 eval-module 的可能关系
- **可选集成**：如果本项目涉及代码模型评测，eval-module 可调用 bigcode-eval 的 Python API
- **非默认优先**：代码模型评测不在 AI Infra 的默认 MVP 范围内，除非明确需求否则可暂不集成
- **评测指标对应**：bigcode-eval 的 Pass@K 指标与 eval-module 的 `evaluate(metric="pass@k")` 概念对应

来源：https://github.com/bigcode-project/bigcode-eval-harness

## 工具选型对照

| 维度 | LM-Eval Harness | Stanford HELM | BigCode Eval |
|------|-----------------|--------------|--------------|
| 评测范围 | 通用 benchmark | 多场景综合 | 代码模型专项 |
| 与 eval-module 关系 | 直接集成优先 | 参考架构 | 可选集成 |
| 工程集成成本 | 低（Python API） | 高（偏外部服务） | 低（Python API） |
| 是否 MVP 必须 | 是 | 否 | 否（除非有代码模型需求） |

## eval-module MVP 的评测工具路径建议

```
eval-module
    ↓ 调用
LM-Eval Harness（主要工具）
    ↓ 下游
inference-service（vLLM/SGLang）
    ↓ 或
外部模型 API（OpenAI GPT-4 等，作为 Judge）
```

eval-module 本身专注于：评测任务管理、结果记录、版本对比。底层执行依赖 lm-eval 或其他评测工具。

## 需要 Codex 最终判断的点

1. eval-module 是否直接集成 lm-eval，还是自行实现评测逻辑？
2. 如果自行实现，评测数据集从哪获取（lm-eval 内置数据集 vs 自己准备）？
3. 评测结果持久化方案（文件？数据库？）是否需要在设计阶段确定？
4. LLM-as-Judge 的 Judge 模型用哪个（GPT-4 还是开源模型）？

Sources:
1. https://github.com/EleutherAI/lm-evaluation-harness — LM-Eval Harness
2. https://crfm.stanford.edu/helm/ — Stanford HELM
3. https://github.com/bigcode-project/bigcode-eval-harness — BigCode Eval Harness
4. https://github.com/tensorzero/tensorzero — TensorZero（参考，eval+observability 集成）

Risk of Staleness:
- LM-Eval Harness 版本更新可能影响 API 兼容性
- BigCode Eval Harness 版本更新可能影响 benchmark 兼容性

Out of Scope Kept:
- 未写代码实现
- 未写最终架构结论
- 未写评测结果存储方案
