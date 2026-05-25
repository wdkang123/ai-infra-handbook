# Task Card

Task ID: T141  
Title: 收紧 TensorRT-LLM 资料包中的模糊更新线索与占位链接  
Owner: MINIMAX  
Type: D-资料型任务  
Priority: P0

## Input

基于：

- `tasks/review-pending/T131-tensorrt-llm-sources-result.md`
- `tasks/review/T131-review.md`

## Expected Output

保留当前资料包结构，但：

1. 删除无精确来源的更新项
2. 用精确 URL 替换占位链接
3. 保持“项目定位 / 官方入口 / 与 Triton IS 的关系 / 更新线索 / 优先阅读链接”结构

## Template

使用 MiniMax 标准输出协议。

## Acceptance Criteria

- 不再出现“GitHub 首页或 Discussions 中有…”这类占位表述
- 更新线索都必须能落到精确官方链接

## Allowed Sources

- NVIDIA 官方文档
- 官方 GitHub
- NVIDIA 官方 blog / release notes

## Out of Scope

- 不写完整章节
