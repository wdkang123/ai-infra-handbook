# v0.1 Release Notes 草稿

这页给出一份更接近最终 GitHub Release 的 v0.1 草稿。
它和 [v0.1 首发发布手册](/08-publication/10-v0-1-release-playbook) 的区别是：首发手册解释“如何发布”，这页更像“发布时可以直接贴什么”。

发布前也可以运行 `PYTHON=.venv/bin/python make launch-pack`，从 [自动生成首发运营包](/08-publication/13-generated-launch-pack) 里拿到基于当前 release brief 和 roadmap pack 的 release notes draft。
这页保留人工精修版本，launch pack 保留机器生成版本。

## 推荐标题

```text
AI Infra Handbook v0.1.0-learning-site
```

## 推荐摘要

```text
这是 AI Infra Handbook 的第一个学习型公开版本。

它不是生产平台，而是一套能边学边跑的 AI Infra 学习站：用文档站、四个可运行学习项目、hands-on labs、案例复盘、输出证据和共学材料，帮助读者理解 LLM serving、AI Gateway、Evaluation / Observability、Finetuning / Training 之间的工程关系。
```

## Highlights

```text
Highlights

- VitePress 学习站已可通过 GitHub Pages 发布
- README、学习路线、从 0 到 1、Runbook 和两周学习计划已经形成新手入口
- 四个学习型项目已形成最小闭环：
  - inference-service
  - ai-gateway
  - eval-module
  - finetune-demo
- Hands-on labs 覆盖 Serving、Gateway、Eval、Finetune、Capstone 和公开发布验收
- 案例复盘覆盖：
  - 请求失败排查
  - 模型发布判断
  - 训练产物复现
  - Gateway fallback/cache
  - Eval 退化与发布阻断
- 示例输出与证据库帮助读者判断命令是否跑对、字段意味着什么、失败时看哪里
- 自动生成材料覆盖：
  - learning inventory
  - course catalog
  - evidence packet
  - release brief
  - workshop packet
  - assessment pack
  - roadmap pack
  - launch pack
- 公开协作材料已补齐：
  - issue templates
  - PR template
  - CONTRIBUTING
  - SECURITY
  - CODE_OF_CONDUCT
  - PUBLICATION_CHECKLIST
  - 维护节奏与 issue triage 文档
```

## Verification

发布前建议把实际结果填到这里：

```text
Verification

- PYTHON=.venv/bin/python make public-check
  - security scan passed
  - docs quality passed
  - project tests passed
  - docs build passed

- npm audit --omit=dev --audit-level=moderate
  - 0 vulnerabilities

- GitHub Actions
  - ci: success
  - docs-pages: success

- GitHub Pages
  - site returns HTTP/2 200
```

如果你跑了完整发布链路，也可以补充：

```text
- PYTHON=.venv/bin/python make infra-smoke
- PYTHON=.venv/bin/python make infra-evidence
- PYTHON=.venv/bin/python make release-brief
- PYTHON=.venv/bin/python make workshop-packet
- PYTHON=.venv/bin/python make assessment-pack
- PYTHON=.venv/bin/python make roadmap-pack
- PYTHON=.venv/bin/python make launch-pack
```

## What This Release Is For

```text
This release is for:

- Learners who want a structured path into AI Infra
- Engineers who want to see how serving, gateway, eval, and finetuning fit together
- Study group organizers who need labs, workbook prompts, review templates, and issue seeds
- Maintainers who want a public-safe learning repo with CI, Pages, security checks, and contribution templates
```

## What This Release Is Not

```text
This release is not:

- A production inference platform
- A production AI gateway
- A full eval platform
- A real training system
- A benchmark leaderboard service

The default path intentionally uses mock/local scaffolds so readers can run, inspect, and modify the system without external services or private credentials.
```

## Suggested First Issues

发布后可以从 [首批公开 Issues 草稿](/08-publication/11-first-public-issues) 或 [自动生成首发运营包](/08-publication/13-generated-launch-pack) 中挑 6 到 10 条创建。
最推荐先创建：

```text
- [Docs] Add first-run FAQ entries for setup and local docs startup
- [Docs] Expand serving and gateway evidence field explanations
- [Lab] Add a gateway fallback and cache regression lab
- [Docs] Add an eval regression review exercise
- [Roadmap] Add a real OpenAI-compatible serving migration guide
- [Roadmap] Add a minimal judge adapter example for eval-module
```

这些 issue 能覆盖新手卡点、证据解释、lab 深度和进阶迁移方向。

## Post-release Checklist

```text
After publishing:

- Confirm the release page links to the GitHub Pages site
- Confirm README links to the public site and release notes if needed
- Confirm ci and docs-pages are green on main
- Confirm open PR count is expected
- Create the first public issues
- Watch first-week feedback and route it to FAQ, troubleshooting, labs, evidence, or roadmap
```

## Changelog Entry

可以把这一段同步到 `CHANGELOG.md` 的第一个正式版本区块：

```text
## v0.1.0-learning-site

### Added

- Initial public learning site for AI Infra.
- Runnable learning scaffolds for inference-service, ai-gateway, eval-module, and finetune-demo.
- Hands-on labs, case studies, assessments, output gallery, workshop kit, production migration notes, and publication playbooks.
- CI, GitHub Pages workflow, dependency review, Dependabot, security scan, issue templates, PR template, and public maintenance guidance.

### Verified

- public-check
- npm audit
- GitHub Actions ci
- GitHub Actions docs-pages
- GitHub Pages HTTP 200
```

## 下一步

- 如果你还没有整理 issue 池，先看 [首批公开 Issues 草稿](/08-publication/11-first-public-issues)。
- 如果你要决定是否现在发布，先看 [v0.1 首发发布手册](/08-publication/10-v0-1-release-playbook)。
- 如果你要自动复核 release notes、starter issues 和发布后检查表，先看 [自动生成首发运营包](/08-publication/13-generated-launch-pack)。
- 如果你要维护首发后一周反馈，看 [维护节奏与运营清单](/08-publication/08-maintainer-rhythm)。
