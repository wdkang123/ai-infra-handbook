# Review Note

Task ID: T901
Task Title: inference-service Scaffold Pack
Reviewer: CODEX
Status: REVISE_REQUIRED

## Findings

1. `tasks/review-pending/T901-inference-service-pyproject-blueprint-v1.md`
   - 安装示例写成了 `pip install -e ".[core]"`、`".[core,sglang]"`，但当前 `pyproject` 并没有定义 `core` 这个 extra。
   - 基础依赖已经在 `[project.dependencies]` 里，继续写 `core` 会误导后续实现。

2. `tasks/review-pending/T901-inference-service-scaffold-manifest.md`
   - 关键 CLI 入口里写了 `pip install -e "inference-service[core]"` 这类命令。
   - 这会把本地路径安装和包名安装混在一起，也延续了不存在的 `core` extra 问题。

## Revision Scope

- 只修这 2 个文件
- 把安装命令改成与当前 blueprint 一致的合法写法
- 不重写整包其他文件
