# LLM Evaluation

> 本页解决：LLM 评测如何从单次分数走向发布判断。
> 读完能做：解释 run、compare、sample analysis、leaderboard 和 release recommendation 的关系。
> 关联代码：`projects/eval-module`、`scripts/build_release_brief.py`。
> 验证命令：`PYTHON=.venv/bin/python make infra-smoke`。

LLM Evaluation 的重点不是得到一个漂亮分数，而是回答：

> 这个 candidate 是否有足够证据进入下一阶段？

## 最小证据链

```text
task -> run -> compare -> sample analysis -> recommendation -> release decision
```

| 对象 | 它回答什么 |
| --- | --- |
| run | 这次结果是什么 |
| compare | 相对 baseline 变化是什么 |
| sample analysis | 哪些样本变好或变差 |
| leaderboard | 横向观察结果 |
| recommendation | pass、warn 还是 block |

## 推荐路径

1. [Evaluation Observability 总览](/04-evaluation-observability/00-overview)
2. [Run、Compare、History](/04-evaluation-observability/01-run-compare-history)
3. [从 Run 到发布决策](/04-evaluation-observability/07-from-run-to-release-decision)
4. [Eval Regression Gate 示例](/04-evaluation-observability/09-eval-regression-gate-example)
5. [Eval 发布门禁 Lab](/07-hands-on-labs/03-eval-release-gate-lab)

## 快速验证

```bash
PYTHON=.venv/bin/python make infra-smoke
cat .tmp/smoke/eval/compare.md
cat .tmp/smoke/eval/baseline/sample_analysis.json
```

## FAQ

### 平均分提高就能发布吗

不能。关键样本退化、settings changed、token 成本上涨或 fallback 异常都可能进入 warn / block。

### block 是模型一定更差吗

不是。block 表示当前证据不支持发布，可能是质量退化，也可能是不可比或证据缺失。

### Eval 和 observability 为什么要一起看

因为质量变化可能来自模型，也可能来自 gateway 路由、cache、fallback、timeout 或训练资产不一致。
