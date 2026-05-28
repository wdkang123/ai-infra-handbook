# 维护者 Triage 节奏

> 本页解决：公开后如何处理 issue、PR、Dependabot、release 和首周反馈，避免项目变成无人维护的资料堆。
> 读完能做：按每日、每周、每月节奏整理贡献入口，并把反馈转成可验证任务。
> 关联代码：`.github/ISSUE_TEMPLATE`、`.github/workflows`、`scripts/build_launch_pack.py`。
> 验证命令：`PYTHON=.venv/bin/python make launch-pack`。

公开增长不是“多发几页文档”，而是把反馈稳定变成更好的 Quickstart、lab、case 和验证命令。

## Triage 优先级

| 优先级 | 类型 | 处理方式 |
| --- | --- | --- |
| P0 | 密钥、个人数据、私有日志、授权问题 | 先按 `SECURITY.md` 处理，不在公开 issue 展开细节 |
| P1 | Quickstart 无法跑通、Pages 无法访问、CI 全红 | 先复现，再标记 `bug` 或 `help wanted` |
| P2 | 文档误导、新手卡点、输出证据不清楚 | 转成 docs / lab / evidence 任务 |
| P3 | 真实后端迁移建议、工具对比、路线图讨论 | 转成 roadmap 或 discussion 风格 issue |
| P4 | 大而泛的功能愿望 | 先拆成可验证的最小 issue |

## 每日 15 分钟

适合项目刚公开后的前两周：

- 看是否有安全相关反馈
- 看 GitHub Pages 和 CI 是否正常
- 看 issue 是否有“卡在第一步”的反馈
- 给无复现信息的 issue 回复 evidence 模板
- 把重复问题链接到 Quickstart、FAQ 或 failure case

## 每周 60 分钟

每周整理一次协作面：

- 关闭已经合并或过期的 starter issue
- 给新手友好的任务加 `good first issue`
- 检查 Dependabot PR 是否只是版本更新，还是需要改 workflow 或配置
- 运行 `make public-check` 复核公开安全与构建
- 看 `launch_pack.md` 里的 release notes、starter issues、发布后 checklist 是否还准确
- 更新 README 的项目状态和下一阶段路线

建议命令：

```bash
PYTHON=.venv/bin/python make public-check
PYTHON=.venv/bin/python make release-brief
PYTHON=.venv/bin/python make launch-pack
```

## 每月 120 分钟

每月做一次路线复盘：

- 哪些页面被反复问到
- 哪些 lab 跑通率最低
- 哪些 issue 真正吸引贡献
- 真实后端迁移是否应该进入下一阶段
- 是否需要更新 vLLM、SGLang、OpenTelemetry、Prometheus、Eval gate 的路线文档
- 是否需要发布一个新的 release notes

月度复盘不要只看新增内容数量，更要看：

- 新手能否 15 分钟跑通
- 读者能否解释 request id、events、metrics、eval report、manifest
- 贡献者能否知道 PR 前跑什么命令
- 维护者能否从 release brief 看出 pass / warn / block 风险

## Issue 状态建议

| 状态 | 含义 |
| --- | --- |
| needs reproduction | 需要命令、输出、环境或 request id |
| ready for contribution | 范围和验收标准清楚，可以被认领 |
| needs maintainer decision | 需要维护者决定路线或边界 |
| blocked by design | 需要先补设计页或接口契约 |
| done in baseline | 当前主线已经覆盖，可以关闭并链接对应页面 |

## 首发后 7 天复盘模板

可以放到 GitHub Discussion 或 issue：

```markdown
## v0.1 首周复盘

### Quickstart

- 多少人能完成 `make quickstart`:
- 最常见失败:
- 需要补的排障:

### Learning path

- 读者最常打开的入口:
- 最容易跳失的章节:
- 需要补深度的章节:

### Evidence

- request id / events 是否清楚:
- metrics 是否能被理解:
- eval report 是否能支持发布判断:
- manifest / evidence packet 是否被使用:

### Contribution

- 哪些 starter issues 有互动:
- 哪些 issue 需要拆小:
- 哪些 PR 需要补验证:

### Next 7 days

- must fix:
- should improve:
- can defer:
```

## `llms.txt` 维护规则

当这些入口变化时，同步更新根目录 `llms.txt` 和 `docs/public/llms.txt`：

- 首页、Quickstart、学习路线、landing page 的 URL
- 社区贡献路径、starter issues、release notes
- vLLM、SGLang、OpenTelemetry、Prometheus、Eval gate 等迁移锚点
- 项目定位或公开边界

更新后运行：

```bash
PYTHON=.venv/bin/python make docs-quality
```

`docs-quality` 会检查两个 `llms.txt` 是否一致，避免 GitHub 根目录和网站公开文件漂移。

## 继续阅读

- [社区贡献路径](/community/00-overview)
- [First PR Playbook](/community/01-first-pr-playbook)
- [公开发布总览](/08-publication/00-overview)
- [自动生成首发运营包](/08-publication/13-generated-launch-pack)
- [Release Brief](/09-reference/09-release-brief)
