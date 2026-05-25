# Review Note

Task ID: T146  
Task Title: 修订 Triton IS 章节初稿中的无来源结论和旧实践  
Review Decision: REVISE_REQUIRED

## Findings

1. 仍保留了 `Triton IS 自身调度开销极低` 这类偏强表述，虽然比上一版收敛，但仍建议改成更中性的“服务层开销通常小于后端推理开销”。
2. 最小实践里直接假设镜像内置 `triton_repo` 示例模型仓库，稳妥性仍不足，建议改成更贴近官方 getting started 的步骤或更明确地说明这是示例路径。

## Action

- 只收紧这两处，不重写整章
