# Task Card

Task ID: T301
Title: inference-service MVP 目录与边界设计
Owner: MINIMAX
Type: B-分析任务
Priority: P1

## Input

基于当前已通过的资料包（vLLM、SGLang、Triton IS、TensorRT-LLM）和 comparison-index v2，理解 inference-service 在整个 AI Infra 项目中的位置。

## Expected Output

产出 inference-service 的 MVP 设计文档，包含：

1. **定位说明**：inference-service 是什么、解决什么问题
2. **目录结构**：最小可运行目录骨架
3. **核心接口**：暴露哪些 API/CLI 接口
4. **依赖关系**：依赖哪些下层组件（vLLM/SGLang/Triton IS）
5. **边界说明**：与 ai-gateway、eval-module 的边界
6. **最小可运行路径**：如何快速跑通一个推理请求

## Template

使用 MiniMax 标准输出协议。

## Acceptance Criteria

- 定位清晰，不做过度设计
- 目录结构最小化，体现 core dependencies
- 接口定义具体可执行
- 边界描述准确，反映与其他模块的协作关系

## Allowed Sources

- 已通过的 vLLM 资料包
- 已通过的 SGLang 资料包
- 已通过的 Triton IS 资料包
- 已通过的 TensorRT-LLM 资料包
- comparison-index v2

## Out of Scope

- 不写完整 inference-serving 手册
- 不做多供应商统一抽象（那是 ai-gateway 的范围）
- 不做 GPU 集群管理
