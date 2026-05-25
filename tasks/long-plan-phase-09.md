# Long Plan Phase 09

## Phase Goal

在 starter blueprint 全部收口后，继续为真实编码阶段准备“implementation-ready fixtures / sample assets”。

## Why This Phase

当前我们已经有：

- API contract
- scaffold blueprints
- starter file blueprints

但真正开始写代码前，还缺一层非常实用的落地输入：

- 请求 / 响应 fixture
- config example
- sample dataset / result JSON
- smoke expected output
- adapter / artifact manifest

这层内容很适合 MiniMax 持续生成，也最能减少后续 Codex 实现时的来回猜测。

## Output Principle

每个 pack 优先产出 4 到 6 个文件，尽量覆盖：

1. fixture catalog
2. sample payloads
3. expected output examples
4. config examples
5. artifact / file manifest

## Topics

1. inference-service fixtures
2. ai-gateway fixtures
3. eval-module fixtures
4. finetune-demo fixtures
5. root integration fixtures
