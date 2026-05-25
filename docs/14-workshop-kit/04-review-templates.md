# 复盘与评审模板

这页提供几组可以直接复用的模板，帮助你把学习过程、公开演示、PR 和 issue 都收敛到“证据驱动”的表达。

模板不是为了增加形式感，而是为了避免复盘变成一句“跑通了”。

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

## 内容评审清单

评审文档或学习材料时，优先看这些问题：

- 新页面是否有清楚的目标读者
- 是否链接到前置页面和后续页面
- 是否有可运行命令或可观察证据
- 是否说明了失败时该看哪里
- 是否避免把学习型项目说成生产平台
- 如果新增页面，是否更新 nav/sidebar/README
- 是否通过 `make docs-quality`

## 工程评审清单

评审代码或脚本时，优先看这些问题：

- 是否保持项目边界清晰
- 是否有测试覆盖关键路径
- 是否更新了 API 或 CLI 文档
- 是否保留 request id、manifest、history 等可观测或可复现信息
- 是否影响 `infra-smoke`
- 是否有新的敏感信息风险

## 公开演示复盘清单

演示前检查：

- 我能在 1 分钟内说清项目定位
- 我能打开文档站首页
- 我能指向学习路线和 hands-on labs
- 我能展示一条请求证据链
- 我能展示一个 eval 或 finetune 产物
- 我能说明当前项目不是生产平台
- 我能指出下一阶段路线

演示后记录：

```text
观众最关心的问题：

最容易误解的地方：

最有说服力的证据：

下次要提前准备的内容：
```
