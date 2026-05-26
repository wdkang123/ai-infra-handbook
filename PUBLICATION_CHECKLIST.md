# Publication Checklist

这个清单用于把仓库发布到 GitHub 前做最后检查。

## 1. 仓库说明

- [ ] `README.md` 能在 1 分钟内说明项目是什么
- [ ] README 有本地启动文档站的命令
- [ ] README 有质量检查命令
- [ ] README 指向学习路线和 hands-on labs
- [ ] README 指向项目成熟度地图和两周学习计划
- [ ] README 指向示例输出与证据库
- [ ] README 指向共学与公开分享套件
- [ ] README 指向学习自测和参考资料
- [ ] README 指向课程目录生成器
- [ ] README 指向自动生成共学包
- [ ] README 指向自动生成测评包
- [ ] README 指向自动生成路线图包
- [ ] README 说明当前是学习型项目，不是生产系统

## 2. 文档站

- [ ] 首页能清楚引导第一次访问者
- [ ] VitePress 导航包含主要学习路径
- [ ] Sidebar 包含新增页面
- [ ] 所有内部链接、heading 锚点、H1 结构、nav/sidebar 路由和首页配置/组件链接能构建通过
- [ ] `PYTHON=.venv/bin/python make docs-quality` 通过
- [ ] `npm run docs:build` 通过

## 3. 项目质量

- [ ] `PYTHON=.venv/bin/python make infra-format` 通过
- [ ] `PYTHON=.venv/bin/python make docs-quality` 通过
- [ ] `PYTHON=.venv/bin/python make infra-check` 通过
- [ ] `PYTHON=.venv/bin/python make infra-smoke` 通过
- [ ] `PYTHON=.venv/bin/python make infra-evidence` 能生成证据包
- [ ] `PYTHON=.venv/bin/python make docs-inventory` 能生成学习站清单
- [ ] `PYTHON=.venv/bin/python make course-catalog` 能生成课程目录
- [ ] `PYTHON=.venv/bin/python make release-brief` 能生成发布摘要
- [ ] `PYTHON=.venv/bin/python make workshop-packet` 能生成共学包
- [ ] `PYTHON=.venv/bin/python make assessment-pack` 能生成测评包
- [ ] `PYTHON=.venv/bin/python make roadmap-pack` 能生成路线图包
- [ ] `PYTHON=.venv/bin/python make infra-release` 在发布前最后一轮通过
- [ ] `.nvmrc` 与 `package.json` 的 Node 版本要求一致
- [ ] CI 工作流能在 GitHub Actions 上执行

## 4. GitHub 协作

- [ ] `CONTRIBUTING.md` 已存在
- [ ] `CODE_OF_CONDUCT.md` 已存在
- [ ] `SECURITY.md` 已存在
- [ ] `CHANGELOG.md` 已存在并记录当前阶段
- [ ] Issue templates 已存在
- [ ] Issue templates 只引用仓库里已经存在的 labels
- [ ] PR template 已存在
- [ ] Dependabot 已覆盖 npm、pip 和 GitHub Actions
- [ ] Dependabot 分组和限流配置能避免依赖 PR 噪音失控
- [ ] Dependabot 配置没有引用仓库里不存在的 labels
- [ ] Dependency review workflow 已存在，并会在依赖相关 PR 上运行
- [ ] GitHub Actions 依赖升级后，对应 workflow 已实际通过
- [ ] `LICENSE` 已存在，README 已说明许可证
- [ ] GitHub repo description、topics、About 链接已设置
- [ ] 第一个 release notes 能说明学习价值、验证命令和项目边界
- [ ] 首批公开 issues 有学习价值、验收标准和验证命令

## 5. 敏感信息

- [ ] `PYTHON=.venv/bin/python make security-check` 通过
- [ ] `PYTHON=.venv/bin/python make public-check` 通过
- [ ] `npm audit --omit=dev --audit-level=moderate` 没有中高风险依赖
- [ ] `git status --short --ignored` 中缓存、输出、虚拟环境和内部协作材料都处于 ignored 状态
- [ ] 没有真实 API key
- [ ] 没有真实云服务凭证
- [ ] 没有私有 endpoint
- [ ] 没有个人本机用户名、个人邮箱、手机号或身份证号
- [ ] 没有带敏感 header 的日志
- [ ] `.env.example` 只包含占位值
- [ ] `.env`、`.env.*`、输出目录、缓存目录不会被提交
- [ ] `tasks/` 和 `prompts/` 中没有个人路径、真实账号、真实 endpoint 或真实密钥
- [ ] `base.md` 和内部交接文档不会进入公开提交

## 6. 学习体验

- [ ] 新读者知道从哪里开始
- [ ] 每条主线都有 overview
- [ ] 每个项目页都有代码入口
- [ ] 至少有一组 hands-on labs
- [ ] 有示例输出与证据库，帮助读者判断命令是否跑对
- [ ] 有自动生成证据包，帮助读者把 smoke 输出整理成复盘材料
- [ ] 有学习站清单，帮助读者和贡献者理解章节、主线和维护信号
- [ ] 有课程目录，帮助讲师和学习小组按模块组织共学
- [ ] 有发布摘要，帮助公开发布前判断课程结构和运行证据是否齐全
- [ ] 有自动生成共学包，帮助讲师把议程、模块卡片、学习者交付和复盘问题整理成一份材料
- [ ] 有自动生成测评包，帮助学习者、讲师和 reviewer 按模块出题、举证和评分
- [ ] 有自动生成路线图包，帮助维护者把测评弱点和发布反馈整理成 GitHub issue 种子
- [ ] 有维护节奏和 issue triage 文档，帮助公开发布后持续处理反馈
- [ ] 有 v0.1 首发发布手册，帮助第一个 release 写清楚范围和边界
- [ ] 有首批公开 issues 和 release notes 草稿，帮助首发后直接落地协作
- [ ] 有共学套件，帮助读者组织学习小组、公开演示和贡献协作
- [ ] 有阶段自测题和参考答案
- [ ] Capstone 可以帮助读者复盘整个系统
- [ ] 公开发布验收 Lab 可以帮助发布前自查

## 7. 发布后可以继续做

- [ ] 配置 GitHub Pages 或其他静态站托管
- [ ] 给 README 增加在线站点链接
- [ ] 创建 `v0.1.0-learning-site` release
- [ ] 增加路线图 issue
- [ ] 从首批公开 issues 草稿中挑选 6 到 10 条创建到 GitHub
- [ ] 标记适合 first-time contributor 的任务
- [ ] 按维护节奏定期整理 Dependabot、issue、FAQ 和路线图
- [ ] 根据共学反馈更新学习者工作簿和带练议程
- [ ] 根据读者反馈补充 FAQ
- [ ] 定期处理 Dependabot 和 dependency review 反馈
