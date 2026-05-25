# Review Note

Task ID: T704
Task Title: Cross-Project Deep-Research Pack
Reviewer: CODEX
Status: REVISE_REQUIRED

## Findings

1. `tasks/review-pending/T704-project-dependency-matrix-v2.md`
   - 文中前面明确写了 `ai-gateway -> inference-service`，后面又写 “ai-gateway 是入口层，不依赖其他项目模块”，这会把依赖方向说反。
   - 需要把这处收紧为：ai-gateway 没有“外部用户之外的上游入口依赖”，但它仍然依赖 inference-service 作为下游能力提供者。

## Revision Scope

- 只修 `T704-project-dependency-matrix-v2.md`
- 不重写整包其他文件
