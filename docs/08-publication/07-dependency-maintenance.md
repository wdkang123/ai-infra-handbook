# 依赖维护与 Bot PR 处理

这页用于说明公开仓库里依赖更新应该怎么处理。  
当项目放到 GitHub 后，Dependabot、GitHub Actions 和安全扫描会开始主动发 PR、评论和邮件。它们不是噪音，而是公开项目维护的一部分。

## 这类通知意味着什么

Dependabot 常见通知大致分三类：

| 类型 | 说明 | 默认动作 |
|------|------|----------|
| 版本升级 PR | 某个 npm、pip 或 GitHub Action 有新版本 | 查看 diff，跑检查，确认后合并或手动升级 |
| 安全告警 PR | 依赖存在已知漏洞 | 优先处理，至少跑 `npm audit` 和 `public-check` |
| 关闭或忽略评论 | 某个 PR 被关闭、分支删除或配置改变 | 确认是否已经用别的提交处理，不要只看邮件判断 main 状态 |

如果邮件里出现 “I won't notify you again about this release”，通常表示当前 release 的提醒被关闭了。它不等于 PR 已经合并，也不等于 main 被改了。先看 PR 的 `state`、`merged` 和当前 main 最新提交。

## 当前仓库的自动化

仓库现在有三层维护入口：

| 文件 | 作用 |
|------|------|
| `.github/dependabot.yml` | 每周检查 npm、pip 和 GitHub Actions 依赖，按生态分组发 PR |
| `.github/workflows/dependency-review.yml` | 依赖相关 PR 上运行 dependency review，发现中高风险依赖时阻断 |
| `.github/workflows/ci.yml` | 跑代码、文档、smoke、证据包和生成器检查 |
| `.github/workflows/docs-pages.yml` | 构建并部署 GitHub Pages 文档站 |

Dependabot 会把同一生态里的更新分组成较少的 PR，避免公开项目一上线就被很多小版本 PR 淹没。
当前配置没有强制指定 PR labels，因为新仓库默认只有少量 GitHub labels；如果后续想自动打 `dependencies`、`ci`、`python` 这类标签，先在仓库 Settings 或 Labels 页面创建它们，再把 labels 配置加回去。

## 推荐处理流程

收到依赖 PR 后按这个顺序处理：

1. 看 PR 标题和 diff，确认改的是 npm、pip 还是 GitHub Actions。
2. 看 PR 是否是安全修复。安全修复优先级高于普通小版本更新。
3. 本地同步依赖文件后运行：

```bash
PYTHON=.venv/bin/python make public-check
```

4. 如果改了 npm 依赖，再运行：

```bash
nvm use
npm audit --omit=dev --audit-level=moderate
```

5. 如果改了 GitHub Actions，推送后确认对应 workflow 真的跑过并通过。
6. 如果 PR 已关闭但建议合理，可以手动改 main，再用自己的提交合入。

## GitHub Actions 升级规则

Actions 依赖看起来只是 YAML 版本号，但它会影响 CI、Pages 和安全检查。  
处理时重点确认：

- 是否来自官方 action 或可信维护者
- 是否是 major 版本升级
- workflow 权限是否仍然最小化
- 触发条件是否没有被放宽
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

如果只是 dev dependency，也不要直接跳过。公开学习项目的构建链路本身也是读者会复制的路径。

## 什么时候关闭 PR

可以关闭依赖 PR 的情况：

- main 已经用另一个提交完成同等升级
- 这个版本和当前项目不兼容，需要等后续版本
- 它只是重复 PR，新的分组 PR 已经覆盖
- 它会引入不必要的大版本迁移，当前阶段先保持稳定

关闭前最好留下原因，避免后续维护者只看到 “closed” 不知道为什么。

## 发布前依赖检查

公开发布或大批量更新前，至少确认：

- Dependabot 配置仍覆盖 `npm`、`pip` 和 `github-actions`
- Dependabot 配置没有引用仓库里不存在的 labels
- dependency review workflow 存在
- `PYTHON=.venv/bin/python make public-check` 通过
- `npm audit --omit=dev --audit-level=moderate` 没有中高风险
- 最新 `ci` 和 `docs-pages` 都通过
- GitHub Pages 站点仍返回 200

依赖维护的目标不是追最新，而是让公开读者拿到一条稳定、可复现、不会把他们带到旧 action 或高风险依赖上的学习路径。
