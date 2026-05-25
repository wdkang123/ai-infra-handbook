# eval-module

这是学习链路里的“质量闭环层”入口。

它的重点不是把 lm-eval 做满，而是让你理解：

- 一次评测 run 至少该留下什么
- 一次 compare 至少该留下什么
- 为什么只输出一份 JSON 不够
- 为什么运行历史也要记录下来
- 为什么 leaderboard 应该从历史结果生成，而不是替代评测过程
- 为什么 leaderboard 需要保留 best/latest result file
- 为什么发布判断需要 recommendation 和 reasons

## 先看哪里

- [main.py](src/eval_module/main.py)
- [lm_eval_runner.py](src/eval_module/runners/lm_eval_runner.py)
- [result_store.py](src/eval_module/results/result_store.py)

## 先跑什么

```bash
cd projects/eval-module
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
  --output ./results/mmlu_compare.json
```

最后生成一个最小 leaderboard：

```bash
PYTHONPATH=src ../../.venv/bin/python -m eval_module.main leaderboard \
  --results-dir ./results \
  --backend vllm \
  --num-fewshot 5 \
  --output ./results/leaderboard.json
```

也可以列出历史 run：

```bash
PYTHONPATH=src ../../.venv/bin/python -m eval_module.main list-runs \
  --results-dir ./results \
  --backend vllm \
  --num-fewshot 5 \
  --output ./results/run_index.json
```

也可以列出历史 compare：

```bash
PYTHONPATH=src ../../.venv/bin/python -m eval_module.main list-comparisons \
  --results-dir ./results \
  --output ./results/comparison_index.json
```

## 你应该看到什么

- 主结果 JSON
- run bundle 目录
- sample outputs JSON
- sample summary JSON
- sample analysis JSON
- compare JSON
- compare markdown
- run index JSON / Markdown
- run index 里的 `task_summaries`
- comparison index JSON / Markdown
- comparison index 里的 `verdict_counts` / `recommendation_counts`
- comparison index 里的 `task_summaries`
- leaderboard JSON / Markdown
- leaderboard 里的 `backend_groups` / `fewshot_groups`
- leaderboard 里的 `best_result_file` / `latest_result_file`
- `summary.release_recommendation`
- `run_history.jsonl`
- `comparison_history.jsonl`

## 这段代码现在解决什么

- 最小 run CLI
- 最小 compare CLI
- 最小 leaderboard CLI
- 最小 list-runs CLI
- 最小 list-comparisons CLI
- run index task summaries
- comparison index verdict/recommendation 聚合
- comparison index task summaries
- backend/few-shot 过滤和 leaderboard 分组视图
- run/comparison bundle 落盘
- sample outputs 落盘
- sample summary 落盘
- sample analysis 落盘
- leaderboard best/latest result file 追踪
- 可追加的历史记录
- `approve / review / block` release recommendation

## 这段代码现在还没解决什么

- 没有真实多模型批量评测调度
- 没有更复杂的 leaderboard 聚合和可视化
- 没有在线评测/回放
- 还没有真正接外部评测系统
