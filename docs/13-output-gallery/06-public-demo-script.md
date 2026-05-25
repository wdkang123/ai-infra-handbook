# 公开演示脚本

## 这一页适合谁

如果你准备把这个项目发到 GitHub、写文章、录视频或给同学/同事讲，这页可以当成演示脚本。

目标不是炫技，而是在 10 到 20 分钟内讲清楚：

- 这个项目解决什么学习问题
- 四个子项目怎么分层
- 一条请求怎么走
- eval 和 finetune 为什么不是孤立工具
- 当前实现和生产系统差在哪里

## 10 分钟版本

### 0-1 分钟：定位

讲法：

```text
这是一个学习型 AI Infra 手册，不是生产平台。
它把文档站、四个可运行项目、hands-on labs、案例复盘和验证命令收在一起。
```

打开：

- [首页](/)
- [从 0 到 1 学习路径](/00-overview/00-zero-to-one)

### 1-3 分钟：系统地图

讲四层：

| 层级 | 项目 | 说明 |
| --- | --- | --- |
| 执行层 | inference-service | 模型服务入口 |
| 治理层 | ai-gateway | 鉴权、路由、限流、fallback |
| 质量层 | eval-module | run、compare、leaderboard |
| 训练层 | finetune-demo | train、checkpoint、export |

打开：

- [四个项目怎么连成系统](/06-projects/06-end-to-end-system-map)

### 3-5 分钟：请求链路

演示：

```bash
PYTHON=.venv/bin/python make infra-smoke
```

讲法：

```text
smoke 不只是跑一个服务，而是覆盖 gateway、inference、eval、finetune 的最小闭环。
```

然后展示：

- `x-request-id`
- `x-upstream-model`
- `/events/requests`
- `/metrics`
- `.tmp/smoke/evidence/evidence_packet.md`

参考：

- [Serving 与 Gateway 输出证据](/13-output-gallery/01-serving-gateway-evidence)
- [自动生成证据包](/13-output-gallery/07-generated-evidence-packet)

### 5-7 分钟：评测证据

讲法：

```text
eval 不应该只剩一个分数。
这里会留下 result、sample outputs、sample summary、sample analysis、compare 和 leaderboard。
```

展示：

- `sample_analysis.json`
- `comparison_index.json`
- `leaderboard.json`

参考：

- [Eval 报告证据](/13-output-gallery/02-eval-report-evidence)

### 7-9 分钟：训练资产

讲法：

```text
finetune 不应该只留下 checkpoint。
可复现训练至少要有 dataset summary、run manifest、checkpoint index 和 export manifest。
```

展示：

- `run_manifest.json`
- `checkpoint_index.json`
- `export_manifest.json`

参考：

- [Finetune 产物证据](/13-output-gallery/03-finetune-artifact-evidence)

### 9-10 分钟：边界和下一步

讲法：

```text
当前项目适合学习、教学、复盘和渐进式改造。
下一步不是把所有东西一次生产化，而是保住接口、观测和验证，再逐层替换真实后端、真实 judge、真实 trainer。
```

打开：

- [生产迁移路线总览](/12-production-migration/00-overview)
- [项目成熟度地图](/00-overview/14-project-maturity-map)

## 20 分钟版本

如果时间更充足，增加三段：

### 加一段：失败排查

演示一个 `401` 或 `404`：

```bash
curl -i -X POST http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"unknown-model","messages":[{"role":"user","content":"hi"}]}'
```

然后查：

```bash
curl -s "http://localhost:8080/events/failures"
```

讲清楚：

- gateway 错误语义
- failure summary
- request timeline

### 加一段：模型发布判断

展示：

- `compare.json`
- `comparison_index.json`
- `release_recommendation`

讲清楚：

- 为什么比较前要检查 task
- 为什么 min delta threshold 能避免噪声
- 为什么 recommendation 不是生产批准

### 加一段：训练到 eval 的资产链

展示：

```text
dataset_summary -> run_manifest -> checkpoint_index -> export_manifest -> eval run
```

讲清楚：

- export 必须能追溯 checkpoint
- checkpoint 必须能追溯 run
- run 必须能追溯 dataset
- eval 结果必须能追溯模型来源

## 演示前检查

演示前先跑：

```bash
nvm use
PYTHON=.venv/bin/python make infra-format
PYTHON=.venv/bin/python make docs-quality
PYTHON=.venv/bin/python make infra-check
PYTHON=.venv/bin/python make infra-smoke
PYTHON=.venv/bin/python make infra-evidence
npm audit --omit=dev --audit-level=moderate
```

如果时间紧，至少跑：

```bash
PYTHON=.venv/bin/python make infra-check
PYTHON=.venv/bin/python make infra-smoke
```

## 演示时不要说什么

避免这些说法：

| 不建议说 | 建议说 |
| --- | --- |
| 这是生产级 AI 平台 | 这是学习型 AI Infra 手册 |
| 这个模型效果更好 | 当前 eval evidence 支持这个 candidate 通过门禁 |
| 训练已经真实完成 | 当前训练路径用于学习资产结构 |
| smoke 证明系统没问题 | smoke 证明最小联调链路没有退化 |

## 演示后可以留下什么

建议留下：

- README 链接
- 学习路线链接
- 示例输出与证据库链接
- 一份复盘证据包
- 一份自动生成的 `evidence_packet.md`
- 一张系统图
- 下一阶段计划

## 关联阅读

- [端到端复盘证据包](/13-output-gallery/04-end-to-end-review-packet)
- [自动生成证据包](/13-output-gallery/07-generated-evidence-packet)
- [公开发布验收 Lab](/07-hands-on-labs/06-public-release-readiness-lab)
- [Capstone 答辩稿](/10-assessments/04-capstone-defense)
- [公开路线图](/08-publication/03-public-roadmap)
