Task ID: T151
Task Title: 为 TensorRT-LLM 资料包补官方文档入口与更稳的更新链接
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 T141 结果和 T141-review-round-2 修订。补官方文档入口，将不稳定的 discussion 链接替换为更稳的 release/tag/blog 链接。

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
- NVIDIA 官方推理产品页：https://www.nvidia.com/en-us/ai-data-science/products/tensorrt/
- NGC 容器镜像（生产部署推荐）：https://catalog.ngc.nvidia.com/orgs/nvidia/containers/tensorrt
- NVIDIA Developer Blog（TensorRT-LLM 文章集合）：https://developer.nvidia.com/blog

注：TensorRT-LLM 官方文档目前托管于 GitHub（README + source docs），而非 docs.nvidia.com。docs.nvidia.com/deeplearning/tensorrt/ 为通用 TensorRT 文档，非 TensorRT-LLM 专用。

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

- **TensorRT-LLM v1.2.0 稳定版发布**（2025-03）：最新稳定 release，包含主流 LLM 支持更新
  - 来源：https://github.com/NVIDIA/TensorRT-LLM/releases
- **DeepSeek-R1 优化支持**：官方提供 DeepSeek-R1 在 TensorRT-LLM 上的最佳性能实践文档
  - Blog：https://github.com/NVIDIA/TensorRT-LLM/blob/main/docs/source/blogs/Best_perf_practice_on_DeepSeek-R1_in_TensorRT-LLM.md
- **Skip Softmax 优化**（2025-12）：NVIDIA 官方博客介绍 TensorRT-LLM 长上下文推理优化
  - Blog：https://developer.nvidia.com/blog/accelerating-long-context-inference-with-skip-softmax-in-nvidia-tensorrt-llm/
- **TensorRT LLM AutoDeploy**（2026-02）：NVIDIA 官方博客介绍自动化推理优化部署
  - Blog：https://developer.nvidia.com/blog/automating-inference-optimizations-with-nvidia-tensorrt-llm-autodeploy/

注：TensorRT-LLM 版本号自 v1.0.0 起，跳过早期 0.x 序列。"Release 0.17.0"条目已删除（无对应 tag）。

## 六、精确优先阅读链接（6 个，均为精确 URL）

1. GitHub 主仓库（含 README 和 Quick Start）：https://github.com/NVIDIA/TensorRT-LLM
2. Triton Backend 集成说明：https://github.com/NVIDIA/TensorRT-LLM/tree/main/triton_backend
3. DeepSeek-R1 最佳性能实践 Blog：https://github.com/NVIDIA/TensorRT-LLM/blob/main/docs/source/blogs/Best_perf_practice_on_DeepSeek-R1_in_TensorRT-LLM.md
4. Release 页面（稳定版）：https://github.com/NVIDIA/TensorRT-LLM/releases
5. NVIDIA 官方推理产品页：https://www.nvidia.com/en-us/ai-data-science/products/tensorrt/
6. NGC 容器镜像：https://catalog.ngc.nvidia.com/orgs/nvidia/containers/tensorrt

Sources:
1. https://github.com/NVIDIA/TensorRT-LLM — 主仓库
2. https://github.com/NVIDIA/TensorRT-LLM/tree/main/triton_backend — Triton backend 集成
3. https://github.com/NVIDIA/TensorRT-LLM/releases — 稳定版 release 列表
4. https://www.nvidia.com/en-us/ai-data-science/products/tensorrt/ — NVIDIA 官方 TensorRT 产品页
5. https://catalog.ngc.nvidia.com/orgs/nvidia/containers/tensorrt — NGC 容器镜像
6. https://developer.nvidia.com/blog/accelerating-long-context-inference-with-skip-softmax-in-nvidia-tensorrt-llm/ — Skip Softmax blog
7. https://developer.nvidia.com/blog/automating-inference-optimizations-with-nvidia-tensorrt-llm-autodeploy/ — AutoDeploy blog

Risk of Staleness:
- TensorRT-LLM 版本迭代快，pip install 的默认版本以实际安装时为准
- Dev branch API 变化比 Release branch 更大
- NVIDIA blog 上的文章反映特定时间点的技术，后续版本可能有变化

Out of Scope Kept:
- 未写成完整章节
- 未做 vLLM/SGLang/Triton IS 全面对比
- 未补充 docs.nvidia.com 链接（TensorRT-LLM 官方文档不在该域名下）

Need Codex Review On:
- 是否需要在入口处更明确地标注"TensorRT-LLM 文档托管于 GitHub 而非 docs.nvidia.com"
