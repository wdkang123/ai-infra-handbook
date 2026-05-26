# GitHub Pages 发布指南

这页说明如何把 VitePress 学习站发布到 GitHub Pages。

当前仓库提供了一个 GitHub Pages workflow：

```text
.github/workflows/docs-pages.yml
```

它支持两种触发方式：

- 手动运行，适合第一次配置 Pages 时验证
- 推送到 `main` 或 `master` 且文档站相关文件变化时自动发布

## 发布前先确认什么

发布前建议确认：

```bash
nvm use 22
PYTHON=.venv/bin/python make public-check
npm audit --omit=dev --audit-level=moderate
```

如果只是想快速确认文档站：

```bash
PYTHON=.venv/bin/python make docs-quality
npm run docs:build
```

不要把 GitHub Pages 当成替代本地验证的工具。Pages 应该负责发布已经验证过的内容。

## 1. 推送仓库

先把仓库推到 GitHub。

当前推荐仓库：

```text
wdkang123/ai-infra-handbook
```

如果你 fork 或改名，后面 `VITEPRESS_BASE` 和 Pages URL 都要跟着调整。

## 2. 配置 GitHub Pages

进入 GitHub 仓库：

```text
Settings -> Pages
```

把 Source 设置为：

```text
GitHub Actions
```

这个设置告诉 GitHub：站点由 Actions workflow 构建和部署。

如果 Source 不是 GitHub Actions，workflow 即使成功，Pages 也可能不按预期发布。

## 3. 运行 workflow

第一次配置时，建议先手动运行一次：

```text
Actions -> docs-pages -> Run workflow
```

选择默认分支，然后运行。

workflow 会执行：

1. checkout
2. setup Node.js
3. `npm ci`
4. 设置 `VITEPRESS_BASE` 为 `/<仓库名>/`
5. `npm run docs:build`
6. 上传 `docs/.vitepress/dist`
7. 部署到 GitHub Pages

之后如果你把文档、VitePress 配置、`package.json`、`package-lock.json`、文档质量脚本或这个 workflow 推送到 `main` / `master`，它也会自动构建和部署。

## 4. 设置 VitePress base

如果你的站点发布在用户或组织根域名，例如：

```text
https://your-name.github.io/
```

通常不需要设置 `base`。

如果发布在项目路径，例如：

```text
https://your-name.github.io/ai-infra-handbook/
```

当前 workflow 会自动设置：

```bash
VITEPRESS_BASE=/ai-infra-handbook/
```

`docs/.vitepress/config.mts` 会读取这个环境变量。

本地构建时没有设置该变量，所以仍然使用 `/`。

如果你使用自定义域名或用户根站点，可以删除 workflow 里的 `VITEPRESS_BASE`，或把它设置成 `/`。

## 5. 发布后更新 README

拿到在线地址后，在 README 的文档站部分补一行：

```md
在线阅读：https://wdkang123.github.io/ai-infra-handbook/
```

这样第一次访问 GitHub 的读者不需要本地构建，也能先浏览内容。

同时建议检查：

- 仓库 About 的 Website 字段
- README 顶部入口
- 首页 GitHub 区块
- 发布总览里的链接

## 6. 如何验证线上站点

部署完成后运行：

```bash
curl -I https://wdkang123.github.io/ai-infra-handbook/
```

期望看到：

```text
HTTP/2 200
```

还应该人工打开：

- 首页
- 从 0 到 1 学习路径
- 第一次实操演练
- 示例输出与证据库
- GitHub 入口与协作地图

确认样式、导航、搜索、侧边栏和 GitHub 编辑链接都正常。

## 7. 常见问题

### Workflow 成功，但页面 404

检查：

- Pages source 是否设置成 GitHub Actions
- workflow 是否真的部署到 `github-pages` environment
- 是否需要设置 `base`
- 浏览器缓存是否还没更新
- 仓库名和 `VITEPRESS_BASE` 是否一致

### 页面能打开，但样式丢失

通常是 `VITEPRESS_BASE` 不对。

项目页通常应该是：

```bash
VITEPRESS_BASE=/仓库名/
```

用户根站点或自定义域名通常应该是：

```bash
VITEPRESS_BASE=/
```

### 本地 build 通过，Pages build 失败

检查：

- Node 版本
- `package-lock.json` 是否提交
- 是否有大小写路径问题
- 新增页面是否已加入 VitePress sidebar
- workflow 权限是否正确

### Pages 旧内容没有更新

检查：

- Actions 是否跑的是最新 commit
- docs-pages 是否 completed / success
- 浏览器缓存
- GitHub Pages cache
- 是否打开了正确 URL

## 8. 自动发布时注意什么

当前 workflow 已经保留手动触发，也支持文档相关 push 自动发布。

建议仍然保留 `public-check`、CI 和 PR review：自动发布应该负责把已验证的内容上线，不应该替代本地验证和 CI。

每次 Pages 发布后，最好确认：

- `docs-pages` 成功
- `ci` 成功
- 首页返回 200
- README 链接仍然正确

## 9. 公开发布检查清单

```text
[ ] GitHub Pages source 设置为 GitHub Actions
[ ] docs-pages workflow 成功
[ ] ci workflow 成功
[ ] 首页返回 HTTP/2 200
[ ] README 有在线站点链接
[ ] 仓库 About 有 Website
[ ] VITEPRESS_BASE 与仓库路径一致
[ ] docs-quality 通过
[ ] public-check 通过
```

## 下一步

- 准备 release 时看 [v0.1 首发发布手册](/08-publication/10-v0-1-release-playbook)。
- 维护 Pages 和 CI 时看 [维护节奏与运营清单](/08-publication/08-maintainer-rhythm)。
- 处理依赖或 Actions 更新时看 [依赖维护与 Bot PR 处理](/08-publication/07-dependency-maintenance)。
