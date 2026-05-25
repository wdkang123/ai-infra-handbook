# 模型发布判断案例

这个案例模拟一次候选模型发布前的评审：

> 你有一个候选模型结果，它在某个 benchmark 上看起来还不错。你要判断它能不能进入下一步发布。

这里的重点不是“分数高就发布”，而是把评测结果变成有证据的工程判断。

## 场景设定

你已经有：

- baseline run
- candidate run
- comparison report
- leaderboard
- run index

你要回答：

- candidate 是否真的比 baseline 好
- 样本级别有没有异常
- task、backend、few-shot 设置是否一致
- release recommendation 是什么
- 这个 recommendation 有哪些不能覆盖的风险

## 第 1 步：生成 baseline 和 candidate run

在学习项目里可以先用同一个模型模拟 baseline 和 candidate：

```bash
cd /path/to/ai-infra/projects/eval-module

PYTHONPATH=src ../../.venv/bin/python -m eval_module.main run \
  --task mmlu \
  --model Qwen/Qwen2.5-0.5B-Instruct \
  --backend-url http://localhost:8000/v1 \
  --output ./results/baseline.json

PYTHONPATH=src ../../.venv/bin/python -m eval_module.main run \
  --task mmlu \
  --model Qwen/Qwen2.5-0.5B-Instruct \
  --backend-url http://localhost:8000/v1 \
  --output ./results/candidate.json
```

真实项目里 baseline 和 candidate 通常来自不同模型、不同 prompt、不同服务版本或不同 checkpoint。

## 第 2 步：先看 run bundle

每个 run 不只是一个分数。你应该看：

- `result.json`
- `result.md`
- `sample_outputs.json`
- `sample_summary.json`
- `sample_analysis.json`
- `run_manifest.json`

重点看 `sample_analysis.json`：

- `pass_rate`
- `min_score`
- `max_score`
- `score_buckets`
- `failed_sample_ids`
- `judge_reason_counts`

如果 overall score 看起来不错，但失败样本集中在某类问题上，就不能只看平均分。

## 第 3 步：生成 comparison report

```bash
PYTHONPATH=src ../../.venv/bin/python -m eval_module.main compare \
  --baseline ./results/baseline.json \
  --candidate ./results/candidate.json \
  --output ./results/compare.json \
  --min-delta 0.01
```

重点看：

- `metric_deltas`
- `release_recommendation`
- `settings_changed`
- `task`
- `baseline_result_file`
- `candidate_result_file`

`release_recommendation` 是门禁建议，不是最终发布命令。

## 第 4 步：判断 recommendation 的语义

常见判断可以这样理解：

| 结果 | 说明 | 下一步 |
| --- | --- | --- |
| `promote` | candidate 达到阈值且没有明显设置冲突 | 可以进入更大样本或灰度 |
| `review` | 有变化但证据不够稳定 | 人工复盘样本和设置 |
| `block` | candidate 明显退化或设置不可比 | 不建议发布 |

即使结果是 `promote`，也要继续问：

- 样本量是否足够
- task 是否覆盖真实业务
- 生产流量分布是否类似
- 是否看过失败样本
- 是否需要人工 judge 或线上 shadow

## 第 5 步：看 leaderboard 和 run index

生成 leaderboard：

```bash
PYTHONPATH=src ../../.venv/bin/python -m eval_module.main leaderboard \
  --history ./run_history.jsonl \
  --output ./results/leaderboard.json
```

生成 run index：

```bash
PYTHONPATH=src ../../.venv/bin/python -m eval_module.main list-runs \
  --history ./run_history.jsonl \
  --output ./results/run_index.json
```

重点看：

- `best_result_file`
- `latest_result_file`
- `backend_groups`
- `task_summaries`
- 每个 run 的 `sample_analysis`

leaderboard 适合展示和排序，run index 更适合复盘和定位。

## 第 6 步：写发布判断

可以用这个模板：

```text
候选对象：

baseline：

candidate：

task / backend / few-shot 是否一致：

核心指标变化：

sample analysis 观察：

release recommendation：

我的最终判断：

还需要补充的证据：
```

示例判断：

```text
candidate 当前可以进入 review，但不直接 promote。
原因是 comparison 没有显示明显退化，但样本量仍小，且 sample_analysis 需要人工查看低分样本。
下一步应该扩大 task 覆盖，并用相同 backend / few-shot 设置重跑。
```

## 这个案例应该带走什么

模型发布判断不是“分数高就上”，而是一个证据链：

1. run 是否可复盘
2. sample 是否可解释
3. compare 是否可比
4. recommendation 是否有阈值依据
5. leaderboard 是否只是展示层
6. 生产风险是否另有验证

如果你能把这条链讲清楚，就已经抓住 eval-module 在系统里的价值了。
