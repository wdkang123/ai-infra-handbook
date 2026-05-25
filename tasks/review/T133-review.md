# Review Note

Task ID: T133  
Task Title: Glossary 第二批术语初稿  
Review Decision: REVISE_REQUIRED

## Findings

1. `Canary Routing`、`Tracing`、`Replay` 等术语主要依赖基础设施背景来源，而不是直接支撑术语定义的精确来源，见 [T133-glossary-batch-02-result.md](tasks/review-pending/T133-glossary-batch-02-result.md#L99)、[T133-glossary-batch-02-result.md](tasks/review-pending/T133-glossary-batch-02-result.md#L129)、[T133-glossary-batch-02-result.md](tasks/review-pending/T133-glossary-batch-02-result.md#L143)。
2. 个别项目关系表述仍有高推断成分，例如把 `vLLM` 直接写成减少 prefill 阶段显存管理开销，或把 `Replay` 直接绑定到 Triton model repository，见 [T133-glossary-batch-02-result.md](tasks/review-pending/T133-glossary-batch-02-result.md#L17) 和 [T133-glossary-batch-02-result.md](tasks/review-pending/T133-glossary-batch-02-result.md#L147)。

## Action

- 只修较弱的 4 个术语：`Canary Routing`、`Rate Limiting`、`Tracing`、`Replay`
- 其余 6 个术语保留
