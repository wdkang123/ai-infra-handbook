# T1205 Review

## Task ID: T1205
## Title: Root Integration Implementation Map Pack
## Reviewer: CODEX
## Status: REVISE_REQUIRED

## 结论

这轮 root integration implementation map 偏差最大：它把根级联调重新写成了 helper script + 新端口 + eval 服务化的一套方案，与已接受 root blueprints 明显冲突。

## Findings

1. `T1205-root-file-order-v1.md` 引入了 `scripts/inference_serve.sh`、`gateway_serve.sh`、`eval_serve.sh`、`finetune_serve.sh` 等 helper scripts，但已接受的 [T1005-root-makefile-blueprint-v2.md](tasks/accepted/T1005-root-makefile-blueprint-v2.md) 主路径是根级 `Makefile` 通过 `$(MAKE) -C <module>` 驱动子项目，而不是新增一组根脚本。
2. `T1205-root-script-dependency-map-v1.md` 把 gateway 端口写成 `8001`，还把 eval-module 写成 `8002` 上的服务；但 accepted root makefile 明确是 gateway `8080`，eval-module 通过 CLI 运行 benchmark，不是常驻 HTTP 服务。
3. `T1205` 整包把根级 integration map 写成了另一套新的调度系统，这会直接让后续实现与已接受的 `T1005 / T1105 / T805` 断裂，尤其会影响 `infra-smoke`、`all-serve`、`eval-run-*` 的调用链。

## Required Fix

- 直接就地修订 `tasks/review-pending/` 下的 `T1205` 原文件，不新增平行版本。
- 全包统一对齐已接受的 `T1005 / T1105 / T805`：
  - 端口口径回到 `INFERENCE_PORT=8000`、`GATEWAY_PORT=8080`
  - eval-module 按 CLI / Make target 使用，不写成 `:8002` 服务
  - 根级调用链以 `Makefile` 和 `$(MAKE) -C ...` 为主，不新增 `*_serve.sh` 作为默认主线
- file order / script dependency map / patch split / validation matrix 都要服务 accepted root blueprints，而不是另起炉灶。
