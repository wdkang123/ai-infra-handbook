# Review Note

Task ID: T171  
Task Title: 搜集 caching / prefix caching / semantic cache 官方资料与核心链接  
Review Decision: REVISE_REQUIRED

## Findings

1. 主线方向是对的，但资料包里混入了不太相关的条目，例如 `OpenAI Evals`，会让主题发散。
2. 表格中有小错误和不够稳的表达，例如“夸引擎/夸实例”这类明显应为“跨引擎/跨实例”的内容，需要清理。
3. Mooncake、LMCache、GPTCache 这些条目可以保留，但要更清楚地区分“KV cache 基础设施”和“semantic cache 产品层”。

## Action

- 删掉无关条目
- 清理表达错误
- 强化分层边界
