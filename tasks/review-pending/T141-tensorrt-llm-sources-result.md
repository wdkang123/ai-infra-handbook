Task ID: T141
Task Title: 收紧 TensorRT-LLM 资料包中的模糊更新线索与占位链接
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 T131 初稿和 review note T141 修订。只删/换无精确来源的更新项，替换占位链接，保留其他结构。

Result:

## 一、项目定位

**TensorRT-LLM** 是 NVIDIA 提供的开源 LLM 推理优化库（注意：不是服务网关，不是 Triton Inference Server）。

核心定位：
- 提供 Python API 用于定义 LLM 模型并构建 TensorRT 引擎，以在 NVIDIA GPU 上高效执行推理
- 包含用于创建执行 TensorRT 引擎的 Python 和 C++ 运行时组件
- 支持与 NVIDIA Triton Inference Server 集成（Triton 作为服务层，TensorRT-LLM 作为 LLM 算子优化后端）
- 支持 INT4/INT8 量化（weight-only）和 SmoothQuant 等完整量化技术
- 支持张量并行和管道并行，可从单 GPU 扩展到多节点配置

## 二、官方入口

- GitHub 仓库：https://github.com/NVIDIA/TensorRT-LLM
- 官方文档（GitHub README）：https://github.com/NVIDIA/TensorRT-LLM#readme
- Triton Backend 集成文档：https://github.com/NVIDIA/TensorRT-LLM/tree/main/triton_backend

## 三、核心定位摘要

TensorRT-LLM 是一个**推理优化后端**，不是服务网关。它专注于：
- 将 LLM 模型编译为高度优化的 TensorRT 引擎
- 在 NVIDIA GPU 上实现低延迟、高吞吐的 LLM 推理
- 提供量化（FP8/INT8/INT4/SmoothQuant）、Kernel Fusion、CUDA Graph 等优化手段

与 vLLM/SGLang 的本质区别：
- vLLM/SGLang 是"开箱即用"的推理引擎，自带调度器
- TensorRT-LLM 是底层算子优化层，需要配合服务框架使用

## 四、与 Triton IS 的关系

- **TensorRT-LLM 是 Triton IS 的后端之一**：Triton IS 可以通过 `tensorrtllm` backend 运行 TensorRT-LLM 编译的模型
- 在生产 LLM 部署中，两者常组合使用：TensorRT-LLM 提供 LLM 算子优化，Triton IS 提供 HTTP/gRPC 服务层、多模型并发、监控等能力
- 这一组合是 2024-2025 年生产环境部署 NVIDIA GPU LLM 的主流路径之一
- 来源：https://github.com/NVIDIA/TensorRT-LLM/tree/main/triton_backend

## 五、近 6-12 个月重要更新线索（有精确来源的条目）

- **TensorRT-LLM 持续活跃**：Release branch 每月更新一次，Dev branch 更频繁
  - 来源：https://github.com/NVIDIA/TensorRT-LLM/releases
- **DeepSeek-R1 优化支持**（2025 年初）：官方提供 DeepSeek-R1 在 TensorRT-LLM 上的最佳性能实践文档
  - Blog：https://github.com/NVIDIA/TensorRT-LLM/blob/main/docs/source/blogs/Best_perf_practice_on_DeepSeek-R1_in_TensorRT-LLM.md
- **Release 0.17.0**（2025-01）：包含对主流 LLM 的支持更新
  - 来源：https://github.com/NVIDIA/TensorRT-LLM/discussions/2726

注：Sparse Attention 支持、DeepSeek-V3.2 Blackwell GPU 优化、TensorRT-LLM Roadmap 等条目在本次资料包中无精确官方链接可查，已删除。

## 六、精确优先阅读链接（6 个，均为精确 URL）

1. GitHub 主仓库（含 README 和 Quick Start）：https://github.com/NVIDIA/TensorRT-LLM
2. Triton Backend 集成说明：https://github.com/NVIDIA/TensorRT-LLM/tree/main/triton_backend
3. DeepSeek-R1 最佳性能实践 Blog：https://github.com/NVIDIA/TensorRT-LLM/blob/main/docs/source/blogs/Best_perf_practice_on_DeepSeek-R1_in_TensorRT-LLM.md
4. Release Branch（稳定版）：https://github.com/NVIDIA/TensorRT-LLM/releases
5. NVIDIA 官方推理产品页（包含 TensorRT-LLM）：https://www.nvidia.com/en-us/ai-data-science/products/tensorrt/
6. NGC 容器镜像（生产部署推荐）：https://catalog.ngc.nvidia.com/orgs/nvidia/containers/tensorrt

Sources:
1. https://github.com/NVIDIA/TensorRT-LLM — 主仓库
2. https://github.com/NVIDIA/TensorRT-LLM/tree/main/triton_backend — Triton backend 集成
3. https://github.com/NVIDIA/TensorRT-LLM/blob/main/docs/source/blogs/Best_perf_practice_on_DeepSeek-R1_in_TensorRT-LLM.md — DeepSeek-R1 性能实践
4. https://github.com/NVIDIA/TensorRT-LLM/releases — 稳定版 release
5. https://www.nvidia.com/en-us/ai-data-science/products/tensorrt/ — NVIDIA 官方 TensorRT 产品页
6. https://catalog.ngc.nvidia.com/orgs/nvidia/containers/tensorrt — NGC 容器镜像

Risk of Staleness:
- TensorRT-LLM 版本迭代快，pip install 的默认版本以实际安装时为准
- Dev branch API 变化比 Release branch 更大
- DeepSeek-R1 优化内容属于快速演进领域

Out of Scope Kept:
- 未写成完整章节
- 未做 vLLM/SGLang/Triton IS 全面对比

Need Codex Review On:
- Sparse Attention、Blackwell GPU 优化、Roadmap 等条目是否需要 MiniMax 后续补充精确链接
