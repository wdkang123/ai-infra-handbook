# 系统 Capstone 与验收 Rubric

这个 capstone 的目标，是让你把整个仓库讲成一个可分享的 AI Infra 小系统。

如果你准备把项目发到 GitHub、写博客、录视频或给别人讲，建议先完成这一页。

## Capstone 任务

你需要完成一份系统说明，回答下面六个问题：

1. 这个系统分成哪几层
2. 一次正常请求怎么经过这些层
3. 每层分别有什么 health、metrics 或 artifact
4. 每层最重要的失败路径是什么
5. 当前实现为什么是学习型，而不是生产级
6. 如果继续升级，最应该先补什么

你可以写成 Markdown，也可以讲给别人听。  
关键不是形式，而是你能不能讲清楚。

如果你想让说明更像真实工程复盘，可以先读 [案例复盘总览](/11-case-studies/00-overview)，再选择一个案例作为你的讲解素材。

## 为什么要做 Capstone

前面的 lab 会训练单点能力：

- serving lab 训练请求和事件
- gateway lab 训练入口治理和失败路径
- eval lab 训练发布判断
- finetune lab 训练资产追溯

Capstone 的作用是把这些单点能力重新合成一个系统故事。

一个读者如果只会跑命令，说明他完成了操作层学习。一个读者如果能解释每个输出属于哪一层，说明他开始建立系统感。一个读者如果能讲清失败路径、证据链和下一步改造，说明他已经能把这个仓库当成真实工程训练场。

所以 Capstone 不是额外作业，而是检验这套学习站是否真的帮你建立了 AI Infra 直觉。

## 系统地图

先用这张最小地图组织你的解释：

```text
调用方
  -> ai-gateway
      - auth
      - routing
      - rate limit
      - fallback
      - cache
      - streaming proxy
  -> inference-service
      - chat completion
      - streaming
      - engine adapter
      - metrics
  -> eval-module
      - run
      - compare
      - bundle
      - history
  -> finetune-demo
      - dataset validation
      - train artifacts
      - checkpoint
      - export
      - manifest
```

这不是说所有请求都会经过四层。  
它表达的是 AI Infra 学习中最关键的四种能力：

- 服务
- 治理
- 评测
- 训练

## 推荐讲解结构

建议把 Capstone 讲成 8 到 12 分钟的说明，而不是把所有页面重新讲一遍。

```text
1. 项目定位：这是学习型 AI Infra 手册，不是生产平台。
2. 系统分层：execution、governance、evaluation、training。
3. 正常请求路径：client 到 gateway 到 inference。
4. 失败路径：auth、routing、upstream、streaming 中至少讲一个。
5. 质量闭环：eval run、compare、recommendation。
6. 训练资产：dataset、run、checkpoint、export、lineage。
7. 当前边界：哪些是 mock，哪些接口和证据边界应该保留。
8. 下一步：选一个最值得继续补的方向。
```

这个结构可以覆盖全局，又不会变成目录朗读。

## 必做验收

### 1. 跑通质量检查

```bash
PYTHON=.venv/bin/python make infra-check
```

你需要知道它检查了什么：

- Python lint
- 四个项目的单元测试
- 文档站构建
- 非 localhost 断链

### 2. 跑通端到端 smoke

```bash
PYTHON=.venv/bin/python make infra-smoke
```

你需要知道它覆盖了什么：

- gateway upstream health
- direct inference
- gateway proxy
- gateway stream proxy
- request id
- auth error
- unknown model
- metrics
- eval run
- eval compare
- finetune run
- finetune export

### 3. 找到每层入口文件

你需要能快速定位：

| 层 | 入口 |
| --- | --- |
| inference-service | `projects/inference-service/src/inference_service/server.py` |
| ai-gateway | `projects/ai-gateway/src/ai_gateway/server.py` |
| eval-module | `projects/eval-module/src/eval_module/main.py` |
| finetune-demo | `projects/finetune-demo/src/finetune_demo/main.py` |

### 4. 找到每层测试文件

你需要能快速定位：

| 层 | 测试 |
| --- | --- |
| inference-service | `projects/inference-service/tests/test_api.py` |
| ai-gateway | `projects/ai-gateway/tests/test_proxy.py` |
| eval-module | `projects/eval-module/tests/test_runner.py` |
| finetune-demo | `projects/finetune-demo/tests/test_trainer.py` |

## Rubric

### Level 1：能跑

你能：

- 启动文档站
- 跑通 `infra-check`
- 跑通 `infra-smoke`
- 发一条 inference 请求
- 发一条 gateway 请求

但你可能还不能清楚解释每层为什么存在。

典型回答：

```text
我能启动服务，也能跑 smoke，但我现在主要知道它跑通了，还不能完整解释每个输出字段。
```

### Level 2：能解释

你能：

- 解释 execution / governance / evaluation / training 四层
- 解释 `401 / 404 / 429 / 502`
- 解释普通响应和 streaming 的差别
- 解释 run bundle 和 comparison bundle
- 解释 training artifact manifest

这时你已经可以把仓库讲给别人听。

典型回答：

```text
这次 401 停在 gateway auth，还没有进入 inference。这个 request id 可以帮助我回到 gateway events，但它不能证明模型回答质量。
```

### Level 3：能改动

你能：

- 给某层新增一个小能力
- 给它补测试
- 更新对应文档
- 跑完整验证

这时你已经从读者变成贡献者。

典型回答：

```text
我给 gateway failure summary 增加了一个聚合字段，补了测试，更新了证据说明页，并重新跑了 docs-quality 和 gateway tests。
```

### Level 4：能迁移

你能：

- 把 mock engine 换成真实 OpenAI-compatible 上游
- 把 gateway 的路由配置扩展成多后端
- 把 eval 的结果接到自己的发布判断
- 把 finetune 的 manifest 思路迁移到真实训练项目

这时这个仓库已经完成它最重要的学习使命：帮你形成可迁移的工程直觉。

典型回答：

```text
如果把 mock inference 换成真实 OpenAI-compatible backend，我会先保住外部接口、request id、metrics、events 和 gateway model mapping，再逐步替换内部 target。
```

## 评分表

| 维度 | Level 1 | Level 2 | Level 3 | Level 4 |
| --- | --- | --- | --- | --- |
| 系统分层 | 能说出四个项目 | 能解释四层职责 | 能说明跨层依赖 | 能设计迁移边界 |
| 请求链路 | 能发请求 | 能解释 headers/events | 能修改并验证链路 | 能接真实 backend |
| 失败排查 | 能看到错误 | 能定位层级 | 能补测试或事件 | 能设计生产观测 |
| Eval 判断 | 能跑 run | 能解释 compare | 能设计 release gate | 能接真实发布流程 |
| 训练资产 | 能跑 train/export | 能解释 manifest | 能补 lineage 字段 | 能迁移到真实 trainer |
| 公开表达 | 能展示页面 | 能讲清系统故事 | 能写复盘和 issue | 能组织共学或贡献流程 |

这个表不要求你一次到 Level 4。它只是帮助你知道自己现在在哪一层，下一步该补什么。

## 答辩问题库

做 Capstone 时，可以让同伴或自己追问这些问题：

1. 为什么 gateway 不直接和 eval 合在一起？
2. 一个 `200` 响应为什么仍然可能需要复盘？
3. `x-request-id` 能证明什么，不能证明什么？
4. Eval 平均分提升但关键样本退化时，你怎么判断？
5. Export manifest 为什么必须记录 source checkpoint？
6. 如果换成真实模型后 smoke 变慢，你先看哪三类证据？
7. 当前项目最容易被误解成生产级能力的是哪里？
8. 你会把哪个后续改进拆成 good first issue？

这些问题比背定义更能检验理解。

## 最终交付物

完成 capstone 后，建议留下一个 `notes/capstone.md`，包含：

```text
# AI Infra Capstone

## 系统分层

## 正常请求路径

## Streaming 路径

## 错误路径

## Metrics 与 Artifacts

## 案例复盘

## 当前边界

## 下一步改进
```

这个文件不需要提交到仓库也可以。  
它的价值是逼你把零散知识组织成一个完整系统。

## 一个合格 Capstone 的样子

合格交付不一定很长，但应该包含：

- 一张系统分层说明
- 一条正常请求路径
- 一条失败路径
- 一条 eval 证据链
- 一条训练资产链
- 当前学习型边界
- 一个后续改进任务

如果你能在 10 分钟内讲完这些，并且能回答两三个追问，就说明这轮学习已经真正形成闭环。
