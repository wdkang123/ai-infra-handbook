# 公开发布验收 Lab

这个 lab 用于把项目从“我本地能跑”推进到“别人从 GitHub 打开也知道怎么学、怎么验证、怎么继续贡献”。

它适合在你准备公开仓库、发朋友圈、写博客或录视频之前做一遍。

## 学习目标

完成后你应该能确认：

- README 能让第一次访问者理解项目定位
- 首页和 sidebar 能引导读者进入学习路线
- 课程大纲、两周计划、lab、自测和参考资料互相能连起来
- 课程目录能把学习主线整理成可带练模块
- 自动共学包能把课程目录和发布摘要整理成议程、模块卡片和交付要求
- 自动测评包能把课程模块整理成题目、证据要求和评分标准
- 四个项目的测试和 smoke 仍然通过
- 文档站能构建成静态站
- 共学套件能帮助别人组织学习、记录证据和反馈问题
- 发布前还剩哪些刻意保留的边界

## 前置知识

建议先完成：

- [课程大纲](/00-overview/12-course-syllabus)
- [项目成熟度地图](/00-overview/14-project-maturity-map)
- [系统 Capstone 与验收 Rubric](/07-hands-on-labs/05-capstone-review-rubric)
- [共学与公开分享套件](/14-workshop-kit/00-overview)
- [公开发布总览](/08-publication/00-overview)

## Step 1：检查第一次访问体验

打开首页，确认第一屏能回答三个问题：

1. 这是什么项目
2. 我应该从哪里开始
3. 我学完后能做什么

重点检查这些入口：

- [学习路线图](/00-overview/02-learning-route)
- [课程大纲](/00-overview/12-course-syllabus)
- [项目成熟度地图](/00-overview/14-project-maturity-map)
- [两周学习计划](/00-overview/15-two-week-learning-plan)
- [深度实战总览](/07-hands-on-labs/00-overview)
- [学习自测总览](/10-assessments/00-overview)
- [验证矩阵](/09-reference/07-validation-matrix)
- [共学与公开分享套件](/14-workshop-kit/00-overview)

验收标准：

- 读者不需要打开源码，也能知道学习顺序
- 首页不是只有口号，而是能进入具体任务

## Step 2：检查 README

从 GitHub 来的读者通常先看 README，所以 README 至少要能回答：

- 项目定位是什么
- 当前不是生产系统
- 本地文档站怎么启动
- 质量检查怎么跑
- 四个项目分别是什么
- 想分享或贡献应该看哪里

验收标准：

- README 能在 1 分钟内说明项目价值
- README 指向课程大纲、成熟度地图、lab、自测、发布清单
- README 指向示例输出和共学套件

## Step 3：跑文档构建

```bash
nvm use
npm install
PYTHON=.venv/bin/python make docs-inventory
PYTHON=.venv/bin/python make course-catalog
PYTHON=.venv/bin/python make docs-quality
npm run docs:build
```

验收标准：

- 文档质量检查通过
- 学习站清单能生成，课程主线没有缺失路由
- 课程目录能生成，模块引用的页面和学习主线没有缺失
- VitePress 构建通过
- 新增页面没有断链
- sidebar 中的链接能被构建器解析

如果构建失败，先看：

- 链接是否少了文件
- sidebar 是否指向了不存在的页面
- Markdown 表格或代码块是否没闭合

## Step 4：跑项目验证

```bash
PYTHON=.venv/bin/python make infra-format
PYTHON=.venv/bin/python make docs-inventory
PYTHON=.venv/bin/python make course-catalog
PYTHON=.venv/bin/python make docs-quality
PYTHON=.venv/bin/python make public-check
PYTHON=.venv/bin/python make infra-smoke
PYTHON=.venv/bin/python make infra-evidence
PYTHON=.venv/bin/python make release-brief
PYTHON=.venv/bin/python make workshop-packet
PYTHON=.venv/bin/python make assessment-pack
PYTHON=.venv/bin/python make roadmap-pack
```

验收标准：

- lint 和格式检查通过
- 学习站清单能汇总章节、页面和课程主线
- 课程目录能把主线整理成入口、核心阅读、实验、自测和证据输出
- 四个项目的单元测试通过
- 文档构建通过
- smoke 覆盖 gateway、inference、eval、finetune 的主链路
- evidence packet 能汇总本轮 smoke 产物
- release brief 能合成学习站清单和运行证据
- workshop packet 能合成课程目录、发布摘要、议程模板、模块卡片和学习者交付
- assessment pack 能合成模块题目、证据要求、rubric 和 Capstone review
- roadmap pack 能合成 GitHub issue 种子、推荐 label、验收标准和验证命令

这一步的目标不是追求测试数量，而是确认公开前的最小学习体验没有断。

## Step 5：检查安全和仓库元信息

```bash
npm audit --omit=dev --audit-level=moderate
```

同时检查：

- `.env` 没有被提交
- `.env.example` 只有占位值
- `LICENSE` 存在
- `CONTRIBUTING.md` 存在
- `CODE_OF_CONDUCT.md` 存在
- `SECURITY.md` 存在
- `CHANGELOG.md` 记录了当前阶段
- `PUBLICATION_CHECKLIST.md` 能指导最后发布

验收标准：

- 没有真实 API key
- 没有私有 endpoint
- 没有敏感日志
- 发布元信息完整

## Step 6：写公开介绍

可以用这个模板写 GitHub description 或文章开头：

```text
AI Infra Manual 是一个面向学习的 AI Infra 小系统。它把文档站、推理服务、AI gateway、评测模块、微调示例、hands-on labs 和自测题放在一个仓库里，目标是帮助读者理解模型服务、平台治理、质量闭环和训练资产化之间的关系。
```

再补一句边界：

```text
当前实现是学习型脚手架，不是生产平台；它适合用于学习、教学、分享和渐进式改造。
```

验收标准：

- 介绍里没有夸大生产能力
- 能清楚说明“为什么要看这个项目”
- 能引导读者从学习路线或第一次实操开始

## Step 7：检查共学和贡献入口

确认这些入口已经可被读者找到：

- [讲师与带练指南](/14-workshop-kit/01-facilitator-guide)
- [学习者工作簿](/14-workshop-kit/02-learner-workbook)
- [学习小组议程](/14-workshop-kit/03-study-group-agenda)
- [复盘与评审模板](/14-workshop-kit/04-review-templates)
- [贡献者协作手册](/14-workshop-kit/05-contribution-playbook)
- [GitHub 发布计划](/14-workshop-kit/06-github-release-plan)
- [自动生成共学包](/14-workshop-kit/07-generated-workshop-packet)
- [自动生成测评包](/10-assessments/06-generated-assessment-pack)
- [自动生成路线图包](/08-publication/05-generated-roadmap-pack)

同时检查：

- PR template 是否要求记录验证和学习影响
- issue templates 是否能收集 bug、docs、lab、evidence 和 workshop feedback
- CONTRIBUTING 是否说明证据、共学和 first-time contributor 任务

验收标准：

- 读者能知道如何学习
- 贡献者能知道如何开始
- 组织者能知道如何收集反馈

## Step 8：记录下一阶段计划

发布前不要把所有事情都补完。更好的做法是明确下一阶段方向：

- 增加真实 vLLM/SGLang 接入说明
- 增加更多示例输出和截图
- 根据共学反馈改进工作簿和议程
- 增加更完整的 eval judge adapter
- 增加 finetune resume 和多 checkpoint 选择说明
- 根据读者反馈扩充 FAQ

验收标准：

- 已知边界被公开说明
- 后续计划和当前学习价值不冲突

## 最终验收清单

- [ ] 首页能引导第一次访问者
- [ ] README 能说明定位、启动、验证和学习路线
- [ ] `docs-inventory` 生成 JSON / Markdown 学习站清单
- [ ] `course-catalog` 生成 JSON / Markdown 课程目录
- [ ] `docs-quality` 通过
- [ ] 文档站构建通过
- [ ] `public-check` 通过
- [ ] `infra-smoke` 通过
- [ ] `infra-evidence` 生成 JSON / Markdown 证据包
- [ ] `release-brief` 生成 JSON / Markdown 发布摘要
- [ ] `workshop-packet` 生成 JSON / Markdown 共学包
- [ ] `assessment-pack` 生成 JSON / Markdown 测评包
- [ ] `roadmap-pack` 生成 JSON / Markdown 路线图包
- [ ] 依赖安全审计没有中高风险问题
- [ ] 发布边界写清楚
- [ ] 共学和贡献入口写清楚
- [ ] 下一阶段计划写清楚

完成这组检查后，这个仓库就不只是“能上传 GitHub”，而是更像一个读者真的可以打开、跟着学、跟着跑、跟着复盘的学习网站。
