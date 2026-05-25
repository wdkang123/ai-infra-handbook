# GitHub Pages 发布指南

这页说明如何把 VitePress 学习站发布到 GitHub Pages。

当前仓库提供了一个 GitHub Pages workflow：  
`.github/workflows/docs-pages.yml`

它支持两种触发方式：

- 手动运行，适合第一次配置 Pages 时验证
- 推送到 `main` 或 `master` 且文档站相关文件变化时自动发布

## 1. 推送仓库

先把仓库推到 GitHub。

发布前建议确认：

```bash
PYTHON=.venv/bin/python make infra-check
nvm use
npm run docs:build
```

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
https://your-name.github.io/ai-infra/
```

当前 workflow 会自动设置：

```bash
VITEPRESS_BASE=/ai-infra/
```

`docs/.vitepress/config.mts` 会读取这个环境变量。  
本地构建时没有设置该变量，所以仍然使用 `/`。

如果你使用自定义域名或用户根站点，可以删除 workflow 里的 `VITEPRESS_BASE`，或把它设置成 `/`。

## 5. 发布后更新 README

拿到在线地址后，在 README 的“文档站”部分补一行：

```md
在线阅读：<你的 GitHub Pages 地址>
```

这样第一次访问 GitHub 的读者不需要本地构建，也能先浏览内容。

## 6. 常见问题

### workflow 成功，但页面 404

检查：

- Pages source 是否设置成 GitHub Actions
- workflow 是否真的部署到 `github-pages` environment
- 是否需要设置 `base`

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

## 7. 自动发布时注意什么

当前 workflow 已经保留手动触发，也支持文档相关 push 自动发布。

建议仍然保留 `infra-check` 和 PR review：自动发布应该负责把已验证的内容上线，不应该替代本地验证和 CI。
