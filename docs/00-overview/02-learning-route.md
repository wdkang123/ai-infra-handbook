# 学习路线图

## 1. 这页是干什么的

这页不是再讲一遍概念，而是把“你接下来怎么学、怎么跑、先看哪里、再改哪里”串成一条路线。

如果你后面是边看文档边跑代码，这页应该作为总导航入口。

如果你是完全新手，建议先看一遍 [从 0 到 1 学习路径](/00-overview/00-zero-to-one)，再回到这页按模块展开。

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

## 3. 一轮最小学习闭环

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

## 4. 每一站你该关注什么

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

## 5. 你后面应该怎么学

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

## 6. 当前边界

现在这套项目更偏“学习型工程脚手架”，不是生产级系统。

所以你后面实际学习时，完全可以：

- 继续让别的大模型帮你补细节
- 根据报错再迭代代码
- 把某一段 mock 替换成更真实实现
- 把某个模块单独拿出来重写

这不是偏离目标，而是这套仓库本来就应该支持这种渐进式细化。
