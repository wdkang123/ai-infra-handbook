# Run、Compare、History

评测系统最容易被做薄的一点，是只留下一个分数。

例如：

```text
accuracy = 0.72
```

这个数字有用，但远远不够。
真正的工程问题通常是：

- 这个分数是怎么跑出来的？
- 用了哪个模型、哪个 backend、多少 few-shot、多少样本？
- 原始输出在哪里？
- 哪些样本错了？
- 和上一次相比差在哪里？
- 这次结果能不能支持发布？
- 三周后还能不能复现和解释？

这就是为什么评测系统需要 run、compare、history 三层。

## 三层分别解决什么

| 层 | 解决的问题 | 典型产物 |
| --- | --- | --- |
| Run | 单次评测发生了什么 | result、raw output、sample outputs、summary、run manifest |
| Compare | 两次结果差在哪里 | comparison JSON/Markdown、delta、verdict、release recommendation |
| History | 多次评测如何追踪 | run_history、comparison_history、run index、leaderboard、comparison index |

如果只有 run，没有 compare，你只能看单次分数。
如果只有 compare，没有 history，你只能看一次性结论。
如果只有 history，没有 run artifact，历史会变成不可查证的流水账。

## Run：把一次评测变成证据对象

run 解决的是：

> 这一次评测到底留下什么证据？

一次好的 run 不应该只生成 `eval_result.json`。
它至少应该保留：

- task
- model
- backend
- num few-shot
- sample count
- metrics
- raw output
- sample outputs
- sample summary
- sample analysis
- run manifest
- markdown summary

这些内容共同回答“这次评测是否可解释”。

## 为什么 sample outputs 很重要

总分告诉你“整体表现”。
sample outputs 告诉你“具体错在哪里”。

比如两个模型 accuracy 都是 0.72，但错误样本完全不同：

- 模型 A 在数学题错得多
- 模型 B 在长文本理解错得多
- 模型 C 分数一样，但输出格式经常不稳定

如果只有总分，你无法做这种判断。
所以 run artifact 必须能回到样本级证据。

当前仓库里 run bundle 会保存：

```text
result.json
raw_output.json
sample_outputs.json
sample_summary.json
sample_analysis.json
run_manifest.json
summary.md
```

这不是为了“文件多”，而是为了让分数可以被解释。

## Compare：把变化变成判断

compare 解决的是：

> candidate 相比 baseline 到底能不能接受？

它不是简单算一个 delta。

一个有用的 compare 至少要回答：

- baseline 是什么？
- candidate 是什么？
- task 是否一致？
- accuracy delta 是多少？
- metric delta 是多少？
- 样本数是否变化？
- few-shot 是否变化？
- 是否达到 `min_delta`？
- verdict 是 pass、regression 还是 needs review？
- release recommendation 是什么？
- 推荐理由是什么？

这一步把“评测分数”推进成“发布判断”。

## 为什么 compare 必须检查条件变化

如果 baseline 和 candidate 的 task 不同，比较没有意义。
如果样本数变了，分数变化可能来自数据而不是模型。
如果 few-shot 变了，prompt 条件也变了。

所以 compare 不应该只是：

```text
candidate_accuracy - baseline_accuracy
```

它还要记录比较条件。
当前仓库里的 comparison summary 会保留：

- `fewshot_changed`
- `sample_count_changed`
- `min_delta`
- `verdict`
- `release_recommendation`
- `release_reasons`

这些字段提醒读者：发布判断不是只看一个 delta。

## History：让评测不再是一次性截图

history 解决的是：

> 多次 run 和 compare 如何形成可追踪序列？

没有 history，每次评测都是孤立文件。
你很难回答：

- 这个模型最近跑过几次？
- 哪次是最好的？
- 最新一次和最好一次是不是同一个？
- 哪个 backend 更稳定？
- 哪些 comparison 曾经阻断发布？
- 某个 task 的历史趋势是什么？

所以当前仓库会追加：

```text
results/run_history.jsonl
results/comparison_history.jsonl
```

JSONL 的好处是简单、追加友好、容易被后续工具读取。
它不华丽，但很适合学习阶段表达“历史要沉淀”。

## Run Index：先盘点历史

run index 解决的是：

> 历史里到底有哪些 run？

它读取 `run_history.jsonl`，把 run 变成一个可读目录。
当前实现支持按 task、model、backend、few-shot 和 limit 过滤，并生成 JSON/Markdown。

run index 适合回答：

- 最近跑了哪些模型？
- 某个 task 有多少次 run？
- latest accuracy 是多少？
- best accuracy 对应哪个 result file？
- sample summary 文件在哪里？
- backend 和 few-shot 覆盖是否一致？

所以合理顺序往往是：

1. 用 run index 盘点历史。
2. 用 leaderboard 看横向表现。
3. 用 compare 做发布判断。

## Leaderboard：展示层，不是真理层

leaderboard 解决的是：

> 多个模型/后端在同一任务下怎么横向看？

它很适合公开展示，但也最容易被误读。

一个 leaderboard 应该从 run history 和 run artifacts 聚合，而不是手写分数表。
否则它会失去可追溯性。

当前仓库的 leaderboard 会展示：

- task
- model
- backend
- few-shot
- best accuracy
- latest accuracy
- run count
- best result file
- latest result file

这能提醒读者：排行榜只是入口，真正证据还在 run artifact 里。

## Comparison Index：发布判断的历史

comparison index 解决的是：

> 过去做过哪些发布判断？

它读取 `comparison_history.jsonl`，聚合：

- baseline / candidate
- verdict counts
- recommendation counts
- task summaries
- average delta
- comparison file

这让 compare 不只是一次性报告，而是可以回看的发布判断历史。

如果某个模型连续几次 `release_recommendation=block`，你就应该回到具体 comparison bundle 看原因，而不是只看最新一条分数。

## 一个具体发布判断场景

假设你有：

- baseline：`model-a`，accuracy 0.7600
- candidate：`model-b`，accuracy 0.7650
- min_delta：0.0100

candidate 看起来涨了 0.0050。
但如果 min_delta 是 0.0100，它不一定能支持发布。

你还要看：

- 样本数是否一致
- few-shot 是否一致
- 失败样本是否集中在关键任务
- token 成本是否明显上升
- judge reason 是否出现新问题
- release recommendation 是否是 approve、review 还是 block

这就是 compare 的价值：它把“涨了一点”变成“是否足以发布”的判断。

## 当前仓库怎么表达

相关文件：

```text
projects/eval-module/src/eval_module/main.py
projects/eval-module/src/eval_module/results/result_store.py
projects/eval-module/src/eval_module/runners/lm_eval_runner.py
```

核心 CLI：

```text
run
compare
leaderboard
list-runs
list-comparisons
list-tasks
```

核心产物：

```text
results/run_history.jsonl
results/comparison_history.jsonl
results/run_index.json
results/leaderboard.json
results/comparison_index.json
```

这些能力共同表达一条主线：

```text
single run -> run bundle -> compare -> comparison bundle -> history -> index/leaderboard
```

## 如何阅读一次 eval 结果

学习时建议不要只看 accuracy，按这个顺序读：

1. 看 run summary：task、model、backend、few-shot、sample count。
2. 看 sample summary：通过数、失败数、平均分。
3. 看 sample analysis：失败样本、分数分桶、judge reason。
4. 看 raw output：确认 runner 返回了什么。
5. 看 run manifest：确认文件之间的关系。
6. 看 run history：确认这次 run 进入历史。
7. 看 compare report：确认是否支持发布。

这样读，评测结果才会从“一个分数”变成“一个可复盘证据包”。

## 常见误区

### “Accuracy 高就可以发布”

不一定。
还要看比较条件、样本数量、关键任务、失败类型、成本和发布风险。

### “Leaderboard 第一就是最好的模型”

不一定。
leaderboard 是展示层，不能替代样本级分析和发布判断。

### “只要保存最终 JSON 就够了”

不够。
没有 sample outputs、summary、analysis 和 manifest，后续很难解释结果。

### “History 只是日志”

不是。
history 是 run、compare、leaderboard 和 release decision 的连接层。

### “Compare 只需要算 delta”

不够。
compare 还要检查条件变化、生成 verdict、说明 release recommendation。

## 学完应该能回答

读完这一页后，你应该能回答：

1. run、compare、history 分别解决什么问题？
2. 为什么一次评测不应该只留下 accuracy？
3. leaderboard 为什么必须能追溯到 run history？
4. compare 为什么要记录 few-shot、样本数和 release recommendation？
5. 当前仓库里哪些文件和 CLI 表达了评测证据链？

## 继续阅读

- [Benchmark、Leaderboard 与 Observability](/04-evaluation-observability/02-benchmark-leaderboard-observability)
- [从 Run 到发布判断](/04-evaluation-observability/07-from-run-to-release-decision)
- [模型发布判断案例](/11-case-studies/02-model-release-decision-walkthrough)
- [Eval 退化阻断案例](/11-case-studies/05-eval-regression-release-gate)
