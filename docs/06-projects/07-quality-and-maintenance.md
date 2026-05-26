# 质量与维护入口

这个仓库的质量目标，不是把学习项目伪装成生产系统。
它的目标是保证每一步学习、改动、联调和公开发布都有清晰验收入口。

换句话说：

- 文档要能被发现、能构建、内链不漂移。
- 项目要能测试、能 smoke、错误路径可解释。
- 公开仓库要避免密钥、个人痕迹和危险文件。
- 迁移路线要保留接口、观测和证据。
- 每次改动后要知道该跑哪些检查。

这页把维护入口集中起来。

## 质量不是一个命令

项目质量至少分成五层：

| 层 | 关注什么 | 典型命令 |
| --- | --- | --- |
| 文档质量 | 内链、H1、导航、构建 | `make docs-quality`、`make docs-build` |
| 代码质量 | lint、单元测试 | `make infra-lint`、`make infra-test` |
| 跨项目链路 | gateway/inference/eval/finetune 能否联动 | `make infra-smoke` |
| 公开安全 | 密钥、私钥、本机路径、个人痕迹 | `make security-check`、`make public-check` |
| 发布证据 | inventory、course catalog、evidence、release/workshop/assessment/roadmap/launch pack | `make infra-release` |

不要把质量理解成“测试过了”。
文档站、公开安全、跨项目证据和发布材料同样属于质量。

## 最常用的本地检查

从仓库根目录执行：

```bash
PYTHON=.venv/bin/python make infra-check
```

它会依次运行：

- Python lint
- 四个项目的单元测试
- 文档质量检查
- VitePress 文档构建

如果准备公开上传或提交 PR，运行：

```bash
PYTHON=.venv/bin/python make public-check
```

它会在 `infra-check` 前先跑安全扫描。

## 文档改动怎么验收

只改 Markdown 正文时，至少跑：

```bash
PYTHON=.venv/bin/python make docs-quality
```

它会检查：

- Markdown 本地链接
- heading 锚点
- H1 结构
- VitePress nav/sidebar 路由
- 首页配置
- Vue 组件链接
- README 关键入口
- 首页文档页统计

如果改了站点结构、首页或导航，再跑：

```bash
npm run docs:build
```

公开分享前，建议跑：

```bash
PYTHON=.venv/bin/python make public-check
```

这样能同时覆盖安全扫描、测试和构建。

## 代码改动怎么验收

如果只改某个项目，可以先跑项目级测试：

```bash
PYTHON=.venv/bin/python make inference-test
PYTHON=.venv/bin/python make gateway-test
PYTHON=.venv/bin/python make eval-test
PYTHON=.venv/bin/python make finetune-test
```

如果改动跨项目，或者影响 API、events、metrics、history、manifest、smoke 产物，继续跑：

```bash
PYTHON=.venv/bin/python make infra-smoke
```

`infra-smoke` 会临时启动 inference-service 和 ai-gateway，并验证：

- direct inference
- gateway proxy
- health / metrics / events
- eval run / compare / leaderboard / index
- finetune train / export / registry / index
- serving/eval/finetune evidence snapshots

它是当前仓库最重要的跨项目闭环。

## 什么时候必须跑 Smoke

只改文档时，通常不需要 smoke。

改到这些内容时，建议跑：

```bash
PYTHON=.venv/bin/python make infra-smoke
```

包括：

- `projects/inference-service/`
- `projects/ai-gateway/`
- `projects/eval-module/`
- `projects/finetune-demo/`
- 根级 `Makefile`
- `scripts/integration_smoke_test.sh`
- `scripts/build_evidence_packet.py`
- 影响 API surface、CLI surface 或 output gallery 的改动

因为这些改动可能让单项目测试通过，但跨项目链路断掉。

## 公开上传前怎么检查

公开仓库最怕“功能能跑，但不该公开的东西进去了”。

公开前至少跑：

```bash
PYTHON=.venv/bin/python make public-check
npm audit --omit=dev --audit-level=moderate
```

`public-check` 会覆盖：

- high-confidence secrets
- private keys
- connection strings
- local paths
- personal markers
- risky file types
- lint/tests/docs build

这对 GitHub 上传很关键。
内容越丰富，越应该经常跑这类检查。

## 当前质量边界

现在这些检查能保证：

- 项目入口不会因为 Python 路径失效。
- 文档站不会悄悄出现内部断链。
- 新增页面不会缺少顶层 H1 或出现多个 H1。
- VitePress nav/sidebar 不会指向不存在页面。
- 首页配置、Vue 静态链接和数据驱动链接不会漂移。
- gateway/inference/eval/finetune 的最小闭环可重复运行。
- inference adapter 的上游失败会稳定映射为结构化错误。
- inference streaming 失败会以结构化 SSE error 结束。
- gateway 普通请求和首 chunk 前 streaming 请求支持 fallback。
- gateway cache 覆盖 TTL 过期和 token 隔离。
- eval compare 可以用最小差异阈值避免噪声判定，并拒绝不同 task 混比。
- finetune 数据、训练产物与导出产物具备基本结构校验。
- 公开候选文件不会包含扫描器能识别的高风险公开问题。

这些检查还不能保证：

- 真实模型推理质量。
- 真实 GPU 训练行为。
- 生产级并发可靠性。
- 完整分布式 tracing。
- 线上权限和计费系统安全。
- 所有内容一定足够深入。

这些边界要讲清楚。
学习项目可以认真，但不能伪装成生产平台。

## 改动类型和推荐检查

| 改动类型 | 最少跑 | 建议再跑 |
| --- | --- | --- |
| Markdown 正文 | `make docs-quality` | `make docs-build` |
| 导航、首页、sidebar | `make docs-quality` | `make public-check` |
| inference API / streaming / events | `make inference-test` | `make infra-smoke` |
| gateway auth / routing / fallback / cache | `make gateway-test` | `make infra-smoke` |
| eval run / compare / index | `make eval-test` | `make infra-smoke` |
| finetune train / export / registry | `make finetune-test` | `make infra-smoke` |
| smoke 或证据包 | `make scripts-test` | `make infra-smoke`、`make infra-evidence` |
| 发布前 | `make public-check` | `make infra-release`、`npm audit --omit=dev --audit-level=moderate` |

更完整的规则见 [验证矩阵](/09-reference/07-validation-matrix)。

## 失败时怎么排查

### docs-quality 失败

先看：

- 新页面是否有 H1。
- 页面是否进了 sidebar。
- 内链路径是否真实存在。
- heading 锚点是否拼错。
- 首页统计是否需要更新。

### 项目测试失败

先看对应项目：

- `projects/inference-service/tests/test_api.py`
- `projects/ai-gateway/tests/test_proxy.py`
- `projects/eval-module/tests/test_runner.py`
- `projects/finetune-demo/tests/test_trainer.py`

不要先猜系统整体问题。
先定位是哪一层破了。

### infra-smoke 失败

先看 `.tmp/smoke` 和 `/tmp/ai-infra-*.log`。
再按系统地图排查：

1. inference 是否启动。
2. gateway 是否启动。
3. gateway health 是否能探测 upstream。
4. direct inference 是否成功。
5. gateway proxy 是否成功。
6. eval 是否生成 run/compare/index。
7. finetune 是否生成 run/export/index。
8. evidence packet 是否能读取产物。

跨项目失败不要只看最后一个错误。
要沿 request id、events、metrics 和 artifact 逐层查。

## 发布证据怎么使用

如果你已经跑过 smoke，可以继续生成证据包：

```bash
PYTHON=.venv/bin/python make infra-evidence
```

它会把 `.tmp/smoke` 里的 serving、eval、finetune 证据汇总成 JSON/Markdown。

继续往公开分享走，可以跑：

```bash
PYTHON=.venv/bin/python make release-brief
PYTHON=.venv/bin/python make workshop-packet
PYTHON=.venv/bin/python make assessment-pack
PYTHON=.venv/bin/python make roadmap-pack
PYTHON=.venv/bin/python make launch-pack
```

这些命令把“项目能跑”进一步变成：

- release readiness
- 共学材料
- 测评题目
- roadmap issue seeds
- 首发运营包

对公开网站来说，这些材料能帮助读者、贡献者和维护者进入同一套标准。

## 常见误区

### “只改文档不用检查”

不对。
文档站有导航、内链、锚点、构建和首页入口，文档改动也可能破站。

### “测试通过就能公开”

不够。
公开前还要跑安全扫描和依赖审计。

### “Smoke 太重，没必要”

如果改跨项目行为，smoke 很必要。
它能发现单项目测试看不到的联动问题。

### “质量检查只是维护者的事”

不是。
学习者也可以通过这些命令理解系统边界。

### “学习项目不用这么认真”

恰好相反。
学习项目越公开，越需要把边界、风险和验收讲清楚。

## 学完应该能回答

读完这一页后，你应该能回答：

1. `infra-check`、`public-check`、`infra-smoke` 分别覆盖什么？
2. 只改文档、改单项目、改跨项目行为时应该跑哪些命令？
3. 当前质量检查能保证什么，不能保证什么？
4. `infra-smoke` 失败时应该怎么沿系统地图排查？
5. 公开发布前为什么要同时看安全扫描、构建、测试和证据包？

## 继续阅读

- [验证矩阵](/09-reference/07-validation-matrix)
- [示例输出与证据库](/13-output-gallery/00-overview)
- [公开仓库卫生规范](/08-publication/06-public-repo-hygiene)
- [生产迁移路线总览](/12-production-migration/00-overview)
