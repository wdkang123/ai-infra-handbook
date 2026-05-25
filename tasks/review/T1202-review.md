# T1202 Review

## Task ID: T1202
## Title: ai-gateway Implementation Map Pack
## Reviewer: CODEX
## Status: REVISE_REQUIRED

## 结论

这轮 gateway implementation map 也偏离了已接受蓝图，尤其是把鉴权和模块边界改成了另一套实现，会直接影响后续 Codex 按错接口编码。

## Findings

1. `T1202-gateway-file-order-v1.md` 引入了 `config_loader.py`、`proxy.py`、`test_auth.py`、`__version__.py` 等额外结构，同时把鉴权写成 `ApiKeyValidator(api_keys, enabled)`。但已接受的 [T1002-ai-gateway-starter-manifest.md](tasks/accepted/T1002-ai-gateway-starter-manifest.md) 和 [T1002-ai-gateway-auth-middleware-blueprint-v1.md](tasks/accepted/T1002-ai-gateway-auth-middleware-blueprint-v1.md) 口径是 `middleware/auth.py` 中的 `AuthMiddleware(...)`。
2. `T1202-gateway-import-map-v1.md` 把 `auth.py` 写成依赖 `httpx`，这与已接受 auth blueprint 不一致。accepted 版本的 auth 中间件只依赖 `fastapi.Request` / `HTTPException` 和配置，不应被 implementation map 改造成代理客户端。
3. `T1202` 整包当前更像“重新设计 gateway”，而不是“为 accepted starter files 生成实施图”。这一层应该约束在 accepted `T1002 / T1102 / T302 / T812` 边界内，不能重新定义类名、模块职责和依赖链。

## Required Fix

- 直接就地修订 `tasks/review-pending/` 下的 `T1202` 原文件，不新增平行版本。
- 全包统一对齐已接受的 `T1002 / T1102 / T302 / T812`：
  - 鉴权按 `AuthMiddleware` / `verify_bearer_token` 口径展开
  - 不把 `auth.py` 写成依赖 `httpx`
  - file order / import map / patch split / validation matrix 均以 accepted starter manifest 中的文件集合为主
- 如果某个补充文件在 accepted 资产里没有明确依据，不要在 implementation map 里把它升级成“默认必须实现”。
