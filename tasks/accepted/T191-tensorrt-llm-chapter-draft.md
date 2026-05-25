Task ID: T191
Task Title: 产出 TensorRT-LLM 章节初稿
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 T141 TensorRT-LLM 资料包和 base.md 章节模板，产出 TensorRT-LLM 章节初稿，使用 10 节结构。

Result:

# TensorRT-LLM

## 1. 这是什么

TensorRT-LLM 是 NVIDIA 提供的开源 LLM 推理优化库，不是服务网关，也不是 Triton Inference Server。它的核心功能是将 LLM 模型编译为高度优化的 TensorRT 引擎，并在 NVIDIA GPU 上实现高效推理。

**注意与 vLLM/SGLang 的本质区别**：
- vLLM/SGLang 是"开箱即用"的推理引擎，自带调度器和 OpenAI 兼容 API
- TensorRT-LLM 是**底层算子优化层**，需要配合服务框架使用，不能单独作为 LLM 服务端点

## 2. 为什么重要

在 AI Infra 推理服务栈中，TensorRT-LLM 的价值在于：

1. **极致推理性能**：通过 TensorRT 引擎编译实现 Kernel Fusion、量化（FP8/INT8/INT4）、CUDA Graph 等优化，在 NVIDIA GPU 上实现低延迟、高吞吐
2. **NVIDIA 生态集成**：与 Triton IS 深度集成，是 2024-2025 年生产环境部署 NVIDIA GPU LLM 的主流路径之一
3. **扩展性强**：支持张量并行和管道并行，可从单 GPU 扩展到多节点配置

## 3. 核心原理

### TensorRT 引擎编译
TensorRT-LLM 提供 Python API 用于定义 LLM 模型结构，并将其编译为 TensorRT 引擎。编译阶段进行算子融合、图优化、 quantization-aware training 等，运行时执行高度优化的 CUDA kernel。

来源：https://github.com/NVIDIA/TensorRT-LLM

### 量化支持
TensorRT-LLM 支持完整的量化技术栈：
- **FP8**：NVIDIA Hopper GPU 原生支持，适合最新 GPU
- **INT8/INT4 (Weight-Only)**：无需校准数据集的量化，适合快速部署
- **SmoothQuant**：减轻量化精度损失的技术

来源：https://github.com/NVIDIA/TensorRT-LLM

### 与 Triton IS 的集成
Triton IS 通过 `tensorrtllm` backend 运行 TensorRT-LLM 编译的模型。这种组合是生产部署的经典架构：TensorRT-LLM 提供算子层优化，Triton IS 提供 HTTP/gRPC 服务层、多模型并发、监控。

来源：https://github.com/NVIDIA/TensorRT-LLM/tree/main/triton_backend

## 4. 常见方案 / 组件

- **TensorRT-LLM Python API**：`model definition → TensorRT engine` 的编译流程
- **TensorRT-LLM Runtime**：执行 TensorRT 引擎的 Python 和 C++ 运行时组件
- **tensorrtllm backend**：Triton IS 的 TensorRT-LLM 后端插件
- **NGC 容器镜像**：生产部署推荐使用 NVIDIA NGC 提供的预装镜像

来源：https://catalog.ngc.nvidia.com/orgs/nvidia/containers/tensorrt

## 5. 关键指标

- **推理延迟（Latency）**：TensorRT-LLM 的核心优势，经过编译优化后通常低于未优化方案
- **吞吐（Throughput）**：取决于 batch size、模型大小、量化精度
- **显存占用（GPU Memory）**：INT4 量化可显著降低显存，支持更大 batch size

注：TensorRT-LLM 的具体性能数据与模型、硬件、量化精度强相关，无法给出通用达标值。

## 6. 常见误区

1. **"TensorRT-LLM 是完整推理服务"**：TensorRT-LLM 是优化后端，需要 Triton IS 等服务框架配合才能作为服务端点
2. **"TensorRT-LLM 比 vLLM 快"**：两者定位不同，TensorRT-LLM 是底层优化库，vLLM 是完整推理引擎；在同一模型、同一硬件下对比需明确前提
3. **"TensorRT-LLM 可以直接通过 API 调用"**：TensorRT-LLM 通过 Python API 构建引擎，通过 Triton IS 或自定义服务层暴露 HTTP/gRPC 接口

## 7. 与项目关系

在 AI Infra 学习路径中，TensorRT-LLM 帮助理解"算子层 + 服务层"分离的架构：

- TensorRT-LLM + Triton IS 是理解"优化引擎 + 服务抽象"分离的经典案例
- 对比 vLLM/SGLang（自带服务层），理解不同层次抽象的权衡
- 如果项目涉及 NVIDIA GPU 生产部署，TensorRT-LLM 是理解性能优化的关键组件

## 8. 最小实践任务

**目标**：使用 NGC 容器快速体验 TensorRT-LLM 的编译和推理流程（使用预编译模型，无需从头编译）。

```bash
# 拉取含 TensorRT-LLM 的 NGC 镜像
docker pull nvcr.io/nvidia/tensorrt:24.01-py3

# 运行基础验证（参考官方文档）
docker run --rm --gpus=1 \
    nvcr.io/nvidia/tensorrt:24.01-py3 \
    python -c "import tensorrt; print(tensorrt.__version__)"

# 注：实际编译 LLM 模型需要参考 TensorRT-LLM 官方文档的详细步骤
# https://github.com/NVIDIA/TensorRT-LLM#quick-start
```

来源：https://catalog.ngc.nvidia.com/orgs/nvidia/containers/tensorrt

## 9. 输出物

- NGC 容器运行中，含 TensorRT-LLM 环境
- 可通过 `python` 验证 tensorrt 和 tensorrt_llm 包
- 了解编译 + 运行的基本流程

## 10. 延伸阅读

1. https://github.com/NVIDIA/TensorRT-LLM — 主仓库（含 Quick Start）
2. https://github.com/NVIDIA/TensorRT-LLM/tree/main/triton_backend — Triton Backend 集成说明
3. https://github.com/NVIDIA/TensorRT-LLM/releases — 稳定版 release
4. https://www.nvidia.com/en-us/ai-data-science/products/tensorrt/ — NVIDIA 官方 TensorRT 产品页
5. https://catalog.ngc.nvidia.com/orgs/nvidia/containers/tensorrt — NGC 容器镜像
6. https://developer.nvidia.com/blog/accelerating-long-context-inference-with-skip-softmax-in-nvidia-tensorrt-llm/ — Skip Softmax 优化 blog

Sources:
1. https://github.com/NVIDIA/TensorRT-LLM — 主仓库
2. https://github.com/NVIDIA/TensorRT-LLM/tree/main/triton_backend — Triton backend 集成
3. https://github.com/NVIDIA/TensorRT-LLM/releases — 稳定版 release
4. https://www.nvidia.com/en-us/ai-data-science/products/tensorrt/ — NVIDIA TensorRT 产品页
5. https://catalog.ngc.nvidia.com/orgs/nvidia/containers/tensorrt — NGC 容器镜像
6. https://developer.nvidia.com/blog/accelerating-long-context-inference-with-skip-softmax-in-nvidia-tensorrt-llm/ — Skip Softmax blog

Risk of Staleness:
- TensorRT-LLM 版本迭代快，pip install 的默认版本以实际安装时为准
- NGC 镜像版本号随时间变化，24.01 为示例版本
- DeepSeek-R1 优化等条目属于快速演进领域

Out of Scope Kept:
- 未写成完整推理服务手册
- 未做 vLLM/SGLang/TensorRT-LLM 全面优劣对比
- 未写 TensorRT 通用（non-LLM）内容

Need Codex Review On:
- 最小实践任务是否需要更具体的可执行步骤（编译模型）
