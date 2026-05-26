# 公开演示脚本

## 这一页适合谁

如果你准备把这个项目发到 GitHub、写文章、录视频或给同学/同事讲，这页可以当成演示脚本。

目标不是炫技，而是在 10 到 20 分钟内讲清楚：

- 这个项目解决什么学习问题
- 四个子项目怎么分层
- 一条请求怎么走
- eval 和 finetune 为什么不是孤立工具
- 当前实现和生产系统差在哪里

## 演示叙事原则

公开演示最容易犯的错误，是把项目讲成“功能列表”。读者真正关心的不是页面有多少、命令有多少，而是：

- 我为什么要学这套东西
- 我从哪里开始不会迷路
- 每个模块在真实 AI Infra 里对应什么位置
- 我跑完命令后应该看什么证据
- 我能不能把这里的思路迁移到自己的项目

所以演示时建议始终围绕一条主线：

```text
一个学习者想理解 AI 应用背后的基础设施：
先看系统地图，再跑最小链路，再读证据，再判断边界，最后选择下一步深入方向。
```

这条主线能避免演示变成“打开很多页面”。每打开一个页面，都要说清楚它回答的问题；每展示一个文件，都要说清楚它证明了什么。

## 5 分钟版本

如果只是会议开场、社群预告或 GitHub README 视频，可以用 5 分钟版本。

### 0-1 分钟：一句话定位

```text
这是一个面向学习和公开共学的 AI Infra Handbook，
用一个 VitePress 站点和四个可运行 Python 小项目，把 serving、gateway、eval、finetune、证据复盘和发布流程串起来。
```

打开首页，只讲三件事：

- 它是学习站，不是生产平台
- 它有文档、项目、lab、案例和公开发布工具
- 它适合想系统理解 AI Infra 的工程学习者

### 1-3 分钟：系统分层

打开 [四个项目怎么连成系统](/06-projects/06-end-to-end-system-map)，用一张图讲：

- inference-service 负责“模型服务接口”
- ai-gateway 负责“治理和接入”
- eval-module 负责“质量判断”
- finetune-demo 负责“训练资产和可追溯”

不要展开所有配置，只说明为什么这四层放在一起学。

### 3-5 分钟：证据和下一步

打开 [示例输出与证据库](/13-output-gallery/00-overview)，强调学习站不是只讲概念，而是要求读者看输出、看 manifest、看 comparison、看 release recommendation。

最后收束到：

```text
如果你第一次来，先按从 0 到 1 路线走；
如果你已经会跑项目，直接看 hands-on labs；
如果你要公开分享或组织共学，就看 workshop kit 和 publication checklist。
```

## 10 分钟版本

### 0-1 分钟：定位

讲法：

```text
这是一个学习型 AI Infra 手册，不是生产平台。
它把文档站、四个可运行项目、hands-on labs、案例复盘和验证命令收在一起。
```

打开：

- [首页](/)
- [从 0 到 1 学习路径](/00-overview/00-zero-to-one)

### 1-3 分钟：系统地图

讲四层：

| 层级 | 项目 | 说明 |
| --- | --- | --- |
| 执行层 | inference-service | 模型服务入口 |
| 治理层 | ai-gateway | 鉴权、路由、限流、fallback |
| 质量层 | eval-module | run、compare、leaderboard |
| 训练层 | finetune-demo | train、checkpoint、export |

打开：

- [四个项目怎么连成系统](/06-projects/06-end-to-end-system-map)

### 3-5 分钟：请求链路

演示：

```bash
PYTHON=.venv/bin/python make infra-smoke
```

讲法：

```text
smoke 不只是跑一个服务，而是覆盖 gateway、inference、eval、finetune 的最小闭环。
```

然后展示：

- `x-request-id`
- `x-upstream-model`
- `/events/requests`
- `/metrics`
- `.tmp/smoke/evidence/evidence_packet.md`

参考：

- [Serving 与 Gateway 输出证据](/13-output-gallery/01-serving-gateway-evidence)
- [自动生成证据包](/13-output-gallery/07-generated-evidence-packet)

### 5-7 分钟：评测证据

讲法：

```text
eval 不应该只剩一个分数。
这里会留下 result、sample outputs、sample summary、sample analysis、compare 和 leaderboard。
```

展示：

- `sample_analysis.json`
- `comparison_index.json`
- `leaderboard.json`

参考：

- [Eval 报告证据](/13-output-gallery/02-eval-report-evidence)

### 7-9 分钟：训练资产

讲法：

```text
finetune 不应该只留下 checkpoint。
可复现训练至少要有 dataset summary、run manifest、checkpoint index 和 export manifest。
```

展示：

- `run_manifest.json`
- `checkpoint_index.json`
- `export_manifest.json`

参考：

- [Finetune 产物证据](/13-output-gallery/03-finetune-artifact-evidence)

### 9-10 分钟：边界和下一步

讲法：

```text
当前项目适合学习、教学、复盘和渐进式改造。
下一步不是把所有东西一次生产化，而是保住接口、观测和验证，再逐层替换真实后端、真实 judge、真实 trainer。
```

打开：

- [生产迁移路线总览](/12-production-migration/00-overview)
- [项目成熟度地图](/00-overview/14-project-maturity-map)

## 20 分钟版本

如果时间更充足，增加三段：

### 加一段：失败排查

演示一个 `401` 或 `404`：

```bash
curl -i -X POST http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"unknown-model","messages":[{"role":"user","content":"hi"}]}'
```

然后查：

```bash
curl -s "http://localhost:8080/events/failures"
```

讲清楚：

- gateway 错误语义
- failure summary
- request timeline

### 加一段：模型发布判断

展示：

- `compare.json`
- `comparison_index.json`
- `release_recommendation`

讲清楚：

- 为什么比较前要检查 task
- 为什么 min delta threshold 能避免噪声
- 为什么 recommendation 不是生产批准

### 加一段：训练到 eval 的资产链

展示：

```text
dataset_summary -> run_manifest -> checkpoint_index -> export_manifest -> eval run
```

讲清楚：

- export 必须能追溯 checkpoint
- checkpoint 必须能追溯 run
- run 必须能追溯 dataset
- eval 结果必须能追溯模型来源

## 不同听众的讲法

同一套项目可以面向不同听众，但重点要换。

| 听众 | 他们关心什么 | 演示重点 |
| --- | --- | --- |
| 初学者 | AI Infra 到底有哪些块 | 首页、从 0 到 1、系统地图、术语解释 |
| 后端工程师 | 请求链路和服务边界 | gateway、inference、events、metrics、failure timeline |
| ML / 算法同学 | eval 和训练资产如何闭环 | eval report、leaderboard、dataset summary、checkpoint lineage |
| 技术负责人 | 学习项目和生产系统差距 | production migration、release brief、成熟度地图 |
| 开源贡献者 | 能从哪里参与 | contribution playbook、first public issues、roadmap pack |
| 讲师/组织者 | 怎么带别人学 | workshop packet、learner workbook、capstone rubric |

如果听众混合，优先讲“系统地图 + 证据链 + 边界”。这三件事最不容易过时，也最能体现项目的学习价值。

## 现场演示路线建议

推荐把浏览器标签页提前排好：

1. 首页
2. 从 0 到 1 学习路径
3. 四个项目怎么连成系统
4. Serving 与 Gateway 输出证据
5. Eval 报告证据
6. Finetune 产物证据
7. 生产迁移路线总览
8. 贡献者协作手册

命令行只保留一个终端窗口，避免现场切来切去。演示时可以先跑过命令，把关键 `.tmp/` 产物留在本机；现场再选择性重新跑 smoke。这样即使网络、依赖或端口出现问题，也能继续讲证据结构。

## 演示前检查

演示前先跑：

```bash
nvm use
PYTHON=.venv/bin/python make infra-format
PYTHON=.venv/bin/python make docs-quality
PYTHON=.venv/bin/python make infra-check
PYTHON=.venv/bin/python make infra-smoke
PYTHON=.venv/bin/python make infra-evidence
npm audit --omit=dev --audit-level=moderate
```

如果时间紧，至少跑：

```bash
PYTHON=.venv/bin/python make infra-check
PYTHON=.venv/bin/python make infra-smoke
```

## 现场失败时怎么处理

公开演示时命令失败并不可怕，真正伤害信任的是假装没失败。

如果 `infra-smoke` 失败，建议这样处理：

1. 先读错误摘要，不急着切页面。
2. 判断是端口、依赖、格式、测试还是业务断言问题。
3. 如果能在 1 分钟内定位，就现场展示排障路径。
4. 如果不能，切到已生成的 evidence packet，说明“这份证据来自演示前验证”。
5. 演示结束后把失败现象整理成 issue 或复盘记录。

可以准备三类备用材料：

| 失败类型 | 备用展示 |
| --- | --- |
| 本地端口冲突 | 已生成的 `.tmp/smoke/evidence/evidence_packet.md` |
| npm / Python 依赖问题 | README 的本地运行步骤和 CI 记录 |
| Pages 或样式问题 | 本地 docs preview 和构建日志 |

这个项目本身就强调证据和复盘，所以一次真实失败反而可以讲清楚工程工作流：先观测，再定位，再修复，再补文档。

## 演示时不要说什么

避免这些说法：

| 不建议说 | 建议说 |
| --- | --- |
| 这是生产级 AI 平台 | 这是学习型 AI Infra 手册 |
| 这个模型效果更好 | 当前 eval evidence 支持这个 candidate 通过门禁 |
| 训练已经真实完成 | 当前训练路径用于学习资产结构 |
| smoke 证明系统没问题 | smoke 证明最小联调链路没有退化 |

## 演示后可以留下什么

建议留下：

- README 链接
- 学习路线链接
- 示例输出与证据库链接
- 一份复盘证据包
- 一份自动生成的 `evidence_packet.md`
- 一张系统图
- 下一阶段计划

## 现场问答准备

常见问题可以提前准备这些回答。

### 这是不是能直接上生产？

不是。它是学习型 scaffold，用来解释接口、边界、证据和迁移路径。生产化需要替换真实鉴权、真实模型后端、持久化、监控告警、容量规划、数据治理和安全审计。

### 为什么不用真实大模型或真实训练？

因为第一阶段目标是让读者理解系统结构和证据链。真实模型会引入费用、权限、网络和不可控输出，反而容易遮住基础设施逻辑。项目保留了迁移路径，后续可以逐层替换。

### 为什么要有这么多自动生成产物？

因为公开学习项目很容易出现“文档说一套、命令跑一套、发布时又说另一套”。inventory、catalog、evidence、release brief、workshop packet、roadmap pack 和 launch pack 的价值，是把学习站、运行证据、共学安排和公开发布变成一条可复核链路。

### 读者应该怎么参与？

第一次贡献优先从文档解释、证据补充、lab 常见失败、FAQ、案例复盘和 issue 复现开始。不要一上来改大架构；先让一个读者卡点被消除。

## 演示后的复盘模板

演示结束后，用这组问题做 10 分钟复盘：

```text
这次听众最先理解的是哪一部分？
哪一页解释不够，需要回头补？
哪个命令或证据最有帮助？
有没有把学习项目误讲成生产平台？
有没有新的 FAQ、lab、case study 或 issue？
下一次演示应该删掉什么、加上什么？
```

复盘不是额外负担，它会直接反哺内容深度。公开学习站越想帮助更多人，就越需要把真实反馈沉淀成页面、lab、案例和 issue。

## 关联阅读

- [端到端复盘证据包](/13-output-gallery/04-end-to-end-review-packet)
- [自动生成证据包](/13-output-gallery/07-generated-evidence-packet)
- [公开发布验收 Lab](/07-hands-on-labs/06-public-release-readiness-lab)
- [Capstone 答辩稿](/10-assessments/04-capstone-defense)
- [公开路线图](/08-publication/03-public-roadmap)
