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

### Level 2：能解释

你能：

- 解释 execution / governance / evaluation / training 四层
- 解释 `401 / 404 / 429 / 502`
- 解释普通响应和 streaming 的差别
- 解释 run bundle 和 comparison bundle
- 解释 training artifact manifest

这时你已经可以把仓库讲给别人听。

### Level 3：能改动

你能：

- 给某层新增一个小能力
- 给它补测试
- 更新对应文档
- 跑完整验证

这时你已经从读者变成贡献者。

### Level 4：能迁移

你能：

- 把 mock engine 换成真实 OpenAI-compatible 上游
- 把 gateway 的路由配置扩展成多后端
- 把 eval 的结果接到自己的发布判断
- 把 finetune 的 manifest 思路迁移到真实训练项目

这时这个仓库已经完成它最重要的学习使命：帮你形成可迁移的工程直觉。

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
