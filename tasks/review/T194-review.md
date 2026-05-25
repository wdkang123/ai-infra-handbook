# Review Note

Task ID: T194  
Task Title: 产出 Observability 章节初稿  
Review Decision: REVISE_REQUIRED

## Findings

1. 第 5 节的指标表里，`TTFT / ITL / TPM / RPS / P99` 的来源过于笼统，像“各推理引擎”“Metrics”这类写法不够支撑章节正文。
2. 第 8 节最小实践使用 Langfuse 的方向没问题，但示例代码和产出物把 `TTFT / ITL` 直接写成可在 dashboard 中查看，当前示例本身并没有证明这一点。
3. 第 10 节延伸阅读里混入了 evaluation 工具，这一章虽然可以提边界，但不应把 evaluation 资料放得太重。

## Action

- 收紧第 5 节，只保留有明确来源且适合作为 observability 章节核心指标的内容
- 把最小实践和输出物收紧成“trace / log / token usage 基本可见”，不要直接承诺 TTFT / ITL 已接通
- 延伸阅读以 observability 为主，evaluation 只保留轻量边界引用
