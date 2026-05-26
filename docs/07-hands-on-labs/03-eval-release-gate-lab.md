# Eval 发布门禁 Lab

## 学习目标

这个 lab 训练你把一次评测结果变成一个可复盘的发布判断。

完成后你应该能说清楚：

- run 和 compare 为什么是两类不同对象
- 为什么一次评测不该只留下一个分数
- `min_delta` 如何避免噪声误判
- `release_recommendation` 为什么只是门禁建议，不是自动发布
- `sample_outputs.json`、`sample_summary.json` 和 `sample_analysis.json` 分别适合回答什么问题
- leaderboard 为什么应该从 run history 生成
- leaderboard 为什么需要保留 best/latest result file
- 为什么不同 task 不能直接比较
- history 为什么比单次截图更有价值

## 前置知识

建议先读：

- [Run、Compare、History](/04-evaluation-observability/01-run-compare-history)
- [从 Run 到发布决策](/04-evaluation-observability/07-from-run-to-release-decision)
- [Benchmark 与生产质量不是一回事](/04-evaluation-observability/08-benchmark-vs-production-quality)
- [eval-module 项目页](/06-projects/03-eval-module)

## 代码入口

重点看这些文件：

- `projects/eval-module/src/eval_module/main.py`
- `projects/eval-module/src/eval_module/runners/lm_eval_runner.py`
- `projects/eval-module/src/eval_module/results/result_store.py`
- `projects/eval-module/tests/test_runner.py`

## Lab 记录表

跑之前先准备一张记录表。
这会让你在 compare 和 leaderboard 阶段更容易解释结果，而不是只复制最终分数。

| 项目 | baseline | candidate | 说明 |
| --- | --- | --- | --- |
| task |  |  | 例如 `mmlu` |
| model |  |  | 模型名或本地别名 |
| backend url |  |  | mock/local/upstream 都要写清 |
| few-shot / 参数 |  |  | 参数不同不能直接比较 |
| result file |  |  | `results/*.json` |
| sample summary |  |  | 通过数、失败数、平均分 |
| run manifest |  |  | 记录执行环境和输入 |
| 备注 |  |  | 记录异常、重跑或人工观察 |

发布门禁的关键不是“有一个分数”，而是分数背后的条件可追踪。

## 操作步骤

### 1. 跑 baseline

```bash
cd /path/to/ai-infra/projects/eval-module
PYTHONPATH=src ../../.venv/bin/python -m eval_module.main run \
  --task mmlu \
  --model Qwen/Qwen2.5-0.5B-Instruct \
  --backend-url http://localhost:8000/v1 \
  --output ./results/lab_baseline.json
```

观察：

- `results/lab_baseline.json`
- `results/lab_baseline/summary.md`
- `results/lab_baseline/sample_outputs.json`
- `results/lab_baseline/sample_summary.json`
- `results/lab_baseline/sample_analysis.json`
- `results/lab_baseline/run_manifest.json`
- `results/run_history.jsonl`

### 2. 跑 candidate

当前 runner 是学习型 mock，因此你可以先用同一个模型模拟 candidate：

```bash
PYTHONPATH=src ../../.venv/bin/python -m eval_module.main run \
  --task mmlu \
  --model Qwen/Qwen2.5-0.5B-Instruct \
  --backend-url http://localhost:8000/v1 \
  --output ./results/lab_candidate.json
```

### 3. 做 compare

```bash
PYTHONPATH=src ../../.venv/bin/python -m eval_module.main compare \
  --baseline ./results/lab_baseline.json \
  --candidate ./results/lab_candidate.json \
  --min-delta 0.01 \
  --output ./results/lab_compare.json
```

观察：

- `results/lab_compare.json`
- `results/lab_compare.md`
- `results/lab_compare/comparison_manifest.json`
- `results/comparison_history.jsonl`

重点看 `summary.release_recommendation` 和 `summary.release_reasons`。  
它们会把结果分成 `approve / review / block`，并说明为什么不能只看 delta。

三种分支可以这样处理：

| recommendation | 含义 | 下一步 |
| --- | --- | --- |
| `approve` | candidate 在当前条件下超过门槛 | 仍要抽查 sample、确认配置一致，再进入发布讨论 |
| `review` | 变化不够显著或存在需要人工判断的因素 | 看 `release_reasons`、sample analysis、run manifest，必要时重跑或补任务 |
| `block` | candidate 明显退化或比较条件不可信 | 不进入发布，先定位退化样本或配置问题 |

把这一步写下来很重要。
真实团队里，门禁系统很少直接“替你发布”，它更多是把风险显性化，让人做可复盘决策。

### 4. 生成 run index

```bash
PYTHONPATH=src ../../.venv/bin/python -m eval_module.main list-runs \
  --results-dir ./results \
  --output ./results/lab_run_index.json
```

观察：

- `results/lab_run_index.json`
- `results/lab_run_index.md`

重点看每次 run 的 `timestamp`、`accuracy`、`result_file` 和 `sample_summary`。run index 不做排名，只帮你把历史事实列出来。

### 5. 生成 comparison index

```bash
PYTHONPATH=src ../../.venv/bin/python -m eval_module.main list-comparisons \
  --results-dir ./results \
  --output ./results/lab_comparison_index.json
```

观察：

- `results/lab_comparison_index.json`
- `results/lab_comparison_index.md`

重点看 `baseline_model`、`candidate_model`、`delta`、`verdict`、`release_recommendation` 和 `comparison_file`。comparison index 是发布判断历史，不是新的评测执行。

### 6. 生成最小 leaderboard

```bash
PYTHONPATH=src ../../.venv/bin/python -m eval_module.main leaderboard \
  --results-dir ./results \
  --output ./results/lab_leaderboard.json
```

观察：

- `results/lab_leaderboard.json`
- `results/lab_leaderboard.md`

重点看每个 task/model 的 `best_accuracy`、`latest_accuracy`、`run_count`、`sample_summary`、`best_result_file` 和 `latest_result_file`。它们说明 leaderboard 是由历史 run 聚合出来的展示对象，而不是新的评测执行。

## 关键观察点

### 观察点 1：run 是事实，compare 是判断

一次 run 只回答：

这个模型在这个 task 上跑出了什么结果。

一次 compare 回答：

candidate 相比 baseline 是否值得被认为更好、更差，还是没有显著变化。

这两个对象不应该混在一起。

### 观察点 2：`min_delta` 是发布判断的一部分

如果 `delta = 0.002`，你不能自动说 candidate 变好了。  
这可能只是 benchmark 噪声。

`min_delta` 的意义是让判断更克制：

- `delta > min_delta` 才是 improved
- `delta < -min_delta` 才是 regressed
- 中间区域是 unchanged

### 观察点 3：不同 task 不应直接比较

`mmlu` 的 accuracy 和 `gsm8k` 的 accuracy 不是同一个问题。  
它们可以放在 dashboard 里并列展示，但不应该直接做一个简单 delta。

当前 `ResultStore` 已经会拒绝这种比较。

### 观察点 4：release recommendation 是可复盘建议

`approve` 不表示系统会自动发布，只表示当前 compare 结果支持发布。  
`review` 表示需要人工复查，例如结果变化太小、few-shot 或样本数改变。  
`block` 表示 candidate 明显退化，不适合继续发布。

### 观察点 5：sample summary 是样本级复盘入口

`sample_outputs.json` 适合逐条看 prompt、prediction、score 和 `judge_reason`。  
`sample_summary.json` 适合快速看样本数量、通过数量、失败数量、平均分和 token 汇总。`sample_analysis.json` 则更像样本级问题清单，会保留 pass rate、score buckets、failed sample ids 和 judge reason counts，方便你先定位“是不是少数样本拖垮结果”。

这两类文件的组合，能避免评测只剩一个总分：你可以先用 summary 判断是否值得追，再进 sample outputs 看具体原因。

### 观察点 6：leaderboard 是展示层，不是执行层

`leaderboard.json` 读取的是 `run_history.jsonl` 指向的 run bundle。  
它不会重新跑 benchmark，也不会替代 compare，只是把历史结果按 task/model/backend/few-shot 摆成更容易横向观察的形态。

run index 更接近“历史清单”，leaderboard 更接近“排行视图”。两者都来自 history，但回答的问题不同：前者问“跑过什么”，后者问“当前哪个最好”。

comparison index 则回答第三个问题：“我们过去做过哪些发布判断”。它从 `comparison_history.jsonl` 生成，比单独翻多个 compare 文件更适合复盘。`verdict_counts` 和 `recommendation_counts` 能让你一眼看到最近判断里 approve/review/block 的分布，`task_summaries` 则能把这个分布收敛到每个 task。

当你切换 backend 或 few-shot 时，leaderboard 的 `backend_groups` 和 `fewshot_groups` 能提醒你：不同评测设置下的结果应该并列观察，而不是被混成同一个“模型分数”。

`best_result_file` 和 `latest_result_file` 很关键：best 告诉你当前排行榜分数来自哪次 run，latest 告诉你最近一次结果在哪里。没有这两个指针，排行榜很容易只剩展示数字，失去回到证据文件的能力。

这正好对应真实评测平台里的分层：run 负责产生事实，compare 负责做两两判断，leaderboard 负责展示多个结果。

## 常见卡点

| 现象 | 可能原因 | 先检查 |
| --- | --- | --- |
| compare 报 task 不一致 | baseline 和 candidate 不是同一任务 | 两个 result JSON 的 task 字段 |
| delta 很小但想直接发布 | 忽略了 `min_delta` | `summary.verdict` 和 `release_reasons` |
| leaderboard 数字看起来奇怪 | 混入了不同 backend 或 few-shot | `backend_groups`、`fewshot_groups` |
| sample summary 看不出原因 | 只看了汇总，没有看逐样本输出 | `sample_outputs.json` 和 `sample_analysis.json` |
| history 缺记录 | 输出目录或 history 文件不一致 | `results/run_history.jsonl`、`comparison_history.jsonl` |

遇到这些问题时，不要先改代码。
先确认比较对象、评测参数和结果文件是否一致。

## 可贴进 PR 的证据块

完成 lab 或修改 eval 逻辑后，可以在 PR 里贴这样的摘要：

```text
Eval evidence:
- baseline: results/lab_baseline.json
- candidate: results/lab_candidate.json
- compare: results/lab_compare.json
- recommendation: review
- reason: delta did not exceed min_delta; sample analysis requires manual review
- checked artifacts: sample_outputs.json, sample_summary.json, sample_analysis.json, comparison_manifest.json
```

这比只写“eval passed”更有价值，因为维护者可以回到具体文件复核。

## 扩展任务

任选一个完成：

1. 给 `sample_outputs.json` 增加一个更接近真实评测的字段，比如 reference answer。
2. 给 leaderboard markdown 增加按任务族或模型家族分组的视图。
3. 给 comparison index 增加按 baseline/candidate model family 的小计。

## 验收标准

完成这个 lab 后，至少要能通过：

```bash
PYTHON=.venv/bin/python make infra-check
```

你还应该能回答：

- 为什么 result JSON 不够，还需要 bundle
- 为什么 compare 要落 Markdown
- 为什么 `release_recommendation` 还需要 `release_reasons`
- 为什么 `judge_reason` 比只有 score 更适合复盘
- 为什么 `sample_summary.json`、`sample_analysis.json` 和 `sample_outputs.json` 要分开
- 为什么 leaderboard 不应该绕过 run history
- 为什么 history 适合长期追踪
- 为什么发布判断不能只看单个 benchmark 分数
