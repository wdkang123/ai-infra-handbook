# Eval 退化与发布阻断案例

这个案例模拟一次发布前评审：

> Candidate 的总体分数只下降了一点，但低分样本集中在关键能力上。你要判断是继续 review、直接 block，还是补测后再决定。

它补充 [模型发布判断案例](/11-case-studies/02-model-release-decision-walkthrough) 的一个更具体场景：平均分没有明显崩，但样本级证据已经在提醒你不要贸然发布。

这个案例训练的是“阻断发布”的判断力。很多时候团队不缺少 approve 的理由，缺少的是在证据不足或风险集中时说“不”的能力。一个好的 release gate 不应该只奖励分数提升，也应该保护核心场景不被平均分掩盖。

## 场景设定

你已经有：

- baseline result
- candidate result
- comparison report
- sample outputs
- sample analysis
- leaderboard
- run index

现在你看到：

- overall score 只下降了一点
- `release_recommendation` 是 `review` 或 `block`
- failed samples 集中在同一类问题
- candidate 可能来自新 prompt、新 checkpoint 或新 serving backend

你的目标不是为模型辩护，而是回答：

- 退化是否真实
- 是否可比
- 退化集中在哪里
- 能不能通过补测解除风险
- 是否应该阻断 release

## 先定义什么叫退化

退化不一定等于总体分数大幅下降。下面几类都可能是退化：

| 退化类型 | 表现 |
| --- | --- |
| 指标退化 | accuracy、pass rate 或其他核心指标下降 |
| 样本退化 | 关键样本失败或低分集中 |
| 行为退化 | 格式、拒答、解释质量、工具调用方式变差 |
| 设置退化 | candidate 使用了不可比设置却被当作提升 |
| 运营退化 | 延迟、成本、错误率变差 |

本案例重点看样本退化和发布门禁。

## 第 1 步：确认比较是否可比

先看 comparison report：

```bash
cat ./results/compare.json
```

重点看：

- `task`
- `metric_deltas`
- `settings_changed`
- `release_recommendation`
- `baseline_result_file`
- `candidate_result_file`

如果 `settings_changed` 显示 task、backend、few-shot、judge 设置不一致，先不要急着下结论。
不可比的结果最多说明“需要重跑”，不能直接说明 candidate 更好或更差。

如果设置不可比，建议直接把结论写成：

```text
当前不判断 candidate 好坏。
原因：comparison settings changed。
动作：用相同 task/backend/few-shot/judge 设置重跑。
```

这不是保守，而是防止错误比较进入发布流程。

## 第 2 步：看样本级输出

```bash
cat ./results/candidate.sample_outputs.json
```

重点看：

- `sample_id`
- `score`
- `passed`
- `judge_reason`
- `prompt_tokens`
- `prediction_tokens`

如果低分样本的 `judge_reason` 重复出现同一类原因，说明退化可能不是随机波动。
比如多次出现“没有遵循格式”“拒答不合理”“事实遗漏”“推理步骤缺失”，就应该进入人工复盘。

样本级输出要看两个方向：

- 失败样本本身是否重要。
- 失败原因是否集中。

如果失败样本都是低风险边缘场景，处理方式可能是 review；如果失败样本属于项目核心能力，即使数量不多，也可能需要 block。

## 第 3 步：看 sample analysis

```bash
cat ./results/candidate.sample_analysis.json
```

重点看：

- `pass_rate`
- `score_buckets`
- `failed_sample_ids`
- `judge_reason_counts`
- `min_score`

一种常见危险信号是：

```text
overall score 变化不大，但 failed_sample_ids 集中在同一类业务关键样本。
```

这意味着平均分稀释了风险。
发布门禁不能只看总分，还要看失败样本是否落在高风险区域。

建议把失败样本按风险分组：

```text
高风险失败：
- 影响核心能力：
- 影响安全边界：
- 影响公开教学目标：

中风险失败：
- 影响局部体验：
- 可以通过文档或 prompt 修正：

低风险失败：
- 边缘样本：
- 不影响当前发布目标：
```

这种分组比只列 failed sample ids 更能支持发布判断。

## 第 4 步：结合 leaderboard 和 run index

```bash
PYTHONPATH=src ../../.venv/bin/python -m eval_module.main leaderboard \
  --history ./run_history.jsonl \
  --output ./results/leaderboard.json

PYTHONPATH=src ../../.venv/bin/python -m eval_module.main list-runs \
  --history ./run_history.jsonl \
  --output ./results/run_index.json
```

重点判断：

- candidate 是否只是最新，但不是最好
- 同一 backend 下 candidate 是否退化
- few-shot 或 task 分组是否改变
- run history 是否能追溯到 result file

leaderboard 适合看排序，run index 适合查上下文。
不要只因为 candidate 出现在最新位置，就默认它应该进入发布。

还要看 candidate 是否打破历史趋势。如果过去多次 run 都稳定，只有这次 candidate 在关键样本退化，应该把它当成强信号；如果历史本来波动很大，可能需要扩大样本或重跑确认。

## 第 5 步：做 release gate 判断

可以用这张表：

| 证据 | 判断 | 推荐动作 |
| --- | --- | --- |
| 设置不可比 | 不能判断好坏 | 重跑相同设置 |
| 总体略降，失败样本随机 | 可能是噪声 | 扩大样本或继续 review |
| 总体略降，失败集中在关键能力 | 有发布风险 | block 或补专门回归集 |
| 总体上升，但高风险样本失败 | 不应直接 approve | 人工复盘并补 guardrail |
| recommendation 为 block | 自动门禁不通过 | 不发布，先修原因 |

如果你无法解释失败样本，就不要发布。
不解释失败样本的发布，本质上是在把风险交给线上用户发现。

### block、review、补测怎么选

| 选择 | 适合情况 |
| --- | --- |
| block | 已确认核心能力退化，或 recommendation 明确阻断 |
| review | 证据有风险但还不足以确认退化 |
| 补测 | 设置不可比、样本量不足或失败聚类需要验证 |
| approve | 指标、样本、设置和风险说明都支持进入下一步 |

`review` 不是拖延，它应该有明确下一步：看哪些样本、补哪个 task、重跑哪种设置、谁来判断。

## 第 6 步：写阻断说明

可以用这个模板：

```text
候选对象：

比较设置是否一致：

总体指标：

退化样本：

judge reason 聚类：

release recommendation：

我的结论：

需要补充的评测：
```

示例：

```text
本次 candidate 不建议发布。
虽然总体分数只下降 0.8%，但 failed_sample_ids 集中在 gateway error explanation 相关样本。
judge_reason_counts 显示多次出现“没有解释 request id 与 upstream error 的关系”。
这说明 candidate 可能损害本项目最核心的学习目标。
下一步应该补一个 gateway incident 回归集，并用相同 backend/few-shot 设置重跑。
```

一份好的阻断说明不需要情绪化，也不需要“证明 candidate 很差”。它只需要说明：当前证据不足以支持发布，或者证据已经显示关键风险。

## 第 7 步：把退化样本转成回归资产

阻断之后，不要让样本只停留在报告里。应该把高风险失败整理成后续回归资产。

可以记录：

```text
sample id：
失败原因：
为什么重要：
期望行为：
当前 candidate 行为：
baseline 行为：
应该加入哪个回归集：
下次发布前如何验证：
```

这样 release gate 就不只是挡一次发布，而是在积累项目的质量记忆。

## 生产系统还需要什么

当前 eval-module 是学习型最小实现。真实发布门禁还需要：

- 固定版本的 eval dataset
- 任务分层和高风险样本集
- judge prompt 版本管理
- 人工 review 抽样
- 线上 shadow 或 canary 反馈
- 评测结果与 serving 版本、prompt 版本、checkpoint 版本绑定
- 回归样本的长期追踪

## 这个案例应该带走什么

发布阻断不是保守，而是工程系统保护学习目标或业务目标的方式。
一次好的 eval 复盘应该能回答：

1. 结果是否可比
2. 总体指标是否足够
3. 样本级失败是否集中
4. 失败是否影响核心场景
5. recommendation 是否有证据支持
6. 补测能不能解除风险

如果这六个问题答不清，最合理的动作通常不是发布，而是继续 review。

## 常见误区

### “只下降一点，不重要”

一点下降也可能集中在高风险能力上。平均数不等于风险分布。

### “recommendation 是 review，所以可以先发”

review 的意思是需要人工复查，不是默认放行。

### “样本少，所以不用管”

样本少时结论要谨慎，但高风险样本失败仍然值得记录和补测。

### “block 会影响推进速度”

真正影响速度的是把风险带上线后再补救。明确阻断和补测路径，反而能让发布流程更稳定。
