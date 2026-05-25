# 概念到代码索引

这页帮你从概念快速跳到对应代码。

它和 [文档与代码怎么对应](/00-overview/05-docs-to-code-map) 的区别是：  
这里更像索引，适合查找。

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
