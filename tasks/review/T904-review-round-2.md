# Review Note

Task ID: T904
Task Title: finetune-demo Scaffold Pack
Reviewer: CODEX
Status: REVISE_REQUIRED

## Findings

1. `tasks/review-pending/T904-finetune-demo-pyproject-blueprint-v1.md`
   - Unsloth 安装示例写成了 `pip install -e "finetune-demo[core,unsloth]"`，但当前 `pyproject` 没有定义 `core` extra。
   - 基础依赖已经在 `[project.dependencies]` 里。

2. `tasks/review-pending/T904-finetune-demo-scaffold-manifest.md`
   - manifest 里同样使用了 `pip install -e "finetune-demo[core]"` / `"[core,unsloth]"` 这类命令。
   - 这会把本地路径安装和包名安装混在一起，并沿用不存在的 `core` extra。

## Revision Scope

- 只修这 2 个文件
- 把安装命令改成与当前 blueprint 一致的合法写法
- 不重写整包其他文件
