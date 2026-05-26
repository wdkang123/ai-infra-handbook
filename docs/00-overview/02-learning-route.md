# 学习路线图

## 1. 这页是干什么的

这页不是再讲一遍概念，而是把“你接下来怎么学、怎么跑、先看哪里、再改哪里”串成一条路线。

如果你后面是边看文档边跑代码，这页应该作为总导航入口。

如果你是完全新手，建议先看一遍 [从 0 到 1 学习路径](/00-overview/00-zero-to-one)，再回到这页按模块展开。

这页还有一个隐藏目标：帮你避免“像逛百科一样学习 AI Infra”。AI Infra 的知识点非常容易散开，今天看 serving，明天看 gateway，后天看评测工具，最后脑子里都是名词，但没有系统判断力。这里的路线会尽量把每一步都绑定到一个工程问题和一份可观察证据上。

你可以把它理解成三层路线：

1. 第一层：先知道系统为什么要分层。
2. 第二层：再知道每一层如何通过接口、命令和产物被观察。
3. 第三层：最后知道一次变更如何被验证、复盘和公开分享。

## 2. 推荐顺序

建议按下面顺序推进：

1. 先看从 0 到 1 路线，知道第一轮要完成什么
2. 再看总论，建立整体地图
3. 再看推理服务，理解模型服务本体
4. 再看网关，理解请求治理和代理层
5. 再看评测模块，理解质量闭环
6. 再看微调模块，理解模型能力如何迭代
7. 最后看示例输出，把每一层证据串成复盘
8. 如果准备分享给别人，再看共学套件，把个人学习变成可复用活动

对应仓库位置：

- 新手入口：[从 0 到 1 学习路径](/00-overview/00-zero-to-one)
- 总论：[什么是 AI Infra](/00-overview/01-what-is-ai-infra)
- 推理服务：[inference-service](/06-projects/01-inference-service)
- 网关：[ai-gateway](/06-projects/02-ai-gateway)
- 评测：[eval-module](/06-projects/03-eval-module)
- 微调：[finetune-demo](/06-projects/04-finetune-demo)
- 输出证据：[示例输出与证据库](/13-output-gallery/00-overview)
- 共学分享：[共学与公开分享套件](/14-workshop-kit/00-overview)

## 3. 路线背后的学习逻辑

这条路线不是按“技术名词难度”排序，而是按“工程理解依赖”排序。

你先理解 AI Infra 是什么，是因为后面每个模块都要回到系统分层。如果你不知道 gateway 为什么单独存在，就很容易把它看成普通反向代理；如果你不知道 eval 为什么是质量闭环，就很容易把它看成跑 benchmark 的脚本。

你先跑 inference-service 和 ai-gateway，是因为请求链路最直观。读者能马上看到 HTTP 请求、状态码、header、events、metrics，比较容易建立“系统行为可以被观察”的直觉。

你再看 eval-module，是因为质量判断需要建立在请求链路之后。否则你会只关注一个分数，而看不到 sample outputs、comparison、history 和 release recommendation 对发布决策的价值。

你最后看 finetune-demo，是因为训练资产的意义通常要和 eval、发布、复现连起来才明显。单独看 `train` 命令很容易以为训练只是生成 checkpoint；放到整条链路里，你会看到 dataset version、run manifest、export manifest 和后续 eval 的关系。

输出证据、案例复盘和共学套件放在后面，不代表它们不重要。恰恰相反，它们是把个人学习变成可复用知识的关键。只是第一轮必须先有一些真实操作，否则复盘会变成空泛总结。

## 4. 一轮最小学习闭环

第一轮不追求把所有代码看完，只追求走完一遍最小闭环：

1. 启动 `inference-service`
2. 启动 `ai-gateway`
3. 用 gateway 代理请求到 inference
4. 跑一次 `eval`
5. 跑一次 `finetune`
6. 看看各自留下了什么产物

根级入口：

```bash
cd /path/to/ai-infra
PYTHON=.venv/bin/python make infra-test
PYTHON=.venv/bin/python make infra-smoke
```

如果这两条通过，说明当前最小学习闭环是通的。

如果你准备开始第一次真正动手，下一篇建议直接看：

- [第一次实操演练](/00-overview/04-first-walkthrough)
- [文档与代码怎么对应](/00-overview/05-docs-to-code-map)
- [项目成熟度地图](/00-overview/14-project-maturity-map)
- [两周学习计划](/00-overview/15-two-week-learning-plan)
- [示例输出与证据库](/13-output-gallery/00-overview)
- [学习者工作簿](/14-workshop-kit/02-learner-workbook)

### 最小闭环要留下什么

跑完第一轮之后，至少应该留下这些东西：

| 证据 | 来自哪里 | 用来说明什么 |
| --- | --- | --- |
| `infra-test` 结果 | 根级 Makefile | 单项目测试和脚本测试能跑通 |
| `infra-smoke` 结果 | 集成 smoke | 四个项目之间的学习链路能联动 |
| gateway 请求 header | `ai-gateway` | request id、cache、upstream model 等单次路径证据 |
| gateway / inference events | 两个服务的 `/events` | 请求在不同层发生过什么 |
| eval compare 输出 | `eval-module` | 发布判断如何从 baseline/candidate 得出 |
| finetune manifest | `finetune-demo` | 训练输入、checkpoint、export 是否可追溯 |

如果你没有这些证据，只能说“我看了文档”或“我跑过命令”。有了这些证据，才可以说“我跑通并理解了一条最小 AI Infra 闭环”。

## 5. 每一站你该关注什么

### inference-service

目标：
理解“模型服务本体”最小需要哪些能力。

先看：

- `projects/inference-service/src/inference_service/main.py`
- `projects/inference-service/src/inference_service/server.py`
- `projects/inference-service/src/inference_service/runtime.py`

先跑：

```bash
cd /path/to/ai-infra/projects/inference-service
PYTHONPATH=src ../../.venv/bin/python -m inference_service.main serve
```

你应该看到：

- `/health` 返回服务状态
- `/metrics` 返回动态请求/token 计数
- `/v1/chat/completions` 返回 mock completion

更进一步，你要能解释：

- 为什么 `mock` engine 仍然保留 OpenAI-compatible 响应结构。
- 为什么服务要提供 `/events`，而不是只提供 `/metrics`。
- 为什么普通响应和 streaming 要共享同一个主接口。
- 如果真实 vLLM/SGLang 上游失败，当前 adapter 应该如何把错误表达给调用方。

练习建议：

1. 先打一次普通请求。
2. 再打一次 `stream=true`。
3. 再带 `X-Request-ID`。
4. 对照 `/events/requests/{request_id}` 解释这条请求。

### ai-gateway

目标：
理解“请求进入平台之后，如何被鉴权、路由、限流和代理”。

先看：

- `projects/ai-gateway/src/ai_gateway/server.py`
- `projects/ai-gateway/src/ai_gateway/router.py`
- `projects/ai-gateway/src/ai_gateway/middleware/auth.py`

你应该观察：

- 为什么 gateway 不自己生成答案
- 为什么要把模型名映射成下游 target model
- `401 / 404 / 429 / 502` 分别代表什么

更进一步，你要能解释：

- 为什么平台层适合做鉴权、路由、限流、缓存和 fallback。
- 为什么 fallback 不能在 streaming 已经开始后随意切换。
- 为什么 `x-upstream-model`、`x-fallback-used`、`x-cache` 这种 header 有学习价值。
- 为什么 `/events/failures` 比只看 HTTP 状态码更适合做失败复盘。

练习建议：

1. 打一条正常请求。
2. 故意去掉 Authorization，观察 `401`。
3. 故意请求不存在的模型，观察 `404`。
4. 查看 `/events/failures`，把失败归类。

### eval-module

目标：
理解“质量闭环”最小是怎么建立的。

先看：

- `projects/eval-module/src/eval_module/main.py`
- `projects/eval-module/src/eval_module/runners/lm_eval_runner.py`
- `projects/eval-module/src/eval_module/results/result_store.py`

你应该观察：

- 一次 run 产出了哪些文件
- comparison bundle 和 run bundle 分别解决什么问题
- leaderboard 为什么依赖 `run_history.jsonl`
- 为什么要有 `run_history.jsonl` 和 `comparison_history.jsonl`

更进一步，你要能解释：

- 为什么一次 run 不是发布判断。
- 为什么 compare 要检查 task 是否一致。
- 为什么 `min_delta` 能避免把小波动误判成提升。
- 为什么 release recommendation 需要 reasons。
- 为什么 leaderboard 不能替代 sample analysis。

练习建议：

1. 跑一次 run。
2. 用同一个结果做一次 compare，先理解报告结构。
3. 修改 `--min-delta`，观察 recommendation 是否变化。
4. 生成 leaderboard 和 list-runs，理解 history 的作用。

### finetune-demo

目标：
理解“训练/微调流程”最小需要沉淀哪些产物。

先看：

- `projects/finetune-demo/src/finetune_demo/main.py`
- `projects/finetune-demo/src/finetune_demo/config.py`
- `projects/finetune-demo/src/finetune_demo/trainer/lora_trainer.py`

你应该观察：

- 为什么要有 `run_manifest.json`
- 为什么要有 `artifacts_manifest.json`
- 为什么会额外记录 `events.jsonl`、`dataset_summary.json`、`latest_checkpoint.json`

更进一步，你要能解释：

- 为什么训练数据要先做 schema 校验。
- 为什么 dataset summary 要记录 role 分布和 sha256。
- 为什么 checkpoint index 比单个 checkpoint 目录更可靠。
- 为什么 export manifest 需要保留 lineage。
- 为什么 run history、dataset registry、export history 是三类不同的历史。

练习建议：

1. 跑一次 train。
2. 先看输出目录，不急着看代码。
3. 跑一次 export。
4. 生成 list-runs、list-datasets、list-exports。
5. 选一个 export manifest，追溯回 dataset version 和 checkpoint。

## 6. 按时间怎么安排

如果你只有一个晚上，可以只完成第一轮闭环；如果你打算认真学两周，可以按下面节奏推进。

| 时间 | 目标 | 交付物 |
| --- | --- | --- |
| 第 1 天 | 打开文档站，跑通检查命令 | 本地环境记录 |
| 第 2 天 | 跑通第一次实操 | 一份 5 行复盘 |
| 第 3 到 4 天 | 深入 inference-service | 一条普通请求和 streaming 证据 |
| 第 5 到 6 天 | 深入 ai-gateway | 一条成功请求和两条失败路径证据 |
| 第 7 到 8 天 | 深入 eval-module | 一份 run/compare/leaderboard 复盘 |
| 第 9 到 10 天 | 深入 finetune-demo | 一份训练产物 lineage 复盘 |
| 第 11 天 | 做一个 hands-on lab | 一份 lab 证据记录 |
| 第 12 天 | 读一个案例并复述 | 一份案例复盘 |
| 第 13 天 | 做 Capstone | 一份端到端故事 |
| 第 14 天 | 整理公开分享材料 | README/issue/release notes 检查 |

这个节奏不是硬性计划。它的核心是每两天至少沉淀一个能被别人看懂的成果，而不是每天只“继续看文档”。

## 7. 你后面应该怎么学

推荐方式不是“先把所有源码啃完”，而是：

1. 先跑起来
2. 看产物
3. 再回头读对应代码
4. 改一个小地方再跑一次
5. 用 [示例输出与证据库](/13-output-gallery/00-overview) 判断证据是否完整
6. 用 [学习者工作簿](/14-workshop-kit/02-learner-workbook) 记录命令、证据和卡点
7. 比较前后结果差异

这样更接近真实工程学习节奏。

如果你已经完成第一轮演练，但不知道下一步该深挖哪条线，可以接着看：

- [第一次跑完之后学什么](/00-overview/06-after-first-walkthrough)

## 8. 如何选择下一条分支

第一轮完成后，不同读者会有不同兴趣。可以按下面方式选择。

| 你更关心 | 推荐继续看 | 适合做的练习 |
| --- | --- | --- |
| 推理性能和服务形态 | 推理服务章节 | 对比普通响应、streaming、metrics |
| 平台治理和多模型入口 | Gateway 章节 | 设计一个新的模型映射或 fallback 场景 |
| 评测和发布门禁 | Eval 章节 | 写一次发布判断复盘 |
| 训练和资产管理 | Finetune 章节 | 追踪一次 dataset 到 export 的 lineage |
| 公开展示 | 输出证据和案例章节 | 整理一份演示脚本 |
| 带别人学习 | 共学套件 | 组织一次 90 分钟议程 |

如果你暂时不知道选哪条，优先选“最能产生证据”的那条。证据越具体，你越容易发现自己真正不懂的部分。

## 9. 当前边界

现在这套项目更偏“学习型工程脚手架”，不是生产级系统。

所以你后面实际学习时，完全可以：

- 继续让别的大模型帮你补细节
- 根据报错再迭代代码
- 把某一段 mock 替换成更真实实现
- 把某个模块单独拿出来重写

这不是偏离目标，而是这套仓库本来就应该支持这种渐进式细化。

## 10. 路线学完以后应该能做什么

完成这条路线后，你不一定能直接负责一个生产级 AI 平台，但应该能稳定做到：

- 看懂一个 AI Infra 项目为什么要拆成 serving、gateway、eval、finetune。
- 对一条请求说出入口、路由、下游、观测和失败路径。
- 对一次评测说出 run、compare、history、leaderboard 各自的作用。
- 对一次训练说出 dataset、checkpoint、manifest、export、history 的关系。
- 对一次改动说出应该跑哪些验证命令。
- 对一次公开分享说出应该展示哪些证据，而不是只展示结论。

如果你能做到这些，就已经有了继续深入真实框架和生产系统的基础。
