# 常见排障手册

这页用于快速定位常见问题。

排障时不要一开始就翻所有代码，先判断问题属于哪一层：

- 环境
- 文档站
- inference-service
- ai-gateway
- eval-module
- finetune-demo
- smoke

## 排障的基本方法

大多数问题都可以按这个顺序处理：

```text
1. 记录你运行的命令
2. 记录错误码、异常或失败阶段
3. 判断是哪一层
4. 找对应 summary/index/timeline/manifest
5. 缩小到一个文件或一个配置
6. 修复后跑最小验证命令
```

不要一上来全量重装依赖，也不要一上来改代码。很多问题只是环境没激活、端口占用、模型名写错、token 缺失、路径大小写不一致。

## 0. `npm` 找不到或 Node 版本不对

现象：

```text
make: npm: No such file or directory
```

常见原因：

- 当前 shell 没加载 nvm
- 没执行 `nvm use 22`
- CI 或本地终端的 Node 版本和项目不一致

处理方式：

```bash
nvm use 22
npm run docs:build
```

如果通过脚本运行，可以用：

```bash
/bin/zsh -lc "source ~/.nvm/nvm.sh && nvm use 22 >/dev/null && npm run docs:build"
```

学习重点：这是环境问题，不是 VitePress 或 Markdown 内容问题。

## 1. `make infra-check` 找不到 Python 包

现象：

```text
ModuleNotFoundError
```

优先检查：

```bash
PYTHON=.venv/bin/python make infra-dev-install
```

然后重跑：

```bash
PYTHON=.venv/bin/python make infra-check
```

相关文件：

- `requirements-dev.txt`
- 根级 `Makefile`
- 各项目 `pyproject.toml`

## 2. 文档站构建失败

命令：

```bash
nvm use
npm run docs:build
```

常见原因：

- 新增页面没有正确闭合 Markdown 代码块
- 内部链接路径写错
- VitePress config 里 sidebar link 写错
- 文件名大小写和链接不一致

优先检查：

- `docs/.vitepress/config.mts`
- 最近新增的 Markdown 文件

## 3. GitHub Pages 样式丢失

常见原因：

- `VITEPRESS_BASE` 不对

项目页一般需要：

```bash
VITEPRESS_BASE=/仓库名/
```

当前 workflow 已经自动设置：

```yaml
VITEPRESS_BASE: /${{ github.event.repository.name }}/
```

如果你使用自定义域名或用户根站点，可能需要改成：

```bash
VITEPRESS_BASE=/
```

相关页面：

- [GitHub Pages 发布指南](/08-publication/01-github-pages)

## 3.1 本地 preview 样式或资源 404

现象：

- 页面能打开，但 CSS/JS 资源 404
- 刚 build 后 preview 仍显示旧样式
- 浏览器控制台有 hashed asset 找不到

常见原因：

- `docs/.vitepress/dist` 被重新构建，但旧 preview 服务还在
- 浏览器缓存了旧资源

处理方式：

```bash
lsof -nP -iTCP:4173 -sTCP:LISTEN
kill <pid>
npm run docs:preview
```

如果只是本地调样式，优先用 `npm run docs:dev`；如果要模拟线上构建，先 `docs:build` 再 `docs:preview`。

## 4. inference-service 请求返回 404

现象：

```json
{"error":{"code":"404"}}
```

常见原因：

- 请求里的 `model` 和配置里的 `engine.model_path` 不一致

默认模型：

```text
Qwen/Qwen2.5-0.5B-Instruct
```

优先看：

- `projects/inference-service/config.yaml`
- `projects/inference-service/src/inference_service/server.py`

## 5. gateway 请求返回 401

常见原因：

- 没有传 `Authorization`
- token 格式不是 `Bearer ...`
- token 不在配置允许列表

正确示例：

```bash
curl -s http://localhost:8080/v1/chat/completions \
  -H 'Authorization: Bearer dev-gateway-key-1' \
  -H 'Content-Type: application/json' \
  -d '{"model":"vllm-local","messages":[{"role":"user","content":"Hello"}]}'
```

优先看：

- `projects/ai-gateway/src/ai_gateway/middleware/auth.py`

## 6. gateway 请求返回 404

常见原因：

- 外部模型名没有配置

默认 gateway model：

```text
vllm-local
```

优先看：

- `projects/ai-gateway/configs/models.yaml`
- `projects/ai-gateway/src/ai_gateway/router.py`

## 7. gateway 请求返回 429

含义：

- 触发了入口限流

优先看：

- `projects/ai-gateway/configs/config.yaml`
- `projects/ai-gateway/src/ai_gateway/runtime.py`

学习重点：

- `429` 不是下游坏了，而是 gateway 主动保护系统

## 8. gateway 请求返回 502

含义：

- 下游服务失败或不可达

优先检查：

```bash
curl -s http://localhost:8000/health
curl -s http://localhost:8080/health
```

如果 gateway health 里 upstream 是 unhealthy，先启动 inference-service。

相关文件：

- `projects/ai-gateway/src/ai_gateway/router.py`
- `projects/ai-gateway/src/ai_gateway/server.py`

## 8.1 fallback 没有按预期发生

先判断请求类型：

- 非 streaming：主 upstream 在返回前失败，可以尝试 fallback
- streaming：只有首个 chunk 之前失败才适合 fallback

检查顺序：

```bash
curl -s "http://localhost:8080/events/requests/<request_id>"
curl -s "http://localhost:8080/events?event_type=fallback_attempt"
curl -s "http://localhost:8080/metrics"
```

再看响应 header：

```text
x-upstream-model
x-fallback-used
```

如果请求已经开始 streaming 并发出了 chunk，中途失败不应该切换备用模型。否则客户端会收到两个模型拼在一起的输出。

## 8.2 cache 没有 HIT

先确认当前配置是否启用 response cache。默认学习路径可能是 `BYPASS`。

如果启用了 cache，还要确认：

- 请求体是否完全一致
- token 是否一致
- 是否是非 streaming 请求
- TTL 是否过期
- max entries 是否淘汰了旧条目

观察 header：

```text
x-cache: BYPASS / MISS / HIT
```

学习重点：response cache 和 KV cache 不是一回事。response cache 是 gateway 层缓存完整响应，KV cache 是模型执行层复用中间状态。

## 9. streaming 没有看到 `[DONE]`

优先确认使用了 `curl -N`：

```bash
curl -N http://localhost:8000/v1/chat/completions ...
```

如果是 gateway streaming：

- 首个 chunk 前失败时可能 fallback
- 全部失败时会发 SSE `error` 再 `[DONE]`
- 中途失败时不会 fallback，会发 SSE `error` 再 `[DONE]`

优先看：

- `projects/inference-service/src/inference_service/server.py`
- `projects/ai-gateway/src/ai_gateway/server.py`

## 10. eval compare 被拒绝

现象：

```text
Cannot compare different tasks
```

原因：

- baseline 和 candidate 的 task 不一致

例如：

- baseline 是 `mmlu`
- candidate 是 `gsm8k`

处理方式：

- 确认两次 run 使用同一个 `--task`

相关文件：

- `projects/eval-module/src/eval_module/results/result_store.py`

## 11. eval release recommendation 是 review

常见原因：

- candidate 和 baseline 没有超过 `min_delta`
- few-shot 设置变了
- 样本数变了

处理方式：

- 先看 `summary.release_reasons`
- 确认 baseline 和 candidate 是否真的可比
- 必要时重新跑相同 task、相同 few-shot、相同 limit 的 run

相关文件：

- `projects/eval-module/src/eval_module/results/result_store.py`

## 11.1 leaderboard 第一但不能发布

这是正常的。

Leaderboard 是展示层，不是发布批准。

发布前还要看：

- candidate 和 baseline 是否同 task
- backend/few-shot/limit 是否一致
- sample outputs 是否有关键失败
- comparison recommendation 是什么
- latency、cost、error rate 是否能接受

如果只是 leaderboard 排名高，但 sample-level evidence 不稳，应该继续 review。

## 12. finetune 训练数据被拒绝

常见原因：

- 文件不存在
- 不是 `.jsonl`
- JSONL 记录不是 chat-style `messages`
- 缺少 user 或 assistant

最小合法样本：

```json
{"messages":[{"role":"user","content":"Hi"},{"role":"assistant","content":"Hello"}]}
```

相关文件：

- `projects/finetune-demo/src/finetune_demo/trainer/lora_trainer.py`

## 13. finetune export lineage 为空

常见原因：

- checkpoint 缺少 `trainer_state.json`
- checkpoint 的 `adapter_config.json` 不是合法 JSON
- checkpoint 不是由当前 demo trainer 生成

处理方式：

- 先检查 `checkpoint-0001/trainer_state.json`
- 再检查 `checkpoint-0001/adapter_config.json`
- 重新从 `train` 命令生成 checkpoint 后再 export

相关文件：

- `projects/finetune-demo/src/finetune_demo/export/adapter_exporter.py`

## 14. smoke 失败

命令：

```bash
PYTHON=.venv/bin/python make infra-smoke
```

排查顺序：

1. 看失败的 `IT-xx` 名称
2. 单独跑对应项目测试
3. 检查 `/tmp/ai-infra-*.log`
4. 确认端口没有被占用
5. 重跑 `infra-check`

常见临时处理：

```bash
make all-stop
PYTHON=.venv/bin/python make infra-smoke
```

相关文件：

- `scripts/integration_smoke_test.sh`
- 根级 `Makefile`

## 15. public-check 失败

`public-check` 是发布前综合检查。它失败时先看失败阶段：

| 阶段 | 常见原因 |
| --- | --- |
| security scan | 候选文件里有疑似密钥、路径、危险文件 |
| project tests | 某个项目行为退化 |
| docs-quality | Markdown 链接、sidebar、首页入口问题 |
| docs-build | VitePress 构建失败或 Node 环境问题 |

处理方式：

1. 先修第一个失败点。
2. 不要因为后面没跑到就假设后面都通过。
3. 修完后重新跑完整 `public-check`。

## 16. 写 issue 或 PR 前怎么描述问题

好的排障报告至少包含：

```text
命令：
预期：
实际：
错误码/日志：
request id / run id：
已检查的证据：
可能层级：
```

如果是公开 issue，不要贴真实 token、真实 endpoint、私有路径或完整敏感日志。用占位值和截取后的关键字段即可。
