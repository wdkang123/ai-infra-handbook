# 公开路线图

这页用于对外说明项目后续会怎么长。

路线图不是承诺日期，而是帮助贡献者理解优先级。

如果准备把路线图拆成 GitHub issue，可以先运行：

```bash
PYTHON=.venv/bin/python make roadmap-pack
```

然后从 `.tmp/roadmap/roadmap_pack.md` 选择 5 到 8 条首批 issue。生成包会把学习价值、建议文件、验收标准和验证命令一起列出来，避免路线图停留在宽泛方向。也可以先用 [首批公开 Issues 草稿](/08-publication/11-first-public-issues) 中已经整理好的 10 条任务作为首发 issue 池。

## 当前阶段

当前项目已经具备：

- VitePress 学习站
- AI Infra 主线文档
- 四个可运行学习项目
- 深度实战 labs
- CI 与 smoke
- GitHub 协作模板
- License、Code of Conduct、Changelog
- 发布检查清单
- 更真实的 token 统计、release recommendation、dataset role stats、export lineage
- eval sample outputs / sample summary / leaderboard、finetune dataset registry 查询 / dataset version、默认 gateway fallback 示例
- gateway fallback headers/metrics、finetune export history 数据版本指纹
- gateway `/events` 结构化事件、leaderboard best/latest result file、dataset registry method/model 过滤与重复登记统计
- inference/gateway `/v1/models` 模型列表、eval run index、finetune dataset registry diff
- inference `/events` 请求事件流、eval comparison index、finetune export index
- inference/gateway `/events` 过滤查询、eval leaderboard/run index 的 backend/few-shot 视图、finetune export status/duration 追踪
- inference/gateway `/events/summary`、eval comparison verdict/recommendation 聚合、finetune export model/dataset summaries
- inference/gateway request timeline、eval comparison task summaries、finetune export manifest pointer
- inference/gateway request timeline 索引、eval run index task summaries、finetune run index
- gateway failure summary、eval sample analysis、finetune checkpoint index
- 首页课程矩阵、项目成熟度地图、两周学习计划和公开发布验收 Lab
- 可执行文档质量检查，覆盖 Markdown 内链、heading 锚点、H1 结构、VitePress nav/sidebar 路由、首页配置与 Vue 组件链接、README 入口和首页统计
- 案例复盘章节，覆盖请求失败排查、模型发布判断和训练产物复现
- 示例输出与证据库章节，覆盖 HTTP header、events、eval report、finetune manifest、失败证据和公开演示脚本
- 共学与公开分享套件章节，覆盖讲师带练、学习者工作簿、学习小组议程、复盘模板、贡献协作和 GitHub 发布计划
- evidence example 与 workshop feedback issue templates，用于结构化收集输出证据和共学反馈
- learning question 与 roadmap task issue templates，用于沉淀学习问题和公开路线图任务
- Reference 层新增 API Surface、CLI Surface 和验证矩阵，帮助读者快速定位接口、命令和检查策略
- 生产迁移路线章节，覆盖 Serving 后端、Gateway 平台化、Eval 评测系统和 Finetune 真实训练迁移
- 自动生成路线图包，能把发布摘要和测评弱点整理成 GitHub issue 种子、推荐 label 和发布后反馈闭环
- 发布维护节奏与 issue triage 文档，帮助公开仓库用低噪音方式持续处理反馈、依赖和路线图
- v0.1 首发发布手册，帮助第一个 release 说明学习价值、验证命令和项目边界
- 首批公开 issues 草稿和 v0.1 release notes 草稿，让首发后的任务池和 release 页面可以直接落地
- 深化案例复盘，新增 Gateway fallback/cache 与 Eval 退化阻断两类更接近真实工程评审的案例

它已经适合开始公开分享和收集反馈。

## Phase 1：学习体验打磨

目标：让第一次来的读者更容易开始。

优先任务：

- 根据真实读者反馈补 FAQ
- 从 [自动生成路线图包](/08-publication/05-generated-roadmap-pack) 中选择 2 到 3 条 good first issue
- 给每个 overview 增加“学完你能做什么”
- 给 lab 增加更多截图、示例输出和证据包模板
- 根据共学反馈改进学习者工作簿、议程和公开演示材料
- 给常见报错增加排查页面
- 给术语索引增加更多交叉链接
- 根据两周学习计划补更多阶段性练习、示例输出和公开演示材料

验收：

- 新读者能在 10 分钟内找到开始路径
- 新读者能在 30 分钟内跑通最小 smoke

## Phase 2：项目实现变得更真实

目标：在不牺牲学习可读性的前提下，让实现更接近真实工程。

优先任务：

- inference-service 继续细化真实 tokenizer / streaming usage
- ai-gateway 增加更细的 fallback 失败原因、重试预算和外部 tracing/logging backend
- eval-module 增加真实 judge adapter、更多 sample 聚合维度和更完整 leaderboard/dashboard 视图
- finetune-demo 增加 registry export、resume 策略和多 checkpoint 选择逻辑
- smoke 继续覆盖更多错误路径、header、metrics 和产物字段

验收：

- 每个新增行为都有测试
- 每个新增行为都有对应文档
- `infra-check` 和 `infra-smoke` 保持稳定

## Phase 3：公开站点运营

目标：让这个学习站可以长期维护。

优先任务：

- 配置 GitHub Pages
- README 增加在线站点链接
- 准备 `v0.1.0-learning-site` release notes
- 设置 repo description、topics 和 About website
- 创建 good first issue
- 创建 roadmap issue
- 用 workshop feedback issue template 收集第一批共学反馈
- 用 learning question 和 roadmap task issue template 收集学习问题与后续任务
- 定期根据反馈整理 FAQ

验收：

- GitHub Pages 能稳定发布
- 新 issue 能被归类到 docs、lab、bug、enhancement
- 贡献者能通过 CONTRIBUTING 快速开始

## Phase 4：真实后端接入

目标：保留学习型路径，同时提供更真实的接入方式。

可能方向：

- 接入本地 OpenAI-compatible vLLM
- 接入本地 SGLang
- 增加真实 eval runner 适配说明
- 增加真实 PEFT/LoRA 训练的迁移指南

验收：

- mock 路径仍可跑
- 真实接入路径有清晰前置条件
- 失败时有明确排查文档

## 暂不优先做什么

这些方向暂时不优先：

- 一上来做完整生产网关
- 引入复杂 Kubernetes 部署
- 做多云平台适配
- 做完整实验追踪平台
- 做完整用户系统

原因不是这些不重要，而是它们会让学习主线变散。

当前项目最重要的价值，仍然是让读者在小系统里看懂 AI Infra 的主干关系。
