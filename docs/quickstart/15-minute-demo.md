# 15 分钟跑通 AI Infra 最小链路

> 本页解决：第一次 clone 后如何跑通 gateway、inference、eval、finetune 和证据包生成。
> 读完能做：发起一次带 request id 的请求，查看 events / metrics，并生成 evidence packet。
> 关联代码：`Makefile`、`scripts/integration_smoke_test.sh`、`scripts/build_evidence_packet.py`、`projects/inference-service`、`projects/ai-gateway`、`projects/eval-module`、`projects/finetune-demo`。
> 验证命令：`PYTHON=.venv/bin/python make quickstart`。

这条路径面向第一次打开仓库的人。它不会把当前项目说成生产平台，而是帮助你用最短路径看到 AI Infra 学习项目里最重要的工程证据：

- request id：一条请求如何被串起来
- events：gateway 和 inference 如何记录时间线
- metrics：服务和平台层暴露了哪些可观测信号
- eval report：评测如何给出 release recommendation
- manifest：训练和导出产物如何保留 lineage
- evidence packet：如何把 smoke 输出汇总成可分享复盘材料

## 0. 环境要求

建议使用：

- Python 3.11+
- Node 22
- `make`
- `curl`
- macOS、Linux 或 WSL

如果你只是跑后端链路，Node 不是必须；如果你要启动文档站，需要 Node 22。

## 1. Clone 仓库

命令：

```bash
git clone https://github.com/wdkang123/ai-infra-handbook.git
cd ai-infra-handbook
```

预期输出：

```text
Cloning into 'ai-infra-handbook'...
```

失败排查：

| 现象 | 处理 |
| --- | --- |
| `repository not found` | 确认仓库地址是否拼写正确，或仓库是否已公开 |
| clone 很慢 | 可以先用浏览器打开 GitHub 仓库，确认网络是否可访问 |
| 目录已存在 | 换一个空目录，或进入已有目录继续后面的步骤 |

对应代码入口：仓库根目录的 `README.md`、`Makefile`、`docs/` 和 `projects/`。

下一步：准备 Python 和 Node 环境。

## 2. Install 依赖

命令：

```bash
python3 -m venv .venv
PYTHON=.venv/bin/python make infra-dev-install
```

如果要启动文档站，再运行：

```bash
nvm use 22
npm install
```

预期输出：

```text
Successfully installed ...
```

`infra-dev-install` 会安装四个学习项目和开发依赖：

- `projects/inference-service`
- `projects/ai-gateway`
- `projects/eval-module`
- `projects/finetune-demo`
- `requirements-dev.txt`

失败排查：

| 现象 | 处理 |
| --- | --- |
| `.venv/bin/python` 不存在 | 重新运行 `python3 -m venv .venv` |
| `pip` 下载失败 | 先确认网络，再重试 `PYTHON=.venv/bin/python make infra-dev-install` |
| `nvm` 找不到 | 先跳过文档站安装，后端 quickstart 不依赖 Node |
| Node 版本不对 | 使用 `nvm use 22`，或查看仓库 `.nvmrc` |

对应代码入口：根目录 `requirements-dev.txt`、各项目的 `pyproject.toml`。

下一步：运行一条聚合 quickstart。

## 3. 运行 `make quickstart`

命令：

```bash
PYTHON=.venv/bin/python make quickstart
```

这个目标会自动执行：

1. 安装开发依赖。
2. 运行 `infra-smoke`，打通 gateway、inference、eval、finetune。
3. 生成根级 evidence packet。
4. 启动本地 inference 和 gateway 服务，方便你继续手动请求。

预期输出会包含多条 smoke 检查：

```text
[PASS] IT-00 gateway upstream health
[PASS] IT-01 gateway proxy
[PASS] IT-07 gateway metrics
[PASS] IT-10b eval release recommendation
[PASS] IT-13c finetune export lineage
Quickstart completed.
Services are available at http://localhost:8000 and http://localhost:8080
```

失败排查：

| 现象 | 处理 |
| --- | --- |
| 端口 `8000` 或 `8080` 被占用 | 运行 `PYTHON=.venv/bin/python make all-stop`，或设置 `INFERENCE_PORT=8100 GATEWAY_PORT=8180` |
| smoke 卡在 health check | 查看 `/tmp/ai-infra-smoke-inference.log` 和 `/tmp/ai-infra-smoke-gateway.log` |
| eval 或 finetune 子检查失败 | 先运行 `PYTHON=.venv/bin/python make infra-check` 定位单元测试问题 |
| 证据包生成失败 | 确认 `.tmp/smoke` 下是否已有 serving、eval、finetune 输出 |

对应代码入口：`scripts/integration_smoke_test.sh` 会写入 `.tmp/smoke`，`scripts/build_evidence_packet.py` 会汇总证据。

下一步：自己发送一次带 request id 的请求。

## 4. Send request

命令：

```bash
curl -sD - -X POST http://localhost:8080/v1/chat/completions \
  -H 'Authorization: Bearer dev-gateway-key-1' \
  -H 'X-Request-ID: req_quickstart_manual_1' \
  -H 'Content-Type: application/json' \
  -d '{"model":"vllm-local","messages":[{"role":"user","content":"用一句话解释 AI Infra。"}]}'
```

预期输出：

```text
HTTP/1.1 200 OK
x-request-id: req_quickstart_manual_1
x-upstream-model: vllm-local
x-cache: bypass

{"id":"chatcmpl_...","object":"chat.completion",...}
```

失败排查：

| 现象 | 处理 |
| --- | --- |
| `401` | 检查是否带了 `Authorization: Bearer dev-gateway-key-1` |
| `404 unknown model` | 使用当前 gateway 暴露的 `vllm-local` |
| `connection refused` | 服务没有启动，重新运行 `PYTHON=.venv/bin/python make quickstart` 或 `make all-serve` |
| `502` | 先看 gateway `/events/failures`，再看 inference `/health` |

对应代码入口：`projects/ai-gateway` 负责鉴权、路由、fallback、events；`projects/inference-service` 负责 `/v1/chat/completions`。

下一步：用 request id 查证据。

## 5. Inspect request id、events 和 metrics

查看 gateway timeline：

```bash
curl -s 'http://localhost:8080/events/requests/req_quickstart_manual_1'
```

预期输出应包含：

```text
request_received
upstream_attempt
request_success
```

查看 gateway 事件摘要：

```bash
curl -s 'http://localhost:8080/events/summary?event_type=request_success&upstream_model=vllm-local'
```

查看 gateway metrics：

```bash
curl -s http://localhost:8080/metrics
```

查看 inference metrics：

```bash
curl -s http://localhost:8000/metrics
```

预期输出中可以重点找：

```text
ai_gateway_requests_total
ai_gateway_fallback_attempts_total
vllm_num_requests_total
vllm_prompt_tokens_total
vllm_completion_tokens_total
```

失败排查：

| 现象 | 处理 |
| --- | --- |
| request id 查不到 | 确认手动请求里真的带了 `X-Request-ID` |
| events 有成功但 metrics 没增长 | 确认查询的是 gateway 还是 inference 的端口 |
| metrics 很多看不懂 | 先读 [Prometheus metrics 对照表](/12-production-migration/07-prometheus-metrics-map) |

对应代码入口：`/events/requests/{request_id}` 是单次请求复盘入口，`/metrics` 是聚合趋势入口。

下一步：生成或查看 evidence packet。

## 6. Generate evidence packet

`make quickstart` 已经生成了根级证据包。你可以重新生成一次：

```bash
PYTHON=.venv/bin/python make infra-evidence
```

预期输出文件：

```text
.tmp/evidence/evidence_packet.json
.tmp/evidence/evidence_packet.md
```

如果你想看 smoke 过程中自动生成的证据包，也可以打开：

```text
.tmp/smoke/evidence/evidence_packet.json
.tmp/smoke/evidence/evidence_packet.md
```

失败排查：

| 现象 | 处理 |
| --- | --- |
| 提示 `.tmp/smoke` 缺文件 | 先运行 `PYTHON=.venv/bin/python make infra-smoke` |
| strict 校验缺 serving 证据 | 查看 `scripts/integration_smoke_test.sh` 的 `save_serving_evidence` |
| markdown 生成了但内容为空 | 检查 `.tmp/smoke/eval` 和 `.tmp/smoke/finetune` 是否存在 |

对应代码入口：`scripts/build_evidence_packet.py`。

下一步：

- 想系统学习：进入 [学习路线图](/00-overview/02-learning-route)。
- 想看输出证据：进入 [示例输出与证据库](/13-output-gallery/00-overview)。
- 想贡献任务：进入 [社区贡献路径](/community/00-overview)。
- 想规划真实迁移：进入 [生产迁移路线总览](/12-production-migration/00-overview)。

## 7. 清理本地服务

如果你只是验证一次，结束后可以停止服务：

```bash
PYTHON=.venv/bin/python make all-stop
```

预期结果：再次访问 `http://localhost:8080/health` 会连接失败。

这一步不会删除 `.tmp/smoke` 或 `.tmp/evidence`，所以你的证据包仍然保留。
