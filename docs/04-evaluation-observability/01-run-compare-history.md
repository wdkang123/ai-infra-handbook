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

## 一个没有证据链的失败例子

很多团队第一次做 eval 时，会留下类似这样的结论：

```text
新模型比旧模型好 3 个点，可以上线。
```

一周后线上反馈变差，大家回头追问：

- 当时测的是哪个数据集？
- prompt 有没有改？
- few-shot 数量一样吗？
- 错误样本集中在哪类问题？
- 新模型是否只是某些简单样本涨分？
- 有没有看长尾样本和格式稳定性？
- 当时的原始输出还在吗？

如果这些证据不存在，评测就变成一次性截图。
分数看起来像事实，实际无法复盘。

run、compare、history 的价值，就是把“我测过”升级成“我能解释这次测量”。

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

## Sample Analysis 应该看什么

样本级分析不只是把失败样本列出来。
更有用的是把失败变成可行动分类。

例如可以按这些维度读 sample outputs：

| 维度 | 你要问的问题 |
| --- | --- |
| 任务类型 | 哪类样本退化最明显 |
| 输出格式 | 是否出现 JSON 破格式、字段缺失、啰嗦 |
| 事实性 | 是否新增幻觉或遗漏关键事实 |
| 指令遵循 | 是否忽略 system prompt 或格式要求 |
| 安全边界 | 是否出现不该回答或拒答不稳 |
| 成本/长度 | 是否靠更长回答换来小幅涨分 |
| judge reason | 评分理由是否一致、是否有噪声 |

一个模型如果总分提高，但关键任务失败更多，未必值得发布。
一个模型如果 accuracy 变化不大，但格式稳定性明显提升，也可能值得进入下一轮灰度。

这就是为什么 sample analysis 是发布判断的一部分，而不是报告里的附录。

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

## Compare 报告应该像一条 PR 评论

一个好的 compare report 不只是给机器读，也应该能直接放进 PR 或 release discussion。

它应该让维护者快速知道：

```text
这次比较：
- baseline 是谁
- candidate 是谁
- 测的是哪个 task
- 条件是否一致
- 核心指标涨跌多少
- 关键样本有没有退化
- 推荐 approve / review / block
- 为什么
- 下一步要补什么证据
```

如果报告只能看到一堆 JSON 字段，读者会回到“看分数猜结论”。
如果报告能写清推荐理由，eval 才真正进入工程协作。

在公开学习项目里，这一点尤其重要。
别人读你的仓库，不只是想知道分数，还想学会你如何把分数变成判断。

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

## 什么时候应该阻断发布

阻断发布不一定要求总分大幅下降。
下面这些情况即使平均分没变，也应该进入 review 或 block：

| 情况 | 为什么危险 |
| --- | --- |
| 比较条件变化 | 无法确认提升来自模型还是测试条件 |
| 关键样本退化 | 业务核心路径比总分更重要 |
| 输出格式破坏 | 下游解析可能失败 |
| 回答长度暴涨 | 成本和延迟可能不可接受 |
| judge reason 显示新风险 | 分数未必捕捉全部质量问题 |
| 样本数太少 | 结论稳定性不足 |
| baseline 证据缺失 | 无法做可信比较 |

这张表可以帮助读者理解：eval gate 不是“卡流程”，而是在保护发布质量。

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

## 如何把一次评测写成公开复盘

如果你要把评测结果放到 GitHub 或博客里，可以用这个结构：

```text
评测目标：
baseline：
candidate：
数据集 / task：
运行条件：
核心指标：
样本级发现：
我排除的误判：
发布建议：
还缺的证据：
相关文件：
```

这个结构比“模型 B 比模型 A 好”更有学习价值。
它能让读者看到：AI Infra 里的质量判断是怎样从证据一步步形成的。

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
