# Task Card

Task ID: T401
Title: Observability Long-Run Pack v1
Owner: MINIMAX
Type: PACK-长跑专题包
Priority: P1

## Input

基于：
- `tasks/accepted/T204-observability-chapter-revision.md`
- `tasks/accepted/T307-observability-sources-index-v1.md`
- `tasks/accepted/T310-observability-comparison-index-v1.md`
- `tasks/accepted/T313-observability-eval-glossary-batch-03.md`
- `tasks/accepted/T301-inference-service-mvp-result.md`
- `tasks/accepted/T302-ai-gateway-mvp-result.md`
- `tasks/accepted/T303-eval-module-mvp-result.md`

## Expected Output

本专题包必须产出以下 4 个文件：

1. `tasks/review-pending/T401-observability-pack-manifest.md`
2. `tasks/review-pending/T401-observability-project-map-v1.md`
3. `tasks/review-pending/T401-observability-practice-catalog-v1.md`
4. `tasks/review-pending/T401-observability-sources-index-v2.md`

## Deliverable Notes

### T401-observability-project-map-v1

说明 observability 在以下模块中的落点与边界：

- inference-service
- ai-gateway
- eval-module

### T401-observability-practice-catalog-v1

整理 6 到 8 个低门槛最小实践：

- tracing
- metrics
- token usage
- dashboard
- request logging

### T401-observability-sources-index-v2

在 v1 基础上收紧和补齐更稳定的优先阅读链接。

### T401-observability-pack-manifest

总结：

- 本包完成了哪些交付物
- 每个交付物的用途
- 哪些点仍需 Codex 判断

## Template

使用 MiniMax 标准输出协议。

## Acceptance Criteria

- 必须写满 4 个输出文件
- 4 个输出都围绕 observability 主线
- 所有重点链接必须是精确 URL
- 不扩写成完整 observability 手册

## Allowed Sources

- 已通过的 observability 相关资产

## Out of Scope

- 不做代码实现
- 不写最终架构结论
