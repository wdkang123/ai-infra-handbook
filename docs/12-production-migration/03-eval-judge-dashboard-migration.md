# Eval 评测系统迁移

这一页说明 `eval-module` 如何从学习型 run / compare 工具，继续走向更真实的评测系统。

当前 eval-module 已经有：

- run bundle
- sample outputs
- sample summary
- sample analysis
- compare
- release recommendation
- leaderboard
- run index
- comparison index

这些结构已经足够支撑迁移，但还不是完整评测平台。

## 当前边界

迁移时应该保留：

- `run`
- `compare`
- `leaderboard`
- `list-runs`
- `list-comparisons`
- `run_history.jsonl`
- `comparison_history.jsonl`
- `sample_analysis.json`
- comparison bundle
- release recommendation

这些是评测可复盘的核心。

## 迁移顺序

### 第一步：扩展 runner adapter

当前 runner 更偏学习型。下一步可以扩展：

- 多 backend adapter
- 多模型批量 run
- timeout / retry
- runner config snapshot
- backend version 记录

但要保留 task、model、backend、few-shot、limit 这些最小可比字段。

### 第二步：引入 judge adapter

真实 LLM 评测往往不只看 exact match 或 accuracy。  
可以逐步增加：

- rule-based judge
- LLM-as-judge
- human review import
- rubric config
- judge model/version snapshot

重点不是“有 judge”，而是 judge 的设置必须进入 run bundle。

### 第三步：把 release recommendation 变成策略层

当前 recommendation 适合学习。更真实时可以扩展：

- per-task threshold
- regression blocking
- required sample pass rate
- changed settings review
- manual override reason
- release gate audit trail

不要让 recommendation 变成一个黑箱字符串。

### 第四步：从 Markdown/JSON 走向 dashboard

dashboard 不应该替代 JSON/Markdown 产物。  
更好的迁移是：

1. 保留 JSON/Markdown 作为事实来源
2. dashboard 读取 run index / leaderboard / comparison index
3. dashboard 提供筛选、趋势和 drill-down

这样工具层可以变，证据层不会散。

## 风险清单

| 风险 | 表现 | 防线 |
| --- | --- | --- |
| 指标不可比 | 不同 task/backend 混在一起排名 | run index 保留 task/backend/few-shot |
| judge 不可复现 | 结果变了但不知道 judge 设置 | judge config 写入 bundle |
| leaderboard 误导 | 一个榜单数字被当成发布结论 | comparison + release recommendation 分开 |
| 样本缺解释 | 分数变化但无法复盘 | sample outputs / sample analysis |
| dashboard 黑箱 | UI 看起来漂亮但证据不可导出 | JSON/Markdown 继续作为产物 |

## 验收清单

- [ ] run bundle 仍然完整
- [ ] sample outputs 和 sample analysis 仍然可读
- [ ] compare 仍然校验 task 一致性
- [ ] release recommendation 有理由
- [ ] run index 和 comparison index 仍然能聚合历史
- [ ] leaderboard 不混淆 backend/few-shot
- [ ] `eval-test` 通过
- [ ] `infra-smoke` 通过

## 应该更新的文档

- [eval-module](/06-projects/03-eval-module)
- [模型发布判断案例](/11-case-studies/02-model-release-decision-walkthrough)
- [API Surface 速查](/09-reference/05-api-surface)
- [CLI Surface 速查](/09-reference/06-cli-surface)
- [产物与文件索引](/09-reference/03-artifacts-and-files)

## 一句话结论

Eval 迁移的关键，是让更多 judge、更多 backend、更多 dashboard 能力进入系统时，仍然保留可比性、可解释性和可复盘产物。
