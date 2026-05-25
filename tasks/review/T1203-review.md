# T1203 Review

## Task ID: T1203
## Title: eval-module Implementation Map Pack
## Reviewer: CODEX
## Status: REVISE_REQUIRED

## 结论

这轮 eval implementation map 的问题在于把已接受的 starter files 拆成了另一套 results 子包结构，导致 runner、CLI 和结果模型都偏离 accepted 契约。

## Findings

1. `T1203-eval-file-order-v1.md` 把 `EvalResult` 拆到了 `src/eval_module/results/eval_result.py`，但已接受的 [T1003-eval-runner-py-blueprint-v1.md](tasks/accepted/T1003-eval-runner-py-blueprint-v1.md) 里，`EvalResult` 就定义在 `src/eval_module/runners/lm_eval_runner.py`。implementation map 不该自创另一套落点。
2. `T1203-eval-import-map-v1.md` 把 CLI 主流程写成 `LmEvalRunner.evaluate(...)`，而已接受 runner blueprint 的公开方法是 `run(...)`，不是 `evaluate(...)`。这会直接把后续调用点写错。
3. `T1203` 的 file order / import map / patch split / validation matrix 都应服务 accepted `T1003 / T1103 / T303 / T813`，而不是把 `results/`、`comparator.py`、`result_store.py` 重新抽成另一套先验结构。

## Required Fix

- 直接就地修订 `tasks/review-pending/` 下的 `T1203` 原文件，不新增平行版本。
- 全包统一对齐已接受的 `T1003 / T1103 / T303 / T813`：
  - `LmEvalRunner.run(...)` 作为主入口
  - `EvalResult` 的归属与字段口径回到 accepted runner blueprint
  - implementation map 优先围绕 accepted starter files，而不是额外发明子包结构
- 如果需要提到补充组件，必须明确标成“后续可选扩展”，不能写成 MVP 默认主路径。
