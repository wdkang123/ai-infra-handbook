# 课程大纲

这页把整个学习站整理成一套可以连续学习的课程。

如果你准备把它分享给别人，可以直接把这页当成“课程目录”。  
如果你自己学习，也可以用它安排一到两周的节奏。

## 课程定位

这不是模型算法课，也不是生产运维课。

它更像一门 AI Infra 工程入门课，目标是帮你建立四个核心直觉：

- 模型如何被服务出来
- 请求如何被平台治理
- 结果如何被评测和比较
- 训练产物如何被资产化
- 输出证据如何被整理成复盘
- 个人学习如何组织成可公开分享的共学材料

课程设计原则是：

- 先系统地图，后实现细节
- 先跑通闭环，后深入单点
- 先建立分层直觉，后替换真实组件
- 每个阶段都用自测确认自己不是只“看过”

## 适合的学习前提

你不需要已经做过 AI Infra，但最好具备：

- 能读懂基础 Python
- 理解 HTTP request / response
- 会在终端执行命令
- 知道什么是大模型 API

如果这些还不熟，也可以学，只是建议放慢节奏，多做 lab。

## 学习成果

学完后，你应该能做到：

- 解释 AI Infra 的执行层、治理层、质量层、训练层
- 跑通本地文档站和四项目 smoke
- 用 gateway 调用 inference-service
- 解释 `401 / 404 / 429 / 502` 的系统语义
- 解释普通响应和 streaming 的差别
- 生成 eval run / comparison bundle
- 理解 release recommendation 为什么只是门禁建议
- 理解 finetune run manifest 和 export manifest
- 理解 dataset role stats 和 export lineage
- 能把 header、events、JSON report 和 manifest 整理成复盘证据包
- 能用工作簿、议程和模板组织一次小规模共学或公开演示
- 看懂这个学习型实现离生产系统还差什么

## 模块 0：建立地图

目标：先知道自己在学什么，不急着看代码。

必读：

1. [从 0 到 1 学习路径](/00-overview/00-zero-to-one)
2. [什么是 AI Infra](/00-overview/01-what-is-ai-infra)
3. [学习路线图](/00-overview/02-learning-route)
4. [面向分享的学习方式](/00-overview/11-public-learning-guide)
5. [项目成熟度地图](/00-overview/14-project-maturity-map)
6. [示例输出与证据库](/13-output-gallery/00-overview)
7. [共学与公开分享套件](/14-workshop-kit/00-overview)

必做：

- 打开文档站
- 浏览首页、路线图、项目总览
- 写下你理解的四层系统地图
- 如果你想按节奏学，先把 [两周学习计划](/00-overview/15-two-week-learning-plan) 加到自己的日程里

验收：

- 你能用 3 分钟解释这个仓库为什么分成四个项目
- 你能完成 [系统地图自测](/10-assessments/01-system-map-check)

## 模块 1：跑通最小闭环

目标：不要只读，先让系统跑起来。

必读：

1. [最小运行手册](/00-overview/03-runbook)
2. [第一次实操演练](/00-overview/04-first-walkthrough)
3. [四个项目怎么连成系统](/06-projects/06-end-to-end-system-map)

必做：

```bash
PYTHON=.venv/bin/python make infra-check
PYTHON=.venv/bin/python make infra-smoke
```

验收：

- 你知道 `infra-check` 和 `infra-smoke` 分别验证什么
- 你能找到四个项目的入口文件

## 模块 2：推理服务层

目标：理解模型服务本体的最小边界。

必读：

1. [模型、Token、Context](/01-llm-fundamentals/01-model-token-context)
2. [Prefill、Decode、KV Cache](/01-llm-fundamentals/02-prefill-decode-kv-cache)
3. [从请求到首个 Token](/01-llm-fundamentals/04-from-request-to-first-token)
4. [inference-service](/06-projects/01-inference-service)

必做：

- 启动 inference-service
- 发送普通 chat completion
- 发送 streaming 请求
- 查看 `/metrics`
- 完成 [Serving 可观测性 Lab](/07-hands-on-labs/01-serving-observability-lab)

验收：

- 你能解释为什么 inference-service 不做平台鉴权
- 你能解释 engine adapter 的作用
- 你能解释 streaming error 为什么不能完全等同普通 JSON error
- 你能完成 [Serving 与 Gateway 自测](/10-assessments/02-serving-gateway-quiz) 里的 Serving 部分

## 模块 3：平台治理层

目标：理解 gateway 为什么不是普通代理。

必读：

1. [鉴权、路由、限流](/03-ai-gateway-platform/01-auth-routing-rate-limit)
2. [Gateway、Router、Fallback、Cache](/03-ai-gateway-platform/03-gateway-router-fallback-cache)
3. [Streaming、错误路径、Upstream Health](/03-ai-gateway-platform/04-streaming-errors-upstream-health)
4. [ai-gateway](/06-projects/02-ai-gateway)

必做：

- 发送正常 gateway 请求
- 触发 `401 / 404 / 429`
- 观察 `/health` 的 upstream status
- 完成 [Gateway 韧性 Lab](/07-hands-on-labs/02-gateway-resilience-lab)

验收：

- 你能解释 gateway 和 inference-service 的边界
- 你能解释 fallback 为什么不是万能重试
- 你能解释 cache 为什么要按 token 隔离
- 你能完成 [Serving 与 Gateway 自测](/10-assessments/02-serving-gateway-quiz) 里的 Gateway 部分

## 模块 4：评测与发布判断

目标：理解评测不是一个分数，而是一套判断流程。

必读：

1. [Run、Compare、History](/04-evaluation-observability/01-run-compare-history)
2. [LLM Evaluation](/04-evaluation-observability/05-llm-evaluation)
3. [从 Run 到发布决策](/04-evaluation-observability/07-from-run-to-release-decision)
4. [eval-module](/06-projects/03-eval-module)

必做：

- 跑一次 eval run
- 跑一次 compare
- 生成一次 leaderboard
- 查看 run bundle 和 comparison bundle
- 完成 [Eval 发布门禁 Lab](/07-hands-on-labs/03-eval-release-gate-lab)

验收：

- 你能解释 run 和 compare 的区别
- 你能解释 `min_delta` 的意义
- 你能解释 `release_recommendation` 的三种结果
- 你能解释 sample outputs 和 sample summary 的区别
- 你能解释 leaderboard 为什么是展示层
- 你能解释为什么不同 task 不能直接比较
- 你能完成 [Eval 与 Finetune 自测](/10-assessments/03-eval-finetune-quiz) 里的 Eval 部分

## 模块 5：训练与复现资产

目标：理解训练工程不是只保存权重。

必读：

1. [LoRA、QLoRA、PEFT](/05-finetuning-training/01-lora-qlora-peft)
2. [训练产物、Checkpoint、Export](/05-finetuning-training/02-run-artifacts-export)
3. [实验追踪、History、复现](/05-finetuning-training/06-experiment-tracking-history-reproducibility)
4. [finetune-demo](/06-projects/04-finetune-demo)

必做：

- 跑一次 finetune train
- 查看 dataset summary
- 查看 dataset registry
- 生成 dataset registry report
- 查看 artifacts manifest
- 跑一次 export
- 完成 [Finetune 复现资产 Lab](/07-hands-on-labs/04-finetune-reproducibility-lab)

验收：

- 你能解释为什么训练 run 是一个资产目录
- 你能解释 `sha256` 和 `size_bytes` 的价值
- 你能解释 dataset registry、dataset role stats、dataset version 和 export lineage 的价值
- 你能解释 export 为什么应该独立于 train
- 你能完成 [Eval 与 Finetune 自测](/10-assessments/03-eval-finetune-quiz) 里的 Finetune 部分

## 模块 6：Capstone

目标：把整套系统讲清楚。

必读：

1. [学习检查点](/00-overview/09-learning-checkpoints)
2. [系统 Capstone 与验收 Rubric](/07-hands-on-labs/05-capstone-review-rubric)
3. [Capstone 答辩稿](/10-assessments/04-capstone-defense)
4. [示例输出与证据库](/13-output-gallery/00-overview)
5. [公开发布验收 Lab](/07-hands-on-labs/06-public-release-readiness-lab)
6. [案例复盘总览](/11-case-studies/00-overview)
7. [共学与公开分享套件](/14-workshop-kit/00-overview)
8. [生产迁移路线总览](/12-production-migration/00-overview)

必做：

- 写一份系统说明
- 整理一份端到端复盘证据包
- 至少读完一个案例复盘，并按案例模板写一次自己的判断
- 用 [复盘与评审模板](/14-workshop-kit/04-review-templates) 整理一次公开展示稿
- 写出一条从学习型实现迁移到真实系统的分阶段路线
- 跑通 `infra-check`
- 跑通 `infra-smoke`
- 对照 rubric 判断自己在哪个 level
- 用 [参考答案与讲解](/10-assessments/05-answer-key) 复盘至少 3 个答不稳的问题
- 用 [验证矩阵](/09-reference/07-validation-matrix) 判断自己的改动该跑哪些检查
- 如果准备公开仓库，跑完发布前验收并记录当前边界

验收：

- 你能给别人讲清楚这个仓库
- 你知道哪些地方是学习型实现
- 你能提出下一步最值得升级的方向

## 两周学习建议

更详细的逐日安排见 [两周学习计划](/00-overview/15-two-week-learning-plan)。

如果每天能投入 1 到 2 小时：

| 天数 | 内容 |
| --- | --- |
| Day 1 | 模块 0，建立地图 |
| Day 2 | 模块 1，跑通闭环 |
| Day 3-4 | 模块 2，推理服务与 Serving Lab |
| Day 5-6 | 模块 3，Gateway 与韧性 Lab |
| Day 7-8 | 模块 4，Eval 与发布门禁 Lab |
| Day 9-10 | 模块 5，Finetune 与复现资产 Lab |
| Day 11 | 读示例输出与案例复盘，整理证据包 |
| Day 12 | 完成 Capstone 和学习自测 |
| Day 13 | 读共学套件，整理工作簿、复盘模板和发布计划 |
| Day 14 | 做公开发布验收 Lab，并自选一个扩展任务补测试 |

如果你时间更少，最小路线是：

1. 模块 0
2. 模块 1
3. Lab 2
4. Lab 3
5. Capstone

这样也能建立一个相对完整的 AI Infra 系统感。
