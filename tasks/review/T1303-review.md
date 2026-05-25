# T1303 Review

## Task ID: T1303
## Title: eval-module Execution Slice Pack
## Reviewer: CODEX
## Status: REVISE_REQUIRED

## 结论

这轮 `eval-module` 的 slice 方向是对的，但执行契约里把蓝图对象当成可直接运行的真实接口了，会误导后续 Codex 的实现入口和验证方式。

## Findings

1. [T1303-eval-slice-contracts-v1.md](tasks/review-pending/T1303-eval-slice-contracts-v1.md#L62) 到 [T1303-eval-slice-contracts-v1.md](tasks/review-pending/T1303-eval-slice-contracts-v1.md#L81) 直接写成 `LmEvalRunner()` 无参实例化，并把 `EvalResult` 当字典用 `result['task']` / `result['backend']`。但已接受的 [T1003-eval-runner-py-blueprint-v1.md](tasks/accepted/T1003-eval-runner-py-blueprint-v1.md) 里，`LmEvalRunner` 需要 `backend_config`，`EvalResult` 也是 dataclass，不是 dict。
2. [T1303-eval-slice-contracts-v1.md](tasks/review-pending/T1303-eval-slice-contracts-v1.md#L114) 到 [T1303-eval-slice-contracts-v1.md](tasks/review-pending/T1303-eval-slice-contracts-v1.md#L122) 也把 `ResultStore.save/load` 的示例写成了直接处理普通 dict，这与 accepted runner/result 口径不一致。

## Required Fix

- 直接就地修订 `T1303` 原文件，不新增平行版本。
- 把 runner、EvalResult、ResultStore 的示例和验收命令统一回 accepted `T1003` 蓝图口径。
- 重点是“契约写法”修正，不需要重写整包。
