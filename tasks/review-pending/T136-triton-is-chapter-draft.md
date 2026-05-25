Task ID: T136
Task Title: 编写 Triton IS 章节模板化初稿
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 T113 资料包（NVIDIA Triton Inference Server 定位、后端支持、与 TensorRT-LLM 关系）和 base.md 章节模板，输出 Triton IS 章节初稿。

Result:

# NVIDIA Triton Inference Server

## 1. 这是什么

NVIDIA Triton Inference Server（Triton IS）是一个开源推理服务平台软件，不是 LLM 专用引擎，也不是内核编译器。它的核心功能是将多个深度学习框架（TensorRT、PyTorch、ONNX、OpenVINO、Python、RAPIDS FIL 等）的模型统一部署为在线推理服务。

与 vLLM/SGLang 的本质区别：
- vLLM/SGLang 是"LLM 专用推理引擎"，自带调度器和 KV Cache 优化
- Triton IS 是"通用推理服务容器"，通过后端抽象接入任意框架的模型

## 2. 为什么重要

在 AI Infra 推理服务栈中，Triton IS 的价值在于：

1. **多框架统一管理**：生产环境通常有 CV 模型（ResNet、VIT）、NLP 模型（BERT）、LLM（Llama、DeepSeek）共存，Triton IS 提供统一接口管理异构模型
2. **生产级治理**：动态 batching、多模型并发、模型版本管理、Prometheus 监控、内置健康检查
3. **企业部署标准**：与 Kubernetes 深度集成，是企业级 AI 部署的事实标准之一

## 3. 核心原理

### Model Repository
以文件系统目录结构组织模型，每个模型有 `config.pbtxt` 描述输入/输出/后端/实例化策略，支持多版本管理。Triton IS 启动时扫描仓库，按配置实例化模型。

来源：https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/model_repository.html

### 推理后端（Backends）
- **TensorRT**：NVIDIA 自研高性能推理引擎，适合 NVIDIA GPU 上的优化推理
- **PyTorch**：直接运行 TorchScript 模型
- **ONNX Runtime**：跨框架模型格式
- **Python**：直接运行 Python 推理逻辑，适合非标准算子或快速原型
- **OpenVINO**：Intel CPU/GPU 推理
- **RAPIDS FIL**：GPU 加速树模型推理

来源：https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/customization_guide/backends.html

### 协议支持
- **HTTP/REST**：标准推理接口，兼容性最强
- **gRPC**：高性能 RPC 协议，适合低延迟场景
- **Metrics**：Prometheus 格式指标，支持与 Kubernetes HPA 集成

来源：https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/

### 与 TensorRT-LLM 的关系
Triton IS 通过 `tensorrtllm` backend 运行 TensorRT-LLM 编译的模型。这一组合是 2024-2025 年生产环境部署 NVIDIA LLM 的主流路径之一：TensorRT-LLM 提供算子层优化，Triton IS 提供服务层（HTTP/gRPC、多模型并发、监控）。

来源：https://github.com/NVIDIA/TensorRT-LLM/tree/main/triton_backend

## 4. 常见方案 / 组件

- **tritonserver**：主服务进程，负责模型加载、请求调度、响应返回
- **Model Repository**：模型存储和组织方式，`config.pbtxt` 定义每个模型的运行配置
- **Dynamic Batching**：Triton IS 内置的动态 batching 器，将多个请求合并为一个批次推理
- **Ensemble Scheduling**：支持多模型串联推理（如：预处理模型 → LLM → 后处理模型），Triton IS 自动管理数据流

来源：https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/

## 5. 关键指标

- **吞吐（Throughput）**：Triton IS 自身调度开销极低，主要瓶颈在推理后端
- **延迟（Latency）**：端到端延迟由后端推理时间 + Triton IS 调度开销构成，通常调度开销 < 1ms
- **多模型并发数**：每个模型可配置多个实例（`instance_group`），Triton IS 自动负载均衡
- **GPU 利用率**：通过 Prometheus metrics 暴露，由后端推理实现决定

## 6. 常见误区

1. **"Triton IS 是 LLM 推理引擎"**：Triton IS 是通用推理服务平台，LLM 推理能力依赖 TensorRT-LLM backend，不是独立 LLM 引擎
2. **"Triton IS 比 vLLM 快"**：Triton IS 本身不加速推理，它提供的是服务抽象；实际推理速度取决于后端（TensorRT/vLLM/SGLang）
3. **"Triton IS 不支持 vLLM"**：Triton IS 有 `vllm` backend 或通过 Python backend 加载 vLLM，但 vLLM 本身已有完整的 OpenAI 兼容 API，生产场景直接用 vLLM 的 API 往往更简单
4. **"Triton IS 只能用在 NVIDIA GPU 上"**：Triton IS 支持 CPU 推理（通过 ONNX Runtime、Python backend），但性能最优场景在 NVIDIA GPU

## 7. 与项目关系

在 AI Infra 学习路径中，Triton IS 帮助理解生产级推理服务的架构要素：

- Triton IS 的 Model Repository 和 Dynamic Batching 是理解 AI Gateway 层资源管理概念的基础
- Triton IS + TensorRT-LLM 组合是理解"服务层 + 算子层"分离的经典案例
- 如果项目目标是构建 AI Gateway 或多模型统一推理平台，Triton IS 是重要的参考实现

## 8. 最小实践任务

**目标**：用 Triton IS 部署一个 ONNX 模型的推理服务（无需 GPU）。

```bash
# 拉取 Triton 镜像（CPU 推理）
docker pull nvcr.io/nvidia/tritonserver:23.10-py3

# 准备模型仓库（以 ONNX 分类模型为例）
mkdir -p model_repository/densenet/1/
# 将 model.onnx 放入 model_repository/densenet/1/

# 启动服务
docker run --rm -p 8000:8000 -p 8001:8001 \
    -v $(pwd)/model_repository:/models \
    nvcr.io/nvidia/tritonserver:23.10-py3 \
    tritonserver --model-repository=/models

# HTTP 推理调用
curl -X POST http://localhost:8000/v2/models/densenet/infer \
    --data-urlencode 'input_data@image.bin' \
    -o prediction.json
```

来源：https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/getting_started.html

## 9. 输出物

- Triton IS 服务运行中（HTTP 端口 8000，gRPC 端口 8001）
- 可通过 `curl` 或 `tritonclient` Python SDK 调用
- Prometheus metrics 端点可用：`http://localhost:8002/metrics`

## 10. 延伸阅读

1. https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/ — 官方文档
2. https://github.com/triton-inference-server/server — 主仓库
3. https://github.com/triton-inference-server/server/releases — 最新 release（2.66.0）
4. https://www.nvidia.com/en-us/ai-data-science/products/triton-inference-server/ — 官方产品页
5. https://github.com/NVIDIA/TensorRT-LLM/tree/main/triton_backend — TensorRT-LLM Triton backend
6. https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/model_repository.html — Model Repository 文档
7. https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/deploy.html — Kubernetes 部署文档

Sources:
1. https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/ — Triton IS 官方文档
2. https://github.com/triton-inference-server/server — 主仓库
3. https://www.nvidia.com/en-us/ai-data-science/products/triton-inference-server/ — 官方产品页
4. https://github.com/NVIDIA/TensorRT-LLM/tree/main/triton_backend — TensorRT-LLM backend
5. https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/customization_guide/backends.html — 后端扩展文档
6. https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/model_repository.html — 模型仓库文档

Risk of Staleness:
- Triton IS release 版本随时间变化，2.66.0 为 2026-03 最新
- NVIDIA 可能在未来版本中调整 Triton IS 与 TensorRT-LLM 的品牌整合方式
- CPU 推理的最小实践可能因版本不同而略有差异

Out of Scope Kept:
- 未写 Triton language/compiler
- 未做与 vLLM/SGLang 的全面优劣对比

Need Codex Review On:
- "Triton IS + TensorRT-LLM"组合在 AI Infra 章节中应放在哪个层级（部署层？协议层？）
- 最小实践是否需要更新为最新版本（当前示例基于 23.10，可能有更新）
