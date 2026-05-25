# Task Card

Task ID: T604
Title: Cross-Project Systemization Pack
Owner: MINIMAX
Type: PACK-0接管链式专题包
Priority: P1

## Input

基于：
- `tasks/accepted/T301-inference-service-mvp-result.md`
- `tasks/accepted/T302-ai-gateway-mvp-result.md`
- `tasks/accepted/T303-eval-module-mvp-result.md`
- `tasks/accepted/T304-finetune-demo-mvp-result.md`
- `tasks/review-pending/T601-inference-integration-map-v1.md`
- `tasks/review-pending/T602-observability-eval-decision-memo-v1.md`
- `tasks/review-pending/T603-finetuning-decision-memo-v2.md`
- `tasks/review-pending/T603-finetune-demo-training-map-v2.md`

## Expected Output

本专题包必须产出以下 7 个文件：

1. `tasks/review-pending/T604-cross-project-pack-manifest.md`
2. `tasks/review-pending/T604-project-dependency-matrix-v1.md`
3. `tasks/review-pending/T604-build-order-roadmap-v1.md`
4. `tasks/review-pending/T604-component-interface-contract-sketch-v1.md`
5. `tasks/review-pending/T604-data-and-telemetry-flow-map-v1.md`
6. `tasks/review-pending/T604-mvp-milestone-board-draft-v1.md`
7. `tasks/review-pending/T604-risk-register-v1.md`

## Deliverable Notes

### dependency-matrix-v1

把 4 个项目之间的输入、输出、依赖方向整理清楚。

### build-order-roadmap-v1

说明如果按最小可验证路径推进，先做什么、后做什么、哪些可以并行。

### interface-contract-sketch-v1

整理提案级接口，不写成“已实现接口”。

### data-and-telemetry-flow-map-v1

把：
- request
- response
- trace
- metric
- evaluation result
- finetune artifact

之间的流向说明清楚。

### milestone-board-draft-v1

给出阶段化里程碑草案，方便 Codex 后续拆成更细任务。

### risk-register-v1

列出 8 到 12 个推进风险，按技术、资料、实现、验证四类整理。

### manifest

总结完成项、未定项、需要 Codex 后续拆解的点。

## Template

使用 MiniMax 标准输出协议。

## Acceptance Criteria

- 必须写满 7 个输出文件
- 必须使用前面专题包的产物作为输入
- 输出仍然是资料级系统化文档，不是实现承诺
- 所有重点链接必须是精确 URL

## Out of Scope

- 不写代码实现
