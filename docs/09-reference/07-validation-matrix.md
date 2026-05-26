# 验证矩阵

这页回答一个维护项目时经常遇到的问题：

> 我改了某一块，应该跑哪些检查？

不要每次都盲目全跑，也不要只跑最轻的命令。  
更好的做法是根据影响面选择验证层级。

## 验证层级

| 层级 | 命令 | 覆盖内容 | 适用场景 |
| --- | --- | --- | --- |
| 格式与 lint | `make infra-format` | Ruff format、Ruff fix、lint | 改 Python 或脚本后 |
| 文档质量 | `make docs-quality` | Markdown 内链与 heading 锚点、H1 结构、VitePress nav/sidebar 路由、首页配置与 Vue 组件链接、README 入口、首页统计 | 改文档、导航、首页后 |
| 学习站清单 | `make docs-inventory` | 章节、页面、课程主线、内容信号和 Makefile 目标盘点 | 改课程结构或公开发布前 |
| 课程目录 | `make course-catalog` | 可带练课程模块、页面组、检查点、讲师提示和推荐命令 | 改课程路径、组织共学或公开课程前 |
| 单元测试 | `make infra-test` | 四个项目测试 | 改项目代码后 |
| 文档构建 | `make docs-build` | VitePress build | 改文档站后 |
| 安全检查 | `make security-check` | 候选入库文件中的密钥、私钥、连接串、本机路径、个人痕迹和危险文件类型 | 公开上传、PR 或 release 前 |
| 公开上传检查 | `make public-check` | security-check + infra-check | GitHub 上传、PR 和公开分享前 |
| 综合检查 | `make infra-check` | lint、测试、docs-quality、docs build | 常规提交前 |
| 端到端 smoke | `make infra-smoke` | gateway / inference / eval / finetune 最小链路 | 改跨项目行为后 |
| 证据包生成 | `make infra-evidence` | 汇总 `.tmp/smoke` 的 serving、eval、finetune 证据 | 跑完 smoke 后整理复盘 |
| 发布摘要 | `make release-brief` | 合成学习站清单和证据包，生成 release readiness 摘要 | GitHub 首发、PR 复盘或公开演示前 |
| 共学包 | `make workshop-packet` | 合成课程目录和发布摘要，生成议程、模块卡片、学习者交付和复盘问题 | 组织共学或公开分享前 |
| 测评包 | `make assessment-pack` | 合成课程目录和共学包，生成模块题目、证据要求、rubric 和 Capstone review | 自测、带练测评或 PR review 前 |
| 路线图包 | `make roadmap-pack` | 合成发布摘要和测评包，生成 GitHub issue 种子、推荐 label 和验收命令 | GitHub 首发、公开路线图或反馈回流前 |
| 首发运营包 | `make launch-pack` | 合成发布摘要和路线图包，生成 release notes、starter issues、默认标签和发布后检查表 | 创建 release、首批 issue 或发布后复盘前 |
| 发布前整体验收 | `make infra-release` | format、inventory、course catalog、public-check、smoke、evidence、release brief、workshop packet、assessment pack、roadmap pack、launch pack | 正式公开发布前 |
| 依赖审计 | `npm audit --omit=dev --audit-level=moderate` | Node 依赖漏洞 | 发布前 |

## 按改动类型选择

| 改动类型 | 最少应该跑 | 建议再跑 |
| --- | --- | --- |
| 只改 Markdown 正文 | `make docs-quality` | `make docs-build` |
| 改 sidebar、首页或导航 | `make docs-quality`、`make docs-inventory` | `make infra-check` |
| 改 README、发布清单、贡献指南 | `make docs-quality` | `make infra-check` |
| 改课程主线或学习路径 | `make docs-inventory`、`make course-catalog`、`make docs-quality` | `make docs-build` |
| 改 inference-service API | `make inference-test` | `make infra-check`、`make infra-smoke` |
| 改 ai-gateway 路由/鉴权/fallback | `make gateway-test` | `make infra-check`、`make infra-smoke` |
| 改 eval run/compare/index | `make eval-test` | `make infra-check`、`make infra-smoke` |
| 改 finetune train/export/index | `make finetune-test` | `make infra-check`、`make infra-smoke` |
| 改 smoke 脚本 | `make infra-smoke` | `make infra-check` |
| 改证据包生成器 | `make scripts-test`、`make infra-evidence` | `make infra-smoke`、`make infra-check` |
| 改学习站清单生成器 | `make scripts-test`、`make docs-inventory` | `make docs-quality`、`make infra-check` |
| 改课程目录生成器 | `make scripts-test`、`make course-catalog` | `make docs-quality`、`make infra-check` |
| 改发布摘要生成器 | `make scripts-test`、`make release-brief` | `make infra-release` |
| 改共学包生成器 | `make scripts-test`、`make workshop-packet` | `make infra-release` |
| 改测评包生成器 | `make scripts-test`、`make assessment-pack` | `make infra-release` |
| 改路线图包生成器 | `make scripts-test`、`make roadmap-pack` | `make infra-release` |
| 改首发运营包生成器 | `make scripts-test`、`make launch-pack` | `make infra-release` |
| 改 GitHub Pages workflow | `make docs-quality`、`npm run docs:build` | 首次配置后手动跑一次 workflow |
| 改 `tasks/` 或 `prompts/` 公开工作台 | `make security-check` | `make public-check` |
| 准备公开发布 | `make public-check`、`make infra-release` | `npm audit --omit=dev --audit-level=moderate` |

## 按系统层选择

### 执行层：inference-service

优先跑：

```bash
PYTHON=.venv/bin/python make inference-test
```

如果改到了 `/v1/chat/completions`、streaming、metrics、events 或模型列表，再跑：

```bash
PYTHON=.venv/bin/python make infra-smoke
```

重点观察：

- direct inference 是否成功
- unknown model 是否仍然返回预期错误
- empty messages 是否仍然校验
- `/events/requests` 是否仍然能查 timeline

### 治理层：ai-gateway

优先跑：

```bash
PYTHON=.venv/bin/python make gateway-test
```

如果改到了鉴权、路由、fallback、cache、事件或 upstream health，再跑：

```bash
PYTHON=.venv/bin/python make infra-smoke
```

重点观察：

- `401 / 404 / 429 / 502` 语义是否保持
- `x-request-id` 是否贯穿
- `x-upstream-model`、`x-fallback-used`、`x-cache` 是否正常
- `/events/failures` 是否仍然聚合失败

### 质量层：eval-module

优先跑：

```bash
PYTHON=.venv/bin/python make eval-test
```

如果改到了 run bundle、comparison、leaderboard、run index、comparison index 或 sample analysis，再跑：

```bash
PYTHON=.venv/bin/python make infra-smoke
```

重点观察：

- `sample_outputs.json`
- `sample_summary.json`
- `sample_analysis.json`
- `run_index.json`
- `comparison_index.json`
- `leaderboard.json`

### 训练层：finetune-demo

优先跑：

```bash
PYTHON=.venv/bin/python make finetune-test
```

如果改到了 train、export、dataset registry、checkpoint index、run/export index，再跑：

```bash
PYTHON=.venv/bin/python make infra-smoke
```

重点观察：

- `run_manifest.json`
- `artifacts_manifest.json`
- `checkpoints/checkpoint_index.json`
- `dataset_registry_report.json`
- `run_index.json`
- `export_index.json`
- `export_manifest.json`
- `.tmp/smoke/evidence/evidence_packet.json`

## 发布前验证顺序

公开发布前建议按这个顺序：

```bash
nvm use
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
PYTHON=.venv/bin/python make launch-pack
npm audit --omit=dev --audit-level=moderate
```

这个顺序的好处是：

1. 先把格式和自动修复做完
2. 先生成学习站清单，检查课程结构是否完整
3. 再生成课程目录，检查可带练模块是否完整
4. 再用轻量文档检查发现导航漂移
5. 再跑测试和文档构建
6. 最后跑端到端链路
7. 汇总本轮输出证据
8. 合成发布摘要
9. 生成共学包，检查公开带练材料是否可用
10. 生成测评包，检查模块题目和评分标准是否可用
11. 生成路线图包，检查首批 issue 是否能承接反馈
12. 生成首发运营包，检查 release notes、starter issues 和发布后检查表是否一致
13. 发布前补依赖安全底线

## 验证失败时怎么判断

| 失败位置 | 优先排查 |
| --- | --- |
| `infra-format` | Ruff 输出的文件和规则 |
| `docs-quality` | 新页面是否进 sidebar、是否有唯一 H1、nav/sidebar 路由和首页配置/组件链接是否存在、链接与 heading 锚点是否存在、首页统计是否更新 |
| `docs-inventory` | 新页面是否有 H1、课程主线里的路由是否存在、`.tmp/docs-inventory/learning_inventory.md` 是否能生成 |
| `course-catalog` | `.tmp/docs-inventory/learning_inventory.json` 是否存在、课程目录里的页面和主线是否仍然完整 |
| `docs-build` | Markdown 语法、VitePress 组件、内部链接 |
| `security-check` | 候选入库文件是否包含真实密钥、本机路径、个人痕迹或危险文件类型 |
| `inference-test` | `projects/inference-service/tests/test_api.py` |
| `gateway-test` | `projects/ai-gateway/tests/test_proxy.py` |
| `eval-test` | `projects/eval-module/tests/test_runner.py` |
| `finetune-test` | `projects/finetune-demo/tests/test_trainer.py` |
| `infra-smoke` | `scripts/integration_smoke_test.sh` 和 `.tmp/smoke` 产物 |
| `infra-evidence` | `.tmp/smoke` 是否存在，或 `scripts/build_evidence_packet.py` 是否能读取关键 JSON |
| `release-brief` | 学习站清单和证据包是否存在、strict 门禁是否发现缺路由或缺证据 |
| `workshop-packet` | 课程目录和发布摘要是否存在、课程目录是否 ready、发布摘要是否 ready |
| `assessment-pack` | 课程目录和共学包是否存在、模块数量是否一致、共学包是否 ready |
| `roadmap-pack` | 发布摘要和测评包是否存在、发布摘要是否 ready、测评包是否 ready、模块和题目是否可用 |
| `launch-pack` | 发布摘要和路线图包是否存在、发布摘要是否 ready、路线图包是否 ready、issue seeds 是否可用 |

如果失败发生在跨服务链路，不要只看最后一个错误。  
先看 request id、events、summary、产物文件，再回到代码。

相关案例：

- [请求失败排查案例](/11-case-studies/01-request-incident-walkthrough)
- [模型发布判断案例](/11-case-studies/02-model-release-decision-walkthrough)
- [训练产物复现案例](/11-case-studies/03-finetune-to-eval-asset-lineage)
