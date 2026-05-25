# Review Note

Task ID: T143  
Task Title: 收紧 glossary 第二批术语中的弱来源与高推断项  
Review Decision: REVISE_REQUIRED

## Findings

1. `Canary Routing`、`Tracing`、`Replay` 仍主要依赖“基础设施背景”来源，而不是直接支撑术语本身的精确来源。
2. `Replay 是 eval-module 的核心测试方法之一` 这种项目关系判断仍偏强，建议收回到更中性的“可用于 staging/回放验证”层面。

## Action

- 只再修 `Canary Routing`、`Tracing`、`Replay`
- `Rate Limiting` 这版可以保留
