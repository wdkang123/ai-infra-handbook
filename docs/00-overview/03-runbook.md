# 最小运行手册

## 1. 这页解决什么问题

这页给你一个最直接的入口：

- 先执行什么命令
- 应该看到什么结果
- 如果想继续深挖，去看哪段代码

如果你后面准备开始“按文档一步步跑”，这页可以直接当成操作手册。

如果你希望照着一篇文档完整走一遍，建议直接配合：

- [第一次实操演练](/00-overview/04-first-walkthrough)
- [文档与代码怎么对应](/00-overview/05-docs-to-code-map)

## 2. 先准备什么

当前默认使用仓库根目录虚拟环境：

```bash
.venv/bin/python
```

根级常用命令入口都在：

- `Makefile`

## 3. 最快验证方法

先跑一遍项目测试：

```bash
cd /path/to/ai-infra
PYTHON=.venv/bin/python make infra-test
```

如果你主要改了文档、导航或首页入口，可以先跑：

```bash
cd /path/to/ai-infra
PYTHON=.venv/bin/python make docs-quality
```

再跑一遍最小联调：

```bash
cd /path/to/ai-infra
PYTHON=.venv/bin/python make infra-smoke
```

如果这两条都通过，说明当前四个项目的最小学习闭环是通的。

## 4. 浏览器里能看什么

当前可以直接在浏览器打开这些地址：

- [http://localhost:8000/health](http://localhost:8000/health)
- [http://localhost:8000/metrics](http://localhost:8000/metrics)
- [http://localhost:8080/health](http://localhost:8080/health)
- [http://localhost:8080/metrics](http://localhost:8080/metrics)

注意：

- 这还不是完整前端网站
- 现在是服务状态页和指标页
- 学习重点是先理解后端链路

## 5. 按项目分别怎么跑

### inference-service

```bash
cd /path/to/ai-infra/projects/inference-service
PYTHONPATH=src ../../.venv/bin/python -m inference_service.main serve
```

最小 streaming 示例：

```bash
curl -N http://localhost:8000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"Qwen/Qwen2.5-0.5B-Instruct","messages":[{"role":"user","content":"Hi stream"}],"stream":true}'
```

看代码：

- `projects/inference-service/src/inference_service/main.py`
- `projects/inference-service/src/inference_service/server.py`
- `projects/inference-service/src/inference_service/runtime.py`

### ai-gateway

```bash
cd /path/to/ai-infra/projects/ai-gateway
PYTHONPATH=src ../../.venv/bin/python -m ai_gateway.main serve
```

最小 streaming 透传示例：

```bash
curl -N http://localhost:8080/v1/chat/completions \
  -H 'Authorization: Bearer sk-test-key-1' \
  -H 'Content-Type: application/json' \
  -d '{"model":"vllm-local","messages":[{"role":"user","content":"Hi stream"}],"stream":true}'
```

最小 request id 示例：

```bash
curl -i -s http://localhost:8080/v1/chat/completions \
  -H 'Authorization: Bearer sk-test-key-1' \
  -H 'X-Request-ID: req_runbook_1' \
  -H 'Content-Type: application/json' \
  -d '{"model":"vllm-local","messages":[{"role":"user","content":"Hi request id"}]}'
```

观察 `/health` 时，重点看 `upstream_services`。现在这一项来自 gateway 对下游 inference `/health` 的最小真实探测，而不是静态配置回显；如果探测失败，gateway 顶层 `status` 也会变成 `degraded`。

看代码：

- `projects/ai-gateway/src/ai_gateway/server.py`
- `projects/ai-gateway/src/ai_gateway/router.py`
- `projects/ai-gateway/src/ai_gateway/middleware/auth.py`

### eval-module

```bash
cd /path/to/ai-infra/projects/eval-module
PYTHONPATH=src ../../.venv/bin/python -m eval_module.main run \
  --task mmlu \
  --model Qwen/Qwen2.5-0.5B-Instruct \
  --backend-url http://localhost:8000/v1 \
  --output ./results/mmlu_eval_result.json
```

```bash
PYTHONPATH=src ../../.venv/bin/python -m eval_module.main compare \
  --baseline ./results/mmlu_eval_result.json \
  --candidate ./results/mmlu_eval_result.json \
  --output ./results/mmlu_compare.json
```

看代码：

- `projects/eval-module/src/eval_module/main.py`
- `projects/eval-module/src/eval_module/results/result_store.py`

### finetune-demo

```bash
cd /path/to/ai-infra/projects/finetune-demo
PYTHONPATH=src ../../.venv/bin/python -m finetune_demo.main train \
  --method lora \
  --model Qwen/Qwen2.5-0.5B-Instruct \
  --dataset ./data/train.jsonl \
  --output ./outputs/demo-run \
  --epochs 1
```

```bash
PYTHONPATH=src ../../.venv/bin/python -m finetune_demo.main export \
  --checkpoint ./outputs/demo-run/checkpoint-0001 \
  --output ./outputs/demo-export
```

看代码：

- `projects/finetune-demo/src/finetune_demo/main.py`
- `projects/finetune-demo/src/finetune_demo/trainer/lora_trainer.py`
- `projects/finetune-demo/src/finetune_demo/export/adapter_exporter.py`

## 6. 你应该关注哪些输出物

### inference-service

- `health`
- `metrics`
- `/v1/models`
- `/events` 和事件过滤查询
- `/events/summary` 事件摘要
- request timeline
- request timeline index
- chat completion 响应

### ai-gateway

- `401 / 404 / 429 / 502`
- `/v1/models`
- gateway metrics
- `/events` 和事件过滤查询
- `/events/summary` 事件摘要
- `/events/failures` 失败摘要
- request timeline
- request timeline index
- `x-cache` / `x-upstream-model` / `x-fallback-used`

### eval-module

- result json
- run bundle
- comparison json
- comparison markdown
- `sample_outputs.json`
- `sample_summary.json`
- `sample_analysis.json`
- `run_index.json`
- `run_index.md`
- run index task summaries
- `comparison_index.json`
- `comparison_index.md`
- comparison verdict/recommendation counts
- comparison task summaries
- `leaderboard.json`
- `leaderboard.md`
- leaderboard backend/few-shot 分组
- leaderboard best/latest result file
- `run_history.jsonl`
- `comparison_history.jsonl`

### finetune-demo

- `run_manifest.json`
- `artifacts_manifest.json`
- `export_manifest.json`
- dataset registry entry / `dataset_registry.jsonl`
- dataset registry report
- dataset registry filter / duplicate count
- dataset registry diff
- dataset version / dataset sha256
- checkpoint index
- `run_history.jsonl`
- `run_index.json`
- `run_index.md`
- `export_history.jsonl`
- `export_index.json`
- `export_index.md`
- export status / duration
- export model/dataset summaries
- export manifest pointer
- run manifest pointer
- checkpoint index pointer

## 7. 下一步应该怎么学

推荐节奏：

1. 跑 root 级命令
2. 跑单项目命令
3. 看产物
4. 对照代码入口
5. 改一点再重跑

如果你卡住了，就把报错和当前产物一起拿来分析，比只看代码更容易定位问题。

如果你跑完这一页之后，不知道下一步该深挖哪条线，继续看：

- [第一次跑完之后学什么](/00-overview/06-after-first-walkthrough)
- [按目标选择学习路径](/00-overview/07-choose-your-path)
