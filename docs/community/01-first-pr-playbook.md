# First PR Playbook

> 本页解决：第一次给这个仓库提 PR 时，怎样把范围、证据和验证命令写清楚。
> 读完能做：选择一个小而完整的改动，按 docs-only、code-only、cross-service 三类路径完成自查。
> 关联代码：`CONTRIBUTING.md`、`.github/pull_request_template.md`、`Makefile`。
> 验证命令：`PYTHON=.venv/bin/python make docs-quality`。

第一次 PR 的目标不是一次性做大，而是让维护者能快速回答三件事：

1. 这个改动解决了哪个学习问题。
2. 读者能看到什么更清楚的证据。
3. 你跑过哪些检查来证明它没有破坏主线。

## 选题方式

优先选能独立验收的任务：

| 类型 | 好的 first PR | 容易失控的 PR |
| --- | --- | --- |
| docs | 给某页补预期输出、失败排查、关联代码入口 | 一次性重写整个章节目录 |
| lab | 增加一个触发命令和证据观察路径 | 同时改多个服务和多个实验 |
| case | 补一个真实卡点的症状、证据、定位、修复 | 只讲故事，不给命令和证据 |
| tooling | 给脚本补一个小的输出字段和测试 | 引入大依赖但没有本地验证 |
| migration | 补接口、metrics、tracing 的对照表 | 默认替换 mock 路径 |

如果你不确定，从 [Starter Issues](/08-publication/15-starter-issues) 里挑 `good-first-issue`、`docs` 或 `lab` 最稳。

## PR 前最小自查

所有 PR 都先检查：

- 是否保持“学习项目，不是生产平台”的定位
- 是否没有删除已有主线内容和路由
- 是否没有提交 `.env`、token、私钥、真实日志、真实用户数据、本机路径、模型权重或缓存
- 是否在 PR 描述里写清楚 why、what、verification、evidence、learning impact

## 三类验证路径

### Docs-only

适用：只改 Markdown、首页入口、导航、图片引用、发布说明。

建议命令：

```bash
PYTHON=.venv/bin/python make docs-quality
npm run docs:build
```

如果新增页面，还要确认：

- `docs/.vitepress/config.mts` sidebar 有链接
- 首页文档页统计没有漂移
- 页面顶部有“本页解决什么、读完能做什么、关联代码入口、验证命令”
- README 或 publication 页是否需要新增入口

### Code-only

适用：只改脚本、测试、CLI 或单服务内部逻辑。

建议命令：

```bash
PYTHON=.venv/bin/python make infra-format
PYTHON=.venv/bin/python make infra-check
```

如果改了自动产物生成器，再补相关命令：

```bash
PYTHON=.venv/bin/python make release-brief
PYTHON=.venv/bin/python make roadmap-pack
PYTHON=.venv/bin/python make launch-pack
```

### Cross-service

适用：改 gateway、inference、eval、finetune 之间的行为、端口、API、metrics、manifest 或证据包。

建议命令：

```bash
PYTHON=.venv/bin/python make infra-check
PYTHON=.venv/bin/python make infra-smoke
PYTHON=.venv/bin/python make infra-evidence
PYTHON=.venv/bin/python make public-check
```

跨服务 PR 的描述里应该至少贴出：

- request id
- events endpoint 或输出文件
- metrics 观察点
- eval report 或 release recommendation
- manifest 或 evidence packet 路径

## PR 描述模板

可以直接复制下面的结构：

```markdown
## What changed

- 

## Why

- 

## Verification

- [ ] `PYTHON=.venv/bin/python make docs-quality`
- [ ] `PYTHON=.venv/bin/python make infra-check`
- [ ] `PYTHON=.venv/bin/python make infra-smoke`
- [ ] `PYTHON=.venv/bin/python make public-check`
- [ ] `npm run docs:build`

## Evidence

- request id:
- events:
- metrics:
- eval report:
- manifest:
- evidence packet:

## Learning impact

- 
```

## 常见 review 反馈

| 反馈 | 为什么重要 | 怎么改 |
| --- | --- | --- |
| 缺少验证命令 | 维护者无法判断改动是否可复现 | 补命令和关键输出 |
| 页面没有代码入口 | 读者不知道概念落在哪里 | 补 `projects/` 或 `scripts/` 路径 |
| 只写结论没有证据 | 学习站会变成提纲 | 补 request id、events、metrics、report、manifest |
| 夸大生产能力 | 项目定位会漂移 | 明确 mock / learning boundary |
| 新增页面没有 sidebar | 读者和构建检查都会迷路 | 更新 VitePress config |
| 使用真实数据 | 公开仓库有安全风险 | 换成 toy data 和脱敏输出 |

## 合并后的下一步

PR 合并后，维护者通常会把剩余问题拆成 issue：

- 还缺哪些平台差异说明
- 是否需要补一个 failure case
- 是否要同步 release brief、roadmap pack 或 launch pack
- 是否应该把读者反馈沉淀到 FAQ

第一次 PR 不需要一次解决所有后续问题。只要它让学习者更容易跑通、看懂或贡献，就是好 PR。

## 继续阅读

- [社区贡献路径](/community/00-overview)
- [公开数据与证据规范](/community/02-safe-data-and-evidence)
- [维护者 Triage 节奏](/community/03-triage-and-maintainer-rhythm)
- [验证矩阵](/09-reference/07-validation-matrix)
