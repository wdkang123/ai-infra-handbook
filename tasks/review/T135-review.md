# Review Note

Task ID: T135  
Task Title: 编写 SGLang 章节模板化初稿  
Review Decision: REVISE_REQUIRED

## Findings

1. 关键指标中把 `ITL ≤ 60ms` 直接写成章节主指标，容易把实验性 issue 里的场景目标误写成通用标准，见 [T135-sglang-chapter-draft.md](tasks/review-pending/T135-sglang-chapter-draft.md#L59)。
2. 最小实践要求“单卡 GPU 启动 DeepSeek-V3”，对于入门最小实践明显过重，不适合作为章节里的可执行起步任务，见 [T135-sglang-chapter-draft.md](tasks/review-pending/T135-sglang-chapter-draft.md#L83)。

## Action

- 把过强指标改成更中性的工程描述
- 把最小实践改成更轻量、可实际执行的模型与步骤
