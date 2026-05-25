# eval-module

这是学习链里的“质量闭环层”。

你在这里主要学的是：

- 一次 run 至少要沉淀哪些东西
- 一次 compare 为什么不该只剩一个 delta
- 一个最小 leaderboard 为什么应该从 history 生成
- 为什么结果目录和 history 文件很重要

`eval-module` 最值得学习的地方，不是它现在已经支持多少 benchmark，  
而是它已经把“评测不该只剩一个结果文件”这件事结构化地做出来了：总分、样本输出、样本分析、run history、compare 和 leaderboard 都有各自的位置。

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

## 这部分当前还没做到什么

- 真实多模型批量评测调度
- 更复杂的 leaderboard 聚合和可视化
- 在线评测 / 回放
- 真正接外部评测系统

## 最适合的继续学习顺序

如果你已经把这页跑过一轮，下一步最推荐接着读：

1. [Run、Compare、History](/04-evaluation-observability/01-run-compare-history)
2. [LLM Evaluation](/04-evaluation-observability/05-llm-evaluation)
3. [从 Run 到发布决策](/04-evaluation-observability/07-from-run-to-release-decision)
4. [Benchmark 与生产质量不是一回事](/04-evaluation-observability/08-benchmark-vs-production-quality)

这样你会更容易从“会跑评测命令”进入“会用结果做判断”。
