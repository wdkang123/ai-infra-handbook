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
