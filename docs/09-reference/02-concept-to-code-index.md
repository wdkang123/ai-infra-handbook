# 概念到代码索引

这页帮你从概念快速跳到对应代码。

它和 [文档与代码怎么对应](/00-overview/05-docs-to-code-map) 的区别是：  
这里更像索引，适合查找。

## 怎么使用这页

如果你刚读完一页文档，不知道该看哪个文件，可以这样走：

1. 找到对应概念。
2. 先打开代码入口文件，不要全项目搜索。
3. 再打开测试文件，看行为怎么被验证。
4. 最后回到输出证据页，看运行后应该留下什么。

这个索引不是让你记路径，而是让你把“概念、实现、测试、证据”连起来。

推荐阅读动作：

```text
概念页
  -> 本页找代码入口
  -> 测试文件看行为边界
  -> Lab 跑命令
  -> 输出证据页做复盘
```

## 请求入口

概念：

- chat completion
- 普通响应
- streaming 响应
- 请求模型校验
- `/v1/models` 模型列表

代码：

- `projects/inference-service/src/inference_service/server.py`
- `projects/ai-gateway/src/ai_gateway/server.py`

测试：

- `projects/inference-service/tests/test_api.py`
- `projects/ai-gateway/tests/test_proxy.py`

相关页面：

- [从请求到首个 Token](/01-llm-fundamentals/04-from-request-to-first-token)
- [Serving 可观测性 Lab](/07-hands-on-labs/01-serving-observability-lab)

验证动作：

```bash
PYTHON=.venv/bin/python make infra-check
PYTHON=.venv/bin/python make infra-smoke
```

## 模型发现

概念：

- inference-service 暴露本服务当前模型
- ai-gateway 暴露平台模型名
- target model
- fallback metadata
- upstream health

代码：

- `projects/inference-service/src/inference_service/server.py`
- `projects/ai-gateway/src/ai_gateway/server.py`
- `projects/ai-gateway/configs/models.yaml`

测试：

- `projects/inference-service/tests/test_api.py`
- `projects/ai-gateway/tests/test_proxy.py`

相关页面：

- [inference-service](/06-projects/01-inference-service)
- [ai-gateway](/06-projects/02-ai-gateway)

验证动作：

```bash
curl -s http://localhost:8000/v1/models
curl -s http://localhost:8080/v1/models
```

## Engine Adapter

概念：

- mock engine
- OpenAI-compatible adapter
- vLLM/SGLang 接入边界
- 上游错误映射

代码：

- `projects/inference-service/src/inference_service/engines.py`
- `projects/inference-service/src/inference_service/config.py`
- `projects/inference-service/src/inference_service/main.py`

相关页面：

- [inference-service](/06-projects/01-inference-service)
- [从学习型服务到真实 Serving Stack](/02-inference-serving/10-from-learning-service-to-real-serving-stack)

## Metrics

概念：

- 请求总数
- 成功/失败请求
- running requests
- token counters
- prompt/completion token boundary
- gateway upstream failures
- gateway fallback attempts/successes
- cache hits/misses
- `x-cache` response header
- `x-upstream-model` / `x-fallback-used` response header
- inference `/events` structured events
- `/events` structured events
- event filters by type/request/model
- event summary counts
- gateway failure summary
- request event timeline

代码：

- `projects/inference-service/src/inference_service/runtime.py`
- `projects/inference-service/src/inference_service/server.py`
- `projects/inference-service/src/inference_service/api/metrics.py`
- `projects/ai-gateway/src/ai_gateway/runtime.py`
- `projects/ai-gateway/src/ai_gateway/server.py`

相关页面：

- [健康检查、Metrics、Request ID](/03-ai-gateway-platform/02-health-metrics-request-id)
- [Tracing、Metrics、Logs](/04-evaluation-observability/03-observability-traces-metrics-logs)

## 鉴权

概念：

- Bearer token
- 入口身份校验
- auth failure metrics

代码：

- `projects/ai-gateway/src/ai_gateway/middleware/auth.py`
- `projects/ai-gateway/src/ai_gateway/server.py`

测试：

- `projects/ai-gateway/tests/test_proxy.py`

相关页面：

- [鉴权、路由、限流](/03-ai-gateway-platform/01-auth-routing-rate-limit)

典型证据：

- HTTP `401`
- `auth_failed` event
- gateway metrics

## 路由与模型名映射

概念：

- 外部模型名
- 内部 target model
- route candidates
- fallback chain

代码：

- `projects/ai-gateway/src/ai_gateway/router.py`
- `projects/ai-gateway/src/ai_gateway/config.py`
- `projects/ai-gateway/configs/models.yaml`

相关页面：

- [外部模型名与内部目标映射](/03-ai-gateway-platform/06-model-name-to-target-mapping)

## Fallback

概念：

- 主下游失败
- 备用模型
- 非流式 fallback
- 首 chunk 前 streaming fallback
- fallback headers
- fallback metrics
- fallback events

代码：

- `projects/ai-gateway/src/ai_gateway/server.py`
- `projects/ai-gateway/src/ai_gateway/router.py`

测试：

- `projects/ai-gateway/tests/test_proxy.py`

相关页面：

- [Gateway、Router、Fallback、Cache](/03-ai-gateway-platform/03-gateway-router-fallback-cache)
- [Gateway 韧性 Lab](/07-hands-on-labs/02-gateway-resilience-lab)

## Response Cache

概念：

- 非流式响应缓存
- TTL
- max entries
- token 隔离

代码：

- `projects/ai-gateway/src/ai_gateway/runtime.py`
- `projects/ai-gateway/src/ai_gateway/server.py`

相关页面：

- [Cache 与 Prefix Caching](/02-inference-serving/06-cache-prefix-caching)
- [Gateway 韧性 Lab](/07-hands-on-labs/02-gateway-resilience-lab)

典型证据：

- `x-cache: BYPASS / MISS / HIT`
- cache hit/miss metrics
- request timeline

## Eval Run / Compare / Leaderboard

概念：

- run
- compare
- min_delta
- release recommendation
- sample-level output
- sample summary
- sample analysis
- judge reason
- run index
- run index task summaries
- comparison index
- comparison verdict/recommendation counts
- comparison task summaries
- leaderboard
- backend/few-shot leaderboard groups
- backend/few-shot run filters
- best/latest result file
- task 一致性
- history
- bundle

代码：

- `projects/eval-module/src/eval_module/main.py`
- `projects/eval-module/src/eval_module/results/result_store.py`
- `projects/eval-module/src/eval_module/runners/lm_eval_runner.py`

相关页面：

- [Run、Compare、History](/04-evaluation-observability/01-run-compare-history)
- [Eval 发布门禁 Lab](/07-hands-on-labs/03-eval-release-gate-lab)

## Finetune Artifacts

概念：

- dataset validation
- dataset registry
- dataset registry report
- dataset registry diff
- method/model registry filters
- duplicate registration count
- dataset version
- dataset role stats
- run manifest
- artifacts manifest
- checkpoint
- checkpoint index
- export manifest
- export history
- run index
- export index
- run manifest pointer
- export status/duration
- export model/dataset summaries
- export manifest pointer
- checkpoint index pointer
- export lineage
- trainer state lineage
- sha256

代码：

- `projects/finetune-demo/src/finetune_demo/trainer/lora_trainer.py`
- `projects/finetune-demo/src/finetune_demo/dataset_registry.py`
- `projects/finetune-demo/src/finetune_demo/run_history.py`
- `projects/finetune-demo/src/finetune_demo/artifacts.py`
- `projects/finetune-demo/src/finetune_demo/main.py`
- `projects/finetune-demo/src/finetune_demo/export/adapter_exporter.py`

相关页面：

- [训练产物、Checkpoint、Export](/05-finetuning-training/02-run-artifacts-export)
- [Finetune 复现资产 Lab](/07-hands-on-labs/04-finetune-reproducibility-lab)

## Smoke

概念：

- 最小联调
- 服务启动
- gateway/inference/eval/finetune 闭环

代码：

- `scripts/integration_smoke_test.sh`
- `Makefile`

相关页面：

- [质量与维护入口](/06-projects/07-quality-and-maintenance)
- [系统 Capstone 与验收 Rubric](/07-hands-on-labs/05-capstone-review-rubric)

## 文档质量与导航

概念：

- Markdown 本地链接
- heading anchor
- VitePress nav/sidebar
- 首页入口
- 首页组件链接
- README 到站点入口

代码：

- `scripts/check_docs_quality.py`
- `docs/.vitepress/config.mts`
- `docs/index.md`
- `docs/.vitepress/theme/components/HomeCourseMatrix.vue`

命令：

```bash
PYTHON=.venv/bin/python make docs-quality
npm run docs:build
```

相关页面：

- [GitHub Pages 发布指南](/08-publication/01-github-pages)
- [公开仓库卫生规范](/08-publication/06-public-repo-hygiene)

## 公开安全检查

概念：

- high-confidence secrets
- private key block
- connection string
- local path
- risky public file types
- personal markers

代码：

- `scripts/security_scan.py`
- `scripts/tests/test_security_scan.py`
- 根级 `Makefile`

命令：

```bash
PYTHON=.venv/bin/python make security-check
PYTHON=.venv/bin/python make public-check
```

相关页面：

- [公开仓库卫生规范](/08-publication/06-public-repo-hygiene)

## 自动生成课程/发布产物

概念：

- learning inventory
- course catalog
- evidence packet
- release brief
- workshop packet
- assessment pack
- roadmap pack
- launch pack

代码：

- `scripts/build_learning_inventory.py`
- `scripts/build_course_catalog.py`
- `scripts/build_evidence_packet.py`
- `scripts/build_release_brief.py`
- `scripts/build_workshop_packet.py`
- `scripts/build_assessment_pack.py`
- `scripts/build_roadmap_pack.py`
- `scripts/build_launch_pack.py`

测试：

- `scripts/tests/test_build_learning_inventory.py`
- `scripts/tests/test_build_course_catalog.py`
- `scripts/tests/test_build_evidence_packet.py`
- `scripts/tests/test_build_release_brief.py`
- `scripts/tests/test_build_workshop_packet.py`
- `scripts/tests/test_build_assessment_pack.py`
- `scripts/tests/test_build_roadmap_pack.py`
- `scripts/tests/test_build_launch_pack.py`

命令：

```bash
PYTHON=.venv/bin/python make docs-inventory
PYTHON=.venv/bin/python make course-catalog
PYTHON=.venv/bin/python make release-brief
PYTHON=.venv/bin/python make workshop-packet
PYTHON=.venv/bin/python make launch-pack
```

相关页面：

- [学习站清单生成器](/09-reference/08-learning-inventory)
- [课程目录生成器](/09-reference/10-course-catalog)
- [发布摘要生成器](/09-reference/09-release-brief)
- [自动生成共学包](/14-workshop-kit/07-generated-workshop-packet)
- [自动生成首发运营包](/08-publication/13-generated-launch-pack)

## 查代码时的经验

优先顺序：

1. 先看项目页给出的入口。
2. 再看 tests，因为 tests 会告诉你行为边界。
3. 再用 `rg` 搜函数名、header 名、event type。
4. 最后才做大范围源码阅读。

常用搜索例子：

```bash
rg "x-request-id" projects
rg "fallback" projects/ai-gateway
rg "release_recommendation" projects/eval-module scripts
rg "checkpoint_index" projects/finetune-demo docs
```

不要只搜概念词。更稳的是搜实际出现在代码或输出里的字段名。
