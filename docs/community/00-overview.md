# 社区贡献路径

> 本页解决：公开后读者如何从学习者变成贡献者。
> 读完能做：选择合适的 issue，按证据标准提交 docs、lab、case、real-backend 或 observability PR。
> 关联代码：`CONTRIBUTING.md`、`.github/ISSUE_TEMPLATE`、`.github/PULL_REQUEST_TEMPLATE.md`、`Makefile`。
> 验证命令：`PYTHON=.venv/bin/python make docs-quality`。

这个项目的社区定位很清楚：它是 AI Infra 学习项目，不是生产平台。贡献者不需要一上来实现大而全的真实系统，更重要的是帮助读者更稳定地完成三件事：

1. 跑起来。
2. 看懂证据。
3. 把学习结果讲清楚。

## 从学习者到贡献者的四个阶段

| 阶段 | 你在做什么 | 适合的贡献 |
| --- | --- | --- |
| 跑通 | 完成 Quickstart，知道 request id、events、metrics 在哪里 | 安装问题、排障说明、平台差异补充 |
| 看懂 | 能解释一次请求、一次 eval、一次 export | 输出截图式说明、FAQ、术语解释 |
| 复盘 | 能把失败现象写成证据链 | case study、failure playbook、lab 验收标准 |
| 迁移 | 能区分 mock 边界和真实后端边界 | vLLM / SGLang / OTel / metrics 设计和小步实现 |

## 推荐第一步

第一次贡献建议从这些入口选一个：

- [15 分钟 Quickstart](/quickstart/15-minute-demo)：补环境差异、预期输出或失败排查。
- [Starter Issues](/08-publication/15-starter-issues)：选一个范围明确的公开首发任务。
- [First PR Playbook](/community/01-first-pr-playbook)：按改动类型选择验证命令和 PR 证据。
- [公开数据与证据规范](/community/02-safe-data-and-evidence)：确认输出、截图、toy data 和 manifest 可以公开。
- [输出证据库](/13-output-gallery/00-overview)：补更清楚的字段说明和复盘例子。
- [失败案例手册](/11-case-studies/06-failure-case-playbook)：把真实卡点整理成症状、证据、定位、修复。
- [生产迁移路线](/12-production-migration/00-overview)：补真实工具和当前学习边界的对照。

## 贡献类型

### Docs

适合：

- 概念解释不够清楚
- 命令预期输出不够明确
- 新手不知道下一步看什么
- 页面缺少关联代码入口或验证命令

验收：

```bash
PYTHON=.venv/bin/python make docs-quality
```

### Lab

适合：

- 能设计一个明确触发命令
- 能给出预期输出和失败排查
- 能把概念落到 request id、events、metrics、report 或 manifest

验收：

```bash
PYTHON=.venv/bin/python make docs-quality
PYTHON=.venv/bin/python make infra-smoke
```

### Real backend

适合：

- vLLM、SGLang、OpenAI-compatible backend 迁移设计
- backend config、model mapping、timeout、metrics、fallback 对齐
- 保留 mock 默认路径，新增可选真实路径

验收：

```bash
PYTHON=.venv/bin/python make infra-check
PYTHON=.venv/bin/python make infra-smoke
```

### Observability

适合：

- request id 规范
- OpenTelemetry GenAI mapping
- Prometheus metrics 对照
- events / logs / traces 如何互相解释

验收：

```bash
PYTHON=.venv/bin/python make docs-quality
PYTHON=.venv/bin/python make infra-check
```

### Eval

适合：

- regression gate
- release recommendation
- failed sample 聚类
- baseline / candidate 可比性

验收：

```bash
PYTHON=.venv/bin/python make scripts-test
PYTHON=.venv/bin/python make infra-check
```

## First PR checklist

更完整的步骤见 [First PR Playbook](/community/01-first-pr-playbook)。快速自查如下：

PR 前先自查：

- 改动是否保持“学习项目，不是生产平台”的定位
- 是否保留已有主线内容和路由
- 新增页面是否出现在 sidebar
- 是否包含本页解决什么、读完能做什么、关联代码入口、验证命令
- 是否没有提交 `.env`、token、私钥、个人路径、日志、模型权重或缓存
- docs-only 改动是否跑过 `make docs-quality`
- code 改动是否跑过 `make infra-check`
- 跨服务改动是否跑过 `make infra-smoke`
- 准备公开发布前是否跑过 `make public-check`

## Issue 评论模板

当你在 issue 里反馈学习卡点，可以直接使用：

````markdown
## 我在学哪一页

链接：

## 我执行的命令

```bash

```

## 我看到的输出或错误

```text

```

## 我已经检查过的证据

- request id:
- events:
- metrics:
- eval report:
- manifest:
- evidence packet:

## 我希望补充什么

````

如果是安全问题，不要贴密钥、token、真实用户数据或私有日志。请按 `SECURITY.md` 的方式报告。

如果要提交输出证据、截图、toy data 或 manifest，先按 [公开数据与证据规范](/community/02-safe-data-and-evidence) 逐项脱敏。

## 维护者如何处理贡献

维护者 review 时优先看：

1. 是否降低了新手跑通成本。
2. 是否让证据链更清楚。
3. 是否保持接口、文档、验证命令一致。
4. 是否避免把学习项目包装成生产平台。
5. 是否有下一步可以拆成 issue。

## 继续阅读

- [贡献指南](https://github.com/wdkang123/ai-infra-handbook/blob/main/CONTRIBUTING.md)
- [Starter Issues](/08-publication/15-starter-issues)
- [First PR Playbook](/community/01-first-pr-playbook)
- [公开数据与证据规范](/community/02-safe-data-and-evidence)
- [维护者 Triage 节奏](/community/03-triage-and-maintainer-rhythm)
- [GitHub 入口与协作地图](/08-publication/14-github-entrypoints)
- [公开发布总览](/08-publication/00-overview)
- [验证矩阵](/09-reference/07-validation-matrix)
