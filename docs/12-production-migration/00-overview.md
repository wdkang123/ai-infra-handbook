# 生产迁移路线总览

> 本页解决：学习型实现如何逐步接近真实工程，而不牺牲可运行、可验证和可复盘。
> 读完能做：为 vLLM、Gateway 加固、Eval gate、真实训练和跨层发布闭环排出迁移顺序。
> 关联代码：`projects/`、`scripts/integration_smoke_test.sh`、`scripts/build_evidence_packet.py`。
> 验证命令：`PYTHON=.venv/bin/python make infra-smoke`。

这一章回答一个进阶问题：

> 当前项目是学习型实现，如果想把它逐步改得更接近真实工程，应该按什么顺序推进？

这里不会把仓库包装成生产平台。相反，它会明确区分：

- 哪些结构应该保留
- 哪些实现可以替换
- 哪些能力必须等边界稳定后再加
- 每一步应该怎么验证
- 迁移后如何继续公开分享和维护

学习型项目最怕两种极端：一种是永远停在 toy demo，另一种是一口气堆成读者跑不起来的重系统。本章的目标，是给出一条中间路线：让项目越来越真实，但不牺牲可学习、可运行、可复盘。

![生产迁移路线示意图](/images/articles/production-migration-overview.jpg)

*图：生产迁移不是推倒重写，而是在保留接口、观测和证据边界的前提下逐步替换内部实现。*

## 迁移不是重写

生产迁移不等于把当前项目推倒重来。

当前仓库最有价值的不是 mock 细节，而是已经形成的边界：

- `inference-service` 暴露模型服务契约
- `ai-gateway` 承担平台治理入口
- `eval-module` 把结果变成可比较对象
- `finetune-demo` 把训练变成可复盘资产
- docs / tests / outputs 把学习证据保留下来

迁移时应该优先保住这些边界，再逐步替换内部执行。

如果迁移后工具更真实了，但接口变乱了、证据丢了、测试跑不通了，那不是升级，而是把学习系统变成黑箱。

## 核心原则

### 1. 先保接口，再替内部

对外接口是系统协作的锚点。

迁移时要尽量保住：

- OpenAI-compatible 风格入口
- `/v1/models`
- `/health`
- `/metrics`
- `/events`
- request id
- CLI 命令形状
- manifest / history / index 文件
- 验证命令

内部可以从 mock engine 换成 vLLM，可以从学习型 gateway 变成更完整策略引擎，可以从 mock trainer 换成 PEFT/Unsloth，但外部学习契约不应该轻易破坏。

### 2. 先保观测，再扩大复杂度

每次变真实，至少要保住：

- request id
- health
- metrics
- structured events
- manifest / index
- 示例输出和复盘证据
- smoke 验证
- 文档说明

复杂系统不可怕，不可观察的复杂系统才可怕。

### 3. 先单点迁移，再跨层联动

不要一口气同时替换 serving、gateway、eval 和 training。

更稳的顺序是：

1. 替换 inference 后端
2. 强化 gateway 策略
3. 扩展 eval 判断
4. 接入真实训练
5. 再做跨层发布流程

这样每一步都有清楚的验证边界。

### 4. 先保学习体验，再追求生产复杂度

这个项目要公开分享，所以迁移后仍然要能被读者理解。

每次引入新工具，都应该补：

- 为什么需要它
- 它替换了哪一层
- 新增了哪些依赖
- 本地如何最小运行
- 没有 GPU 或外部服务时如何阅读
- 验证命令是什么
- 失败时怎么排查

如果只接工具不补学习路径，网站会变成配置碎片。

## 迁移路线图

### 阶段一：Serving 后端更真实

目标：把 `inference-service` 内部执行从 mock 逐步迁移到真实 serving runtime。

候选方向：

- OpenAI-compatible upstream
- vLLM
- SGLang
- Triton Inference Server
- TensorRT-LLM

优先保留：

- `/v1/chat/completions`
- `/v1/models`
- streaming 行为
- metrics
- events
- request timeline
- 错误映射

对应章节：

- [Serving 后端迁移](/12-production-migration/01-serving-backend-migration)
- [从学习型服务到真实 Serving Stack](/02-inference-serving/10-from-learning-service-to-real-serving-stack)
- [vLLM Adapter 设计](/12-production-migration/05-vllm-adapter-design)
- [SGLang 迁移对比](/12-production-migration/08-sglang-migration-notes)

### 阶段二：Gateway 平台化加固

目标：让 `ai-gateway` 从最小代理层向更真实的平台治理层演进。

候选方向：

- 更细粒度 token / tenant / project 管理
- 更真实 rate limit
- 路由策略配置化
- fallback 策略分层
- cache 隔离和失效策略
- usage / cost 统计
- audit log
- upstream pool

优先保留：

- 外部模型名到内部目标映射
- request id
- cache/fallback headers
- upstream health
- failure summary
- structured events

对应章节：

- [Gateway 平台化加固](/12-production-migration/02-gateway-platform-hardening)
- [从 Demo Gateway 到真实平台](/03-ai-gateway-platform/07-from-demo-gateway-to-real-platform)

### 阶段三：Eval 进入发布门禁

目标：让 `eval-module` 从最小评测脚手架走向更真实的质量判断系统。

候选方向：

- 更丰富 task 集合
- judge prompt versioning
- sample-level review
- regression gate
- dashboard
- run bundle archive
- baseline/candidate promotion
- production feedback sampling

优先保留：

- run
- compare
- history
- leaderboard
- sample analysis
- recommendation
- 评测配置可追溯

对应章节：

- [Eval 评测系统迁移](/12-production-migration/03-eval-judge-dashboard-migration)
- [从 Run 到发布决策](/04-evaluation-observability/07-from-run-to-release-decision)
- [Eval Regression Gate 示例](/04-evaluation-observability/09-eval-regression-gate-example)

### 阶段四：Finetune 接真实训练

目标：让 `finetune-demo` 从资产骨架逐步接入真实训练执行。

候选方向：

- PEFT
- TRL
- Unsloth
- Transformers Trainer
- experiment tracking
- artifact store
- resume
- 自动 eval handoff

优先保留：

- dataset registry
- run manifest
- checkpoint index
- export manifest
- history
- dataset diff
- export lineage

对应章节：

- [Finetune 真实训练迁移](/12-production-migration/04-finetune-real-training-migration)
- [从 Demo Training 到真实训练系统](/05-finetuning-training/08-from-demo-training-to-real-training-system)

### 阶段五：跨层发布闭环

目标：把 serving、gateway、eval、training 串成更完整的发布流程。

典型链路：

```text
Train or prompt/model change
  -> Export or config candidate
  -> Eval run
  -> Compare report
  -> Gateway route or serving target update
  -> Smoke and public evidence
  -> Release notes
```

这一阶段不只是加功能，而是把“变更能否发布”变成流程。

## 迁移章节

- [Serving 后端迁移](/12-production-migration/01-serving-backend-migration)
- [Gateway 平台化加固](/12-production-migration/02-gateway-platform-hardening)
- [Eval 评测系统迁移](/12-production-migration/03-eval-judge-dashboard-migration)
- [Finetune 真实训练迁移](/12-production-migration/04-finetune-real-training-migration)
- [vLLM Adapter 设计](/12-production-migration/05-vllm-adapter-design)
- [OpenTelemetry GenAI Tracing 设计](/12-production-migration/06-opentelemetry-genai-tracing)
- [Prometheus Metrics 对照表](/12-production-migration/07-prometheus-metrics-map)
- [SGLang 迁移对比](/12-production-migration/08-sglang-migration-notes)

## 一张迁移地图

```text
学习型系统
  -> 保留接口和观测
  -> 替换 inference 执行后端
  -> 增强 gateway 路由、配额、追踪
  -> 扩展 eval judge、dashboard、发布门禁
  -> 接入真实 trainer、checkpoint、resume
  -> 串起训练、评测、发布和回滚
  -> 用 smoke / case studies / validation matrix 收住风险
```

## 每次迁移都要回答的问题

| 问题 | 为什么重要 |
| --- | --- |
| 哪个接口不能变 | 避免上游调用方和文档全部失效 |
| 哪个产物必须保留 | 避免后续无法复盘 |
| 哪个指标会变化 | 避免性能或质量变化不可见 |
| 哪些输出证据要更新 | 避免读者不知道新实现是否跑对 |
| 哪个失败路径会新增 | 避免迁移后只会看 happy path |
| 哪条测试或 smoke 要扩展 | 避免靠人工感觉判断 |
| 哪个文档要同步更新 | 避免公开网站和代码脱节 |
| 新依赖是否会影响本地运行 | 避免读者 clone 后跑不起来 |

## 推荐验收命令

迁移类改动至少跑：

```bash
PYTHON=.venv/bin/python make infra-format
PYTHON=.venv/bin/python make infra-check
PYTHON=.venv/bin/python make infra-smoke
```

如果只改文档或迁移说明，先跑：

```bash
PYTHON=.venv/bin/python make docs-quality
```

公开发布前再跑：

```bash
PYTHON=.venv/bin/python make public-check
```

更细的选择见 [验证矩阵](/09-reference/07-validation-matrix)。

迁移完成后，也应该同步更新 [示例输出与证据库](/13-output-gallery/00-overview)，确保读者看到的是新实现下的证据口径。

## 如何判断迁移是成功的

一次迁移成功，不只是“新工具跑起来了”。它还应该满足：

- 读者能看懂为什么迁移
- 本地仍有可运行路径
- 文档和代码边界一致
- 关键输出证据更新
- 测试或 smoke 覆盖新增路径
- 失败时有明确排查入口
- 公开仓库没有引入密钥、个人路径或危险文件
- GitHub Pages 能正常发布

这就是本项目“公网级别分享”的迁移标准。

## 常见误区

### 误区一：迁移生产化就是把 mock 全删掉

不一定。可以保留 mock 作为教学路径和测试替身，同时增加真实后端选项。

### 误区二：真实依赖越多，项目越专业

依赖越多，运行门槛越高。公开学习站要平衡真实感和可达性。

### 误区三：先接工具，后补文档

这样最容易让网站变薄。每次迁移都应该同步补学习路径、边界说明和验证命令。

### 误区四：只要 CI 过了就可以发布

CI 是底线。公开发布还要看安全扫描、文档入口、输出证据、release notes 和读者体验。

### 误区五：四个项目可以各自独立生产化

可以分别演进，但最终要回到跨层闭环。Serving、gateway、eval、training 分开学习，合起来才是 AI Infra。
