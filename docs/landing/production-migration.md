# Production Migration

> 本页解决：学习型 AI Infra 项目如何逐步接近真实工程，而不牺牲可运行和可复盘。
> 读完能做：为 vLLM、SGLang、OpenTelemetry、Prometheus、Eval gate 迁移排优先级。
> 关联代码：`projects/`、`scripts/integration_smoke_test.sh`、`scripts/build_evidence_packet.py`。
> 验证命令：`PYTHON=.venv/bin/python make infra-smoke`。

Production Migration 在本项目里不是“马上上生产”，而是：

1. 保留接口。
2. 保留观测。
3. 保留证据。
4. 小步替换内部实现。

## 迁移顺序

| 阶段 | 目标 |
| --- | --- |
| vLLM adapter | 把 mock serving 替换为真实 OpenAI-compatible backend |
| Prometheus metrics | 对齐 gateway、adapter、runtime 三层指标 |
| OpenTelemetry GenAI | 把 request id / events 迁移到 tracing 思路 |
| SGLang 对比 | 引入结构化生成和 agentic workload 对比 |
| Eval release gate | 把 pass / warn / block 接入发布流程 |

## 推荐路径

1. [生产迁移路线总览](/12-production-migration/00-overview)
2. [vLLM Adapter 设计](/12-production-migration/05-vllm-adapter-design)
3. [OpenTelemetry GenAI Tracing 设计](/12-production-migration/06-opentelemetry-genai-tracing)
4. [Prometheus Metrics 对照表](/12-production-migration/07-prometheus-metrics-map)
5. [SGLang 迁移对比](/12-production-migration/08-sglang-migration-notes)

## 迁移底线

每次迁移至少要回答：

- `/v1/chat/completions` 是否仍然稳定
- `/v1/models` 是否仍然可解释
- request id 是否贯穿
- events 和 metrics 是否仍然能复盘
- eval report 是否能判断质量变化
- manifest 是否能追溯训练资产
- evidence packet 是否能汇总公开证据

## FAQ

### 为什么不直接接真实 GPU serving

因为公开学习项目要先保证 clone 后可运行。真实 backend 应该是可选路径。

### mock 以后会删除吗

不建议删除。mock 是教学路径和测试替身，真实后端是迁移路径。

### 什么时候才算迁移成功

不是新工具跑起来就成功，而是接口、观测、证据、测试、文档和失败案例都能解释新路径。
