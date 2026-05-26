# Changelog

这个文件记录面向学习者和贡献者的重要变化。
格式参考 [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)，版本语义保持轻量。

## Unreleased

### Added

- 新增 VitePress 学习站入口、导航、侧边栏和本地构建流程。
- 新增 AI Infra 总览、学习路线、运行手册、第一次实操、课程大纲、术语索引和 FAQ。
- 新增 LLM fundamentals、inference serving、gateway platform、evaluation observability、finetuning training 等学习模块。
- 新增四个学习型项目：`inference-service`、`ai-gateway`、`eval-module`、`finetune-demo`。
- 新增跨项目 smoke 测试和根级 `Makefile` 验证入口。
- 新增 hands-on labs、Capstone rubric、学习自测、参考资料和排障手册。
- 新增 GitHub Actions CI、GitHub Pages workflow、issue templates、PR template、贡献指南、安全说明和发布清单。
- 新增 MIT license、Code of Conduct、Changelog 和 `.env.example`，补齐公开仓库基础元信息。
- 新增 mock token usage 估算、gateway `x-cache` header、eval release recommendation、finetune dataset role stats 和 export lineage。
- 扩展 smoke，覆盖更多 inference 错误路径、eval recommendation 字段和 finetune 产物字段。
- 新增默认 gateway fallback 配置示例、eval sample outputs、finetune dataset version 与 cache eviction 测试。
- 新增 gateway fallback attempts/successes metrics、`x-upstream-model` / `x-fallback-used` header、eval `sample_summary.json` / sample judge reason，以及 finetune dataset version 到 export history 的传递。
- 新增 eval leaderboard CLI，从 `run_history.jsonl` 聚合最小排行榜 JSON/Markdown，并扩展 smoke 覆盖 leaderboard 产物。
- 新增 finetune dataset registry 草图，训练时生成 `data/dataset_registry_entry.json` 并追加 `dataset_registry.jsonl`，将 dataset id 贯穿到 trainer/export lineage。
- 新增 finetune `list-datasets` CLI，可从 `dataset_registry.jsonl` 生成 dataset registry JSON/Markdown 报告，并扩展 smoke 覆盖。
- 新增 gateway `/events` 结构化事件端点、eval leaderboard best/latest result file 追踪、finetune registry method/model 过滤与重复登记统计。
- 新增 inference/gateway `/v1/models` 模型列表、eval `list-runs` run index、finetune `diff-datasets` registry diff，并扩展 smoke 覆盖。
- 新增 inference `/events` 请求事件流、eval `list-comparisons` comparison index、finetune `list-exports` export index，并扩展 smoke 覆盖。
- 新增 inference/gateway `/events` 查询过滤、eval leaderboard/run index 的 backend 与 few-shot 过滤/分组，以及 finetune export status/duration 记录，并扩展 smoke 覆盖。
- 新增 inference/gateway `/events/summary` 事件摘要、eval comparison index verdict/recommendation 聚合，以及 finetune export model/dataset summaries，并扩展 smoke 覆盖。
- 新增 inference/gateway `/events/requests/{request_id}` 请求 timeline、eval comparison task summaries，以及 finetune `export_manifest_file` 指针，并扩展 smoke 覆盖。
- 新增 inference/gateway `/events/requests` 请求 timeline 索引、eval run index task summaries，以及 finetune `list-runs` run index，并扩展 smoke 覆盖。
- 新增 gateway `/events/failures` 失败摘要、eval `sample_analysis.json` 样本分析、finetune checkpoint index，并扩展 smoke 覆盖。
- 新增首页课程矩阵、项目成熟度地图、两周学习计划和公开发布验收 Lab，让学习站更适合公开分享前自查。
- 新增 `scripts/docs_quality_check.py` 和 `make docs-quality`，自动检查 Markdown 内链、heading 锚点、H1 结构、VitePress nav/sidebar 路由、首页配置与 Vue 组件链接、README 关键入口和首页文档页统计，并接入 `infra-check` 与 Pages workflow。
- 新增案例复盘章节，覆盖请求失败排查、模型发布判断和训练产物复现，把多项目能力串成可复盘工程故事。
- 新增 API Surface、CLI Surface 和验证矩阵参考页，集中整理接口、命令和按改动类型选择验证命令的规则。
- 新增生产迁移路线章节，说明如何从学习型实现逐步迁移到更真实的 serving、gateway、eval 和 finetune 系统。
- 新增示例输出与证据库章节，覆盖 Serving/Gateway 输出、Eval 报告、Finetune 产物、端到端证据包、失败症状地图和公开演示脚本。
- 新增共学与公开分享套件章节，覆盖讲师带练、学习者工作簿、学习小组议程、复盘评审模板、贡献者协作和 GitHub 发布计划。
- 新增 evidence example 与 workshop feedback issue templates，让公开发布后的输出证据和共学反馈能结构化进入仓库。
- 新增 learning question 与 roadmap task issue templates，让学习问题和公开路线图任务能结构化进入仓库。
- 新增维护节奏与 issue triage 文档，说明公开发布后如何处理 Dependabot、反馈、labels、路线图和低噪音协作。
- 新增 v0.1 首发发布手册，提供 release notes 模板、发布前门禁和发布后 24 小时检查口径。
- 新增首批公开 issues 草稿和 v0.1 release notes 草稿，帮助首发后直接创建任务池和 release 页面。
- 新增 Gateway fallback/cache 与 Eval 退化阻断案例，强化平台层成功响应复盘和评测发布门禁判断。
- 新增 Dependabot 配置，覆盖 npm、pip 和 GitHub Actions 依赖更新提醒。
- 新增 `scripts/build_evidence_packet.py`、`make infra-evidence` 和脚本测试，可把 smoke 产物汇总成 JSON / Markdown 端到端证据包。
- 扩展 smoke，保存 serving/gateway 快照并校验证据包生成结果。
- 新增 `scripts/build_learning_inventory.py`、`make docs-inventory` 和脚本测试，可把文档站章节、页面、课程主线、内容信号和 Makefile 目标汇总成 JSON / Markdown 学习站清单。
- 新增学习站清单参考页和首页证据闭环区块，让 GitHub 发布、共学带练和课程维护有更清晰的课程地图入口。
- 新增 `scripts/build_release_brief.py`、`make release-brief`、`make infra-release` 和脚本测试，可把学习站清单与证据包合成为 JSON / Markdown 发布摘要。
- 新增发布摘要参考页，把 GitHub 首发、PR 复盘、公开演示和共学带练接到同一份 release readiness 材料。
- 新增 `scripts/build_course_catalog.py`、`make course-catalog` 和脚本测试，可把学习站清单整理成 JSON / Markdown 可带练课程目录。
- 新增课程目录参考页，把 7 条学习主线组织成入口、核心阅读、实验、自测、证据、迁移讨论和讲师提示。
- 新增 `scripts/build_workshop_packet.py`、`make workshop-packet` 和脚本测试，可把课程目录与发布摘要合成 JSON / Markdown 共学包。
- 新增自动生成共学包参考页，把议程模板、模块卡片、学习者交付、带练检查表和复盘问题接入共学套件。
- 新增 `scripts/build_assessment_pack.py`、`make assessment-pack` 和脚本测试，可把课程目录与共学包合成 JSON / Markdown 测评包。
- 新增自动生成测评包参考页，把模块题目、证据要求、rubric、讲师追问和 Capstone review 接入学习自测。
- 新增 `scripts/build_roadmap_pack.py`、`make roadmap-pack` 和脚本测试，可把发布摘要与测评包合成 JSON / Markdown 路线图包。
- 新增自动生成路线图包参考页，把 GitHub issue 种子、推荐 label、验收标准和验证命令接入公开发布流程。
- 新增 `scripts/build_launch_pack.py`、`make launch-pack` 和脚本测试，可把发布摘要与路线图包合成 JSON / Markdown 首发运营包。
- 新增自动生成首发运营包参考页，把 release notes、starter issues、默认标签规范和发布后检查表接入公开发布流程。
- 新增 `make security-check` 和 `make public-check`，在公开上传前扫描候选入库文件中的密钥、私钥、连接串、本机路径、个人痕迹和危险文件类型。
- 新增脱敏后的 `tasks/` / `prompts/` 公开工作台说明，保留项目拆解、研究、评审和 AI 协作方法。
- 新增深度教程页写作标准，明确核心章节不能停留在提纲，需要覆盖场景、机制、取舍、观察方式、仓库映射和常见误区。

### Changed

- 将项目定位从零散学习资料收敛为“文档站 + 可运行脚手架 + 最小联调链路”的学习手册。
- 将公开发布流程整理为 GitHub Pages 指南和发布前检查清单。
- 将首页、课程大纲、学习路线、两周计划、案例复盘、生产迁移路线和贡献指南接入证据驱动与共学分享路径。
- 扩展 PR template，要求记录 docs-quality、输出证据、学习影响和公开路径影响。
- 将 GitHub Pages workflow 扩展为手动触发和文档相关 push 自动发布双入口。
- 将验证矩阵、命令速查、发布验收和输出证据库接入自动证据包生成流程。
- 将验证矩阵、命令速查、README 和发布清单接入学习站清单生成流程。
- 将验证矩阵、命令速查、README、发布清单、贡献指南和 PR template 接入发布摘要生成流程。
- 将首页、导航、CI、Pages workflow、README、发布清单、贡献指南、PR template 和参考资料接入课程目录生成流程。
- 将 `infra-release`、CI、README、发布清单、贡献指南、PR template、发布验收 Lab 和 GitHub 发布计划接入共学包生成流程。
- 将 `infra-release`、CI、README、发布清单、贡献指南、PR template、自测总览和发布验收 Lab 接入测评包生成流程。
- 将 `infra-release`、CI、README、发布清单、贡献指南、PR template、首页证据闭环和公开发布章节接入路线图包生成流程。
- 将 `infra-release`、README、发布清单、v0.1 发布手册、首批 issues 草稿和 release notes 草稿接入首发运营包生成流程。
- 将 CI、PR template、贡献指南、发布计划、README、SECURITY 和发布清单统一到 `public-check` 公开上传检查口径。
- 将 Node 版本约束收紧到 22，与 `.nvmrc`、CI 和本地推荐命令保持一致。
- 将 issue templates 的默认 labels 收敛到 GitHub 默认标签，避免新仓库因为未创建自定义 labels 产生提示。
- 将 Prefill/Decode/KV Cache、vLLM/SGLang、Triton/TensorRT-LLM、Gateway 鉴权路由限流、Benchmark/Leaderboard/Observability、LoRA/QLoRA/PEFT 从提纲式说明扩写为教程式核心章节。
- 将 Token/Context、TTFT/ITL/Throughput、服务选型取舍、Gateway health/metrics/request id、Eval run/compare/history、Finetune run/artifacts/export 扩写为带场景、机制、观察方式、误区和仓库映射的深度教程页。
- 将请求到首个 token、Streaming/Batching/Metrics、Gateway 平台边界、模型名映射、SFT/DPO 训练目标、微调决策、实验追踪复现、Benchmark 与生产质量扩写为教程式核心页。
- 将学习型 Serving/Gateway 到真实系统、四条生产迁移路线、端到端系统地图和质量维护入口扩写为分阶段迁移、风险、验收和证据闭环教程页。

### Verified

- `PYTHON=.venv/bin/python make infra-format`
- `PYTHON=.venv/bin/python make docs-quality`
- `PYTHON=.venv/bin/python make infra-check`
- `PYTHON=.venv/bin/python make infra-smoke`
