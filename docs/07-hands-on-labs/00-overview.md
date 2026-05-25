# 深度实战总览

这一组 lab 是为了把学习网站从“能读”推进到“能练”。

前面的章节会告诉你 AI Infra 有哪些层、每层为什么存在。  
这一组 lab 则要求你真的动手观察、修改、验证和复盘。

## 使用方式

每个 lab 都按同一套结构组织：

- 学习目标
- 前置知识
- 代码入口
- 操作步骤
- 观察点
- 扩展任务
- 验收标准

建议你不要一次做完所有 lab。更好的节奏是：

1. 做一个 lab
2. 跑一次 `infra-check`
3. 对照 [示例输出与证据库](/13-output-gallery/00-overview) 看懂关键输出
4. 写下你观察到的系统行为
5. 再进入下一个 lab

## Lab 列表

### Lab 1：Serving 可观测性

入口：[Serving 可观测性 Lab](/07-hands-on-labs/01-serving-observability-lab)

你会观察一次请求如何影响：

- `/v1/chat/completions`
- streaming SSE
- `/metrics`
- `x-request-id`
- engine adapter 错误语义

适合建立执行层直觉。

### Lab 2：Gateway 韧性

入口：[Gateway 韧性 Lab](/07-hands-on-labs/02-gateway-resilience-lab)

你会观察 gateway 如何处理：

- 鉴权失败
- 模型不存在
- 限流
- 下游 5xx
- fallback
- streaming error event
- cache 命中

适合建立治理层直觉。

### Lab 3：Eval 发布门禁

入口：[Eval 发布门禁 Lab](/07-hands-on-labs/03-eval-release-gate-lab)

你会把一次评测结果变成一个发布判断：

- 运行 benchmark
- 保存 run bundle
- 生成 comparison
- 设置 `min_delta`
- 避免不同 task 混比
- 复盘 history

适合建立质量闭环直觉。

### Lab 4：Finetune 复现资产

入口：[Finetune 复现资产 Lab](/07-hands-on-labs/04-finetune-reproducibility-lab)

你会检查一次训练 run 是否留下足够资产：

- dataset summary
- training args
- metrics
- logs
- checkpoint
- artifacts manifest
- export manifest

适合建立训练工程资产直觉。

### Lab 5：系统 Capstone

入口：[系统 Capstone 与验收 Rubric](/07-hands-on-labs/05-capstone-review-rubric)

你会把四层串起来，形成一份可以对外展示的系统解释：

- 执行层
- 治理层
- 质量层
- 训练层
- 失败路径
- 验收命令

适合在准备分享、写博客、做 GitHub README 前完成。

### Lab 6：公开发布验收

入口：[公开发布验收 Lab](/07-hands-on-labs/06-public-release-readiness-lab)

你会从公开读者视角检查这个仓库是否已经准备好分享：

- 首页和 README 是否能说明定位
- 课程路线、两周计划、lab、自测是否互相连通
- 文档站是否能构建
- `infra-check`、`infra-smoke`、依赖安全审计是否通过
- 学习型边界是否写清楚

适合在上传 GitHub、配置 Pages、写公开介绍前完成。

### 配套：示例输出与证据库

入口：[示例输出与证据库](/13-output-gallery/00-overview)

它不是一个额外 lab，而是每个 lab 后面的复盘工具：

- Serving / Gateway lab 后看 header、metrics、events 和 timeline
- Eval lab 后看 sample outputs、sample analysis、compare 和 leaderboard
- Finetune lab 后看 run manifest、checkpoint index、export manifest 和 registry report
- Capstone 前整理一份端到端复盘证据包

## 推荐顺序

如果你是第一次做：

1. Lab 1
2. Lab 2
3. Lab 3
4. Lab 4
5. Lab 5
6. Lab 6
7. 示例输出与证据库

如果你已经有后端经验，但 AI Infra 经验不多：

1. Lab 2
2. Lab 1
3. Lab 3
4. Lab 5

如果你更关心模型迭代：

1. Lab 3
2. Lab 4
3. Lab 1
4. Lab 5
5. Lab 6

## 通用验收命令

每做完一个 lab，至少跑：

```bash
PYTHON=.venv/bin/python make infra-check
```

如果改到了跨服务链路，再跑：

```bash
PYTHON=.venv/bin/python make infra-smoke
```

这两个命令不是形式主义。它们能帮你确认：

- 文档没有断链
- 单元测试没有回退
- 四个项目的最小闭环仍然成立

## 复盘模板

每做完一个 lab，可以用这个模板复盘：

```text
我今天改动或观察的是哪一层：

它的上游是谁：

它的下游是谁：

正常路径是什么：

失败路径是什么：

我用什么命令验证：

我看到哪些产物或指标变化：

如果要走向生产系统，下一步还缺什么：
```

真正的学习不只是“命令通过”，而是你能把这些问题回答清楚。

如果你做完 lab 后想进一步验收自己，可以进入 [学习自测总览](/10-assessments/00-overview)。  
那里会把系统地图、Serving、Gateway、Eval、Finetune 和 Capstone 拆成更具体的答题与演示任务。
