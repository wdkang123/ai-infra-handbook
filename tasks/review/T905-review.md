# Review Note

Task ID: T905
Task Title: Developer Workflow Scaffold Pack
Reviewer: CODEX
Status: REVISE_REQUIRED

## Findings

1. `tasks/review-pending/T905-dev-workflow-scaffold-manifest.md`
   - 文档把根级任务看板写成了 `TASKBOARD.md`，但当前仓库实际使用的是 `tasks/task-board.md`。
   - 如果后续照这个 scaffold 落地，会把工作流文件名带偏。

2. `tasks/review-pending/T905-codex-implementation-handoff-v1.md`
   - 同样把交接目标写成了 `TASKBOARD.md`，并要求实现后更新 `TASKBOARD.md` 状态。
   - 这和当前仓库真实约定不一致。

3. `tasks/review-pending/T905-repo-task-runner-map-v1.md`
   - 多处安装示例写成了 `pip install -e inference-service`、`pip install -e "eval-module[core]"`、`pip install -e "finetune-demo[core]"`。
   - 这些写法混淆了“本地路径 editable install”和“包名 + extras”，会误导后续真正执行。

## Revision Scope

- 只修这 3 个文件
- 把 `TASKBOARD.md` 对齐到当前仓库真实路径约定
- 把安装命令改成与本地路径安装语义一致的合法写法
- 不重写整包其他文件
