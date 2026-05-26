# 复盘与评审模板

这页提供几组可以直接复用的模板，帮助你把学习过程、公开演示、PR 和 issue 都收敛到“证据驱动”的表达。

模板不是为了增加形式感，而是为了避免复盘变成一句“跑通了”。

一个好的复盘至少要回答四个问题：

1. 我试图验证什么。
2. 我实际看到了什么。
3. 这些证据能支持什么结论。
4. 这些证据还不能支持什么结论。

很多工程学习记录的问题不在于写得短，而在于没有边界。比如“模型效果变好了”就是一个边界不清的结论；“在相同 task、backend、few-shot 设置下，candidate accuracy 高于 baseline 且超过 `min_delta`，但仍缺少线上生产指标”就是一个更可靠的结论。

下面这些模板都围绕这个原则设计：先收证据，再写判断，最后说明剩余风险。

## 学习复盘模板

适合每次完成一个 lab 后填写。

```text
标题：
日期：
学习目标：

我读了哪些页面：

我运行了哪些命令：

我看到的关键输出：

我保存的证据：

这次最重要的理解：

我遇到的问题：

我是怎么定位的：

我还需要补的内容：
```

合格标准：

- 至少包含一个命令
- 至少包含一个输出证据
- 至少包含一个自己的判断
- 不只写“成功”或“失败”

升级标准：

- 能说明这次操作验证了哪条系统边界。
- 能说明哪些证据只是辅助观察，不能直接支持结论。
- 能提出一个下一步可执行问题。

示例：

```text
这次我验证的是 gateway 的 fallback 行为。
我看到主上游失败后，响应 header 中 x-fallback-used=true，x-upstream-model 变成备用模型。
gateway events 中有 fallback_attempt 和 fallback_success。
因此我能确认非流式请求在首个响应前可以 fallback。
但我还不能确认 streaming 已经输出 chunk 后的失败处理，需要继续做 streaming error 练习。
```

## 请求链路复盘模板

适合 Serving 或 Gateway 相关练习。

```text
请求目标：
请求入口：
模型名：
request id：
是否 stream：
是否 fallback：
是否 cache：

响应状态：
响应 header：
gateway events：
gateway summary：
inference events：
metrics：

我对这次请求的解释：

如果这次失败，我会先查：
```

推荐配套页面：

- [Serving 与 Gateway 输出证据](/13-output-gallery/01-serving-gateway-evidence)
- [请求失败排查案例](/11-case-studies/01-request-incident-walkthrough)

请求链路复盘最重要的是把“看到响应”拆成多层证据：

| 证据 | 说明什么 | 不能说明什么 |
| --- | --- | --- |
| HTTP status | 请求最终成功或失败 | 失败属于哪一层 |
| response header | 单次路由、cache、request id 等路径信息 | 长期趋势 |
| gateway events | gateway 内部发生了什么 | inference 内部细节 |
| inference events | 模型服务层发生了什么 | 平台鉴权和路由 |
| metrics | 一段时间内计数变化 | 单条请求完整 timeline |

写复盘时最好至少引用两类证据。只引用 body 通常不够，因为 body 更像业务结果，而不是系统路径。

## Eval 发布判断模板

适合评测练习或模型发布讨论。

```text
评测目标：
baseline：
candidate：
task：
backend：
few-shot：

baseline result：
candidate result：
comparison report：
sample analysis：
leaderboard：

指标变化：
样本层风险：
配置是否可比：
release recommendation：

我的发布判断：

还缺哪些生产证据：
```

合格的发布判断要说明：

1. 分数变化
2. 样本变化
3. 配置是否可比
4. 是否存在回归
5. 是否应该继续观察生产指标

更完整的发布判断可以加一段风险说明：

```text
风险说明：
- 这次 compare 的 task 是否覆盖目标场景：
- 样本量是否足够：
- few-shot / backend / prompt 是否一致：
- 是否存在某类样本退化：
- 是否需要人工 spot check：
- 是否需要线上灰度或回放：
```

这段很重要，因为 eval 很容易被误用成“分数高就发布”。真实发布判断通常是多证据合并：离线分数、样本分析、任务覆盖、生产风险、回滚路径缺一不可。

## Finetune 产物复盘模板

适合训练、导出、复现实验。

```text
训练目标：
base model：
training method：
dataset path：
dataset version：
output dir：

run manifest：
checkpoint index：
export manifest：
export history：
dataset registry：

这次训练能否复现：
export 能否追溯到 checkpoint：
后续 eval 应该记录哪些来源：
```

推荐配套页面：

- [Finetune 产物证据](/13-output-gallery/03-finetune-artifact-evidence)
- [训练产物复现案例](/11-case-studies/03-finetune-to-eval-asset-lineage)

训练产物复盘不要只写 checkpoint 路径。一个更完整的训练复盘应该能追溯：

```text
dataset path -> dataset summary -> dataset version -> run manifest -> checkpoint index -> export manifest -> export history
```

如果这条链断了，就说明后续评测和发布会存在来源不清的问题。学习阶段就养成这种记录习惯，后面接真实训练系统时会轻松很多。

## Capstone 展示模板

适合公开演示或阶段答辩。

```text
1. 我为什么选择这个项目

2. 系统由哪些部分组成

3. 一次请求如何流过系统

4. 我如何观察成功路径

5. 我如何观察失败路径

6. eval 如何支持发布判断

7. finetune 产物如何被复现

8. 当前项目和生产系统的差距

9. 我下一步会怎么推进
```

展示时建议每一段都配一个具体证据，而不是只讲概念。

Capstone 展示最容易犯的错误是把它做成“项目介绍”。更好的方式是把它做成“工程判断展示”。

可以按这个节奏讲：

1. 我先说明系统分层。
2. 我演示一条成功请求，证明链路能通。
3. 我演示一条失败路径，证明边界能观察。
4. 我展示 eval compare，说明发布判断如何形成。
5. 我展示 finetune manifest，说明训练资产如何追溯。
6. 我说明当前项目不是什么，避免过度宣称。
7. 我提出下一步最值得推进的改进。

这样展示出来的不是“我做了很多页面”，而是“我能用证据说明一个 AI Infra 学习系统如何工作”。

## PR 描述模板

仓库已经有 `.github/pull_request_template.md`，下面是更适合学习内容改动的填写方式。

```text
## What changed

- 新增或修改了哪些页面、代码或模板

## Why

- 解决哪个学习卡点
- 改善哪个运行或复盘流程

## Evidence

- 跑过哪些命令
- 看到了哪些输出
- 是否更新了导航、README、sidebar

## Verification

- [ ] PYTHON=.venv/bin/python make infra-format
- [ ] PYTHON=.venv/bin/python make docs-quality
- [ ] PYTHON=.venv/bin/python make infra-check
- [ ] PYTHON=.venv/bin/python make infra-smoke

## Learning impact

- 新读者会更容易理解什么
- 贡献者后续应该注意什么
```

如果 PR 是文档深化，建议额外补两项：

```text
## Depth check

- 这次是否补充了场景：
- 是否补充了机制解释：
- 是否补充了观察方式：
- 是否补充了失败路径或常见误区：
- 是否链接到代码、命令或证据：

## Public-readiness check

- 是否避免个人信息：
- 是否避免密钥、真实 token、私有路径：
- 是否避免把学习型实现说成生产平台：
```

这两项可以防止文档 PR 只是在列表上增加几个项目，而没有真正提升学习深度。

## Issue 记录模板

适合把共学反馈转成 GitHub issue。

```text
## 问题类型

- 文档不清楚
- 命令失败
- 输出证据不足
- lab 任务不完整
- 案例需要补充
- 发布或贡献流程问题

## 发生位置

页面或文件：

## 现象

我看到的是：

## 期望

我希望读者能：

## 证据

命令、输出、截图或日志：

## 建议改法

-
```

更适合公开仓库的 issue 还可以加一个“读者影响”字段：

```text
## 读者影响

这个问题会让新读者：
- 不知道下一步该读哪里
- 不知道命令是否成功
- 不知道输出证据说明什么
- 误解当前项目成熟度
- 无法参与贡献
```

有了读者影响，issue 的优先级会更容易判断。不是所有小问题都要立刻修，但会阻断第一轮学习的问题应该优先处理。

## 内容评审清单

评审文档或学习材料时，优先看这些问题：

- 新页面是否有清楚的目标读者
- 是否链接到前置页面和后续页面
- 是否有可运行命令或可观察证据
- 是否说明了失败时该看哪里
- 是否避免把学习型项目说成生产平台
- 如果新增页面，是否更新 nav/sidebar/README
- 是否通过 `make docs-quality`

### 内容深度评审

如果目标是让页面更像教程而不是提纲，可以继续检查：

- 页面是否解释了“为什么这个主题重要”。
- 页面是否给出一个真实学习场景。
- 页面是否说明读者应该观察哪些输出。
- 页面是否说明常见误区或错误理解。
- 页面是否有完成标准。
- 页面是否能回答“读完后我会做什么”。
- 页面是否和相邻章节形成连续路线。

如果一页只有定义、列表和链接，通常还不够饱满。至少要再补：场景、机制、操作、证据、误区、下一步。

## 工程评审清单

评审代码或脚本时，优先看这些问题：

- 是否保持项目边界清晰
- 是否有测试覆盖关键路径
- 是否更新了 API 或 CLI 文档
- 是否保留 request id、manifest、history 等可观测或可复现信息
- 是否影响 `infra-smoke`
- 是否有新的敏感信息风险

### 工程学习价值评审

这个仓库的代码不只是为了功能，也承担教学职责。评审时可以额外看：

- 新增能力是否能被读者通过命令观察到。
- 失败路径是否有测试。
- 输出是否能进入 evidence 或 case study。
- 变更是否保持四个项目的边界清晰。
- 是否新增了难以解释的隐式行为。
- 是否需要更新文档到代码映射。

如果代码变强了但读者看不懂它验证什么，学习价值也会打折。

## 公开演示复盘清单

演示前检查：

- 我能在 1 分钟内说清项目定位
- 我能打开文档站首页
- 我能指向学习路线和 hands-on labs
- 我能展示一条请求证据链
- 我能展示一个 eval 或 finetune 产物
- 我能说明当前项目不是生产平台

演示后复盘：

```text
这次演示最顺的一段：

听众最困惑的一段：

哪份证据最有说服力：

哪份证据还不够清楚：

有没有出现误解项目成熟度的地方：

下一次演示前要补的页面或脚本：
```

公开演示的价值不只在当场展示，也在于它会暴露读者真正卡住的地方。把这些卡点收回来，网站会持续变厚。
- 我能指出下一阶段路线

演示后记录：

```text
观众最关心的问题：

最容易误解的地方：

最有说服力的证据：

下次要提前准备的内容：
```
