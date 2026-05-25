# Review Note

Task ID: T114  
Task Title: 修订 glossary 第一批术语，补精确来源并收紧易误导表述  
Review Decision: REVISE_REQUIRED

## Findings

1. 大部分术语已经变稳，但 `Router` 术语仍然混入了高波动表述，例如 Agentic AI 场景下的 memory/tool-use 决策能力。
2. `Router` 的来源仍不够精确，`https://github.com/vllm-project` 只是组织页，不是可以直接支撑术语定义的精确来源。
3. glossary 的目标是提供稳固底层定义，这一项更适合收回到“请求分发和治理组件”的基础定义，不应提前延伸到 Agentic 语义。

## Action

- 只修 `Router` 这一项，不重写其余 9 项
- 删除高波动 Agentic 扩展表述
- 用精确文档或仓库页面替换模糊来源
