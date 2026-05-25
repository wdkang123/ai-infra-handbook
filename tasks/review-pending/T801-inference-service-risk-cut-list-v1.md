# inference-service Risk Cut List v1

## Task ID: T801
## Task Title: inference-service Execution Prep Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T301 MVP 设计，准备 inference-service 实施前包。

---

# inference-service Risk Cut List v1

## 概述

本文档定义 inference-service 的主要风险和缓解措施，供 Codex 实施前参考。

---

## 风险清单

| 风险 ID | 风险描述 | 影响 | 概率 | 缓解措施 |
|---------|---------|------|------|---------|
| R-01 | GPU 显存不足导致 OOM | 高 | 高 | 使用量化模型；降低 gpu_memory_utilization |
| R-02 | vLLM 版本不兼容导致 API 失败 | 中 | 中 | 锁定版本；测试环境验证 |
| R-03 | 模型加载时间过长 | 中 | 中 | 本地缓存；预热请求 |
| R-04 | 多 GPU 并行配置复杂 | 中 | 低 | MVP 单 GPU；后续引入 tensor_parallel |
| R-05 | 引擎抽象层接口与实际 API 不匹配 | 高 | 中 | 先实现 vLLM 专用版本；抽象层后续 |
| R-06 | SGLang 生态不如 vLLM 成熟 | 低 | 低 | MVP 默认 vLLM；SGLang 按需引入 |

---

## 风险详解

### R-01：GPU 显存不足

**风险描述**：LoRA adapter 加载 + base model 推理显存需求超出实际硬件。

**影响**：推理失败，OOM。

**缓解措施**：
- 使用 QLoRA 4-bit 量化降低显存
- 降低 `vllm.gpu_memory_utilization`（默认 0.9 → 0.7）
- 使用更小的模型（0.5B/1B/3B）

**验证方法**：
```bash
nvidia-smi --query-gpu=memory.free,memory.total --format=csv
```

---

### R-02：vLLM 版本不兼容

**风险描述**：vLLM 版本更新导致 API 不兼容。

**影响**：需要修改 inference-service 代码。

**缓解措施**：
- 在 `pyproject.toml` 锁定版本范围：`vllm>=0.6.0,<0.7.0`
- 在测试环境验证后再更新版本
- 记录已知兼容版本列表

**参考**：
- https://docs.vllm.ai/en/latest/changelog.html
- https://github.com/vllm-project/vllm/releases

---

### R-03：模型加载时间过长

**风险描述**：首次启动时模型下载和加载耗时。

**影响**：服务启动慢，影响开发体验。

**缓解措施**：
- 使用本地模型缓存（设置 `model.cache_dir`）
- 使用较小的模型用于开发（0.5B）
- 在 Dockerfile 中预加载模型

**验证方法**：
```bash
time inference-service serve --model Qwen/Qwen2.5-0.5B-Instruct
```

---

### R-04：多 GPU 并行配置复杂

**风险描述**：tensor_parallel_size > 1 时配置复杂。

**影响**：MVP 阶段不引入多 GPU。

**缓解措施**：
- MVP 默认 `tensor_parallel_size=1`
- 文档中注明多 GPU 是后续阶段

---

### R-05：引擎抽象层接口不匹配

**风险描述**：BaseEngine 抽象与实际 vLLM API 差异大。

**影响**：需要频繁修改抽象层。

**缓解措施**：
- MVP 先实现 vLLM 专用代码，不做抽象
- 等 vLLM API 稳定后再重构抽象层
- 或使用 vLLM 内置的 engine interface

---

### R-06：SGLang 生态不如 vLLM 成熟

**风险描述**：SGLang 文档和问题解决资源少。

**影响**：接入 SGLang 成本高。

**缓解措施**：
- MVP 默认 vLLM
- SGLang 作为备选，文档补充

---

## MVP 阶段必须规避的风险

| 风险 | 规避措施 |
|------|---------|
| GPU OOM | 使用量化模型 + 小模型 |
| 版本不兼容 | 锁定版本 |
| 启动慢 | 本地缓存 |
| 多 GPU 复杂 | 单 GPU |

---

## 风险决策点

| 决策点 | 选项 | 建议 |
|--------|------|------|
| 默认引擎 | vLLM / SGLang | vLLM |
| GPU 型号 | Ampere / Hopper / 其他 | 确认后决定 TRT-LLM 引入 |
| 模型大小 | 0.5B / 3B / 7B | 0.5B 用于 MVP |
| 版本锁定 | v0.6.x | v0.6.3（稳定） |

---

Sources:
1. https://docs.vllm.ai/en/latest/getting_started/installation.html — vLLM Installation
2. https://docs.vllm.ai/en/latest/models/engine_args.html — vLLM Engine Arguments
3. https://github.com/vllm-project/vllm/releases — vLLM Releases

Risk of Staleness:
- 风险可能随硬件和软件版本变化

Out of Scope Kept:
- 未写完整应急预案
- 未写监控告警配置
