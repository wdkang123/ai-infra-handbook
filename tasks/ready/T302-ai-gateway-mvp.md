# Task Card

Task ID: T302
Title: ai-gateway MVP 目录与边界设计
Owner: MINIMAX
Type: B-分析任务
Priority: P1

## Input

基于当前已通过的 AI Gateway 资料包（T181 收紧版）、Router 资料包（T183 收紧版），理解 ai-gateway 在整个 AI Infra 项目中的位置。

## Expected Output

产出 ai-gateway 的 MVP 设计文档，包含：

1. **定位说明**：ai-gateway 是什么、解决什么问题
2. **目录结构**：最小可运行目录骨架
3. **核心接口**：暴露哪些 API/CLI 接口
4. **依赖关系**：依赖哪些下层组件（vLLM/SGLang、Triton IS、或直接对接各模型 API）
5. **边界说明**：与 inference-service、eval-module 的边界
6. **最小可运行路径**：如何快速跑通一个请求到响应的完整流程

## Template

使用 MiniMax 标准输出协议。

## Acceptance Criteria

- 定位清晰，不做过度设计
- 目录结构最小化，体现核心功能（路由、限流、鉴权等）
- 接口定义具体可执行
- 边界描述准确，反映与其他模块的协作关系

## Allowed Sources

- 已通过的 AI Gateway 资料包（T181）
- 已通过的 Router 资料包（T183）
- 已通过的 Cache 资料包（T182）

## Out of Scope

- 不写完整 gateway 产品手册
- 不做多供应商统一 SDK 抽象（仅做接入层）
- 不做复杂的 AI Safety/Guardrails 实现
