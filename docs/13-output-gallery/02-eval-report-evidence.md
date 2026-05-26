# Eval 报告证据

## 这一页看什么

Eval 输出最容易被误读成“一个分数”。

但当前 `eval-module` 的价值不只在分数，而在它把评测证据拆成了几层：

| 证据 | 回答的问题 |
| --- | --- |
| `result.json` | 这次 run 的总体结果是什么 |
| `sample_outputs.json` | 每个样本具体发生了什么 |
| `sample_summary.json` | 样本级结果如何聚合 |
| `sample_analysis.json` | 失败样本、分数桶、judge reason 如何分布 |
| `run_index.json` | 多个 run 如何索引和过滤 |
| `compare.json` | baseline 和 candidate 的差异是什么 |
| `comparison_index.json` | 多次 comparison 的 verdict/recommendation 分布是什么 |
| `leaderboard.json` | 多个 run 的排名和分组是什么 |

## 先用三步读报告

第一次看 eval 产物时，不要从最大 JSON 文件开始。

推荐顺序：

1. 先看 `sample_summary.json`，确认整体通过率和样本数量。
2. 再看 `sample_analysis.json`，找失败样本和 judge reason 模式。
3. 最后看 `compare.json`，判断 candidate 相比 baseline 是否值得继续。

这样能避免被 `result.json` 里的总体分数带偏。

一个好习惯是：每看到一个分数，都追问“哪些样本支撑了它”。

## Run 总体结果

一次 run 通常从命令开始：

```bash
PYTHONPATH=src ../../.venv/bin/python -m eval_module.main run \
  --model vllm-local \
  --backend mock \
  --output-dir /tmp/eval-demo
```

`result.json` 适合先看：

```json
{
  "model": "vllm-local",
  "backend": "mock",
  "metrics": {
    "accuracy": 0.8
  },
  "task_summaries": [
    {
      "task": "toy_qa",
      "sample_count": 5
    }
  ]
}
```

重点不是背字段，而是看它是否能回答：

- 评测的是哪个模型
- 用的是哪个 backend
- 任务是什么
- 主要 metric 是什么
- 样本数量够不够支撑判断

## Sample outputs

`sample_outputs.json` 适合逐条看样本。

你应该关注：

| 字段 | 含义 |
| --- | --- |
| `sample_id` | 样本标识 |
| `prompt` | 输入 |
| `prediction` | 模型输出 |
| `score` | 样本分数 |
| `passed` | 是否通过 |
| `judge_reason` | 为什么这样判 |
| `prompt_tokens` | 输入 token |
| `completion_tokens` | 输出 token |

它回答的是：

> 分数背后，具体样本长什么样？

如果 `accuracy` 下降，不要先猜模型坏了，先打开 `sample_outputs.json` 看失败样本。

### 失败样本怎么读

读失败样本时，建议记录：

```text
sample id：
prompt：
prediction：
expected / rubric：
score：
judge reason：
可能原因：
下一步动作：
```

下一步动作可能是：

- 修改 prompt
- 修改 judge rubric
- 补训练数据
- 修输出格式约束
- 标记为人工复核
- 从发布候选里排除

评测的价值不只是给分，而是把失败样本变成下一轮改进材料。

## Sample summary

`sample_summary.json` 更适合快速扫：

```json
{
  "sample_count": 5,
  "passed_count": 4,
  "failed_count": 1,
  "average_score": 0.8,
  "total_prompt_tokens": 120,
  "total_completion_tokens": 30
}
```

它回答的是：

> 这次 run 的样本级结果整体如何？

如果你只想快速判断“这次有没有明显失败”，先看 summary。

## Sample analysis

`sample_analysis.json` 更像问题清单：

```json
{
  "pass_rate": 0.8,
  "score_buckets": {
    "0.0-0.5": 1,
    "0.5-1.0": 4
  },
  "failed_sample_ids": ["sample-3"],
  "judge_reason_counts": {
    "mock score below threshold": 1
  }
}
```

它回答的是：

> 失败集中在哪里？judge reason 有没有模式？

这比只看 average score 更适合复盘。

## Compare 报告

`compare.json` 不只是两个分数相减。

它还会把判断拆成：

| 字段 | 含义 |
| --- | --- |
| `metric_deltas` | 指标变化 |
| `verdict` | improve / regress / neutral |
| `release_recommendation` | 是否建议通过 |
| `task_summaries` | 任务级聚合 |
| `changed_eval_settings` | 评测设置是否变化 |

你要特别关注：

1. baseline 和 candidate 是否同 task
2. backend 和 few-shot 设置是否一致
3. delta 是否超过阈值
4. recommendation 是基于哪些证据得出的

如果 task 不一致，当前工具会拒绝比较。这是好事：错误比较比没有比较更危险。

## Compare 里的 review 不等于失败

`release_recommendation` 是 `review` 时，不要直接理解成模型失败。

它通常表示：

- delta 没有超过门槛
- 评测设置变化了
- 样本数或 task 上下文需要人工判断
- candidate 没有明显赢过 baseline

这时更好的动作是打开 `release_reasons` 和 sample-level evidence，而不是调低 `min_delta` 让结果好看。

## Leaderboard

`leaderboard.json` 适合看多次 run：

| 字段 | 含义 |
| --- | --- |
| `entries` | run 排名 |
| `best_result_file` | 当前 best 指向哪个 result |
| `latest_result_file` | 最新 result |
| `backend_groups` | 按 backend 分组 |
| `fewshot_groups` | 按 few-shot 分组 |

不要把不同 backend、不同 few-shot 的结果直接混成一个结论。

如果 leaderboard 里分组很多，优先按同组比较。

## Run index 和 comparison index

`run_index.json` 适合回答：

- 有多少次 run
- 最近一次 run 是什么
- 每个 task 的结果概况是什么
- backend / few-shot 过滤后还剩哪些结果

`comparison_index.json` 适合回答：

- 有多少次 comparison
- verdict 分布是什么
- recommendation 分布是什么
- 哪些 task 经常被比较

这两个文件很适合给 dashboard 做后端数据源，也适合公开分享时做证据索引。

## PR 或发布里怎么引用

如果某个 PR 改了 prompt、模型路由、eval runner、训练 export 或发布判断，建议在 PR 描述里贴简版证据：

```text
Eval evidence:
- baseline:
- candidate:
- task:
- metric delta:
- release recommendation:
- failed sample ids:
- report files:
```

不要只贴“accuracy 从 0.80 到 0.84”。没有 task、样本和 compare context，这个数字很难被 review。

## 如何避免误读

| 误读 | 更稳的解释 |
| --- | --- |
| 分数高就可以发布 | 分数只是门禁输入，还要看样本、风险和业务场景 |
| 一次 compare 就代表模型更好 | 需要看 task、backend、样本和阈值 |
| sample_outputs 太细，不重要 | 它是解释分数变化的关键证据 |
| leaderboard 第一就是生产最佳 | leaderboard 只说明当前评测集合里的排名 |

## 复盘模板

```text
run id：
model/backend/task：
核心 metric：
sample_count：
失败样本：
judge reason 分布：
compare verdict：
release recommendation：
我会继续看：
我不会据此断言：
```

## 关联阅读

- [eval-module](/06-projects/03-eval-module)
- [Eval 发布门禁 Lab](/07-hands-on-labs/03-eval-release-gate-lab)
- [模型发布判断案例](/11-case-studies/02-model-release-decision-walkthrough)
- [CLI Surface 速查](/09-reference/06-cli-surface)
