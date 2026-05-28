# Eval Regression Gate 示例

> 本页解决：如何把 eval compare 结果转成 pass / warn / block 的发布门禁判断。
> 读完能做：解释 release recommendation 为什么不能只看平均分，以及哪些退化会阻断发布。
> 关联代码：`projects/eval-module`、`scripts/build_release_brief.py`、`scripts/integration_smoke_test.sh`。
> 验证命令：`PYTHON=.venv/bin/python make infra-smoke`。

Regression gate 的目标不是让机器替人发布，而是把“是否可以继续推进”变成可讨论、可复盘、可审查的证据。

## 最小输入

一个 release gate 至少需要：

| 输入 | 说明 |
| --- | --- |
| baseline run | 当前稳定版本或上一个候选 |
| candidate run | 本次要评估的新模型、prompt 或 adapter |
| compare report | delta、threshold、sample analysis、settings changed |
| observability evidence | request id、events、metrics、fallback、timeout |
| asset lineage | 如果来自训练，必须能追溯 dataset、run、checkpoint、export |

如果这些输入缺失，门禁不应该直接 pass。

## pass / warn / block

| Recommendation | 含义 | 典型条件 | 下一步 |
| --- | --- | --- | --- |
| `pass` | 可以进入下一阶段 | 指标不退化，关键样本通过，配置可比，运行证据正常 | 继续小流量、发布准备或公开演示 |
| `warn` | 可以继续 review，但不能无脑发布 | 平均分略升但关键样本有疑点；配置有小变化；token 或 latency 明显变化 | 人工复核样本，补跑局部任务 |
| `block` | 不建议发布 | 关键指标退化、配置不可比、失败样本集中、fallback / timeout 异常、lineage 不一致 | 阻断 release，修复后重新评测 |

## 一个具体示例

假设 compare report：

```json
{
  "baseline": "baseline.json",
  "candidate": "candidate.json",
  "summary": {
    "overall_delta": 0.01,
    "regression_count": 3,
    "settings_changed": false,
    "release_recommendation": "block",
    "release_reasons": [
      "critical samples regressed",
      "factuality score dropped below threshold"
    ]
  }
}
```

这个结果看起来 `overall_delta` 仍然是正数，但 gate 给出 `block` 是合理的，因为平均分不能掩盖关键样本退化。

## Gate 规则示例

这是一个学习型规则，不代表生产标准：

| 条件 | 建议 |
| --- | --- |
| `settings_changed=true` | 至少 `warn` |
| `overall_delta < -min_delta` | `block` |
| `regression_count > 0` 且样本属于核心能力 | `block` |
| `overall_delta` 小幅提升但 completion tokens 增加超过 30% | `warn` |
| gateway fallback 或 timeout 在评测期间出现 | `warn` 或 `block` |
| export manifest lineage mismatch | `block` |
| 所有指标稳定，关键样本无退化，运行证据正常 | `pass` |

## 触发命令

当前 smoke 已经会跑 eval baseline、compare、leaderboard 和 release recommendation：

```bash
PYTHON=.venv/bin/python make infra-smoke
```

如果只想看 eval 模块，可以进入项目目录：

```bash
cd projects/eval-module
PYTHON=../../.venv/bin/python PYTHONPATH=src ../../.venv/bin/python -m eval_module.main run \
  --task mmlu \
  --model Qwen/Qwen2.5-0.5B-Instruct \
  --backend-url http://localhost:8000/v1 \
  --output ../../.tmp/eval/baseline.json
```

再进行 compare：

```bash
cd projects/eval-module
PYTHON=../../.venv/bin/python PYTHONPATH=src ../../.venv/bin/python -m eval_module.main compare \
  --baseline ../../.tmp/eval/baseline.json \
  --candidate ../../.tmp/eval/baseline.json \
  --output ../../.tmp/eval/compare.json
```

## 观察证据

重点查看：

```text
.tmp/smoke/eval/compare.json
.tmp/smoke/eval/compare.md
.tmp/smoke/eval/baseline/sample_outputs.json
.tmp/smoke/eval/baseline/sample_analysis.json
.tmp/smoke/eval/comparison_index.json
.tmp/evidence/evidence_packet.md
```

你应该能回答：

- baseline 和 candidate 是否可比
- task 是否一致
- threshold 是多少
- 是否有 regression
- release recommendation 是 pass、warn 还是 block
- recommendation 的 reason 是否能对应到样本或运行证据

## 与 release brief 的关系

Release brief 不应该只把 eval recommendation 复制出来，而应该解释它对发布意味着什么。

| Eval recommendation | Release brief 口径 |
| --- | --- |
| `pass` | 质量侧没有阻断，但仍需检查安全、文档、证据和公开边界 |
| `warn` | 发布前需要人工 review，说明原因和补测计划 |
| `block` | 不建议发布，必须说明阻断证据、修复路径和重新验证命令 |

## 常见误读

### 平均分提升就一定 pass

不对。关键样本退化、输出成本暴涨、settings changed 或 fallback 异常都可能让结果进入 warn / block。

### block 就说明模型绝对更差

也不对。block 的意思是“当前证据不支持发布”。可能是模型变差，也可能是评测不可比、证据缺失或 lineage 不一致。

### warn 可以忽略

warn 是需要人工审查的信号。公开项目里，warn 至少要留下复盘问题和下一步验证命令。

## 复盘问题

- 这次 gate 的主证据来自 compare、sample analysis、metrics 还是 manifest？
- 如果要把 `warn` 推进到 `pass`，缺哪一条证据？
- 如果要把 `block` 解除，应该改模型、prompt、数据、gateway，还是评测配置？
- release notes 是否如实说明了当前 recommendation？
