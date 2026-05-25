# Security Policy

这个仓库是学习型项目，不应直接作为生产系统部署。

## 支持范围

当前重点关注：

- 文档中可能误导用户泄露 API key 的内容
- 示例配置中意外提交真实密钥
- 鉴权、header 转发、cache 隔离相关的明显问题
- 依赖或脚本中会影响本地开发安全的行为

暂不承诺生产级安全响应，例如：

- 完整的漏洞赏金流程
- 生产环境加固建议
- 合规审计

## 报告方式

如果你发现安全问题，请不要在公开 issue 中贴真实 token、密钥、日志或内部 URL。

建议提交一个 issue，只描述：

- 受影响的模块
- 问题类型
- 如何在不暴露敏感信息的前提下复现
- 你期望的安全行为

如果后续仓库启用 GitHub Security Advisories，可以优先使用私密报告通道。

## 密钥处理约定

贡献示例时请使用占位符：

```text
sk-example
sk-test-key-1
YOUR_API_KEY
```

本地环境变量可以参考 `.env.example`。  
真实 `.env` 和 `.env.*` 文件已被 `.gitignore` 忽略，但仍请在提交前确认没有把真实密钥写进文档、配置或日志。

提交前建议运行：

```bash
PYTHON=.venv/bin/python make security-check
```

公开上传或发 PR 前，也可以运行：

```bash
PYTHON=.venv/bin/python make public-check
```

不要提交：

- 真实 API key
- 云服务凭证
- 私有 endpoint
- 包含敏感 header 的请求日志

## 学习型边界

当前实现包含一些刻意简化：

- 本地 Bearer token 示例
- 内存限流和内存 cache
- mock inference engine
- mock finetune artifacts

这些用于学习分层和系统行为，不代表生产安全方案。
