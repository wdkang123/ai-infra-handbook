# Task Card

Task ID: T303
Title: eval-module MVP 目录与边界设计
Owner: MINIMAX
Type: B-分析任务
Priority: P1

## Input

基于：
- `tasks/accepted/T162-observability-eval-sources-result.md`
- `tasks/accepted/T175-benchmark-sources-result.md`
- `tasks/accepted/T301-inference-service-mvp-result.md`
- `tasks/accepted/T302-ai-gateway-mvp-result.md`

## Expected Output

产出 `eval-module` 的 MVP 设计文档，包含：

1. 定位说明
2. 最小目录结构
3. 核心接口或任务入口
4. 依赖关系
5. 与 inference-service / ai-gateway / benchmark 的边界
6. 最小可运行路径

## Template

使用 MiniMax 标准输出协议。

## Acceptance Criteria

- 定位清晰，不做过度设计
- 以“调用已有推理入口做评测”为主，不重新实现推理服务
- 如果写 CLI / SDK 示例，必须明确它们是**提案接口**，不是现有实现
- 目录结构最小化

## Allowed Sources

- 已通过的 T162 / T175
- 已通过的 T301 / T302 设计稿

## Out of Scope

- 不写完整 benchmark 系统
- 不做 Leaderboard 平台设计
