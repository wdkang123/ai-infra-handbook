# 文档与项目怎么联动

## 为什么项目总览后面还需要这一页

项目总览解决的是“这四个项目各自干什么”。

但当你真正开始学习时，更常见的问题会变成：

- 我刚读完一页文档
- 现在应该回哪个项目、哪个文件？
- 我应该跑哪条命令？
- 这个概念在代码里哪里体现？
- 输出结果应该在哪里看？

这一页就是用来解决这个问题的。

它不是完整源码导览，而是一张“文档到代码再到证据”的路标。

## 先记一张最简单的联动图

```text
基础概念
  -> inference-service / ai-gateway

推理服务
  -> inference-service

平台层
  -> ai-gateway

评测与观测
  -> eval-module + root smoke / metrics / events

微调训练
  -> finetune-demo

公开发布与共学
  -> docs + scripts + .github
```

你不需要一开始记所有文件，只要先记住“每组内容主要落在哪个项目”。

## 推荐的学习动作

最稳的节奏通常是：

1. 读一页文档。
2. 回一个项目。
3. 只开 1 到 2 个文件。
4. 跑一条最小命令。
5. 看一个输出证据。
6. 回到文档写一句复盘。

这样最容易把：

- 概念
- 代码
- 命令
- 结果
- 复盘

连成一条线。

## Inference-service 最适合承接哪些文档

它最适合承接：

- [模型、Token、Context](/01-llm-fundamentals/01-model-token-context)
- [Prefill、Decode、KV Cache](/01-llm-fundamentals/02-prefill-decode-kv-cache)
- [从请求到首个 Token](/01-llm-fundamentals/04-from-request-to-first-token)
- [Streaming、Batching、Metrics](/02-inference-serving/09-streaming-batching-metrics)
- [vLLM](/02-inference-serving/04-vllm)
- [SGLang](/02-inference-serving/05-sglang)

如果你读完这些页，最该回看的通常是：

- `projects/inference-service/src/inference_service/server.py`
- `projects/inference-service/src/inference_service/runtime.py`
- `projects/inference-service/src/inference_service/engines.py`
- `projects/inference-service/tests/test_api.py`

推荐命令：

```bash
PYTHON=.venv/bin/python make infra-check
```

推荐输出证据：

- `/health`
- `/v1/models`
- `/v1/chat/completions`
- `/metrics`
- `/events`
- request timeline

## AI Gateway 最适合承接哪些文档

它最适合承接：

- [鉴权、路由、限流](/03-ai-gateway-platform/01-auth-routing-rate-limit)
- [健康检查、Metrics、Request ID](/03-ai-gateway-platform/02-health-metrics-request-id)
- [Gateway、Router、Fallback、Cache](/03-ai-gateway-platform/03-gateway-router-fallback-cache)
- [Streaming、错误路径、Upstream Health](/03-ai-gateway-platform/04-streaming-errors-upstream-health)
- [平台层与模型服务层边界](/03-ai-gateway-platform/05-platform-vs-model-service)
- [外部模型名与内部目标映射](/03-ai-gateway-platform/06-model-name-to-target-mapping)

如果你读完这些页，最该回看的通常是：

- `projects/ai-gateway/src/ai_gateway/server.py`
- `projects/ai-gateway/src/ai_gateway/router.py`
- `projects/ai-gateway/src/ai_gateway/runtime.py`
- `projects/ai-gateway/src/ai_gateway/middleware/auth.py`
- `projects/ai-gateway/tests/test_proxy.py`

推荐命令：

```bash
PYTHON=.venv/bin/python make infra-smoke
```

推荐输出证据：

- `x-request-id`
- `x-upstream-model`
- `x-fallback-used`
- `x-cache`
- `/events/failures`
- `/events/requests/{request_id}`

## Eval-module 最适合承接哪些文档

它最适合承接：

- [Run、Compare、History](/04-evaluation-observability/01-run-compare-history)
- [LLM Evaluation](/04-evaluation-observability/05-llm-evaluation)
- [Benchmark、Arena、Leaderboard](/04-evaluation-observability/06-benchmark-arena-leaderboard)
- [从 Run 到发布决策](/04-evaluation-observability/07-from-run-to-release-decision)
- [Benchmark 与生产质量不是一回事](/04-evaluation-observability/08-benchmark-vs-production-quality)

如果你读完这些页，最该回看的通常是：

- `projects/eval-module/src/eval_module/main.py`
- `projects/eval-module/src/eval_module/runners/lm_eval_runner.py`
- `projects/eval-module/src/eval_module/results/result_store.py`
- `projects/eval-module/tests/test_runner.py`

推荐命令：

```bash
PYTHON=.venv/bin/python make infra-check
```

推荐输出证据：

- run JSON
- run Markdown
- sample outputs
- sample summary
- comparison JSON
- comparison Markdown
- run history
- leaderboard

## Finetune-demo 最适合承接哪些文档

它最适合承接：

- [LoRA、QLoRA、PEFT](/05-finetuning-training/01-lora-qlora-peft)
- [训练产物、Checkpoint、Export](/05-finetuning-training/02-run-artifacts-export)
- [Unsloth 与训练栈](/05-finetuning-training/03-unsloth-training-stack)
- [数据集、Run、Checkpoint](/05-finetuning-training/04-datasets-runs-checkpoints)
- [实验追踪、History、复现](/05-finetuning-training/06-experiment-tracking-history-reproducibility)
- [什么时候该微调](/05-finetuning-training/07-when-to-finetune)

如果你读完这些页，最该回看的通常是：

- `projects/finetune-demo/src/finetune_demo/main.py`
- `projects/finetune-demo/src/finetune_demo/config.py`
- `projects/finetune-demo/src/finetune_demo/trainer/lora_trainer.py`
- `projects/finetune-demo/src/finetune_demo/export/adapter_exporter.py`
- `projects/finetune-demo/tests/test_trainer.py`

推荐输出证据：

- dataset summary
- dataset registry
- run state
- checkpoint index
- artifacts manifest
- export manifest
- export history

## Docs、Scripts、GitHub 配置承接什么

公开发布、课程生成和共学材料主要落在：

- `docs/`
- `scripts/`
- `.github/`
- `README.md`
- `CHANGELOG.md`
- `CONTRIBUTING.md`
- `SECURITY.md`

适合承接：

- [公开仓库卫生规范](/08-publication/06-public-repo-hygiene)
- [依赖维护与 Bot PR 处理](/08-publication/07-dependency-maintenance)
- [GitHub 入口与协作地图](/08-publication/14-github-entrypoints)
- [共学与公开分享套件](/14-workshop-kit/00-overview)
- [验证矩阵](/09-reference/07-validation-matrix)

推荐命令：

```bash
PYTHON=.venv/bin/python make docs-quality
PYTHON=.venv/bin/python make public-check
```

推荐输出证据：

- docs-quality 结果
- security scan 结果
- VitePress build
- GitHub Actions
- GitHub Pages 200

## 一张快速索引表

| 你读到的内容 | 先看项目 | 再看证据 |
| --- | --- | --- |
| Token / prefill / decode | inference-service | usage、metrics、events |
| Gateway auth / route | ai-gateway | status、headers、events |
| Fallback / cache | ai-gateway | `x-fallback-used`、`x-cache`、metrics |
| LLM Evaluation | eval-module | run、compare、sample analysis |
| Leaderboard | eval-module | run history、leaderboard JSON/MD |
| LoRA / export | finetune-demo | checkpoint index、export manifest |
| Public release | docs + scripts + workflows | public-check、Actions、Pages |

## 常见误区

### 误区一：读完文档再一次性看代码

太晚。更好的方式是一页文档对应一两个文件。

### 误区二：只看代码不看输出

代码告诉你实现，输出证据告诉你行为是否真的发生。

### 误区三：看到文件很多就全打开

不要。先找入口文件和测试文件，再顺着调用深入。

### 误区四：把项目页当目录说明

项目页的作用是把概念、代码、命令和证据接起来。

## 这一页学完应该带走什么

项目页不是代码目录说明，文档页也不是纯理论文章。

它们本来就应该联动起来看：一边解释为什么，一边展示现在是怎么做的。

当你能从一页文档找到对应代码、运行命令、输出证据和验证方式时，这个学习站的价值才真正发挥出来。
