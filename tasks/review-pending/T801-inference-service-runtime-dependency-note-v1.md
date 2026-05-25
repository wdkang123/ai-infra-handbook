# inference-service Runtime Dependency Note v1

## Task ID: T801
## Task Title: inference-service Execution Prep Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T301 MVP 设计，准备 inference-service 实施前包。

---

# inference-service Runtime Dependency Note v1

## 概述

本文档定义 inference-service 的运行时依赖，包括 Python 包、硬件、系统级依赖。

---

## Python 依赖

### 核心依赖

| 包 | 版本建议 | 说明 | 用途 |
|----|---------|------|------|
| `fastapi` | `>=0.115.0` | Web 框架 | API 服务 |
| `uvicorn[standard]` | `>=0.30.0` | ASGI 服务器 | 生产运行 |
| `pydantic` | `>=2.0.0` | 数据验证 | 配置和请求验证 |
| `pydantic-settings` | `>=2.0.0` | 配置管理 | 环境变量加载 |
| `pyyaml` | `>=6.0` | YAML 解析 | config.yaml 加载 |
| `httpx` | `>=0.27.0` | HTTP 客户端 | 健康检查等 |
| `prometheus-client` | `>=0.20.0` | Prometheus 客户端 | metrics 暴露 |

### 推理引擎依赖

| 包 | 版本建议 | 说明 | 用途 |
|----|---------|------|------|
| `vllm` | `>=0.6.0,<0.7.0` | vLLM 引擎（默认） | 推理计算 |
| `sglang` | `>=0.1.0` | SGLang 引擎（可选） | 备选推理引擎 |
| `tritonclient[all]` | `>=3.0.0` | Triton 客户端（可选） | Triton 后端 |

来源：https://docs.vllm.ai/en/latest/getting_started/installation.html
来源：https://pypi.org/project/vllm/

---

## 系统级依赖

### 硬件要求

| 组件 | 最低要求 | 推荐配置 | 说明 |
|------|---------|---------|------|
| GPU | NVIDIA GPU | A100/H100/A10G | 推理必须 |
| 显存 | 6GB | 24GB+ | 取决于模型大小 |
| CUDA | 11.8+ | 12.1+ | vLLM 要求 |
| 内存 | 16GB | 32GB+ | 模型加载 |

来源：https://docs.vllm.ai/en/latest/getting_started/requirements.html

### 系统包

| 包 | 说明 | 用途 |
|----|------|------|
| `nvidia-cuda-toolkit` | CUDA 工具链 | GPU 计算 |
| `libopenmpi-dev` | OpenMPI | 分布式通信（可选） |
| `openssh-client` | SSH 客户端 | 远程管理 |

---

## 依赖版本兼容性

### vLLM 与 CUDA 版本

| vLLM 版本 | CUDA 11.8 | CUDA 12.1 |
|-----------|-----------|-----------|
| 0.5.x | 支持 | 支持 |
| 0.6.x | 支持 | 支持 |
| 0.7.x | 待确认 | 支持 |

来源：https://docs.vllm.ai/en/latest/getting_started/installation.html

### vLLM 与 Python 版本

| vLLM 版本 | Python 3.9 | Python 3.10 | Python 3.11 | Python 3.12 |
|-----------|-----------|-------------|-------------|-------------|
| 0.6.x | 支持 | 支持 | 支持 | 支持 |

---

## GPU 显存估算

### 模型显存需求参考

| 模型大小 | BF16 显存 | INT4 量化 | INT8 量化 |
|---------|----------|---------|---------|
| 7B | ~14GB | ~4GB | ~8GB |
| 13B | ~26GB | ~7GB | ~14GB |
| 70B | ~140GB | ~35GB | ~70GB |

### LoRA Adapter 额外显存

| LoRA rank | 额外显存（FP16） |
|-----------|----------------|
| 8 | ~50MB |
| 16 | ~100MB |
| 64 | ~400MB |

---

## 版本锁定建议

### pyproject.toml 锁定策略

```toml
[project]
dependencies = [
    "fastapi>=0.115.0,<0.116.0",
    "uvicorn[standard]>=0.30.0,<0.31.0",
    "vllm>=0.6.0,<0.7.0",
    "prometheus-client>=0.20.0,<0.21.0",
]
```

### 容器化建议

- 使用 NVIDIA CUDA 基础镜像（`nvidia/cuda:12.1.0-runtime-ubuntu22.04`）
- 在容器内安装 vLLM，避免系统级冲突

---

## 常见运行时问题

| 问题 | 原因 | 缓解措施 |
|------|------|---------|
| CUDA OOM | 显存不足 | 降低 `gpu_memory_utilization`，使用量化 |
| 模型加载慢 | 模型文件大 | 使用本地缓存 |
| GPU 未识别 | CUDA 未正确安装 | 检查 `nvidia-smi` 输出 |
| vLLM 启动失败 | 依赖缺失 | 使用官方安装脚本 |

来源：https://docs.vllm.ai/en/latest/getting_started/installation.html

---

Sources:
1. https://docs.vllm.ai/en/latest/getting_started/installation.html — vLLM Installation
2. https://docs.vllm.ai/en/latest/getting_started/requirements.html — vLLM Requirements
3. https://docs.nvidia.com/deeplearning/triton-inference-server/ — Triton IS

Risk of Staleness:
- vLLM 版本更新频繁，依赖兼容性可能变化

Out of Scope Kept:
- 未写 Kubernetes 部署依赖
- 未写分布式训练依赖
