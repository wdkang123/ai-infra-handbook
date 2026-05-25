# 失败症状到证据地图

## 这一页怎么用

当你本地跑项目失败时，不要先猜“是不是代码坏了”。

更稳的顺序是：

1. 先确定失败发生在哪一层
2. 再找对应证据
3. 再决定是否需要改代码

这一页按症状整理优先检查的证据。

## 总入口

| 症状 | 先看什么 | 可能层级 |
| --- | --- | --- |
| 文档站打不开 | `npm run docs:dev` 输出 | 文档站 |
| `infra-check` 失败 | 失败阶段名称 | 综合质量 |
| gateway 返回 `401` | Authorization header | 治理层 |
| gateway 返回 `404` | model name / route config | 治理层 |
| gateway 返回 `429` | rate limit event | 治理层 |
| gateway 返回 `502` | upstream attempt / inference health | 治理层或执行层 |
| streaming 卡住 | SSE event / `[DONE]` | 执行层或治理层 |
| eval compare 失败 | task/backend/few-shot 设置 | 质量层 |
| finetune train 失败 | dataset schema / dataset summary | 训练层 |
| export 失败 | checkpoint index / source checkpoint | 训练层 |

## 文档站失败

先跑：

```bash
nvm use
npm run docs:build
```

如果失败，优先看：

| 信息 | 说明 |
| --- | --- |
| Markdown 文件路径 | 哪一页出错 |
| VitePress component name | 是否是首页组件 |
| dead link | 是否是内部链接或锚点 |

再跑：

```bash
PYTHON=.venv/bin/python make docs-quality
```

`docs-quality` 现在会覆盖：

- Markdown 本地链接
- heading 锚点
- VitePress nav/sidebar 路由
- 首页 frontmatter 入口
- 首页 Vue 组件链接
- sidebar 覆盖
- 首页文档页统计
- README 和发布页关键入口

## Gateway 失败

### 401

先看请求 header：

```text
Authorization: Bearer dev-gateway-key-1
```

再查 events：

```bash
curl -s "http://localhost:8080/events?event_type=auth_failed"
```

如果能看到 `auth_failed`，说明请求已经进 gateway，但没有通过鉴权。

### 404

先看请求里的 model：

```json
{
  "model": "vllm-local"
}
```

再查：

```bash
curl -s http://localhost:8080/v1/models
curl -s "http://localhost:8080/events?event_type=route_not_found"
```

如果 `/v1/models` 里没有这个外部模型名，问题通常在路由配置或请求体。

### 429

查：

```bash
curl -s "http://localhost:8080/events?event_type=rate_limited"
```

这说明 gateway 层已经保护住请求入口。

### 502

先查 gateway health：

```bash
curl -s http://localhost:8080/health
```

再查 gateway timeline：

```bash
curl -s "http://localhost:8080/events/requests/<request_id>"
```

如果有 `upstream_attempt` 后失败，继续查 inference health：

```bash
curl -s http://localhost:8000/health
```

## Inference 失败

常见症状：

| 症状 | 证据 |
| --- | --- |
| unknown model | `404` 和 model list |
| empty messages | `422` validation error |
| upstream adapter 失败 | structured engine error |
| streaming 中途失败 | SSE `error` event |

优先查：

```bash
curl -s http://localhost:8000/v1/models
curl -s http://localhost:8000/events
curl -s http://localhost:8000/metrics
```

## Eval 失败

如果 `run` 失败，先看：

- task 是否存在
- backend 是否有效
- output dir 是否可写

如果 `compare` 失败，先看：

- baseline 和 candidate 是否是同 task
- metric 是否存在
- min delta threshold 是否过高
- eval settings 是否变化

优先证据：

```text
result.json
sample_outputs.json
sample_analysis.json
compare.json
comparison_index.json
```

## Finetune 失败

如果 train 失败，先看：

| 证据 | 说明 |
| --- | --- |
| dataset path | 文件是否存在 |
| dataset schema | 是否有 messages |
| assistant response | 是否有 assistant 输出 |
| dataset summary | role counts 是否正常 |

如果 export 失败，先看：

| 证据 | 说明 |
| --- | --- |
| source checkpoint | checkpoint 是否存在 |
| checkpoint index | 是否有 adapter 文件 |
| adapter hash | 文件是否完整 |
| export history | status 和 duration |

## 一个排障动作的好顺序

```text
1. 记录命令
2. 记录 HTTP status 或 CLI exit
3. 找 request id 或 run id
4. 查 summary/index
5. 查单条 timeline/sample/manifest
6. 判断是哪一层
7. 再改代码或配置
```

## 关联阅读

- [常见排障手册](/09-reference/04-troubleshooting)
- [Serving 与 Gateway 输出证据](/13-output-gallery/01-serving-gateway-evidence)
- [Eval 报告证据](/13-output-gallery/02-eval-report-evidence)
- [Finetune 产物证据](/13-output-gallery/03-finetune-artifact-evidence)
