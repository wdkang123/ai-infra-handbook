# Task Card

Task ID: T112  
Title: 修订 SGLang 资料包，替换占位链接并修正来源归属  
Owner: MINIMAX  
Type: D-资料型任务  
Priority: P0

## Input

基于 `tasks/review-pending/T102-sglang-sources-result.md` 和 `tasks/review/T102-review.md` 修订。

## Expected Output

输出一版更严格的 SGLang 资料包，要求：

1. 修正中文资料站的归属描述
2. 将“优先阅读链接”全部替换成精确 URL
3. 将内容分成：
   - 稳定主线资料
   - 实验性特性 / issue / PoC
   - 近 6-12 个月更新线索

## Template

使用 MiniMax 标准输出协议。

## Acceptance Criteria

- 至少 6 个精确链接
- 不再出现“README 或 blog 链接”这类占位写法
- 区分正式文档和实验性 issue
- 来源归属前后一致

## Allowed Sources

- `https://docs.sglang.ai/`
- `https://github.com/sgl-project/sglang`
- 官方 issue / release / blog
- `https://github.com/sgl-project/sglang-jax`

## Out of Scope

- 不写完整章节
- 不做 benchmark 最终结论
