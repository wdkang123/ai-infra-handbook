# 首批公开 Issues 草稿

这页把项目首发后可以创建的第一批 GitHub issues 直接整理成可复制草稿。
它的目标是让公开仓库一打开就能看到清楚、可验证、适合不同贡献者参与的小任务。

## 使用原则

先不要一次创建太多 issue。首批建议 6 到 10 条，覆盖：

- FAQ 和排障
- 示例输出和证据库
- hands-on lab
- 工程案例
- 生产迁移
- 公开发布和维护

每条 issue 都应该有：

- 学习价值
- 建议范围
- 验收标准
- 推荐验证命令
- 默认 labels

初期只使用 GitHub 默认 labels：`documentation`、`enhancement`、`good first issue`、`help wanted`、`question`。
如果你已经在仓库里创建了 `lab`、`evidence`、`feedback`、`case-study` 等自定义标签，可以手动补上。

## 推荐创建顺序

| 顺序 | 类型 | 为什么先做 |
| --- | --- | --- |
| 1 | FAQ / 排障 | 第一批读者最容易卡在启动和理解路径 |
| 2 | 输出证据 | 读者跑完命令后需要知道看哪里 |
| 3 | Lab 补强 | 让学习变成可执行任务 |
| 4 | 案例复盘 | 提升内容深度和工程判断力 |
| 5 | 生产迁移 | 给进阶读者清楚方向 |
| 6 | 发布维护 | 让仓库可长期运营 |

## Issue 1：补充首次运行 FAQ

```text
Title:
[Docs] Add first-run FAQ entries for setup and local docs startup

Labels:
documentation, good first issue

Learning value:
New learners often get stuck before reaching the AI Infra concepts. This issue improves the first 10 minutes of the project by documenting common setup and docs startup questions.

Scope:
- Add 3 to 5 FAQ entries about Node 22, npm install, Python virtualenv, docs dev server, and where to start after opening the site.
- Link each FAQ answer to the relevant runbook or troubleshooting page.

Suggested files:
- docs/00-overview/10-faq.md
- docs/00-overview/03-runbook.md
- docs/09-reference/04-troubleshooting.md

Acceptance criteria:
- Each FAQ entry has a concrete symptom and next step.
- Each entry links to at least one deeper page.
- No real local username, private path, token, or account detail is included.

Verification:
- PYTHON=.venv/bin/python make docs-quality
```

## Issue 2：补充 Serving/Gateway 输出证据字段解释

```text
Title:
[Docs] Expand serving and gateway evidence field explanations

Labels:
documentation, good first issue

Learning value:
Learners can run the commands, but they need help understanding which headers, events, and metrics prove the request path is healthy.

Scope:
- Add short explanations for x-request-id, x-upstream-model, x-fallback-used, x-cache, and events timeline fields.
- Include one sanitized example for success and one for fallback.

Suggested files:
- docs/13-output-gallery/01-serving-gateway-evidence.md
- docs/13-output-gallery/05-failure-evidence-map.md
- docs/11-case-studies/04-gateway-fallback-cache-incident.md

Acceptance criteria:
- Fields are explained in learner-friendly language.
- Examples are sanitized and use placeholder request ids.
- The page explains what each field can prove and what it cannot prove.

Verification:
- PYTHON=.venv/bin/python make docs-quality
```

## Issue 3：增加 Gateway fallback 回归 Lab

```text
Title:
[Lab] Add a gateway fallback and cache regression lab

Labels:
documentation, enhancement, help wanted

Learning value:
Gateway fallback and cache are easy to misunderstand because the response may be 200 even when the path changed. A lab helps learners practice controlled degradation analysis.

Scope:
- Add a lab that sends repeated gateway requests with request ids.
- Ask learners to compare x-fallback-used, x-cache, gateway timeline, and failure summary.
- Include a short reflection question about quality, cost, and latency risk.

Suggested files:
- docs/07-hands-on-labs/02-gateway-resilience-lab.md
- docs/11-case-studies/04-gateway-fallback-cache-incident.md
- docs/13-output-gallery/01-serving-gateway-evidence.md

Acceptance criteria:
- The lab has goal, prerequisites, commands, evidence requirements, and acceptance criteria.
- It does not require any external model or paid service.
- It points to at least one case study and one evidence page.

Verification:
- PYTHON=.venv/bin/python make docs-quality
- PYTHON=.venv/bin/python make public-check
```

## Issue 4：补充 Eval 退化阻断练习

```text
Title:
[Docs] Add an eval regression review exercise

Labels:
documentation, enhancement

Learning value:
Learners should understand that model release decisions are not only based on aggregate score. Sample-level regression and setting comparability matter.

Scope:
- Add a short exercise that asks learners to inspect comparison report, sample outputs, and sample analysis.
- Include a release gate decision template.
- Link to the Eval regression case study.

Suggested files:
- docs/07-hands-on-labs/03-eval-release-gate-lab.md
- docs/11-case-studies/05-eval-regression-release-gate.md
- docs/10-assessments/03-eval-finetune-quiz.md

Acceptance criteria:
- Exercise includes review, block, and retest outcomes.
- It explains when settings_changed invalidates a comparison.
- It includes at least one reflection question about failed sample clusters.

Verification:
- PYTHON=.venv/bin/python make docs-quality
```

## Issue 5：增加 OpenAI-compatible Serving 迁移指南

```text
Title:
[Roadmap] Add a real OpenAI-compatible serving migration guide

Labels:
enhancement, help wanted

Learning value:
Advanced learners need a clear bridge from the mock inference-service to a real OpenAI-compatible local serving backend.

Scope:
- Explain the migration path from learning service to real vLLM/SGLang-style OpenAI-compatible endpoint.
- Keep the mock path as the default.
- Document environment variables, health checks, request shape, and failure boundaries.

Suggested files:
- docs/02-inference-serving/10-from-learning-service-to-real-serving-stack.md
- docs/12-production-migration/01-serving-backend-migration.md
- projects/inference-service/README.md

Acceptance criteria:
- The guide clearly separates learning mock path and real backend path.
- It does not require readers to download large models just to follow the default tutorial.
- It includes rollback guidance if the real backend is unavailable.

Verification:
- PYTHON=.venv/bin/python make docs-quality
- PYTHON=.venv/bin/python make public-check
```

## Issue 6：增加最小 Judge Adapter 示例

```text
Title:
[Roadmap] Add a minimal judge adapter example for eval-module

Labels:
enhancement, help wanted

Learning value:
Evaluation becomes much clearer when learners can see where a judge adapter fits between raw model output, sample scoring, and release recommendation.

Scope:
- Add a small documented adapter interface or example.
- Keep the default eval path lightweight and offline-friendly.
- Explain how judge prompt/versioning would be handled in a real system.

Suggested files:
- docs/04-evaluation-observability/04-evaluation-tools-and-surfaces.md
- docs/12-production-migration/03-eval-judge-dashboard-migration.md
- projects/eval-module/src/eval_module/
- projects/eval-module/tests/

Acceptance criteria:
- The adapter example is small and testable.
- It does not require external API keys by default.
- Docs explain what is learning scaffold vs production judge service.

Verification:
- PYTHON=.venv/bin/python make infra-check
```

## Issue 7：补充 Finetune checkpoint selection Lab

```text
Title:
[Lab] Add a finetune checkpoint selection and resume lab

Labels:
documentation, enhancement

Learning value:
Training artifacts become meaningful when learners can decide which checkpoint to export, why it is resumable, and how dataset fingerprints connect to eval.

Scope:
- Add a lab section about checkpoint index, latest checkpoint, hash, export manifest, and dataset sha256.
- Include a decision checklist for choosing a checkpoint.
- Link the lab to the finetune asset lineage case study.

Suggested files:
- docs/07-hands-on-labs/04-finetune-reproducibility-lab.md
- docs/11-case-studies/03-finetune-to-eval-asset-lineage.md
- docs/13-output-gallery/03-finetune-artifact-evidence.md

Acceptance criteria:
- Learners can explain why a checkpoint is safe or unsafe to export.
- The lab includes artifact evidence requirements.
- No real model weights or private datasets are committed.

Verification:
- PYTHON=.venv/bin/python make docs-quality
- PYTHON=.venv/bin/python make public-check
```

## Issue 8：补充 Streaming 中途失败案例

```text
Title:
[Docs] Add a streaming partial failure case study

Labels:
documentation, enhancement

Learning value:
Streaming failures are different from normal 4xx/5xx responses because the client may have already received partial output. Learners should understand why fallback after first chunk is dangerous.

Scope:
- Add a case study or subsection about streaming error events.
- Compare pre-first-token fallback and post-first-chunk failure.
- Link to gateway streaming errors and output evidence pages.

Suggested files:
- docs/03-ai-gateway-platform/04-streaming-errors-upstream-health.md
- docs/11-case-studies/01-request-incident-walkthrough.md
- docs/13-output-gallery/05-failure-evidence-map.md

Acceptance criteria:
- The page explains why not every streaming failure can safely fallback.
- It includes a request id based evidence trail.
- It distinguishes server behavior from client UX handling.

Verification:
- PYTHON=.venv/bin/python make docs-quality
```

## Issue 9：整理首发反馈到 FAQ 和路线图

```text
Title:
[Roadmap] Turn first-week feedback into FAQ and roadmap updates

Labels:
documentation, help wanted

Learning value:
The first week after public launch should improve the learning path instead of producing scattered comments.

Scope:
- Collect repeated feedback themes from issues, workshop feedback, or direct reader notes.
- Convert repeated questions into FAQ or troubleshooting entries.
- Convert larger tasks into bounded roadmap issues.

Suggested files:
- docs/00-overview/10-faq.md
- docs/09-reference/04-troubleshooting.md
- docs/08-publication/03-public-roadmap.md
- docs/08-publication/11-first-public-issues.md

Acceptance criteria:
- At least 3 feedback themes are categorized.
- FAQ/troubleshooting gets concrete updates.
- Larger work is split into issues with acceptance criteria.

Verification:
- PYTHON=.venv/bin/python make docs-quality
```

## Issue 10：补充 v0.1 release 后复盘

```text
Title:
[Docs] Add a v0.1 release retrospective

Labels:
documentation

Learning value:
Release retrospectives teach maintainers how to keep a public learning project honest: what was promised, what was verified, and what still needs work.

Scope:
- Add a short v0.1 retrospective after the first release is created.
- Record CI/Pages status, public-check result, open issue themes, and next roadmap priorities.
- Keep the tone factual and learning-oriented.

Suggested files:
- docs/08-publication/10-v0-1-release-playbook.md
- CHANGELOG.md
- docs/08-publication/03-public-roadmap.md

Acceptance criteria:
- Retrospective includes verification commands and outcomes.
- It lists what v0.1 intentionally does not cover.
- It links to next issues or roadmap sections.

Verification:
- PYTHON=.venv/bin/python make public-check
```

## 创建前检查

真正创建这些 issues 前，建议先确认：

- 仓库 labels 至少有 GitHub 默认标签
- Issue templates 能正常显示
- `main` 上 `ci` 和 `docs-pages` 最近一次通过
- [Issue 分类与标签策略](/08-publication/09-issue-triage-and-labels) 已经更新
- [维护节奏与运营清单](/08-publication/08-maintainer-rhythm) 已经说明每周 triage 节奏

首批 issues 的目标不是把路线图铺满，而是给读者一个清楚信号：这个项目欢迎小而可验证的贡献。
