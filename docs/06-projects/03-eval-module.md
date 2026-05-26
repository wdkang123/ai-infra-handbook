# eval-module

这是学习链里的“质量闭环层”。

你在这里主要学的是：

- 一次 run 至少要沉淀哪些东西
- 一次 compare 为什么不该只剩一个 delta
- 一个最小 leaderboard 为什么应该从 history 生成
- 为什么结果目录和 history 文件很重要

`eval-module` 最值得学习的地方，不是它现在已经支持多少 benchmark，  
而是它已经把“评测不该只剩一个结果文件”这件事结构化地做出来了：总分、样本输出、样本分析、run history、compare 和 leaderboard 都有各自的位置。

## 这层的工程心智模型

可以把 `eval-module` 想成一个“质量判断工厂”：

```text
task + model + backend
  -> run
  -> result bundle
  -> sample evidence
  -> compare
  -> recommendation
  -> history / index / leaderboard
```

它不是简单地“跑 benchmark”。它真正训练的是：如何把一次质量观察变成可以比较、可以复盘、可以进入发布讨论的对象。

如果没有这层，模型或 prompt 的变化很容易只剩一句“感觉变好了”。有了 run、sample analysis、compare 和 history，讨论才会从感觉变成证据。

## 先看哪些代码

- `projects/eval-module/src/eval_module/main.py`
- `projects/eval-module/src/eval_module/runners/factory.py`
- `projects/eval-module/src/eval_module/runners/lm_eval_runner.py`
- `projects/eval-module/src/eval_module/results/result_store.py`

第一次看代码时，最推荐顺序是：

1. 先看 `main.py`，理解 run / compare / leaderboard 入口
2. 再看 `factory.py`，理解 runner 后端为什么应该有统一入口
3. 再看 `result_store.py`，理解 bundle 和 history 为什么存在
4. 最后再看 runner，理解“执行一次评测”和“沉淀一次评测”不是同一件事

代码阅读时最重要的分界是：

- runner 负责“怎么跑”。
- result store 负责“怎么记录和比较”。
- CLI 负责“学习者如何触发和查看”。

真实评测系统也会有类似边界。执行评测和沉淀证据是两件事，把它们分开，后续才容易接更多后端、更多任务和更多报告形式。

## 先跑什么

```bash
cd /path/to/ai-infra/projects/eval-module
PYTHONPATH=src ../../.venv/bin/python -m eval_module.main run \
  --task mmlu \
  --model Qwen/Qwen2.5-0.5B-Instruct \
  --backend-url http://localhost:8000/v1 \
  --output ./results/mmlu_eval_result.json
```

然后再跑 compare：

```bash
PYTHONPATH=src ../../.venv/bin/python -m eval_module.main compare \
  --baseline ./results/mmlu_eval_result.json \
  --candidate ./results/mmlu_eval_result.json \
  --min-delta 0.01 \
  --output ./results/mmlu_compare.json
```

`--min-delta` 用来定义最小有效差异。比如 baseline 和 candidate 只差 `0.005`，而 `--min-delta 0.01`，这次 compare 会判为 `unchanged`，避免把正常评测波动误写成质量提升或退化。

compare 还会拒绝不同 task 之间的比较。比如 `mmlu` 和 `gsm8k` 的 accuracy 不是同一个语义空间，直接做 delta 很容易误导发布判断。

compare 现在还会输出 `release_recommendation`：

- `approve`：candidate 明确超过 `min_delta`，且 few-shot、样本数等设置一致
- `review`：结果基本持平，或评测设置发生变化，需要人工复查
- `block`：candidate 退化超过 `min_delta`

这不是自动发布系统，而是把“是否能发布”从口头判断变成可记录的评测产物。

## 一次 eval 判断怎么形成

可以按这条链理解：

```text
run result
  -> sample outputs
  -> sample summary
  -> sample analysis
  -> compare report
  -> release recommendation
  -> comparison history
```

其中最容易被跳过的是 sample analysis。很多初学者只看 overall score，但 LLM 评测的风险往往藏在样本层：某一类样本集中失败、judge reason 重复出现、输出 token 暴涨、低分集中在关键能力上。

所以这页要训练的是：先看分数，但不要停在分数。

如果你已经有多次 run，可以再生成一个最小 leaderboard：

```bash
PYTHONPATH=src ../../.venv/bin/python -m eval_module.main leaderboard \
  --results-dir ./results \
  --backend vllm \
  --num-fewshot 5 \
  --output ./results/leaderboard.json
```

这个 leaderboard 不是完整前端页面，而是从 `run_history.jsonl` 读取结果，按 task/model/backend/few-shot 汇总 best accuracy、latest accuracy、run count、样本摘要，以及 best/latest 对应的 result file。它还会生成 `backend_groups` 和 `fewshot_groups`，让你看到同一个模型在不同后端或 few-shot 设置下不应该被混成一个数字。

如果你想先浏览历史 run，而不是直接看排行榜，可以生成 run index：

```bash
PYTHONPATH=src ../../.venv/bin/python -m eval_module.main list-runs \
  --results-dir ./results \
  --backend vllm \
  --num-fewshot 5 \
  --output ./results/run_index.json
```

`run_index.json` / `run_index.md` 是 history 的浏览层。它按时间列出 run、result file、accuracy、样本数、backend 和 few-shot，也支持按 backend/few-shot 过滤，适合在进入 leaderboard 或 compare 前先盘点“到底跑过哪些结果”。

run index 现在还会生成 `task_summaries`：按 task 汇总 run count、模型/后端/few-shot 覆盖数、best/latest accuracy，以及 best/latest 对应的 result file。这样你不需要先进入 leaderboard，也能快速回答“这个 task 最近跑过几次、最好结果是哪一次、最新结果是否退化”。

compare 也可以生成 comparison index：

```bash
PYTHONPATH=src ../../.venv/bin/python -m eval_module.main list-comparisons \
  --results-dir ./results \
  --output ./results/comparison_index.json
```

`comparison_index.json` / `comparison_index.md` 读取 `comparison_history.jsonl`，把 baseline、candidate、delta、verdict、release recommendation、comparison file、verdict counts、recommendation counts、task summaries 和平均 delta 摆出来，适合复盘“过去做过哪些发布判断，以及每个 task 的发布判断分布如何”。

如果你想让这轮练习更有感觉，建议不要只停在命令通过，而是按这个顺序看：

1. 先看主结果 JSON
2. 再看 run bundle 目录
3. 再看 compare JSON / Markdown
4. 再看 `sample_outputs.json`
5. 再看 `sample_summary.json`
6. 再看 `sample_analysis.json`
7. 再看 `run_index.json` / `run_index.md`
8. 再看 `comparison_index.json` / `comparison_index.md`
9. 再看 `leaderboard.json` / `leaderboard.md`
10. 最后看 `run_history.jsonl` 和 `comparison_history.jsonl`

## 做一个 30 分钟练习

1. 跑一次 baseline run。
2. 用同一个结果跑一次 compare，理解报告结构。
3. 修改 `--min-delta`，观察 recommendation 如何变化。
4. 生成 run index、comparison index 和 leaderboard。
5. 写一段发布判断，不超过 8 行。

复盘模板：

```text
task：
baseline：
candidate：
delta：
min_delta：
release recommendation：
sample analysis 里最重要的发现：
我是否会进入下一阶段：
还缺什么证据：
```

这个练习的重点不是制造真实提升，而是理解发布判断对象怎么长出来。

## 你应该观察什么

- 主结果 JSON
- run bundle 目录
- compare JSON
- compare Markdown
- `release_recommendation` 和 `release_reasons`
- `sample_outputs.json`
- `sample_summary.json`
- `sample_analysis.json`
- `run_index.json`
- `run_index.md`
- run index 里的 `task_summaries`
- `comparison_index.json`
- `comparison_index.md`
- comparison index 里的 `verdict_counts` / `recommendation_counts`
- comparison index 里的 `task_summaries`
- `leaderboard.json`
- `leaderboard.md`
- leaderboard 里的 `best_result_file` / `latest_result_file`
- `run_history.jsonl`
- `comparison_history.jsonl`

这里最关键的学习问题是：

- 为什么一次 run 不该只留下一个分数
- 为什么 sample-level output 里要保留 `prompt_tokens`、`prediction_tokens` 和 `judge_reason`
- 为什么 `sample_summary.json` 能帮你快速判断样本级结果是否值得继续追
- 为什么 `sample_analysis.json` 要继续保留 pass rate、score bucket、失败样本 id 和 judge reason 计数
- 为什么 compare 本身也应该被对象化
- 为什么 leaderboard 只能汇总历史结果，不能替代 run/compare
- 为什么 backend/few-shot 是 leaderboard 和 run index 的重要查询维度
- 为什么 run index 的 task summaries 能帮你先看 best/latest 证据文件，再决定是否进入 leaderboard 或 compare
- 为什么长期看结果时，history 比单次截图更重要

## 这部分当前已经做到什么

- 最小 run / compare / leaderboard / list-runs / list-comparisons / list-tasks CLI
- run / comparison bundle 落盘
- sample-level output 落盘
- sample summary 落盘
- sample analysis 落盘，包含 pass rate、score buckets、failed sample ids 和 judge reason counts
- 从 `run_history.jsonl` 聚合的 run index JSON/Markdown，支持 backend/few-shot 过滤和 task summaries
- 从 `comparison_history.jsonl` 聚合的 comparison index JSON/Markdown，包含 verdict/recommendation 计数和 task summaries
- 从 `run_history.jsonl` 聚合的最小 leaderboard JSON/Markdown，包含 backend/few-shot 分组与 best/latest result file
- sample judge reason、prompt tokens 和 prediction tokens
- JSON + Markdown 报告
- 可追加 history
- runner factory 扩展点
- compare 的 `min_delta` 判定阈值
- compare 的 task 一致性校验
- compare 的 release recommendation 与原因列表

也就是说，它已经不只是“能跑一次”，而是已经开始具备“能积累判断上下文”的结构。

## 如何判断自己学懂了

| 能力 | 合格表现 |
| --- | --- |
| run 理解 | 能说明 result、sample outputs、sample summary、sample analysis 的区别 |
| compare 理解 | 能解释 task 一致性、min_delta、verdict、release recommendation |
| history 理解 | 能说明 run history 和 comparison history 为什么需要追加记录 |
| leaderboard 理解 | 能说明 leaderboard 是展示/汇总层，不是发布门禁 |
| 发布判断 | 能写出 approve/review/block 的证据和剩余风险 |

如果你只能跑出 `accuracy`，还没有真正掌握 eval-module。合格的学习目标是能把评测结果讲成一段有边界的工程判断。

## 这部分当前还没做到什么

- 真实多模型批量评测调度
- 更复杂的 leaderboard 聚合和可视化
- 在线评测 / 回放
- 真正接外部评测系统

这些缺口对应真实生产评测平台的复杂度。当前仓库先保留最小对象模型：run、sample、compare、history、leaderboard。对象模型理解清楚后，再接真实任务调度和在线回放会更自然。

## 最适合的继续学习顺序

如果你已经把这页跑过一轮，下一步最推荐接着读：

1. [Run、Compare、History](/04-evaluation-observability/01-run-compare-history)
2. [LLM Evaluation](/04-evaluation-observability/05-llm-evaluation)
3. [从 Run 到发布决策](/04-evaluation-observability/07-from-run-to-release-decision)
4. [Benchmark 与生产质量不是一回事](/04-evaluation-observability/08-benchmark-vs-production-quality)

这样你会更容易从“会跑评测命令”进入“会用结果做判断”。
