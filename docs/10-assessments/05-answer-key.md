# 参考答案与讲解

这里不是唯一答案。  
AI Infra 的很多问题没有标准话术，但有相对稳定的判断依据：边界是否清楚、链路是否完整、失败路径是否能解释、验证方式是否可信。

## 系统地图

### inference-service 的核心问题

它是执行层，负责把模型能力包装成 HTTP 服务。  
在这个仓库里，它提供 `/health`、`/metrics`、`/v1/chat/completions`，并通过 engine adapter 把请求交给具体生成后端。

合格回答应该包含：

- 它不负责平台鉴权
- 它应该关心请求格式、生成结果、streaming、engine 错误语义和服务指标
- 它是 gateway 的下游

### gateway 为什么不是普通 proxy

因为它承担平台治理职责。  
普通 proxy 只转发请求，而 gateway 还需要处理：

- 认证
- 模型名映射
- 限流
- request id
- fallback
- cache
- upstream health
- 统一错误语义

所以它是治理层，不只是网络转发层。

### eval-module 为什么是质量闭环

它不只是执行一个分数脚本。  
它把一次评测变成可追踪资产：

- run
- metrics
- sample outputs
- sample summary
- report
- bundle
- history
- comparison
- leaderboard

质量判断需要比较、追踪和复盘，所以 eval-module 属于质量闭环层。

### finetune-demo 为什么强调资产

训练工程的核心不是“命令跑完”，而是以后能不能解释和复现这次训练。  
因此需要保存：

- config
- dataset summary
- metrics
- logs
- checkpoint
- artifacts manifest
- export manifest

没有这些信息，训练结果很难被审计、复现或接入后续 serving / eval。

## Serving 与 Gateway

### TTFT 和总耗时

TTFT 是从请求发出到收到第一个 token 的时间。  
总耗时是完整响应结束的时间。

TTFT 主要影响用户是否觉得系统“开始响应了”。  
总耗时影响任务什么时候真正完成。

streaming 可以降低体感等待，因为用户更早看到第一个 token。  
但模型仍然需要继续 decode 后续 token，所以它不等于让完整生成免费变快。

### Streaming error 为什么特殊

普通 JSON response 在发送 body 前可以决定最终 status 和错误结构。  
Streaming 一旦已经开始发送 chunk，HTTP status 通常已经确定，后续失败只能通过 stream 内的 error event 或连接中断表达。

因此 gateway 做 streaming fallback 时必须区分：

- 首个 chunk 前失败：还可以尝试 fallback
- 首个 chunk 后失败：不能假装请求从未开始，只能向客户端发 error event 或结束流

### 常见错误归属

| 场景 | 期望 status | 主要归属层 |
| --- | --- | --- |
| 缺少认证头 | `401` | gateway |
| 认证格式错误 | `401` | gateway |
| 模型名不存在 | `404` | gateway routing |
| 超过限流 | `429` | gateway |
| upstream 5xx | `502` | gateway 调用下游 |
| engine adapter 映射上游错误 | `502` | inference-service / engine adapter |
| request body 缺少 messages | `422` | inference-service 请求校验 |

这里的关键不是背 status，而是知道错误应该在哪一层被发现，排障入口在哪里。

## Eval

### run 和 compare

run 是一次独立评测，回答“这个候选在某个 task 上表现如何”。  
compare 是两个 run 的对比，回答“candidate 相对 baseline 是否有变化，以及变化是否足以影响判断”。

run 关注单次结果。  
compare 关注发布决策。

当前 compare 还会给出 `release_recommendation`：

- `approve`：结果超过 `min_delta`，且关键评测设置一致
- `review`：结果基本持平，或 few-shot / 样本数等设置改变
- `block`：candidate 退化超过 `min_delta`

它是发布门禁建议，不是自动发布按钮。真正发布前仍然要看样本、业务风险和线上观测。

### sample outputs、sample summary 和 leaderboard

sample outputs 适合回答“具体样本发生了什么”，所以应该包含 prompt、prediction、score、judge reason 等解释字段。  
sample summary 适合回答“这批样本整体如何”，例如样本数、通过/失败数量、平均分和 token 汇总。

leaderboard 是更上一层展示对象。  
它应该从 `run_history.jsonl` 指向的 run bundle 生成，汇总 best accuracy、latest accuracy、run count、backend/few-shot 分组，以及 best/latest result file。它不应该绕过 run 直接写一个分数表，否则排行榜会失去可追溯性。

comparison index 也是展示层。它应该从 `comparison_history.jsonl` 聚合 verdict counts、recommendation counts、task summaries 和平均 delta，帮助你先看发布判断的整体分布，再回到单个 comparison file 查证原因。

### min_delta

`min_delta` 是最小有效差异。  
它避免把很小的波动误解成真实提升或下降。

如果 candidate 只比 baseline 高 0.001，而 `min_delta` 是 0.01，就不应该轻易说 candidate 显著更好。

### 为什么 task 必须一致

不同 task 的指标语义可能不同。  
强行比较会把两个不同问题混成一个发布判断。

例如一个 run 是摘要任务，另一个 run 是分类任务，即使都有 `score` 字段，也不代表它们可比。

## Finetune

### checkpoint 和 export

checkpoint 是训练过程中的中间资产，通常服务于恢复训练、检查状态或后续导出。  
export 是面向使用或交付的结果，应该有更明确的 manifest 和完整性信息。

两者拆开能让训练过程和交付过程更清楚。

### manifest 的价值

manifest 至少解决三件事：

- 说明有哪些文件属于这次资产
- 记录大小和 hash，帮助检查完整性
- 为后续复现、审计、发布提供依据

如果缺少 `sha256` 和 `size_bytes`，你就很难判断文件是否被替换、截断或错误复用。

当前 `dataset_summary.json` 还会记录 role 分布、message 数、数据集大小和 dataset sha256。  
这些信息能帮助你判断训练输入是不是同一批数据，以及 chat-style 数据里 user / assistant / system 的结构是否合理。

`dataset_registry_entry.json` 和 `dataset_registry.jsonl` 更像数据登记层。  
前者说明这次 run 使用的数据资产叫什么，后者把多次 run 的数据输入追加成历史索引。它们让 dataset id、路径、sha256、role 分布和来源 run 能连起来。

`list-datasets` 生成的 registry report 是读取层。  
它不改变训练结果，只是把追加式 registry 汇总成 JSON/Markdown，让你更容易看见 dataset 数量、登记次数、关联模型、最近来源 run、过滤条件和重复登记数量。

`dataset_version` 是基于 sha256 的轻量指纹。  
它不是完整数据管理平台，但足以帮助学习者建立“训练输入也应该版本化”的工程直觉。

当前 `export_manifest.json` 还会记录 lineage。  
lineage 能把导出的 adapter 追溯回 source checkpoint、base model、训练方法、训练数据路径和 epochs，降低后续复现成本。manifest 和 export history 里的 status / duration 则让导出过程本身也能被复盘。

export index 里的 export manifest pointer、model summaries 和 dataset summaries 则是交付资产的查询层。它们不改变 adapter，只是让你从 base model 或 dataset id 的角度盘点“导出过哪些东西”，并能回到具体 manifest 查证 lineage。

### dataset schema 为什么训练前校验

训练开始后才发现数据结构不对，会浪费时间，而且可能生成无意义资产。  
训练前校验能把失败提前，让错误更靠近根因。

这个仓库里，dataset 至少应该能表达 user 输入和 assistant 回复。  
如果没有 assistant response，SFT 类训练目标就没有可靠监督信号。

## Capstone

### 为什么 smoke 不能替代单元测试

smoke 验证跨项目最小闭环，适合发现集成断裂。  
单元测试验证模块内部的边界条件，适合定位具体逻辑错误。

只靠 smoke 会漏掉很多局部逻辑问题。  
只靠单元测试又可能漏掉服务之间的契约问题。

所以两者关系是互补，不是替代。

### 为什么这个项目不能直接当生产平台

合格回答应该主动承认学习型边界，例如：

- engine 后端仍有 mock 或简化实现
- 没有真实多租户和密钥管理
- 没有完整持久化、审计和权限模型
- 没有生产级部署、扩缩容和熔断策略
- eval 和 finetune 仍是教学型闭环

这不是缺点，而是项目定位。  
它先帮助读者建立主干关系，再逐步替换更真实的组件。

## 自动测评包怎么使用

[自动生成测评包](/10-assessments/06-generated-assessment-pack) 不是替代这页参考答案，而是把当前课程目录里的模块自动转成可测评任务。

使用时可以这样判断：

- 如果学习者答不出诊断题，先回到模块入口页
- 如果学习者能跑命令但说不清证据意义，回到示例输出与证据库
- 如果学习者能解释证据但提不出改进，回到生产迁移或案例复盘
- 如果多个学习者卡在同一题，把它转成 FAQ、lab 补充或 issue

评分时不要追求统一话术。  
更重要的是看回答能否指向页面、代码、命令或产物，并能说明这些证据的边界。
