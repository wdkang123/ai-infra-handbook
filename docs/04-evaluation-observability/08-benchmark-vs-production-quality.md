# Benchmark 与生产质量不是一回事

很多学习者第一次接触模型评测时，会自然产生一个简单判断：

> 榜单分数越高，线上效果越好。

这句话有时有用，但绝对不够稳。
benchmark 是重要起点，但生产质量是更复杂的系统问题。

如果把两者画等号，你可能会做出很危险的发布决策：换了一个排行榜更高的模型，结果真实用户体验变差、成本上升、延迟增加、格式更不稳定，甚至关键场景退化。

## Benchmark 更擅长回答什么

benchmark 更擅长回答：

> 在固定任务、固定数据、固定评测口径下，模型表现如何？

它的价值在于受控比较。

例如：

- 同一个数据集
- 同一个 prompt template
- 同一个 few-shot 设置
- 同一个 judge 或 metric
- 同一个采样参数
- 同一个 backend 条件

在这些条件尽量一致时，benchmark 可以帮助你判断模型能力的相对差异。

这非常有价值。
没有 benchmark，模型比较会更容易变成体感争论。

## 生产质量更擅长回答什么

生产质量回答的是：

> 在你的真实用户、真实输入、真实工作流、真实成本和真实延迟约束下，这个系统是否更好？

它不只关心模型能力，还关心系统表现。

生产质量通常包括：

- 真实任务成功率
- 输出格式稳定性
- 延迟和首 token 体验
- token 成本
- 失败率和超时率
- RAG 命中质量
- tool call 成功率
- 用户取消率
- 安全和合规边界
- 回归风险
- 可观测性和排障成本

所以生产质量不是一个分数，而是一组场景化判断。

## 两者为什么不能直接等价

Benchmark 和生产质量之间隔着很多系统因素。

| 因素 | Benchmark 里可能被控制 | 生产里会发生什么 |
| --- | --- | --- |
| Prompt | 固定模板 | prompt 会随产品迭代变化 |
| 输入分布 | 固定数据集 | 用户输入长短、噪声、语言和意图都变 |
| Context | 通常受控 | 历史消息、RAG 文档、工具结果会混入 |
| Latency | 可能不作为核心指标 | 用户强烈感知 TTFT 和 ITL |
| Cost | 可能只统计 token | 还要看预算、租户、峰值流量 |
| Failure | benchmark 多看正确率 | 生产还要看 429、502、timeout、fallback |
| Output format | 可能人工看 | 生产常需要机器解析，格式错就是失败 |
| Observability | 不一定要求 | 生产必须能排查和复盘 |

因此，一个模型 benchmark 强，不代表它在你的系统里一定强。

## 一个具体例子

假设模型 A 和模型 B 在公开 benchmark 上：

| 模型 | Benchmark accuracy |
| --- | --- |
| A | 82.0% |
| B | 84.5% |

看起来 B 更好。
但你的真实系统里可能出现：

| 维度 | A | B |
| --- | --- | --- |
| 平均 prompt token | 1800 | 2600 |
| 平均 completion token | 500 | 900 |
| TTFT | 1.2s | 3.8s |
| JSON 格式错误率 | 1% | 8% |
| 关键业务回归 | 无 | 有 |
| 成本 | 较低 | 较高 |

这时 B 是否更适合上线，就不是 benchmark accuracy 能单独决定的。

生产发布要看综合判断，而不是只看分数。

## Benchmark 仍然很重要

强调“benchmark 不等于生产质量”，不是说 benchmark 没用。

Benchmark 的价值包括：

- 提供稳定比较基线
- 帮你筛掉明显不合适的模型
- 帮你观察模型能力上限
- 帮你做回归测试起点
- 帮你和历史结果对齐

问题不在 benchmark，而在误用 benchmark。

正确姿势是：

```text
benchmark -> 本地 eval run -> compare -> 场景回归 -> observability -> release decision
```

而不是：

```text
leaderboard rank -> 直接上线
```

## Leaderboard 应该怎么读

Leaderboard 是展示层，不是真理层。

一个好的 leaderboard 应该能追溯：

- 分数来自哪个 run
- run 的 task 是什么
- backend 是什么
- few-shot 是多少
- sample count 是多少
- best 和 latest 是否一致
- result file 在哪里
- sample analysis 在哪里

当前仓库的 leaderboard 从 `run_history.jsonl` 和 run artifact 聚合，而不是手写分数。
这是为了让读者知道：榜单上的数字必须能回到证据。

## 生产判断需要哪些额外证据

当你从 benchmark 走向生产判断时，建议补齐这些证据：

| 证据 | 用来回答 |
| --- | --- |
| eval run bundle | 这次评测怎么跑出来的 |
| comparison report | candidate 相比 baseline 是否真的更好 |
| sample analysis | 错误集中在哪些样本 |
| token usage | 成本是否明显变化 |
| gateway events | 是否发生 fallback、cache、route 问题 |
| serving metrics | 请求量、失败率、token counters 是否异常 |
| latency metrics | TTFT、ITL、总耗时是否可接受 |
| release recommendation | 是否 approve、review 或 block |

这些证据合起来，才接近生产发布判断。

## 一个模型发布判断流程

可以按这个顺序：

1. 先看公开 benchmark 或历史 benchmark，筛选候选。
2. 用当前系统的 eval-module 跑本地 run。
3. 保存 run bundle，检查 sample summary 和 sample analysis。
4. 用 compare 对比 baseline 和 candidate。
5. 看 release recommendation 和 reasons。
6. 用 gateway 入口做最小真实路径测试。
7. 看 token usage、metrics、events 和 latency。
8. 如果涉及微调，追溯 dataset、run、checkpoint、export lineage。
9. 通过后再进入 canary 或小流量验证。
10. 上线后继续看 production feedback 和 regression。

这个流程比“分高就上”慢一点，但更稳。

## 当前仓库怎么表达

相关文件：

```text
projects/eval-module/src/eval_module/main.py
projects/eval-module/src/eval_module/results/result_store.py
projects/ai-gateway/src/ai_gateway/server.py
projects/inference-service/src/inference_service/server.py
```

Eval 模块表达：

- run
- compare
- leaderboard
- list-runs
- list-comparisons
- run bundle
- comparison bundle
- release recommendation

Gateway / inference 表达：

- platform entrypoint
- model routing
- fallback/cache
- request id
- events
- metrics
- token usage

这些模块合在一起，是为了让你把“模型分数”接到“系统质量”。

## 与微调的关系

微调后尤其不能只看训练 loss 或单个 benchmark。

你还需要问：

- 训练数据和 baseline 是否可追溯？
- adapter 是否能追溯到 checkpoint？
- export 是否保留 manifest？
- eval 是否覆盖关键场景？
- candidate 是否在 compare 中通过？
- 是否有基础能力退化？
- 成本和延迟是否变化？

这就是为什么 [Finetune 到 Eval 的资产链路案例](/11-case-studies/03-finetune-to-eval-asset-lineage) 很重要。
微调产物必须进入评测和发布判断，不应该孤立看。

## 常见误区

### “排行榜第一就应该上线”

风险很大。
排行榜只能说明某个口径下表现好，不代表你的真实系统更好。

### “Benchmark 没用，真实业务才重要”

也不对。
benchmark 是稳定比较起点，能避免完全靠主观体感。

### “生产反馈好，就不用 benchmark”

不稳。
没有 benchmark 和回归集，你可能看不到隐藏退化。

### “只要 accuracy 涨了就发布”

不够。
还要看成本、延迟、格式、失败率、关键场景和 release recommendation。

### “Eval 和 observability 是两套无关系统”

不是。
eval 负责受控比较，observability 负责真实运行解释，两者要一起支撑发布判断。

## 学完应该能回答

读完这一页后，你应该能回答：

1. benchmark 更适合回答什么，生产质量更适合回答什么？
2. 为什么 leaderboard 不能替代 run artifact 和 sample analysis？
3. 为什么模型 accuracy 上升仍然可能不适合上线？
4. 发布判断除了分数，还应该看哪些系统证据？
5. 当前仓库如何把 eval、gateway、inference 和 finetune 证据接起来？

## 继续阅读

- [Benchmark、Leaderboard 与 Observability](/04-evaluation-observability/02-benchmark-leaderboard-observability)
- [Run、Compare、History](/04-evaluation-observability/01-run-compare-history)
- [从 Run 到发布判断](/04-evaluation-observability/07-from-run-to-release-decision)
- [Eval 退化阻断案例](/11-case-studies/05-eval-regression-release-gate)
