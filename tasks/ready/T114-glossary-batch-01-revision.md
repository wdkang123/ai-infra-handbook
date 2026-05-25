# Task Card

Task ID: T114  
Title: 修订 glossary 第一批术语，补精确来源并收紧易误导表述  
Owner: MINIMAX  
Type: C-普通章节任务  
Priority: P0

## Input

基于 `tasks/review-pending/T104-glossary-batch-01-result.md` 和 `tasks/review/T104-review.md` 修订。

## Expected Output

保留 10 个术语，但修订为更稳定的版本：

1. 所有来源都要变成精确 URL
2. 删掉占位来源
3. 收紧高争议或高波动表述
4. 保持“一句话定义 / 工程意义 / 项目关系 / 易混淆点”结构

## Template

使用 MiniMax 标准输出协议。

## Acceptance Criteria

- 至少 5 个精确高质量来源
- 不出现模糊来源名
- 每个术语尽量保持短小稳定
- 不额外扩写成章节

## Allowed Sources

- vLLM 官方文档
- SGLang 官方文档
- 官方论文 / 官方 issue / 官方 blog
- 其他明确可追溯的高质量资料

## Out of Scope

- 不扩展术语数量
- 不新增训练侧大术语集
