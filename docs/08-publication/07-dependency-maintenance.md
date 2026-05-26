# 依赖维护与 Bot PR 处理

这页用于说明公开仓库里依赖更新应该怎么处理。

当项目放到 GitHub 后，Dependabot、GitHub Actions 和安全扫描会开始主动发 PR、评论和邮件。它们不是噪音，而是公开项目维护的一部分。

如果不建立处理规则，维护者很容易出现两种极端：

- 看到 bot PR 就全部忽略，导致依赖慢慢过期
- 看到升级就全部合并，导致构建或教程路径突然坏掉

更稳的方式是：按风险、生态、验证结果和项目阶段处理。

## 这类通知意味着什么

Dependabot 常见通知大致分三类：

| 类型 | 说明 | 默认动作 |
| --- | --- | --- |
| 版本升级 PR | 某个 npm、pip 或 GitHub Action 有新版本 | 查看 diff，跑检查，确认后合并或手动升级 |
| 安全告警 PR | 依赖存在已知漏洞 | 优先处理，至少跑 `npm audit` 和 `public-check` |
| 关闭或忽略评论 | 某个 PR 被关闭、分支删除或配置改变 | 确认是否已经用别的提交处理，不要只看邮件判断 main 状态 |

如果邮件里出现 “I won't notify you again about this release”，通常表示当前 release 的提醒被关闭了。它不等于 PR 已经合并，也不等于 main 被改了。

先看 PR 的：

- `state`
- `merged`
- changed files
- latest main commit
- Actions 状态

不要只根据邮件做判断。

## 当前仓库的自动化

仓库现在有几层维护入口：

| 文件 | 作用 |
| --- | --- |
| `.github/dependabot.yml` | 每周检查 npm、pip 和 GitHub Actions 依赖，按生态分组发 PR |
| `.github/workflows/dependency-review.yml` | 依赖相关 PR 上运行 dependency review，发现中高风险依赖时阻断 |
| `.github/workflows/ci.yml` | 跑代码、文档、smoke、证据包和生成器检查 |
| `.github/workflows/docs-pages.yml` | 构建并部署 GitHub Pages 文档站 |

Dependabot 会把同一生态里的更新分组成较少的 PR，避免公开项目一上线就被很多小版本 PR 淹没。

当前配置没有强制指定 PR labels，因为新仓库默认只有少量 GitHub labels。如果后续想自动打 `dependencies`、`ci`、`python` 这类标签，先在仓库 Settings 或 Labels 页面创建它们，再把 labels 配置加回去。

## 推荐处理流程

收到依赖 PR 后按这个顺序处理：

1. 看 PR 标题和 diff，确认改的是 npm、pip 还是 GitHub Actions。
2. 看 PR 是否是安全修复。安全修复优先级高于普通小版本更新。
3. 看是否是 major 版本升级。major 升级不要自动合并。
4. 本地同步依赖文件后运行：

```bash
PYTHON=.venv/bin/python make public-check
```

5. 如果改了 npm 依赖，再运行：

```bash
nvm use 22
npm audit --omit=dev --audit-level=moderate
```

6. 如果改了 GitHub Actions，推送后确认对应 workflow 真的跑过并通过。
7. 如果 PR 已关闭但建议合理，可以手动改 main，再用自己的提交合入。
8. 合并后观察 Pages 和站点首页。

## 按风险分类处理

### 低风险更新

通常包括：

- patch 版本
- dev dependency 小升级
- 文档构建工具的小版本更新
- 官方 action 的 patch/minor 升级

处理方式：

- 查看 changelog
- 跑 `public-check`
- 看 Actions
- 合并或手动更新

### 中风险更新

通常包括：

- minor 版本但影响构建链路
- pip dev tool 升级
- VitePress / Vite / TypeScript 相关升级
- pytest、ruff、mypy 等工具升级

处理方式：

- 本地跑完整验证
- 确认锁文件变化合理
- 确认文档站构建正常
- 必要时单独提交，方便回滚

### 高风险更新

通常包括：

- major 版本
- GitHub Actions 权限或发布链路变化
- 安全相关依赖大升级
- 会改变构建输出、路由、Node/Python 版本的升级

处理方式：

- 不自动合并
- 先开本地分支或单独提交
- 阅读 release notes
- 更新文档和验证矩阵
- 跑本地和云端检查
- 合并后观察 Pages

## GitHub Actions 升级规则

Actions 依赖看起来只是 YAML 版本号，但它会影响 CI、Pages 和安全检查。

处理时重点确认：

- 是否来自官方 action 或可信维护者
- 是否是 major 版本升级
- workflow 权限是否仍然最小化
- 触发条件是否没有被放宽
- Pages 部署权限是否仍然正确
- 推送后对应 workflow 是否实际成功

例如 Pages artifact action 升级后，需要确认 `docs-pages` 运行成功，并再次访问站点：

```bash
curl -I -L https://wdkang123.github.io/ai-infra-handbook/
```

期望看到 `HTTP/2 200`。

## npm 与 pip 升级规则

npm 和 pip 依赖升级要同时看“能不能装”和“公开风险”：

- `package-lock.json` 和 `package.json` 必须一起检查
- `requirements-dev.txt` 变化后要跑 Python lint 和测试
- 依赖审计不能代替项目测试
- 只为文档站构建服务的依赖，也要走 `public-check`
- 不把本地虚拟环境、缓存、构建产物提交进仓库
- 不在不理解影响的情况下删除 lock file

如果只是 dev dependency，也不要直接跳过。公开学习项目的构建链路本身也是读者会复制的路径。

## 什么时候关闭 PR

可以关闭依赖 PR 的情况：

- main 已经用另一个提交完成同等升级
- 这个版本和当前项目不兼容，需要等后续版本
- 它只是重复 PR，新的分组 PR 已经覆盖
- 它会引入不必要的大版本迁移，当前阶段先保持稳定
- 它要求的环境与项目公开运行路径冲突

关闭前最好留下原因，避免后续维护者只看到 “closed” 不知道为什么。

## 什么时候不要关闭 PR

这些情况不要轻易关闭：

- PR 是安全修复
- 当前版本已有中高危漏洞
- 升级影响的是 GitHub Actions 官方维护链路
- PR 暴露了当前 CI 或构建路径已经落后
- dependency review 明确提示风险

如果暂时不能合并，也应该留下说明：

```text
暂不合并，原因：
需要补充验证：
计划重新评估时间：
```

## 发布前依赖检查

公开发布或大批量更新前，至少确认：

- Dependabot 配置仍覆盖 `npm`、`pip` 和 `github-actions`
- Dependabot 配置没有引用仓库里不存在的 labels
- dependency review workflow 存在
- `PYTHON=.venv/bin/python make public-check` 通过
- `npm audit --omit=dev --audit-level=moderate` 没有中高风险
- 最新 `ci` 和 `docs-pages` 都通过
- GitHub Pages 站点仍返回 200
- release notes 没有承诺未验证的依赖状态

## 处理记录应该写在哪里

小更新可以只在 PR 里说明。

重要更新建议同步：

- PR 描述
- `CHANGELOG.md`
- 发布说明
- 相关文档页
- 验证矩阵

例如 Node 版本、VitePress、GitHub Actions 发布链路、security scan 规则发生变化时，都应该记录。

## 常见误区

### 误区一：Dependabot PR 都是噪音

不是。公开项目的依赖维护是读者信任的一部分。

### 误区二：安全 PR 可以等有空再看

安全 PR 优先级更高，至少要确认影响范围。

### 误区三：CI 过了就不看 diff

不够。依赖升级可能改变行为、权限、构建输出或未来维护成本。

### 误区四：开发依赖不重要

公开学习项目里，开发依赖也是读者本地运行路径的一部分。

### 误区五：关闭 PR 就等于问题结束

关闭只是状态变化。你还要知道风险是否已经被处理。

依赖维护的目标不是追最新，而是让公开读者拿到一条稳定、可复现、不会被旧 action 或高风险依赖拖累的学习路径。
