# Review Note

Task ID: T101  
Task Title: vLLM 官方资料与核心链接搜集  
Review Decision: REVISE_REQUIRED

## Findings

1. `vLLM-Omni` 和 `vLLM-Ascend` 被混入“主项目近 6-12 个月更新线索”，但这两者都应明确标注为独立项目或插件，而不是主仓库 release 的一部分。
2. “vLLM-Omni 公告”被指向 `vllm` 主仓库 release 搜索，这会误导后续章节写作；应改为独立仓库或独立文档入口。
3. `Sources` 中出现了不相关的 `docs.sglang.ai`，不符合任务卡里的来源范围。
4. 部分性能数字可以保留为历史背景，但需要精确绑定来源，并显式标为“历史 benchmark/官方早期数据”，不要直接混入当前能力摘要。

## Action

- 重写资料包中的“更新线索”和“优先阅读链接”
- 将 `vllm`、`vllm-omni`、`vllm-ascend` 的关系写清楚
- 删除无关来源
- 用精确链接替换模糊指向
