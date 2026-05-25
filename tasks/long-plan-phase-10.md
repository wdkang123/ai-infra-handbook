# Long Plan Phase 10

## Phase Goal

在 blueprint 和 fixture 都收口之后，进入 implementation map 阶段。

## Why This Phase

当前我们已经有：

- MVP / contract / scaffold
- starter file blueprints
- fixture / sample asset

但真正开始编码前，还缺：

- 每个项目的按文件实现顺序
- import / dependency map
- 最小测试顺序
- patch 切分建议
- 验证矩阵

这些内容适合继续交给 MiniMax 批量生成，能显著减少 Codex 真正开写时的路径选择成本。

## Output Principle

每个 pack 优先产出：

1. file implementation order
2. import/dependency map
3. patch split proposal
4. validation matrix
5. blocker/risk checklist

## Topics

1. inference-service implementation map
2. ai-gateway implementation map
3. eval-module implementation map
4. finetune-demo implementation map
5. cross-project integration implementation map
