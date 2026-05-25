# Task Card

Task ID: T304
Title: finetune-demo MVP 目录与边界设计
Owner: MINIMAX
Type: B-分析任务
Priority: P1

## Input

基于：
- `tasks/accepted/T173-lora-peft-sources-result.md`
- `tasks/accepted/T174-unsloth-sources-result.md`

## Expected Output

产出 `finetune-demo` 的 MVP 设计文档，包含：

1. 定位说明
2. 最小目录结构
3. 核心脚本 / 接口
4. 依赖关系
5. 与 inference-service 的交接边界
6. 最小可运行路径

## Template

使用 MiniMax 标准输出协议。

## Acceptance Criteria

- 聚焦 LoRA / QLoRA / Unsloth 路径
- 目录结构最小化，体现数据、训练脚本、导出结果
- 如果写 CLI / 命令示例，必须明确它们是**提案接口**，不是现有实现
- 不把分布式训练、复杂数据治理塞进 MVP

## Allowed Sources

- 已通过的 T173 / T174

## Out of Scope

- 不写完整训练平台
- 不做多节点训练设计
