# Task Card

Task ID: T704
Title: Cross-Project Deep-Research Pack
Owner: MINIMAX
Type: PACK-深研究0接管专题包
Priority: P1

## Input

基于：
- `tasks/accepted/T301-inference-service-mvp-result.md`
- `tasks/accepted/T302-ai-gateway-mvp-result.md`
- `tasks/accepted/T303-eval-module-mvp-result.md`
- `tasks/accepted/T304-finetune-demo-mvp-result.md`
- `tasks/review-pending/T604-project-dependency-matrix-v1.md`
- `tasks/review-pending/T604-build-order-roadmap-v1.md`
- `tasks/review-pending/T604-component-interface-contract-sketch-v1.md`
- `tasks/review-pending/T604-data-and-telemetry-flow-map-v1.md`
- `tasks/review-pending/T604-risk-register-v1.md`

## Expected Output

本专题包必须产出以下 8 个文件：

1. `tasks/review-pending/T704-cross-project-pack-manifest.md`
2. `tasks/review-pending/T704-project-dependency-matrix-v2.md`
3. `tasks/review-pending/T704-build-order-roadmap-v2.md`
4. `tasks/review-pending/T704-interface-contract-boundary-notes-v1.md`
5. `tasks/review-pending/T704-data-and-telemetry-flow-map-v2.md`
6. `tasks/review-pending/T704-component-ownership-map-v1.md`
7. `tasks/review-pending/T704-mvp-milestone-board-v2.md`
8. `tasks/review-pending/T704-risk-register-v2.md`

## Deliverable Notes

### v2 类文件

在 T604 的基础上做更清晰的边界收口和推进顺序收紧。

### ownership-map-v1

把四个模块各自负责什么、不负责什么梳理清楚。

### interface-contract-boundary-notes-v1

重点解释哪些接口是提案、哪些是依赖外部工具、哪些只适合后续阶段。

### milestone-board-v2

把 Phase 进一步拆细，便于 Codex 后续拆任务。

### manifest

总结本包升级了什么、未定项和对下一包可复用输入。

## Template

使用 MiniMax 标准输出协议。

## Acceptance Criteria

- 必须写满 8 个输出文件
- 必须保持跨项目系统化主线
- 所有重点链接必须是精确 URL
- 不写成最终定版架构

## Out of Scope

- 不写代码实现
