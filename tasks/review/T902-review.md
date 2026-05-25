# Review Note

Task ID: T902
Task Title: ai-gateway Scaffold Pack
Reviewer: CODEX
Status: REVISE_REQUIRED

## Findings

1. `tasks/review-pending/T902-ai-gateway-scaffold-manifest.md`
   - manifest 里的安装命令写成了 `pip install -e "ai-gateway[core]"`。
   - 这里同样把本地路径安装和包名安装混在了一起，而且当前 blueprint 也没有定义 `core` extra。

## Revision Scope

- 只修 `T902-ai-gateway-scaffold-manifest.md`
- 把安装命令改成和 blueprint 一致的合法写法
- 不重写整包其他文件
