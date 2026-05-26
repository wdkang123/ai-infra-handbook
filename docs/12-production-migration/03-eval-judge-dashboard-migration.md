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

这些结构已经足够支撑迁移，但它还不是完整评测平台。
真实评测系统还会面对更多 backend、更多 judge、更多任务、更多人参与和更复杂发布门禁。

## 迁移时最应该保留什么

优先保留这些命令和产物：

```text
run
compare
leaderboard
list-runs
list-comparisons
run_history.jsonl
comparison_history.jsonl
sample_outputs.json
sample_summary.json
sample_analysis.json
run_manifest.json
comparison bundle
release recommendation
```

这些不是实现细节，而是评测可复盘的核心。

如果未来接 dashboard、数据库或更复杂 judge，仍然应该能回到这些事实产物。

## 第一阶段：扩展 Runner Adapter

当前 runner 更偏学习型。下一步可以扩展：

- 多 backend adapter
- 多模型批量 run
- timeout / retry
- runner config snapshot
- backend version 记录
- prompt template version
- task config snapshot

但要保留最小可比字段：

- task
- model
- backend
- num few-shot
- sample count
- timestamp
- result file

如果这些字段不稳定，leaderboard 和 compare 很快会失去意义。

## 第二阶段：引入 Judge Adapter

真实 LLM 评测往往不只看 exact match 或 accuracy。
你可能会逐步引入：

- rule-based judge
- LLM-as-judge
- rubric-based judge
- human review import
- pairwise preference judge
- safety judge
- format judge

重点不是“有 judge”，而是 judge 设置必须进入 run bundle。

Judge 配置至少要记录：

| 字段 | 为什么重要 |
| --- | --- |
| judge type | rule、LLM、human、hybrid 不可混看 |
| judge model/version | LLM judge 本身会变 |
| rubric version | 评分标准必须可追溯 |
| prompt template | judge prompt 变化会影响分数 |
| temperature / params | judge 随机性会影响稳定性 |
| human reviewer source | 人审导入要说明来源 |

没有这些字段，分数变化很难解释。

## 第三阶段：把 Release Recommendation 变成策略层

当前 recommendation 适合学习。
更真实时可以扩展为 release gate policy。

可以逐步支持：

- per-task threshold
- regression blocking
- required sample pass rate
- changed settings review
- critical sample blocklist
- cost regression threshold
- latency regression threshold
- manual override reason
- release gate audit trail

但不要让 recommendation 变成黑箱字符串。

一条发布判断至少应该说明：

- 结论是什么
- 触发了哪些规则
- 哪些证据支持它
- 哪些风险需要人工复核
- 是否允许 override
- override reason 是什么

## 第四阶段：从 JSON/Markdown 走向 Dashboard

dashboard 很有价值，但 dashboard 不应该替代事实产物。

更好的迁移是：

```text
run bundle / comparison bundle / history
  -> index / leaderboard
  -> dashboard
```

也就是说：

1. JSON/Markdown 仍然是事实来源。
2. dashboard 读取 run index、leaderboard、comparison index。
3. dashboard 提供筛选、趋势和 drill-down。
4. dashboard 里的每个数字都能跳回 artifact。

如果 dashboard 只能看漂亮图，不能导出证据，那它会削弱复盘能力。

## 第五阶段：引入任务集和数据集版本

真实 eval 会面对多个任务和版本：

- mmlu
- gsm8k
- custom domain task
- regression set
- safety set
- formatting set
- latency/cost benchmark

每个任务集都需要版本。

建议记录：

- task id
- dataset version
- sample count
- sampling rule
- prompt template version
- judge config version
- backend config version

这样你才能判断一次分数变化是模型变化、数据变化、prompt 变化，还是 judge 变化。

## 第六阶段：和 Gateway / Production 连接

评测系统不应该只打孤立后端。
如果真实用户走 gateway，eval 至少要有能力打平台入口。

这样可以覆盖：

- 外部模型名映射
- gateway fallback
- cache bypass 或 cache policy
- request id
- upstream target
- platform latency
- token usage

这会让 release decision 更接近真实调用路径。

## 当前仓库相关文件

重点文件：

```text
projects/eval-module/src/eval_module/main.py
projects/eval-module/src/eval_module/results/result_store.py
projects/eval-module/src/eval_module/runners/lm_eval_runner.py
projects/eval-module/tests/test_runner.py
```

迁移时常改：

- `main.py`：新增 CLI 或参数。
- `lm_eval_runner.py`：扩展 runner adapter。
- `result_store.py`：扩展 run/comparison/leaderboard/index 产物。
- tests：保护可比性和发布判断。

## 风险清单

| 风险 | 表现 | 防线 |
| --- | --- | --- |
| 指标不可比 | 不同 task/backend/few-shot 混在一起排名 | run index 保留比较条件 |
| judge 不可复现 | 结果变了但不知道 judge 设置 | judge config 写入 bundle |
| leaderboard 误导 | 榜单数字被当成发布结论 | leaderboard 和 comparison 分层 |
| 样本缺解释 | 分数变化但无法复盘 | sample outputs / sample analysis |
| dashboard 黑箱 | UI 漂亮但证据不可导出 | JSON/Markdown 作为事实来源 |
| 发布门禁过硬 | 自动 block 但无理由 | release reasons 和 override |
| 发布门禁过软 | 退化仍然 promote | regression rules 和 critical samples |

## 验收清单

Eval 迁移至少确认：

- [ ] run bundle 仍然完整
- [ ] sample outputs、sample summary、sample analysis 仍然可读
- [ ] compare 仍然校验 task 一致性
- [ ] compare 仍然记录 changed settings
- [ ] release recommendation 有理由
- [ ] run index 和 comparison index 仍然能聚合历史
- [ ] leaderboard 不混淆 backend/few-shot
- [ ] 新 judge 配置写入产物
- [ ] dashboard 或新视图能回到 artifact
- [ ] `PYTHON=.venv/bin/python make eval-test` 通过
- [ ] `PYTHON=.venv/bin/python make infra-smoke` 通过

## 应该更新的文档

- [eval-module](/06-projects/03-eval-module)
- [Run、Compare、History](/04-evaluation-observability/01-run-compare-history)
- [Benchmark、Leaderboard 与 Observability](/04-evaluation-observability/02-benchmark-leaderboard-observability)
- [模型发布判断案例](/11-case-studies/02-model-release-decision-walkthrough)
- [API Surface 速查](/09-reference/05-api-surface)
- [CLI Surface 速查](/09-reference/06-cli-surface)
- [产物与文件索引](/09-reference/03-artifacts-and-files)

## 常见误区

### “Dashboard 有了，JSON/Markdown 就不用保留”

不建议。
dashboard 是视图，JSON/Markdown 是可审查证据。

### “LLM-as-judge 更智能，所以不用记录配置”

相反。
LLM judge 更需要记录模型版本、prompt、参数和 rubric。

### “Leaderboard 第一就可以发布”

不够。
发布判断需要 compare、sample analysis、成本、延迟和场景风险。

### “Run history 只是临时日志”

不是。
它是 leaderboard、run index、趋势分析和 release decision 的基础。

### “人工 review 和自动 eval 是两套东西”

不应该完全割裂。
人工 review 也应该能进入历史和 comparison 证据链。

## 学完应该能回答

读完这一页后，你应该能回答：

1. Eval 系统迁移时哪些产物最应该保留？
2. 为什么 judge 配置必须进入 run bundle？
3. Release recommendation 为什么应该是策略层，而不是黑箱字符串？
4. Dashboard 应该如何和 JSON/Markdown 证据共存？
5. 为什么 eval 最终要和 gateway/platform entrypoint 连接？

## 继续阅读

- [Run、Compare、History](/04-evaluation-observability/01-run-compare-history)
- [Benchmark 与生产质量不是一回事](/04-evaluation-observability/08-benchmark-vs-production-quality)
- [从 Run 到发布判断](/04-evaluation-observability/07-from-run-to-release-decision)
- [验证矩阵](/09-reference/07-validation-matrix)
