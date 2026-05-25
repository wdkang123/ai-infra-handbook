# 生产迁移路线总览

这一章回答一个进阶问题：

> 当前项目是学习型实现，如果我想把它逐步改得更接近真实工程，应该按什么顺序推进？

这里不会把仓库包装成生产平台。  
相反，它会明确区分：

- 哪些结构应该保留
- 哪些实现可以替换
- 哪些能力必须等边界稳定后再加
- 每一步应该怎么验证

## 核心原则

### 1. 先保接口，再替内部

当前四个项目最有价值的不是 mock 细节，而是边界：

- inference-service 暴露 OpenAI-compatible 风格入口
- ai-gateway 负责入口治理
- eval-module 把结果变成可比较对象
- finetune-demo 把训练变成可复盘资产

迁移时优先保住这些边界，再替换内部执行。

### 2. 先保观测，再扩大复杂度

每次变真实，至少要保住：

- request id
- health
- metrics
- structured events
- manifest / index
- 示例输出和复盘证据
- smoke 验证

如果真实实现更复杂，却更难排查，那不是升级，而是把学习系统变成黑箱。

### 3. 先单点迁移，再跨层联动

不要一口气同时替换 serving、gateway、eval 和 training。  
更稳的顺序是：

1. 替换 inference 后端
2. 强化 gateway 策略
3. 扩展 eval 判断
4. 接入真实训练
5. 再做跨层发布流程

## 迁移章节

- [Serving 后端迁移](/12-production-migration/01-serving-backend-migration)
- [Gateway 平台化加固](/12-production-migration/02-gateway-platform-hardening)
- [Eval 评测系统迁移](/12-production-migration/03-eval-judge-dashboard-migration)
- [Finetune 真实训练迁移](/12-production-migration/04-finetune-real-training-migration)

## 一张迁移地图

```text
学习型系统
  -> 保留接口和观测
  -> 替换 inference 执行后端
  -> 增强 gateway 路由、配额、追踪
  -> 扩展 eval judge、dashboard、发布门禁
  -> 接入真实 trainer、checkpoint、resume
  -> 用 smoke / case studies / validation matrix 收住风险
```

## 每次迁移都要回答的问题

| 问题 | 为什么重要 |
| --- | --- |
| 哪个接口不能变 | 避免上游调用方和文档全部失效 |
| 哪个产物必须保留 | 避免后续无法复盘 |
| 哪个指标会变化 | 避免性能或质量变化不可见 |
| 哪些输出证据要更新 | 避免读者不知道新实现是否跑对 |
| 哪个失败路径会新增 | 避免迁移后只会看 happy path |
| 哪条测试或 smoke 要扩展 | 避免靠人工感觉判断 |

## 推荐验收命令

迁移类改动至少跑：

```bash
PYTHON=.venv/bin/python make infra-format
PYTHON=.venv/bin/python make infra-check
PYTHON=.venv/bin/python make infra-smoke
```

如果只改文档或迁移说明，先跑：

```bash
PYTHON=.venv/bin/python make docs-quality
```

更细的选择见 [验证矩阵](/09-reference/07-validation-matrix)。
迁移完成后，也应该同步更新 [示例输出与证据库](/13-output-gallery/00-overview)，确保读者看到的是新实现下的证据口径。
