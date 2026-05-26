# Eval 与 Finetune 自测

这页检查你是否理解质量闭环和训练资产化。

如果说 Serving 与 Gateway 自测更关注“请求如何运行”，这一页更关注：

> 输出如何被判断，训练结果如何被复现，二者如何连接成能力迭代闭环。

建议先完成：

- [Eval 发布门禁 Lab](/07-hands-on-labs/03-eval-release-gate-lab)
- [Finetune 复现资产 Lab](/07-hands-on-labs/04-finetune-reproducibility-lab)
- [从 Run 到发布决策](/04-evaluation-observability/07-from-run-to-release-decision)
- [数据集、Run、Checkpoint](/05-finetuning-training/04-datasets-runs-checkpoints)

## 通过标准

你可以认为自己通过本页，如果你能做到：

- 解释 eval run、compare、history、leaderboard 的关系
- 说明 `min_delta`、task 校验和 sample evidence 为什么重要
- 解释 dataset registry、run manifest、checkpoint index、export manifest 的边界
- 画出 finetune export 到 eval compare 的链路
- 给一个 candidate 写出 approve / review / block 判断
- 找到对应 CLI、代码和输出产物

## A. Eval 基础题

请用自己的话回答：

1. eval run 和 eval compare 的区别是什么？
2. 为什么 history 比单个 JSON 文件更适合做长期判断？
3. comparison bundle 里应该保留哪些信息？
4. `min_delta` 解决的是什么判断问题？
5. 为什么不同 task 的 run 不应该直接比较？
6. 为什么 Markdown report 和 JSON report 都有价值？
7. `release_recommendation` 为什么仍然需要人工复查？
8. 一个 benchmark 分数变高，为什么不等于可以立刻发布？
9. 如果某个 metric 消失了，compare report 应该怎么表达？
10. leaderboard 为什么应该从 run history 生成？
11. sample outputs 为什么比单个总分更能解释退化？
12. observability 信号如何影响发布判断？

回答时尽量给出一个“如果不这样做会怎样”的反例。

## B. Eval 实操题

运行一次 eval，再运行一次 compare。

然后找到这些产物并解释它们：

| 产物 | 你要说明 |
| --- | --- |
| run JSON | task、metrics、metadata |
| run Markdown | 面向人阅读的摘要 |
| run bundle | 为什么要打包 |
| sample outputs | 样本级输出如何解释分数 |
| sample summary | 样本级结果如何快速汇总 |
| sample analysis | 哪些样本值得复查 |
| history | 如何做长期追踪 |
| comparison JSON | baseline 和 candidate 如何对应 |
| comparison Markdown | 如何帮助发布讨论 |
| leaderboard | 多个模型或多次 run 如何横向观察 |
| release recommendation | approve / review / block 的理由 |

然后回答：

```text
这次 run 的 task 是：
最重要的 metric 是：
如果要作为发布门禁，我会设置的 min_delta 是：
我不敢发布的原因可能是：
我还需要补充看的 sample 是：
```

## C. Eval 场景题

### 场景 1：candidate 比 baseline 高 0.001

请说明：

- 这是否一定意味着 candidate 更好
- `min_delta` 应该如何影响结论
- 你还需要看哪些指标或样本
- 如果 candidate 成本更高，判断是否会改变

### 场景 2：candidate 新增一个 metric

请说明 comparison report 应该如何呈现。

再说明新增 metric 对历史趋势有什么影响。

### 场景 3：baseline 和 candidate 属于不同 task

请说明系统为什么应该直接拒绝。

再说明如果强行比较，会误导哪类决策。

### 场景 4：leaderboard 上 candidate 排名最高

请说明为什么这仍然不等于一定发布。

至少考虑：

- task 是否一致
- backend 是否一致
- few-shot 是否一致
- latest 和 best 的区别
- sample-level regression

## D. Finetune 基础题

请用自己的话回答：

1. LoRA 和全量微调在工程资产上有什么差别？
2. QLoRA 的价值主要体现在哪些资源约束下？
3. PEFT 为什么强调 adapter？
4. SFT 和 DPO 的训练目标有什么不同？
5. 为什么训练 run 需要独立目录？
6. checkpoint 和 export 的区别是什么？
7. manifest 为什么需要记录 `sha256` 和 `size_bytes`？
8. dataset role 统计比单纯记录数多解决了什么问题？
9. dataset schema 校验为什么应该发生在训练前？
10. dataset registry 和 dataset summary 分别解决什么问题？
11. export lineage 如果断了，会影响后续哪个环节？
12. 为什么训练结果最终必须进入 eval？

## E. Finetune 实操题

运行一次训练和导出。

然后找到这些信息：

| 信息 | 你要说明 |
| --- | --- |
| training args | 这次 run 的关键配置 |
| dataset summary | 数据规模、version、role 分布、hash 是否可追踪 |
| dataset registry | 数据输入是否能跨 run 登记和追溯 |
| dataset registry report | 登记表是否能被人读和工具读 |
| metrics | 训练过程是否留下可比较数据 |
| logs | 人如何复盘过程 |
| checkpoint | 训练中间资产在哪里 |
| checkpoint index | 哪些 checkpoint 可用、状态如何 |
| artifacts manifest | 文件完整性如何描述 |
| export manifest | 导出结果是否可复现、是否保留 lineage |
| export history | 多次导出如何横向追踪 |

然后回答：

```text
如果这个 run 三个月后要复现，我还缺什么信息：
如果 export 失败，我会先检查：
如果 dataset schema 不合法，我希望错误发生在：
如果这个 export 要进入 eval，我需要传递哪些 metadata：
```

## F. 跨模块题

请解释下面这条链路：

```text
finetune run -> export -> serving candidate -> eval run -> compare -> release decision
```

要求说明：

- 每一步的输入
- 每一步的输出
- 哪些产物应该被保存
- 哪一步失败会阻止发布
- 哪些失败只是提示需要复查
- 哪些字段应该贯穿 lineage

一个好的回答应该能把训练资产和质量判断连接起来，而不是把 finetune 和 eval 看成两个孤立项目。

## G. 发布判断题

假设一个 adapter 导出成功，并在 eval 中比 baseline 高 0.02，但 sample analysis 发现两个关键样本格式错误。

请写一段判断：

```text
我的建议是：
主要证据是：
主要风险是：
还需要补充验证：
是否可以发布：
```

不要只写“分数高所以发布”。

## H. 加分题

任选一个改进方向，写出设计方案和验证方式：

1. 给 eval-module 增加更真实的 sample-level output
2. 给 comparison report 增加 sample-level summary
3. 给 eval-module 增加 leaderboard best-result 链接
4. 给 finetune-demo 增加 dataset registry 查询命令
5. 增加 export 到 eval 的 handoff manifest

要求说明：

- 你会改哪些文件
- 你会新增哪些测试
- 你会如何更新文档
- 你会跑哪些验证命令

## 复盘模板

完成后写下：

```text
我最理解的 eval 对象是：
我最理解的 finetune 对象是：
我最容易混淆的是：
我能解释的一条 lineage 是：
我下一步要补的证据是：
```

这份复盘会帮助你准备 Capstone。
