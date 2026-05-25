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

## Markdown 证据包

`evidence_packet.md` 是给人看的轻量摘要，适合贴进：

- 学习复盘
- PR 描述
- issue 评论
- 公开演示讲稿

如果你要做更完整的复盘，再对照：

- [端到端复盘证据包](/13-output-gallery/04-end-to-end-review-packet)
- [复盘与评审模板](/14-workshop-kit/04-review-templates)

## Strict 模式

加上 `--strict` 后，只要缺少关键证据文件，脚本就会失败。

这适合 CI、smoke 或发布前检查，因为你希望第一时间知道：

- serving snapshot 没有生成
- eval comparison 缺失
- finetune export manifest 缺失
- 某个 JSON 文件损坏

如果只是临时本地整理，可以不加 `--strict`。脚本会生成 partial packet，并在 `missing_artifacts` 里列出缺失项。

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
