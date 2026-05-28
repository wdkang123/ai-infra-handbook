# v0.1.0 Release Notes

> 本页解决：公开首发时如何说明项目价值、验证命令、学习边界和下一阶段路线。
> 读完能做：把这份说明整理成 GitHub Release、README 摘要或公开分享开场。
> 关联代码：`Makefile`、`scripts/build_launch_pack.py`、`scripts/build_release_brief.py`、`scripts/build_evidence_packet.py`。
> 验证命令：`PYTHON=.venv/bin/python make public-check`。

## Release title

`v0.1.0 - Public Learning Launch`

## 一句话说明

AI Infra Handbook v0.1.0 是面向后端、平台和 AI 应用开发者的公开学习首发版：它把 AI Infra 概念、四个可运行项目、hands-on labs、输出证据、案例复盘和 GitHub 贡献入口串成一条可验证学习路径。

## 适合放在 GitHub Release 顶部的英文摘要

AI Infra Handbook v0.1.0 is the first public learning release. It is a learning project, not a production platform. The release helps backend, platform, and AI application developers understand AI Infra through runnable code, structured docs, hands-on labs, and evidence-driven review.

## 本次包含什么

| 模块 | 内容 | 读者能获得什么 |
| --- | --- | --- |
| Quickstart | `make quickstart`、手动请求、request id、events、metrics、evidence packet | 15 分钟内看到端到端链路 |
| Inference | `/v1/chat/completions`、`/v1/models`、streaming、mock token usage、metrics | 理解模型服务对外契约 |
| Gateway | auth、routing、fallback、cache、upstream health、failure summary | 理解平台治理边界 |
| Eval | run、compare、leaderboard、sample analysis、release recommendation | 理解质量如何进入发布判断 |
| Finetune | dataset registry、run manifest、checkpoint index、export manifest、lineage | 理解训练资产如何复现 |
| Public growth | release notes、starter issues、community path、landing pages、llms.txt | 让项目更适合公开传播和贡献 |
| Migration anchors | vLLM、SGLang、OpenTelemetry GenAI、Prometheus metrics、eval regression gate | 为真实 AI Infra 演进留接口 |

## 验证命令

首发前建议至少执行：

```bash
PYTHON=.venv/bin/python make docs-quality
PYTHON=.venv/bin/python make infra-check
PYTHON=.venv/bin/python make infra-smoke
PYTHON=.venv/bin/python make public-check
```

如果要生成公开运营材料，再执行：

```bash
PYTHON=.venv/bin/python make release-brief
PYTHON=.venv/bin/python make roadmap-pack
PYTHON=.venv/bin/python make launch-pack
```

## 发布边界

这不是生产平台，不能直接承诺：

- 承载真实生产流量
- 提供 GPU serving SLA
- 直接替代组织内的 API Gateway
- 直接接入真实密钥、真实用户数据或生产日志
- 覆盖完整模型安全、计费、审计、灰度、回滚和合规流程

它当前承诺的是学习价值：

- 能跑通最小 AI Infra 链路
- 能用证据解释请求、评测、训练和发布判断
- 能把 mock 后端逐步迁移到真实后端
- 能让读者通过 issue 和 PR 继续贡献

## 推荐 release body

```markdown
## AI Infra Handbook v0.1.0

这是第一版公开学习发布。项目定位是 AI Infra 工程学习手册，不是生产平台。

### Highlights

- 15 分钟 Quickstart：`make quickstart`
- 四个可运行学习项目：`inference-service`、`ai-gateway`、`eval-module`、`finetune-demo`
- request id、events、metrics、eval report、manifest 和 evidence packet 证据链
- Labs、案例复盘、输出证据库、共学套件和学习自测
- vLLM、SGLang、OpenTelemetry GenAI、Prometheus metrics 和 Eval release gate 迁移路线

### Validation

- `PYTHON=.venv/bin/python make docs-quality`
- `PYTHON=.venv/bin/python make infra-check`
- `PYTHON=.venv/bin/python make infra-smoke`
- `PYTHON=.venv/bin/python make public-check`

### Known boundaries

- 当前默认实现仍是学习型 mock / local scaffold
- 不建议接入真实密钥、真实用户数据或生产流量
- 后续将优先推进真实 serving adapter、观测标准映射、metrics dashboard 和 eval release gate
```

## 发布后 24 小时检查

| 检查项 | 看什么 |
| --- | --- |
| GitHub Pages | 首页、Quickstart、Release、Starter Issues、Community、Migration 页面是否可访问 |
| README | 英文摘要、项目定位、Quickstart 和贡献入口是否清楚 |
| Issues | 首批 issue 是否有 label、验收标准和验证命令 |
| Security | 是否误提交 `.env`、token、个人路径、日志、模型权重或缓存 |
| Feedback | 读者最先卡在哪里，是否集中在安装、端口、命令或术语 |

## 下一阶段路线

1. 把 vLLM adapter 从设计页推进到可选实现。
2. 给 gateway / inference 增加 OpenTelemetry GenAI tracing 的版本化映射。
3. 把当前 Prometheus-style metrics 和 vLLM metrics 对齐到可观察清单。
4. 把 eval regression gate 从示例推进到 release brief 的强约束。
5. 把 starter issue 转成 GitHub issue，并按社区反馈滚动维护。
