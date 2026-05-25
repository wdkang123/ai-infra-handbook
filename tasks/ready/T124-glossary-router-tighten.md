# Task Card

Task ID: T124  
Title: 收紧 glossary 中 Router 术语的高波动表述并补精确来源  
Owner: MINIMAX  
Type: C-普通章节任务  
Priority: P0

## Input

基于：

- `tasks/review-pending/T114-glossary-batch-01-result.md`
- `tasks/review/T114-review-round-2.md`

## Expected Output

只修订 `Router` 这一项，保留现有四段结构：

1. 一句话定义
2. 工程上下文中的意义
3. 和项目的关系
4. 易混淆点

同时满足：

- 删除 Agentic memory/tool-use 的扩展描述
- 用精确来源替换组织页或模糊来源

## Template

使用 MiniMax 标准输出协议。

## Acceptance Criteria

- 只修 Router 项，不重写整份 glossary
- 表述稳健，不提前延伸到高波动语义
- 至少给 2 个精确可追溯来源

## Allowed Sources

- 官方文档
- 官方仓库具体页面
- 高质量、可追溯的资料页

## Out of Scope

- 不新增术语
- 不重写其余 9 项
