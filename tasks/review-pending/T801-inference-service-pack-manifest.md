# inference-service Execution Prep Pack Manifest

## Task ID: T801
## Task Title: inference-service Execution Prep Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T301 MVP 设计、T701 决策 memo、T701 部署模式图、T701 实践目录、T714 依赖矩阵、T715 任务拆解，准备 inference-service 实施前包。

---

# inference-service Execution Prep Pack Manifest

## 包概述

本包为 inference-service 模块的实施前准备包，8 个文件全部完成，从 repo layout、API contract、config surface、runtime dependencies、test plan、validation checklist、risk cut list 七个维度收束可执行输入。

## 已完成交付物

| 文件 | 内容 |
|------|------|
| T801-inference-service-repo-layout-v1.md | 目录结构设计 |
| T801-inference-service-api-contract-v1.md | OpenAI 兼容 API 接口定义 |
| T801-inference-service-config-surface-v1.md | 配置项清单 |
| T801-inference-service-runtime-dependency-note-v1.md | 运行时依赖说明 |
| T801-inference-service-test-plan-v1.md | 测试计划 |
| T801-inference-service-validation-checklist-v1.md | 验收清单 |
| T801-inference-service-risk-cut-list-v1.md | 风险裁剪清单 |

## 本包升级了什么

| 维度 | T301 MVP | T801（本包） |
|------|---------|-------------|
| 目录结构 | 骨架 | 完整可执行目录 |
| API 定义 | 简单列表 | 详细接口契约 |
| 配置项 | 提到有 config | 完整 config surface |
| 运行时依赖 | 简单提到 | 版本锁定建议 |
| 测试计划 | 无 | 单元+集成+端到端 |
| 验收清单 | 无 | 逐项可验证 |
| 风险清单 | 无 | 6 个风险及缓解 |

## 供 Codex 直接使用的输入

### 开箱即用
- **Repo Layout**：直接对应 `src/inference_service/` 目录结构
- **Config Surface**：对应 `config.yaml` / `pyproject.toml` 配置
- **Validation Checklist**：逐项验证清单

### 关键决策点（本包未解决，需要 Codex 判断）
1. **默认引擎**：vLLM vs SGLang（已有建议：vLLM）
2. **GPU 型号**：确认是否支持 TensorRT-LLM（Ampere/Hopper）
3. **多模型管理**：MVP 单模型还是多模型切换

## 关键链接

| 资源 | URL |
|------|-----|
| vLLM 文档 | https://docs.vllm.ai/ |
| SGLang 文档 | https://sglang.readthedocs.io/ |
| Triton IS 文档 | https://docs.nvidia.com/deeplearning/triton-inference-server/ |
| TensorRT-LLM | https://nvidia.github.io/TensorRT-LLM/ |

## 与其他包的关系

| 包 | 关系 |
|----|------|
| T802 ai-gateway | 上游调用 inference-service |
| T803 eval-module | 通过 lm-eval backend 调用 inference-service |
| T804 finetune-demo | 加载 adapter 到 inference-service |
| T805 cross-project | 整体集成测试 |

## 整体完成度

| 专题包 | 文件数 | 完成度 |
|--------|--------|--------|
| T801 inference-service | 8 | 100% |

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://sglang.readthedocs.io/ — SGLang
3. https://docs.nvidia.com/deeplearning/triton-inference-server/ — Triton IS
4. https://nvidia.github.io/TensorRT-LLM/ — TensorRT-LLM
5. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval

Risk of Staleness:
- 各引擎版本更新快，具体 API 以实际版本为准

Out of Scope Kept:
- 未写代码实现
- 未写 Dockerfile
- 未写 K8s 部署配置
