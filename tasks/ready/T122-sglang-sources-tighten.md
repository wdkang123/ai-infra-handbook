# Task Card

Task ID: T122  
Title: 收紧 SGLang 资料包中的模糊 release 引用和额外对比段  
Owner: MINIMAX  
Type: D-资料型任务  
Priority: P0

## Input

基于：

- `tasks/review-pending/T112-sglang-sources-result.md`
- `tasks/review/T112-review-round-2.md`

## Expected Output

输出一版更收敛的 SGLang 资料包，要求：

1. 所有重点更新线索都换成精确 URL
2. 删除或压缩多余的对比段
3. 保持三段结构：
   - 稳定主线资料
   - 实验性特性
   - 近 6-12 个月更新线索

## Template

使用 MiniMax 标准输出协议。

## Acceptance Criteria

- 不再出现仅指向 releases 列表的模糊重点链接
- 不再出现额外扩展的框架对比段
- 资料包结构清晰，适合作为章节底稿

## Allowed Sources

- `https://docs.sglang.ai/`
- `https://github.com/sgl-project/sglang`
- 具体 tag / release / issue / blog URL
- `https://github.com/sgl-project/sglang-jax`

## Out of Scope

- 不写完整章节
- 不做 benchmark 结论
