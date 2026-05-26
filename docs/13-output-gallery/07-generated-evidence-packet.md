# 自动生成证据包

这页说明新加入的证据包生成器怎么用。

前面的证据库页面告诉你“应该看什么”。证据包生成器进一步做了一件事：

> 把 smoke 过程中留下的 Serving、Gateway、Eval、Finetune 产物自动汇总成一份可以复盘和分享的 JSON / Markdown。

## 什么时候用它

适合这些场景：

- 你刚跑完 `make infra-smoke`
- 你要整理一次端到端复盘
- 你准备公开演示项目
- 你想把本轮运行证据贴进 PR、issue 或学习者工作簿

它不替代人工理解，但能帮你把证据集中到一个入口。

## 证据包解决的具体问题

手动复盘时，最常见的问题不是没有证据，而是证据散落在多个目录里：

- Serving / Gateway 的证据在 smoke snapshot 里。
- Eval 的证据在 result、bundle、history 和 leaderboard 里。
- Finetune 的证据在 run manifest、checkpoint index、export manifest 和 registry 里。
- 发布复盘还需要把这些内容重新组织成一段人能读懂的话。

证据包生成器做的事情，就是把这些分散证据收敛成一个“索引层”。它不会替你判断系统是否生产可用，但会帮你快速回答：

- 本轮 smoke 是否覆盖了四个项目。
- 哪些证据已经生成。
- 哪些关键证据缺失。
- Eval 的发布建议是什么。
- Finetune 的 export 是否成功。
- 复盘时应该从哪些文件继续展开。

把它理解成“复盘入口”，不要理解成“最终报告”。最终报告仍然需要你写结论、说明风险和下一步。

## 命令

先跑 smoke：

```bash
PYTHON=.venv/bin/python make infra-smoke
```

smoke 会在 `.tmp/smoke` 下生成服务快照、eval 产物、finetune 产物和证据包：

```text
.tmp/smoke/
  serving/
  eval/
  finetune/
  evidence/
```

你也可以单独重新生成证据包：

```bash
PYTHON=.venv/bin/python make infra-evidence
```

默认输出：

```text
.tmp/evidence/evidence_packet.json
.tmp/evidence/evidence_packet.md
```

如果你想指定 smoke 目录和输出位置：

```bash
PYTHON=.venv/bin/python scripts/build_evidence_packet.py \
  --smoke-dir .tmp/smoke \
  --output .tmp/evidence/evidence_packet.json \
  --markdown-output .tmp/evidence/evidence_packet.md \
  --strict
```

## 证据包里有什么

`evidence_packet.json` 会包含三大 section：

| Section | 来源 | 说明 |
| --- | --- | --- |
| `serving_gateway` | `.tmp/smoke/serving` | health、model list、metrics、events summary、request timeline |
| `eval` | `.tmp/smoke/eval` | baseline、sample summary、sample analysis、comparison、leaderboard、run/comparison index |
| `finetune` | `.tmp/smoke/finetune` | run manifest、dataset summary、checkpoint index、export manifest、run/export index |

顶层 summary 会给出：

- 哪些 section 可用
- 缺了多少证据文件
- eval 的 release recommendation
- finetune export status

## 15 分钟读法

如果你刚生成了一份证据包，不需要从头读完整 JSON。可以按这个顺序看：

1. 先看 `summary`，确认本轮证据是否完整。
2. 再看 `missing_artifacts`，确认有没有关键缺口。
3. 看 `serving_gateway.health`，确认两个服务是否都健康。
4. 看 `serving_gateway.events`，确认请求和失败是否有 timeline。
5. 看 `eval.comparison.release_recommendation`，确认质量判断建议。
6. 看 `eval.sample_analysis`，确认样本级风险。
7. 看 `finetune.export.status` 和 `finetune.export.lineage`，确认训练产物来源。
8. 最后打开 Markdown 摘要，看它是否足够贴进 PR 或学习复盘。

这 8 步能让你快速判断：这份 evidence packet 是可以用于公开复盘，还是只能作为本地调试材料。

## 关键字段怎么看

### Serving / Gateway

重点看：

- `health.inference_status`
- `health.gateway_status`
- `health.gateway_upstream_services`
- `models.inference_model_ids`
- `models.gateway_model_ids`
- `events.gateway_status_code_counts`
- `metrics.inference_metric_names`
- `metrics.gateway_metric_names`

它们能帮你确认：

- 服务是否启动
- gateway 是否能探测 upstream
- 模型列表是否暴露正确
- request / failure / metrics 是否留下了可观察证据

如果这里缺数据，通常说明 smoke 没有成功跑完、服务没有启动，或 snapshot 路径不对。不要直接跳到 eval/finetune，因为请求链路证据不完整时，端到端复盘的地基就不稳。

### Eval

重点看：

- `run.task`
- `run.model`
- `run.accuracy`
- `sample_summary.pass_rate`
- `comparison.verdict`
- `comparison.release_recommendation`
- `indexes.verdict_counts`

它们能帮你确认：

- 这次 eval 是什么任务、什么模型、什么 backend
- 样本层是否有失败
- candidate 是否达到发布门禁
- comparison history 里当前判断分布如何

这里最容易误读的是 `release_recommendation`。`approve` 不是“直接上线”，而是“离线比较结果和当前设置支持进入下一阶段”。你仍然需要看样本、任务覆盖、生产风险和回滚路径。

### Finetune

重点看：

- `run.method`
- `run.dataset_id`
- `dataset.dataset_version`
- `checkpoint.latest_checkpoint`
- `checkpoint.adapter_model_sha256`
- `export.status`
- `export.lineage`

它们能帮你确认：

- 训练 run 是否能追溯到 dataset
- checkpoint 是否有可校验指纹
- export 是否成功
- adapter 是否能追溯回 checkpoint、dataset 和训练参数

如果 `export.status` 是 success，但 lineage 缺 dataset 或 checkpoint 信息，就不要把它当成完整训练证据。训练产物的价值不仅在于文件存在，还在于能追溯来源。

## 完整度怎么判断

可以用下面三档判断一份证据包。

| 档位 | 表现 | 适合用途 |
| --- | --- | --- |
| Partial | 有 section 缺失或 missing artifacts 较多 | 本地排障 |
| Complete | Serving/Gateway、Eval、Finetune 三类证据齐全 | PR 复盘、学习记录 |
| Review-ready | 证据齐全，Markdown 摘要能说明结论和边界 | 公开演示、Capstone、release brief |

如果目标是公开分享，至少要达到 Complete；如果要做首发 release 或正式演示，最好达到 Review-ready。

## Markdown 证据包

`evidence_packet.md` 是给人看的轻量摘要，适合贴进：

- 学习复盘
- PR 描述
- issue 评论
- 公开演示讲稿

如果你要做更完整的复盘，再对照：

- [端到端复盘证据包](/13-output-gallery/04-end-to-end-review-packet)
- [复盘与评审模板](/14-workshop-kit/04-review-templates)

## 在 PR 里怎么引用

一个简洁的 PR 片段可以这样写：

```text
## Evidence

- Generated evidence packet: `.tmp/evidence/evidence_packet.md`
- Serving/Gateway: health OK, request timeline available
- Eval: release recommendation = `review`
- Finetune: export status = `success`, lineage includes dataset version and checkpoint

## Remaining risk

- Evidence is from learning smoke, not production traffic.
- Eval sample count is small; production release would require broader evaluation.
```

这样写比单独贴 “public-check passed” 更有信息量。它告诉 reviewer：你不只是跑了命令，也知道证据的边界。

## Strict 模式

加上 `--strict` 后，只要缺少关键证据文件，脚本就会失败。

这适合 CI、smoke 或发布前检查，因为你希望第一时间知道：

- serving snapshot 没有生成
- eval comparison 缺失
- finetune export manifest 缺失
- 某个 JSON 文件损坏

如果只是临时本地整理，可以不加 `--strict`。脚本会生成 partial packet，并在 `missing_artifacts` 里列出缺失项。

## 常见问题

### evidence packet 缺 serving_gateway

优先确认 `make infra-smoke` 是否完整执行，以及 `.tmp/smoke/serving` 是否存在。Serving/Gateway 证据通常来自 smoke snapshot，不是凭空生成。

### Eval 有 run，但没有 comparison

说明你有单次评测结果，但缺少发布判断层。补跑 compare 或完整 smoke，再重新生成证据包。

### Finetune 有 run，但 export status 缺失

说明训练产物链路没有走到交付资产。复盘时可以说明训练 run 存在，但不要声称 adapter 已经可用于后续 eval。

### Markdown 摘要太短

Markdown 是索引摘要，不是完整文章。如果要公开分享，需要继续使用 [端到端复盘证据包](/13-output-gallery/04-end-to-end-review-packet) 把关键字段写成解释。

## 它不能证明什么

证据包能证明“这套学习链路的本轮输出是否完整”，但不能证明：

- 真实模型质量足够好
- 生产延迟达标
- fallback 策略已经生产可用
- mock finetune 产物可以直接上线

这些仍然需要真实后端、真实数据和生产观测。

## 下一步

如果你刚生成了一份证据包，建议接着做三件事：

1. 把 Markdown 摘要贴进 [学习者工作簿](/14-workshop-kit/02-learner-workbook)
2. 用 [失败症状到证据地图](/13-output-gallery/05-failure-evidence-map) 检查有没有异常
3. 用 [Capstone 答辩稿](/10-assessments/04-capstone-defense) 练习讲清这份证据
