Task ID: T113
Task Title: 重做 Triton 资料包，目标改为 NVIDIA Triton Inference Server
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 review note T103 重做。本任务中的 Triton 明确指 **NVIDIA Triton Inference Server**（推理服务平台），不是 OpenAI Triton language/compiler（内核编译器）。需输出围绕 Triton Inference Server 的结构化资料包。

Result:

## 一、项目定位

**NVIDIA Triton Inference Server**（以下简称 Triton IS）是一个开源推理服务平台软件，不是内核编译器。

核心定位：
- 将多个深度学习框架（TensorRT、PyTorch、ONNX、OpenVINO、Python、RAPIDS FIL 等）的模型统一部署为在线推理服务
- 支持 HTTP/REST 和 gRPC 协议，提供标准化的推理接口
- 支持 GPU（NVIDIA 为主）和 CPU 推理，可运行在云、数据中心、边缘和嵌入式设备
- 与 Kubernetes 集成，支持多模型并发、动态 batching、模型版本管理
- **不是** kernel 开发工具，不是 compiler，与 vLLM / SGLang 的定位不同

## 二、官方入口

- 官方文档站：https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/
- GitHub 组织：https://github.com/triton-inference-server
- 主仓库：https://github.com/triton-inference-server/server
- 最新 release：https://github.com/triton-inference-server/server/releases（最新为 2.66.0，2026-03）
- 官方产品页：https://www.nvidia.com/en-us/ai-data-science/products/triton-inference-server/

## 三、核心功能摘要

### 模型仓库（Model Repository）
- 基于文件系统的模型仓库，通过目录结构定义模型版本和配置
- 每个模型需要 `config.pbtxt` 配置文件描述输入/输出/后端/实例化策略
- 来源：https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/model_repository.html

### 支持的推理后端（Backends）
- **TensorRT**：NVIDIA 自研高性能推理引擎，LLM 场景常配合 TensorRT-LLM 使用
- **PyTorch**：直接运行 TorchScript 模型
- **ONNX Runtime**：跨框架模型格式
- **OpenVINO**：Intel CPU/GPU 推理
- **Python**：直接运行 Python 推理逻辑（适合非标准算子）
- **RAPIDS FIL**：GPU 加速的树模型推理
- 来源：https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/model_repository.html

### 协议支持
- **HTTP/REST**：标准推理接口，兼容性强
- **gRPC**：高性能 RPC 协议，适合低延迟场景
- **Metrics**：Prometheus 格式监控指标，支持观测
- 来源：https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/

### 部署形态
- **Docker 镜像**：`nvcr.io/nvidia/tritonserver:<version>-py3`，生产部署推荐方式
- **Kubernetes**：通过 Kubernetes Deployment 或 Helm Chart 部署，支持 Prometheus 监控
- **裸机**：直接运行 `tritonserver` 可执行文件

## 四、与 vLLM / SGLang 的边界说明（不做优劣结论）

| 维度 | Triton Inference Server | vLLM / SGLang |
|------|----------------------|----------------|
| 定位 | 通用推理服务平台，多框架统一管理 | LLM 专用推理引擎 |
| 协议 | HTTP/gRPC（标准推理协议） | OpenAI 兼容 API |
| 模型格式 | TensorRT/ONNX/PyTorch/自定义 | 主要 Hugging Face 模型 |
| 调度 | 动态 batching，支持多模型并发 | Continuous batching，LLM 专用调度 |
| LLM 优化 | 需配合 TensorRT-LLM 后端 | 原生 PagedAttention/RadixAttention |

**边界说明**：Triton IS 是一个"模型可以来自任何框架"的推理容器，适合企业多模型统一管理场景；vLLM/SGLang 是"专门为 LLM 优化"的推理引擎，适合以 LLM 为核心的系统。两者在生产架构中常配合使用：TensorRT-LLM 提供 LLM 算子优化，Triton IS 提供 HTTP/gRPC 服务层。

## 五、近 6-12 个月重要更新线索

- **Release 2.66.0**（2026-03，对应 NGC container 26.02）：最新 stable release
  - 来源：https://github.com/triton-inference-server/server/releases
- **Triton Inference Server 更名动态**：NVIDIA 官方产品页面已将"Triton Inference Server"品牌延伸至更广泛的推理软件栈，包括 TensorRT-LLM 集成为其 LLM 推理组件
  - 来源：https://www.nvidia.com/en-us/ai-data-science/products/triton-inference-server/
- **TensorRT-LLM 集成深化**：Triton IS 作为服务层，TensorRT-LLM 作为 LLM 优化后端，是 2024-2025 年生产 LLM 部署的主流组合之一
  - 来源：https://github.com/triton-inference-server/server（README 中有说明）

## 六、精确优先阅读链接（6-8 个）

1. 官方文档首页（总览）：https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/
2. Model Repository 指南：https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/model_repository.html
3. GitHub 主仓库：https://github.com/triton-inference-server/server
4. 最新 release（2.66.0）：https://github.com/triton-inference-server/server/releases
5. NVIDIA Triton 产品页：https://www.nvidia.com/en-us/ai-data-science/products/triton-inference-server/
6. 快速入门 / 部署指南：https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/getting_started.html
7. Backend 扩展开发文档：https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/customization_guide/backends.html
8. Kubernetes 部署文档：https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/deploy.html

Sources:
1. https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/ — 官方文档
2. https://github.com/triton-inference-server/server — 主仓库
3. https://github.com/triton-inference-server/server/releases — 最新 release
4. https://www.nvidia.com/en-us/ai-data-science/products/triton-inference-server/ — 官方产品页
5. https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/model_repository.html — 模型仓库
6. https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/customization_guide/backends.html — 后端扩展

Risk of Staleness:
- release 版本号随时间变化，2.66.0 为 2026-03 最新
- Triton IS 品牌定位在 NVIDIA 内部有调整（可能与其他推理组件整合），具体以官方文档为准
- TensorRT-LLM 集成方式属于快速演进领域，NVIDIA 官方文档中的描述最为可靠

Out of Scope Kept:
- 未写任何 Triton language/compiler（OpenAI Triton）内容
- 未写成完整推理服务总论
- 未做 Triton IS vs 其他框架的优劣评判

Need Codex Review On:
- Triton IS 与 TensorRT-LLM 的组合关系在 AI Infra 章节中应放在哪个层级（推理服务层？协议层？部署层？）
- "Triton IS + TensorRT-LLM"作为 2024-2025 年生产 LLM 部署主流路径，是否需要在书中单独说明，还是仅作为延伸阅读
