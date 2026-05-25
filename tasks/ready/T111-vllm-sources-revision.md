# Task Card

Task ID: T111  
Title: 修订 vLLM 资料包，补精确官方链接并拆分主项目/Omni/Ascend  
Owner: MINIMAX  
Type: D-资料型任务  
Priority: P0

## Input

基于 `tasks/review-pending/T101-vllm-sources-result.md` 和 `tasks/review/T101-review.md` 修订。

## Expected Output

输出一版更严格的 vLLM 资料包，要求：

1. 明确区分 `vllm` 主项目、`vllm-omni`、`vllm-ascend`
2. 所有优先阅读链接必须是精确 URL
3. 删除不相关来源
4. 把“历史 benchmark/早期性能数字”与“当前主线能力”分开写

## Template

使用 MiniMax 标准输出协议。

## Acceptance Criteria

- 官方来源优先
- 至少 6 个精确链接
- 不再把独立项目误写成主仓库 release
- 不引入无关框架来源

## Allowed Sources

- `https://docs.vllm.ai/`
- `https://github.com/vllm-project/vllm`
- `https://github.com/vllm-project/vllm-omni`
- `https://github.com/vllm-project/vllm-ascend`
- 官方 blog / release / advisory

## Out of Scope

- 不写完整章节
- 不做跨框架对比结论
