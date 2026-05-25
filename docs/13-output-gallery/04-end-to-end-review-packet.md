# 端到端复盘证据包

## 什么是证据包

证据包是一组能讲清一次系统行为的最小材料。

它不是把所有日志和 JSON 都贴出来，而是把关键证据整理成：

1. 我跑了什么
2. 系统经过哪些层
3. 每层留下了什么证据
4. 这些证据能说明什么
5. 这些证据不能说明什么
6. 下一步应该怎么改

如果你准备把项目分享给别人，证据包会比“我做了一个 AI Infra 项目”更有说服力。

## 最小证据包结构

建议每次复盘都按这个结构收集：

| 部分 | 证据 | 来源 |
| --- | --- | --- |
| 环境 | Node/Python/命令结果 | `make infra-check` |
| 请求链路 | request id、header、timeline | gateway / inference |
| 质量判断 | run、sample analysis、compare | eval-module |
| 训练资产 | run manifest、checkpoint index、export manifest | finetune-demo |
| 结论 | 是否通过、风险是什么、下一步是什么 | 人工复盘 |

## 一份可以公开分享的复盘

你可以按下面模板写：

```text
主题：
我验证的是：

系统层级：
- 执行层：
- 治理层：
- 质量层：
- 训练层：

运行命令：
- ...

关键证据：
- request id：
- gateway header：
- event timeline：
- eval sample analysis：
- finetune manifest：

结论：
- 已确认：
- 未确认：
- 下一步：
```

## 请求链路证据

先选一条 request id。

建议固定传：

```bash
X-Request-ID: demo_review_1
```

然后收集：

```bash
curl -s "http://localhost:8000/events/requests/demo_review_1"
curl -s "http://localhost:8080/events/requests/demo_review_1"
```

这两条证据应该能回答：

- 请求是否进入 gateway
- gateway 是否调用了 inference
- gateway 有没有 fallback 或 cache 行为
- inference 是否完成生成
- 两层的 request id 是否能对齐

如果 gateway 有 timeline，inference 没有 timeline，说明请求可能没有打到 inference，或者 request id 没有传递到下游。

## Eval 证据

复盘时不要只写“eval 通过了”。

至少保留：

- `result.json`
- `sample_summary.json`
- `sample_analysis.json`
- `compare.json`
- `leaderboard.json`

写结论时推荐用：

```text
本次 run 的 average score 是：
失败样本数量是：
主要 judge reason 是：
compare verdict 是：
release recommendation 是：
```

这会比只贴一个分数更像工程判断。

## Finetune 证据

如果复盘里包含训练或导出，至少保留：

- `run_manifest.json`
- `dataset_summary.json`
- `checkpoint_index.json`
- `export_manifest.json`
- `run_index.json`
- `export_index.json`

如果你已经跑过 smoke，也可以先用生成器汇总：

```bash
PYTHON=.venv/bin/python make infra-evidence
```

然后打开：

```text
.tmp/evidence/evidence_packet.json
.tmp/evidence/evidence_packet.md
```

写结论时推荐用：

```text
训练数据 sha 是：
训练方法是：
checkpoint index 指向：
export manifest 指向：
adapter hash 是：
```

这样别人才能判断你的结果是否可追溯。

## 证据包应该避免什么

| 不推荐 | 原因 |
| --- | --- |
| 只贴一张终端截图 | 无法检索、无法复盘 |
| 只说 smoke 通过 | 不知道每层留下了什么证据 |
| 只贴完整 JSON | 太长，读者抓不到重点 |
| 只写“模型更好” | 没有说明评测任务和样本 |
| 只写“训练成功” | 没有说明数据、checkpoint 和 export |

更好的方式是：

1. 保留原始产物
2. 摘出关键字段
3. 写清楚解释边界

## README 或分享文章可以怎么写

可以写成：

```text
我跑通了一条最小 AI Infra 闭环：

1. gateway 接收请求并路由到 inference-service
2. inference-service 返回 OpenAI-compatible completion
3. eval-module 生成 run、sample analysis、compare 和 leaderboard
4. finetune-demo 生成 run manifest、checkpoint index 和 export manifest
5. smoke 覆盖 gateway / inference / eval / finetune 的最小链路

证据包括：
- gateway request timeline
- inference metrics
- eval sample_analysis.json
- finetune checkpoint_index.json
- export_manifest.json
```

## 复盘分级

| 等级 | 标准 |
| --- | --- |
| 初级 | 能跑命令，能说成功或失败 |
| 合格 | 能指出每层关键输出 |
| 良好 | 能解释字段含义和系统边界 |
| 优秀 | 能把输出串成一次工程决策 |

## 关联阅读

- [第一次实操演练](/00-overview/04-first-walkthrough)
- [自动生成证据包](/13-output-gallery/07-generated-evidence-packet)
- [系统 Capstone 与验收 Rubric](/07-hands-on-labs/05-capstone-review-rubric)
- [请求失败排查案例](/11-case-studies/01-request-incident-walkthrough)
- [模型发布判断案例](/11-case-studies/02-model-release-decision-walkthrough)
