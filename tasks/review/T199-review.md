# Review Note

Task ID: T199  
Task Title: 产出 finetuning comparison-index v1  
Review Decision: REVISE_REQUIRED

## Findings

1. 整体结构是对的，但“与本项目关系”这一维缺少来源列，不满足 comparison-index 任务“每个维度给出来源”的要求。
2. `Unsloth` 的定位行里仍然直接写了 `2x 速度、50% 显存减少`，作为 comparison-index 可再收敛成“官方宣称的训练加速与显存优化”，避免把营销数字放太前面。

## Action

- 给“与本项目关系”这一维补上来源列
- 把 Unsloth 的性能数字改成更克制的定位表达
- 不重写整份 comparison-index
