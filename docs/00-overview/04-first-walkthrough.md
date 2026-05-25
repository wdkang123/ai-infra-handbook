# 第一次实操演练

## 1. 这篇文档的目标

这不是完整教程，而是你第一次真正上手时的演练单。

目标很简单：

- 不要求你一次看懂所有代码
- 只要求你把四个项目串起来跑一遍
- 跑完之后知道每个模块大概负责什么

如果你第一次开始实际动手，建议直接照这篇做。

## 2. 开始前你要知道什么

这次演练里你会碰到四个模块：

1. `inference-service`：模型服务本体
2. `ai-gateway`：请求治理和代理层
3. `eval-module`：评测与对比输出
4. `finetune-demo`：训练/导出产物

你不需要先把它们的源码看完，只需要先知道：

- inference 负责“回答”
- gateway 负责“转发和治理”
- eval 负责“记录评测结果”
- finetune 负责“记录训练产物”

## 3. 第一步：先跑仓库总验证

在仓库根目录执行：

```bash
cd /path/to/ai-infra
PYTHON=.venv/bin/python make infra-test
PYTHON=.venv/bin/python make infra-smoke
```

如果这两条都通过，你就已经确认：

- 四个项目当前最小闭环是通的
- 当前环境可以继续往下学

## 4. 第二步：单独看 inference-service

先启动它：

```bash
cd /path/to/ai-infra/projects/inference-service
PYTHONPATH=src ../../.venv/bin/python -m inference_service.main serve
```

打开：

- [http://localhost:8000/health](http://localhost:8000/health)
- [http://localhost:8000/metrics](http://localhost:8000/metrics)

然后发请求：

```bash
curl -s http://localhost:8000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"Qwen/Qwen2.5-0.5B-Instruct","messages":[{"role":"user","content":"Hello inference"}]}'
```

再刷新一次 `/metrics`。

这一步你应该观察：

- 为什么请求数变了
- 为什么 token 数变了
- 为什么这层只负责服务模型，不负责鉴权和路由

再试一次最小 streaming：

```bash
curl -N http://localhost:8000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"Qwen/Qwen2.5-0.5B-Instruct","messages":[{"role":"user","content":"Hello stream"}],"stream":true}'
```

这一步你应该观察：

- 同一个接口既可以一次性返回 JSON，也可以按事件流返回
- 底层模型服务开始出现“流式能力”的影子
- gateway 这一层后来也已经把最小 streaming 继续透传上来了

再主动打一条错误请求：

```bash
curl -i -s http://localhost:8000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"unknown-model","messages":[{"role":"user","content":"Hello inference"}]}'
```

你应该观察：

- `404` 是在服务层返回的
- 返回体也已经收成统一 `error` 结构

看代码入口：

- `projects/inference-service/src/inference_service/server.py`
- `projects/inference-service/src/inference_service/runtime.py`

## 5. 第三步：再看 ai-gateway

启动 gateway：

```bash
cd /path/to/ai-infra/projects/ai-gateway
PYTHONPATH=src ../../.venv/bin/python -m ai_gateway.main serve
```

打开：

- [http://localhost:8080/health](http://localhost:8080/health)
- [http://localhost:8080/metrics](http://localhost:8080/metrics)

这次你可以先观察 `/health` 里 `upstream_services` 的值。现在它不是静态写死的“healthy”，而是 gateway 对下游 inference `/health` 做出来的一次最小真实探测；如果下游探测失败，gateway 顶层 `status` 也会变成 `degraded`。

然后试三种请求：

### 正常代理

```bash
curl -s http://localhost:8080/v1/chat/completions \
  -H 'Authorization: Bearer dev-gateway-key-1' \
  -H 'Content-Type: application/json' \
  -d '{"model":"vllm-local","messages":[{"role":"user","content":"Hello gateway"}]}'
```

### 不带 token

```bash
curl -i -s http://localhost:8080/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"vllm-local","messages":[{"role":"user","content":"Hello"}]}'
```

### 未知模型

```bash
curl -i -s http://localhost:8080/v1/chat/completions \
  -H 'Authorization: Bearer dev-gateway-key-1' \
  -H 'Content-Type: application/json' \
  -d '{"model":"unknown-model","messages":[{"role":"user","content":"Hello"}]}'
```

这一步你应该观察：

- gateway 自己不生成内容
- gateway 只是验证、路由、转发
- `401 / 404` 都是在平台层拦住的

你也可以主动试一下 `stream=true`：

```bash
curl -i -N http://localhost:8080/v1/chat/completions \
  -H 'Authorization: Bearer dev-gateway-key-1' \
  -H 'Content-Type: application/json' \
  -d '{"model":"vllm-local","messages":[{"role":"user","content":"Hello"}],"stream":true}'
```

现在它会把下游的最小 SSE 事件流继续向上透传。你可以把这一步和前一节直接访问 inference 的 streaming 放在一起看：底层服务负责产生事件流，gateway 负责在鉴权和路由之后把它继续转发出来。

再试一条带 request id 的请求：

```bash
curl -i -s http://localhost:8080/v1/chat/completions \
  -H 'Authorization: Bearer dev-gateway-key-1' \
  -H 'X-Request-ID: req_walkthrough_1' \
  -H 'Content-Type: application/json' \
  -d '{"model":"vllm-local","messages":[{"role":"user","content":"Hello request id"}]}'
```

这一步你应该观察：

- gateway 会把 `x-request-id` 返回给你
- 这类 header 不是业务内容本身，但对跨服务排查很重要
- 以后如果链路再变复杂，request id 就会越来越有价值

看代码入口：

- `projects/ai-gateway/src/ai_gateway/server.py`
- `projects/ai-gateway/src/ai_gateway/router.py`

## 6. 第四步：跑一次 eval

```bash
cd /path/to/ai-infra/projects/eval-module
PYTHONPATH=src ../../.venv/bin/python -m eval_module.main run \
  --task mmlu \
  --model Qwen/Qwen2.5-0.5B-Instruct \
  --backend-url http://localhost:8000/v1 \
  --output ./results/demo_run.json
```

然后再跑 compare：

```bash
PYTHONPATH=src ../../.venv/bin/python -m eval_module.main compare \
  --baseline ./results/demo_run.json \
  --candidate ./results/demo_run.json \
  --output ./results/demo_compare.json
```

再生成一个最小 leaderboard：

```bash
PYTHONPATH=src ../../.venv/bin/python -m eval_module.main leaderboard \
  --results-dir ./results \
  --backend vllm \
  --num-fewshot 5 \
  --output ./results/demo_leaderboard.json
```

再生成 run index：

```bash
PYTHONPATH=src ../../.venv/bin/python -m eval_module.main list-runs \
  --results-dir ./results \
  --backend vllm \
  --num-fewshot 5 \
  --output ./results/demo_run_index.json
```

这一步你应该去看：

- `./results/demo_run.json`
- `./results/demo_run/`
- `./results/demo_run/sample_analysis.json`
- `./results/demo_compare.json`
- `./results/demo_compare/`
- `./results/demo_leaderboard.json`
- `./results/demo_leaderboard.md`
- `./results/demo_run_index.json`
- `./results/demo_run_index.md`
- `./results/demo_run_index.json` 里的 `task_summaries`
- `./results/run_history.jsonl`
- `./results/comparison_history.jsonl`

你应该理解：

- 一次 run 不只是一个分数
- 样本分析能帮你先看 pass rate、score bucket 和 judge reason 分布
- 一次 compare 也不只是一个 delta
- leaderboard 是从 history 聚合出来的展示层
- run index 是从 history 聚合出来的历史清单
- leaderboard 里的 backend/few-shot 分组能避免不同评测设置被混成一个分数
- history 文件为什么对长期追踪有价值

## 7. 第五步：跑一次 finetune

```bash
cd /path/to/ai-infra/projects/finetune-demo
PYTHONPATH=src ../../.venv/bin/python -m finetune_demo.main train \
  --method lora \
  --model Qwen/Qwen2.5-0.5B-Instruct \
  --dataset ./data/train.jsonl \
  --output ./outputs/demo-run \
  --epochs 1
```

然后导出：

```bash
PYTHONPATH=src ../../.venv/bin/python -m finetune_demo.main export \
  --checkpoint ./outputs/demo-run/checkpoint-0001 \
  --output ./outputs/demo-export
```

再查看 dataset registry：

```bash
PYTHONPATH=src ../../.venv/bin/python -m finetune_demo.main list-datasets \
  --registry ./outputs/dataset_registry.jsonl \
  --output ./outputs/dataset_registry_report.json \
  --markdown-output ./outputs/dataset_registry_report.md
```

再查看训练 run history：

```bash
PYTHONPATH=src ../../.venv/bin/python -m finetune_demo.main list-runs \
  --history ./outputs/run_history.jsonl \
  --output ./outputs/run_index.json \
  --markdown-output ./outputs/run_index.md
```

再查看 export history：

```bash
PYTHONPATH=src ../../.venv/bin/python -m finetune_demo.main list-exports \
  --history ./outputs/export_history.jsonl \
  --output ./outputs/export_index.json \
  --markdown-output ./outputs/export_index.md
```

这一步你应该去看：

- `./outputs/demo-run/run_manifest.json`
- `./outputs/demo-run/artifacts_manifest.json`
- `./outputs/demo-run/logs/events.jsonl`
- `./outputs/demo-run/data/dataset_summary.json`
- `./outputs/demo-run/data/dataset_registry_entry.json`
- `./outputs/demo-run/checkpoints/checkpoint_index.json`
- `./outputs/dataset_registry.jsonl`
- `./outputs/dataset_registry_report.json`
- `./outputs/dataset_registry_report.md`
- `./outputs/demo-export/export_manifest.json`
- `./outputs/run_history.jsonl`
- `./outputs/run_index.json` 里的 `run_manifest_file`
- `./outputs/run_index.json` 里的 `checkpoint_index_file`
- `./outputs/run_index.json` 里的 `model_summaries` 和 `dataset_summaries`
- `./outputs/export_history.jsonl`
- `./outputs/export_index.json` 里的 `status_counts` 和 `average_duration_seconds`

你应该理解：

- 训练 run 为什么要有结构化产物
- 为什么 checkpoint 不该是唯一输出
- 为什么 checkpoint index 比单个 latest checkpoint 更适合继续扩展 resume/export
- 为什么 dataset registry 能跨 run 追踪训练输入
- 为什么 registry report 是读取已有登记，而不是重新训练
- 为什么 run index 是读取已有训练历史，而不是重新训练
- 为什么 export index 是读取已有导出历史，而不是重新导出
- 为什么 dataset version 要从 train 继续传到 export
- 为什么 history 能帮助你比较多次实验

## 8. 第六步：做一个最小改动练习

现在挑一个最小改动，不要同时改很多地方。

推荐选一个：

1. 改 `inference-service` 里 mock 回复文本
2. 改 `ai-gateway` 的限流阈值
3. 改 `eval-module` 里某个 task 的 mock 分数
4. 改 `finetune-demo` 的 mock `loss`

改完之后，重新跑对应模块，再看结果变化。

## 9. 这轮演练结束后你应该得到什么

如果你把这篇完整走完，你不一定已经“精通 AI Infra”，但你应该已经得到：

- 一张更清楚的系统地图
- 一条从文档到代码到运行结果的路径
- 对四个项目分工的直觉
- 对后续继续细化代码的信心

这就够了。
