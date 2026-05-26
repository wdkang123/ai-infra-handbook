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

## 1.1 运行手册的读法

这页不是让你机械复制命令，而是训练一种最重要的工程习惯：

```text
运行命令 -> 观察输出 -> 判断属于哪一层 -> 找代码入口 -> 改一点再验证
```

如果只复制命令，你可能会得到一个“成功”或“失败”的结果；如果按上面这条链路走，你会知道结果为什么成功、失败应该查哪里、下一步该看哪个文件。

所以每跑一条命令，建议顺手记录三件事：

| 记录项 | 示例 |
| --- | --- |
| 命令做了什么 | 启动 inference-service / 运行 smoke / 生成 eval result |
| 成功时看到什么 | health ok、metrics 输出、manifest 文件生成 |
| 失败时先查哪里 | 端口、依赖、request id、events、测试输出 |

这会让 runbook 从“命令清单”变成“学习路线”。

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

## 3.1 怎么理解 root 级命令

根目录命令是为了把多个项目的验证收在一起。

| 命令 | 适合什么时候跑 | 它主要证明什么 |
| --- | --- | --- |
| `make docs-quality` | 改文档、导航、链接 | 文档站结构没有明显断裂 |
| `make infra-test` | 改某个项目代码 | 单项目测试仍然通过 |
| `make infra-check` | 准备较大改动或提交 | lint、测试、文档构建等核心检查通过 |
| `make infra-smoke` | 改跨项目链路 | gateway、inference、eval、finetune 最小闭环没断 |
| `make public-check` | 准备公开发布 | 公网级分享前的基本安全和卫生检查 |

不要每改一个字都跑最重命令。更好的方式是根据改动范围选择验证。这样既节省时间，也能让验证结果更有解释力。

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

这些页面虽然很朴素，但它们很有价值。`/health` 告诉你服务是否可用，`/metrics` 告诉你服务发生过什么，gateway 的 health 还会把下游 upstream 状态聚合进来。真实平台里的 dashboard，本质上也是把这些信号用更好的方式组织起来。

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

运行后可以顺手问自己：

- 普通响应和 streaming 响应有什么不同？
- usage 字段说明了什么？
- unknown model 会如何表达？
- `/metrics` 是否记录了这次请求？

### ai-gateway

```bash
cd /path/to/ai-infra/projects/ai-gateway
PYTHONPATH=src ../../.venv/bin/python -m ai_gateway.main serve
```

最小 streaming 透传示例：

```bash
curl -N http://localhost:8080/v1/chat/completions \
  -H 'Authorization: Bearer dev-gateway-key-1' \
  -H 'Content-Type: application/json' \
  -d '{"model":"vllm-local","messages":[{"role":"user","content":"Hi stream"}],"stream":true}'
```

最小 request id 示例：

```bash
curl -i -s http://localhost:8080/v1/chat/completions \
  -H 'Authorization: Bearer dev-gateway-key-1' \
  -H 'X-Request-ID: req_runbook_1' \
  -H 'Content-Type: application/json' \
  -d '{"model":"vllm-local","messages":[{"role":"user","content":"Hi request id"}]}'
```

观察 `/health` 时，重点看 `upstream_services`。现在这一项来自 gateway 对下游 inference `/health` 的最小真实探测，而不是静态配置回显；如果探测失败，gateway 顶层 `status` 也会变成 `degraded`。

看代码：

- `projects/ai-gateway/src/ai_gateway/server.py`
- `projects/ai-gateway/src/ai_gateway/router.py`
- `projects/ai-gateway/src/ai_gateway/middleware/auth.py`

运行后可以顺手问自己：

- 正确 token 和错误 token 的响应差异是什么？
- `x-request-id` 是否按预期透传或生成？
- `x-cache`、`x-upstream-model`、`x-fallback-used` 分别说明什么？
- 如果 upstream 不健康，gateway health 如何变化？

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

运行后可以顺手问自己：

- result json 只是分数，还是包含样本和配置？
- compare 为什么需要 baseline 和 candidate？
- 如果 baseline 和 candidate 是同一个文件，报告还能说明什么？
- run history 是否能帮助你找到之前结果？

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

运行后可以顺手问自己：

- run manifest 记录了哪些训练来源？
- checkpoint index 和 export manifest 是什么关系？
- dataset registry 能否解释这次训练用的数据？
- export 产物未来如何进入 eval？

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

## 6.1 输出物怎么读

第一次看到这些输出物，很容易觉得它们太多。可以先按用途分类：

| 用途 | 代表输出 | 你要问的问题 |
| --- | --- | --- |
| 状态 | health、metrics | 服务是否可用，是否发生过请求 |
| 请求证据 | events、timeline、request id | 一次请求经过了哪些阶段 |
| 质量证据 | result、compare、leaderboard | 候选结果是否比基线更好 |
| 训练证据 | manifest、checkpoint index、export history | 产物能否追溯来源 |
| 发布证据 | evidence packet、public-check 输出 | 是否适合公开分享 |

先按用途读，再看具体字段，会轻松很多。

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

## 8. 常见运行失败的第一反应

遇到失败时，先不要把所有依赖删掉重装。建议按这个顺序排查：

1. 命令是否在正确目录运行。
2. 是否使用了 `.venv/bin/python`。
3. Node 是否是 22。
4. 端口是否被旧进程占用。
5. 服务是否已启动。
6. 请求 header 是否缺少 token 或 content type。
7. 错误是否能在 `/events` 或 `/events/failures` 找到。
8. 文档失败是否是链接、frontmatter 或构建问题。

如果能把失败定位到某一层，问题通常就已经解决了一半。
