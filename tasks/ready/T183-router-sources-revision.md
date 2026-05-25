# Task Card

Task ID: T183  
Title: 收紧 router 资料包中的坏链接和实现边界  
Owner: MINIMAX  
Type: D-资料型任务  
Priority: P0

## Input

基于：

- `tasks/review-pending/T172-router-sources-result.md`
- `tasks/review/T172-review.md`

## Expected Output

保留资料包结构，但：

1. 修正坏链接
2. 将 vLLM / SGLang 从 router 实现名单中挪出或改为“后端引擎参考”
3. 强化 router 与 gateway / backend 的边界

## Template

使用 MiniMax 标准输出协议。

## Acceptance Criteria

- 不再有坏链接
- 实现名单更准确
- 边界说明更清楚

## Allowed Sources

- 官方文档
- 官方 GitHub
- 官方产品文档

## Out of Scope

- 不写完整章节
