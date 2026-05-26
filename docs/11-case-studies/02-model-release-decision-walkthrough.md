# 模型发布判断案例

这个案例模拟一次候选模型发布前的评审：

> 你有一个候选模型结果，它在某个 benchmark 上看起来还不错。你要判断它能不能进入下一步发布。

这里的重点不是“分数高就发布”，而是把评测结果变成有证据的工程判断。

这个案例可以当成一次发布评审演练。你不是在问“candidate 有没有赢”，而是在问“当前证据是否足够支持它进入下一阶段”。这两个问题很像，但工程含义不同。

发布判断通常要同时看三类证据：

- 指标证据：分数、delta、阈值、排行榜位置。
- 样本证据：失败样本、judge reason、低分集中度。
- 设置证据：task、backend、few-shot、prompt、模型或 checkpoint 来源。

缺少任何一类，结论都应该更谨慎。

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

## 先定义发布问题

在看分数之前，先写清楚你要发布的到底是什么。

```text
候选对象：
变化来源：
- 新模型
- 新 prompt
- 新 checkpoint
- 新 serving backend
- 新 gateway 路由

目标场景：
核心风险：
最低可接受标准：
必须阻断的条件：
```

如果你不先定义变化来源，很容易把所有结果都叫“模型变好了/变差了”。但真实项目里，分数变化可能来自 prompt、backend、采样参数、数据集版本、judge 设置或模型本身。

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

运行后先保存两个 result file 的路径。后面所有判断都应该能追溯到这两个文件，而不是只引用截图或口头分数。

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

建议用下面问题检查 run bundle：

```text
这个 run 的 task 是：
backend 是：
few-shot 是：
样本数是：
最低分样本是：
失败最多的 judge reason 是：
这次 run 是否能被别人复查：
```

这一步的目标是确认单个 run 自己是否可靠。一个不可复盘的 run，即使分数很高，也不适合进入发布判断。

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

如果 compare 报告提示设置变化，先不要急着解释好坏。应该先回答：这些变化是否会影响比较语义。比如 backend 变化可能影响 latency 和输出格式，few-shot 变化可能影响 accuracy，judge prompt 变化可能影响评分口径。

## 第 4 步：判断 recommendation 的语义

常见判断可以这样理解：

| 结果 | 说明 | 下一步 |
| --- | --- | --- |
| `approve` | candidate 达到阈值且没有明显设置冲突 | 可以进入更大样本或灰度 |
| `review` | 有变化但证据不够稳定 | 人工复盘样本和设置 |
| `block` | candidate 明显退化或设置不可比 | 不建议发布 |

即使结果是 `approve`，也要继续问：

- 样本量是否足够
- task 是否覆盖真实业务
- 生产流量分布是否类似
- 是否看过失败样本
- 是否需要人工 judge 或线上 shadow

### 推荐结论和人工判断的关系

`release_recommendation` 是一个结构化建议，帮助你把阈值、可比性和结果方向固定下来。但它不应该替代人工判断。

可以这样使用：

| recommendation | 人工还要看什么 |
| --- | --- |
| `approve` | 样本是否覆盖关键场景，是否需要灰度 |
| `review` | 哪些证据不足，补测是否能解除疑问 |
| `block` | 阻断原因是否清楚，是否需要回归集 |

如果 recommendation 和你的直觉冲突，不要直接覆盖它。先回到 evidence：是阈值不合理、样本不覆盖，还是你忽略了某个失败聚类。

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

leaderboard 最大的误用是把它当作发布结论。它能告诉你“历史上谁最好、最新是谁、按 backend/few-shot 怎么分组”，但不能告诉你 candidate 是否适合当前业务场景。

run index 的价值在于上下文：如果 candidate 是最新结果但不是 best result，你需要解释为什么仍然考虑发布；如果 candidate 是 best result，也要确认它不是因为设置改变而不可比。

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
candidate 当前可以进入 review，但不直接 approve。
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

## 常见错误判断

### 只看总体分数

总体分数会掩盖样本分布。尤其是学习型项目，某些样本可能代表核心教学目标。如果这些样本退化，即使平均分变化不大，也应该谨慎。

### 忽略设置变化

task、backend、few-shot、judge 设置不一致时，比较结果可能只是配置变化的结果，不是 candidate 真变好。

### 把 leaderboard 当 release gate

leaderboard 是展示和检索层，不是完整发布门禁。发布门禁还要看 sample analysis、风险、回滚和生产证据。

### 没有说明剩余风险

一个成熟的发布判断应该说明“当前证据支持什么”和“当前证据不能覆盖什么”。没有风险说明的 approve 很容易变成过度自信。

## 生产发布还需要补什么

当前案例只覆盖离线评测判断。真实发布还需要：

- 固定版本的评测集。
- 高风险样本和回归集。
- serving 版本、prompt 版本、checkpoint 版本绑定。
- latency、成本、错误率和用户体验指标。
- shadow/canary 流量。
- 回滚策略和 owner。

学习阶段先把离线证据链写清楚，后续才能自然接到生产发布流程。
