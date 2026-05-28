# Starter Issues

> 本页解决：公开首发后应该先创建哪些低噪音、可验收、适合贡献的 issue。
> 读完能做：把 20 个任务复制到 GitHub Issues，并为每个任务补充 label、验收标准和验证命令。
> 关联代码：`scripts/build_roadmap_pack.py`、`scripts/build_launch_pack.py`、`.github/ISSUE_TEMPLATE`。
> 验证命令：`PYTHON=.venv/bin/python make roadmap-pack`。

这些 starter issues 的目标不是把仓库一次性推成生产平台，而是把公开读者的反馈入口整理清楚：哪里可以补文档，哪里可以做 lab，哪里可以接真实后端，哪里适合 good first issue。

## 使用方式

每个 issue 建议包含：

- 背景：为什么这个任务对学习者有价值
- 范围：本次只做什么，不做什么
- 验收标准：PR 合并前必须看到什么
- 验证命令：贡献者应该跑什么
- 推荐 label：优先使用已有 label，必要时再新建

## 20 个 starter issue

### 01. docs: 给 Quickstart 增加 Windows / WSL 跑通记录

Labels: `docs`, `good-first-issue`

背景：当前 Quickstart 以通用命令为主，公开后很多学习者会在 Windows / WSL 上尝试。

范围：

- 补充 Windows / WSL 环境差异说明
- 不改 Python 服务逻辑
- 不新增平台专属依赖

验收标准：

- Quickstart 有 Windows / WSL 注意事项
- 包含常见端口、venv、Node 版本问题
- `make docs-quality` 通过

验证命令：

```bash
PYTHON=.venv/bin/python make docs-quality
```

### 02. docs: 给 request id 排查路径增加截图式输出说明

Labels: `docs`, `observability`, `good-first-issue`

背景：新手通常不知道 events timeline 里哪些字段最重要。

范围：

- 补一组示例输出片段
- 标注 `request_received`、`upstream_attempt`、`request_success`
- 不改变 API 返回结构

验收标准：

- 文档能解释 request id 如何串联 gateway 和 inference
- 链接到输出证据库
- `make docs-quality` 通过

验证命令：

```bash
PYTHON=.venv/bin/python make docs-quality
```

### 03. lab: 增加 Gateway timeout 复现实验

Labels: `lab`, `gateway`, `observability`

背景：timeout 是 AI Gateway 最常见的上游失败之一，适合做成可复现 lab。

范围：

- 设计触发命令和观察路径
- 说明 status、events、failure summary、metrics 的证据关系
- 不要求真实 upstream 故障注入框架

验收标准：

- lab 包含症状、命令、预期输出、修复方式
- 链接失败案例页
- `make docs-quality` 通过

验证命令：

```bash
PYTHON=.venv/bin/python make docs-quality
```

### 04. lab: 把 eval regression gate 变成独立练习

Labels: `lab`, `eval`

背景：读者需要练习如何从 compare report 得出 pass / warn / block。

范围：

- 以当前 eval-module 输出为基础
- 增加 baseline / candidate 对比任务说明
- 不接入外部 benchmark

验收标准：

- lab 有阈值、样本证据、release recommendation
- 包含 pass / warn / block 判断
- `make docs-quality` 通过

验证命令：

```bash
PYTHON=.venv/bin/python make docs-quality
```

### 05. real-backend: 设计 vLLM adapter 配置样例

Labels: `real-backend`, `serving`, `good-first-issue`

背景：真实后端迁移需要先固定配置入口，避免硬编码。

范围：

- 提议 `INFERENCE_BACKEND=mock|openai-compatible|vllm`
- 说明 backend URL、model mapping、timeout、metrics endpoint
- 不要求实现真实 GPU serving

验收标准：

- 设计页和代码入口对齐
- 保留 mock 默认路径
- `make docs-quality` 通过

验证命令：

```bash
PYTHON=.venv/bin/python make docs-quality
```

### 06. real-backend: 增加 vLLM /v1/models 对齐检查

Labels: `real-backend`, `serving`

背景：Gateway 的 model mapping 依赖模型列表契约，迁移真实后端时必须先对齐。

范围：

- 描述 vLLM `/v1/models` 和当前 mock `/v1/models` 的字段关系
- 提出最小 adapter contract
- 不改生产部署

验收标准：

- 有字段对照表
- 有失败时 fallback 策略说明
- `make docs-quality` 通过

验证命令：

```bash
PYTHON=.venv/bin/python make docs-quality
```

### 07. observability: 增加 OpenTelemetry GenAI version mapping 表

Labels: `observability`, `real-backend`

背景：GenAI semantic conventions 仍可能变化，项目需要版本化映射表。

范围：

- 增加当前字段到 OTel 字段的映射
- 标注 spec version 和验证日期
- 不强行引入 tracing SDK

验收标准：

- 映射覆盖 request id、model span、token usage、latency、error、tool call
- 文档提醒 Development 状态风险
- `make docs-quality` 通过

验证命令：

```bash
PYTHON=.venv/bin/python make docs-quality
```

### 08. observability: 增加 Prometheus metrics 示例查询

Labels: `observability`, `docs`

背景：读者看到 metrics 文本后，还需要知道该观察什么。

范围：

- 增加 PromQL 风格示例
- 覆盖请求数、错误率、fallback、token、latency
- 不要求接入真实 Prometheus

验收标准：

- 每个查询都有学习解释
- 链接 metrics 对照表
- `make docs-quality` 通过

验证命令：

```bash
PYTHON=.venv/bin/python make docs-quality
```

### 09. eval: 把 release gate 接入 CI release check 草案

Labels: `eval`, `publication`, `ci`

背景：当前 release brief 已经能输出 pass / warn / block，下一步可以设计一个轻量 release check，让发布 PR 更早看到风险。

范围：

- 设计 CI 里如何读取 release brief JSON
- 说明 warn 和 block 在 PR、release、手动发布中的处理差异
- 不要求马上阻断所有普通 PR

验收标准：

- 有 CI 草案和失败消息示例
- 保留学习项目默认可运行路径
- `make docs-quality` 通过

验证命令：

```bash
PYTHON=.venv/bin/python make docs-quality
```

### 10. eval: 增加 failed sample 聚类说明

Labels: `eval`, `docs`

背景：平均分之外，失败样本聚类更接近真实发布判断。

范围：

- 在 eval 章节补 failed sample 聚类阅读方法
- 不实现新算法
- 链接失败案例

验收标准：

- 有样本证据表
- 有何时 block 的判断规则
- `make docs-quality` 通过

验证命令：

```bash
PYTHON=.venv/bin/python make docs-quality
```

### 11. gateway: 增加 fallback used header 的端到端说明

Labels: `gateway`, `observability`, `good-first-issue`

背景：`x-fallback-used` 是读者理解平台风险的关键入口。

范围：

- 说明 header、events、metrics 三者关系
- 不改 fallback 策略
- 给出一个复盘模板

验收标准：

- 文档能解释成功响应背后的 fallback 风险
- 链接 Gateway 失败案例
- `make docs-quality` 通过

验证命令：

```bash
PYTHON=.venv/bin/python make docs-quality
```

### 12. gateway: 设计 tenant / token 最小配额模型

Labels: `gateway`, `real-backend`

背景：真实 Gateway 需要从单 token 示例演进到更真实的调用方治理。

范围：

- 只做设计，不实现生产配额系统
- 说明 token、tenant、project、model scope
- 保留学习项目默认 token

验收标准：

- 有配置样例和迁移风险
- 说明对 events / metrics 的影响
- `make docs-quality` 通过

验证命令：

```bash
PYTHON=.venv/bin/python make docs-quality
```

### 13. finetune: 增加 export manifest lineage mismatch lab

Labels: `finetune`, `lab`

背景：训练资产如果 lineage 不一致，不应该进入 eval 和 release。

范围：

- 设计一个人为构造 mismatch 的练习
- 说明 dataset registry、run manifest、export manifest 如何交叉验证
- 不引入真实训练框架

验收标准：

- 有触发命令、观察证据、修复方式
- 链接 failure case playbook
- `make docs-quality` 通过

验证命令：

```bash
PYTHON=.venv/bin/python make docs-quality
```

### 14. finetune: 为 dataset registry 增加贡献者数据清单

Labels: `finetune`, `community`

背景：公开项目不能随意接收真实用户数据，需要贡献清单约束。

范围：

- 增加数据脱敏、来源、许可、schema checklist
- 不收集真实个人数据
- 不新增数据集

验收标准：

- 贡献路径说明如何提交 toy data
- 明确禁止提交敏感数据
- `make docs-quality` 通过

验证命令：

```bash
PYTHON=.venv/bin/python make docs-quality
```

### 15. community: 建立 issue 复盘样例库

Labels: `community`, `docs`, `good-first-issue`

背景：模板已经有了，下一步需要给读者看“好 issue 长什么样”。

范围：

- 增加 3 个脱敏 issue 样例
- 覆盖 Quickstart 卡住、Gateway timeout、Eval regression
- 不使用真实用户日志

验收标准：

- 每个样例包含命令、证据、定位和下一步
- 链接 First PR Playbook 和公开数据规范
- `make docs-quality` 通过

验证命令：

```bash
PYTHON=.venv/bin/python make docs-quality
```

### 16. community: 增加 First PR walkthrough 示例

Labels: `community`, `good-first-issue`

背景：First PR Playbook 已经说明步骤，示例 walkthrough 可以进一步降低首次贡献成本。

范围：

- 选择一个 docs-only 小改动做完整 walkthrough
- 展示如何写 PR 描述、verification 和 evidence
- 不新增 bot 或复杂 automation

验收标准：

- walkthrough 能被新手照着完成
- 链接 PR template 和验证矩阵
- `make docs-quality` 通过

验证命令：

```bash
PYTHON=.venv/bin/python make docs-quality
```

### 17. docs: 为 landing pages 增加搜索摘要复核

Labels: `docs`, `seo`

背景：5 个 landing pages 已经有 FAQ，下一步需要复核页面摘要、站内链接和分享标题是否一致。

范围：

- 检查 title、description、H1、首段、FAQ 的一致性
- 补充面向搜索和分享的摘要句
- 不夸大生产能力

验收标准：

- 每个 landing page 都能说明读者读完能做什么
- 链接 Quickstart、主线章节和对应迁移锚点
- `make docs-quality` 通过

验证命令：

```bash
PYTHON=.venv/bin/python make docs-quality
```

### 18. docs: 设计 llms.txt 自动生成脚本

Labels: `docs`, `seo`, `community`

背景：当前 `docs-quality` 已经检查根目录和公开 assets 的 `llms.txt` 一致性，下一步可以从配置生成它，减少手工维护。

范围：

- 设计生成输入：VitePress nav、landing pages、community pages、migration anchors
- 输出根目录 `llms.txt` 和 `docs/public/llms.txt`
- 不改变站点路由

验收标准：

- 有脚本设计或最小实现
- 保持两个文件完全一致
- `make docs-quality` 和 `npm run docs:build` 通过

验证命令：

```bash
PYTHON=.venv/bin/python make docs-quality
npm run docs:build
```

### 19. real-backend: 增加 SGLang 最小迁移 lab 设计

Labels: `real-backend`, `lab`, `serving`

背景：SGLang 适合作为结构化生成和 agentic workload 的对比迁移目标。

范围：

- 先补 lab 设计，不要求完整实现
- 对比 vLLM 和当前 mock backend
- 保留 OpenAI-compatible 契约

验收标准：

- 有运行前提、接口对齐、观测证据和失败路径
- 链接 SGLang 对比页
- `make docs-quality` 通过

验证命令：

```bash
PYTHON=.venv/bin/python make docs-quality
```

### 20. publication: 首发后 7 天反馈复盘

Labels: `publication`, `community`

背景：公开首发不是结束，首周反馈最能决定后续路线。

范围：

- 设计首发后 7 天复盘模板
- 覆盖 README、Quickstart、issue、CI、Pages、学习卡点
- 不新增自动化

验收标准：

- 模板能直接放到 GitHub Discussion 或 issue
- 关联 release notes 和 community path
- `make docs-quality` 通过

验证命令：

```bash
PYTHON=.venv/bin/python make docs-quality
```
