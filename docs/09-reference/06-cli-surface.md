# CLI Surface 速查

这页把四个项目的 CLI 入口集中到一起。

阅读项目页时适合看解释；真正动手时适合来这里查命令。

## 根目录 Makefile

| 命令 | 用途 | 什么时候跑 |
| --- | --- | --- |
| `make infra-dev-install` | 安装四个 Python 子项目和开发工具 | 第一次开发 |
| `make infra-format` | Ruff format + 自动修复 | 提交前、批量修改后 |
| `make docs-quality` | 文档内链、sidebar、README 入口和首页统计检查 | 改文档或导航后 |
| `make docs-inventory` | 生成学习站章节、页面、课程主线和维护信号清单 | 改课程结构或公开发布前 |
| `make course-catalog` | 生成可带练课程模块、检查点和讲师提示 | 组织共学、公开课程或 GitHub 首发前 |
| `make infra-test` | 四个项目单元测试 | 改代码后 |
| `make docs-build` | VitePress 构建 | 改文档站后 |
| `make security-check` | 扫描候选入库文件中的密钥、个人痕迹和危险文件类型 | 公开上传、PR 或 release 前 |
| `make public-check` | `security-check` + `infra-check` | GitHub 上传、PR 和公开分享前 |
| `make infra-check` | lint、测试、docs-quality、docs build | 常规全量检查 |
| `make infra-smoke` | 端到端最小链路 | 改跨项目行为后 |
| `make infra-evidence` | 从 `.tmp/smoke` 汇总端到端证据包 | smoke 后整理复盘材料 |
| `make release-brief` | 合成学习站清单和证据包，生成发布摘要 | GitHub 首发、PR 复盘、公开演示前 |
| `make workshop-packet` | 合成课程目录和发布摘要，生成可带练共学包 | 组织共学、公开分享或课后复盘前 |
| `make assessment-pack` | 合成课程目录和共学包，生成模块测评包 | 自测、带练测评或 PR review 前 |
| `make roadmap-pack` | 合成发布摘要和测评包，生成 GitHub issue 种子 | GitHub 首发、公开路线图或反馈回流前 |
| `make launch-pack` | 合成发布摘要和路线图包，生成首发运营包 | 创建 release、首批 issue 或发布后复盘前 |
| `make infra-release` | 跑发布前完整本地检查 | 正式公开发布前 |
| `make infra-clean` | 清理四个项目输出 | 本地环境整理 |

常用组合：

```bash
PYTHON=.venv/bin/python make infra-format
PYTHON=.venv/bin/python make docs-inventory
PYTHON=.venv/bin/python make course-catalog
PYTHON=.venv/bin/python make public-check
PYTHON=.venv/bin/python make infra-smoke
PYTHON=.venv/bin/python make release-brief
PYTHON=.venv/bin/python make workshop-packet
PYTHON=.venv/bin/python make assessment-pack
PYTHON=.venv/bin/python make roadmap-pack
PYTHON=.venv/bin/python make launch-pack
```

## inference-service

| 命令 | 关键参数 | 用途 |
| --- | --- | --- |
| `serve` | `--engine`、`--model`、`--engine-base-url`、`--engine-api-key`、`--host`、`--port` | 启动模型服务 |
| `health-check` | `--url` | 请求 `/health` |
| `version` | 无 | 输出版本 |

示例：

```bash
cd projects/inference-service
PYTHONPATH=src ../../.venv/bin/python -m inference_service.main serve \
  --engine mock \
  --model Qwen/Qwen2.5-0.5B-Instruct \
  --port 8000
```

如果要接 OpenAI-compatible 上游：

```bash
PYTHONPATH=src ../../.venv/bin/python -m inference_service.main serve \
  --engine openai-compatible \
  --engine-base-url http://localhost:8001/v1 \
  --engine-api-key local-engine-key \
  --model Qwen/Qwen2.5-0.5B-Instruct
```

## ai-gateway

| 命令 | 关键参数 | 用途 |
| --- | --- | --- |
| `serve` | `--host`、`--port` | 启动 gateway |
| `health-check` | `--url` | 请求 `/health` |

示例：

```bash
cd projects/ai-gateway
PYTHONPATH=src ../../.venv/bin/python -m ai_gateway.main serve --port 8080
```

gateway 的模型映射来自：

- `projects/ai-gateway/configs/models.yaml`
- `projects/ai-gateway/src/ai_gateway/config.py`

## eval-module

| 命令 | 关键参数 | 输出 |
| --- | --- | --- |
| `run` | `--task`、`--model`、`--backend-url`、`--num-fewshot`、`--limit`、`--output` | result JSON、run bundle、history |
| `compare` | `--baseline`、`--candidate`、`--min-delta`、`--output` | comparison JSON/Markdown/bundle |
| `leaderboard` | `--results-dir`、`--history`、`--task`、`--backend`、`--num-fewshot`、`--limit`、`--output` | leaderboard JSON/Markdown |
| `list-runs` | `--results-dir`、`--history`、`--task`、`--model`、`--backend`、`--num-fewshot`、`--limit`、`--output` | run index JSON/Markdown |
| `list-comparisons` | `--results-dir`、`--history`、`--task`、`--verdict`、`--recommendation`、`--limit`、`--output` | comparison index JSON/Markdown |
| `list-tasks` | 无 | task 列表 |

最小 run：

```bash
cd projects/eval-module
PYTHONPATH=src ../../.venv/bin/python -m eval_module.main run \
  --task mmlu \
  --model Qwen/Qwen2.5-0.5B-Instruct \
  --backend-url http://localhost:8000/v1 \
  --output ./results/mmlu_eval_result.json
```

发布判断：

```bash
PYTHONPATH=src ../../.venv/bin/python -m eval_module.main compare \
  --baseline ./results/mmlu_eval_result.json \
  --candidate ./results/mmlu_eval_result.json \
  --min-delta 0.01 \
  --output ./results/mmlu_compare.json
```

索引类命令：

```bash
PYTHONPATH=src ../../.venv/bin/python -m eval_module.main leaderboard --output ./results/leaderboard.json
PYTHONPATH=src ../../.venv/bin/python -m eval_module.main list-runs --output ./results/run_index.json
PYTHONPATH=src ../../.venv/bin/python -m eval_module.main list-comparisons --output ./results/comparison_index.json
```

## finetune-demo

| 命令 | 关键参数 | 输出 |
| --- | --- | --- |
| `train` | `--method`、`--model`、`--dataset`、`--output`、`--epochs`、`--config`、LoRA/QLoRA 参数 | run manifest、checkpoint、dataset summary、history |
| `save` | `--checkpoint`、`--output` | adapter export、export manifest |
| `export` | `--checkpoint`、`--output` | adapter export、export manifest |
| `list-datasets` | `--registry`、`--dataset-id`、`--method`、`--model`、`--output`、`--markdown-output` | dataset registry report |
| `diff-datasets` | `--registry`、`--left`、`--right`、`--output`、`--markdown-output` | dataset diff |
| `list-exports` | `--history`、`--dataset-id`、`--model`、`--limit`、`--output`、`--markdown-output` | export index |
| `list-runs` | `--history`、`--dataset-id`、`--model`、`--method`、`--limit`、`--output`、`--markdown-output` | finetune run index |

最小 train：

```bash
cd projects/finetune-demo
PYTHONPATH=src ../../.venv/bin/python -m finetune_demo.main train \
  --method lora \
  --model Qwen/Qwen2.5-0.5B-Instruct \
  --dataset ./data/train.jsonl \
  --output ./outputs/demo-run \
  --epochs 1
```

导出：

```bash
PYTHONPATH=src ../../.venv/bin/python -m finetune_demo.main export \
  --checkpoint ./outputs/demo-run/checkpoint-0001 \
  --output ./outputs/demo-export
```

索引类命令：

```bash
PYTHONPATH=src ../../.venv/bin/python -m finetune_demo.main list-runs \
  --history ./outputs/run_history.jsonl \
  --output ./outputs/run_index.json \
  --markdown-output ./outputs/run_index.md

PYTHONPATH=src ../../.venv/bin/python -m finetune_demo.main list-datasets \
  --registry ./outputs/dataset_registry.jsonl \
  --output ./outputs/dataset_registry_report.json \
  --markdown-output ./outputs/dataset_registry_report.md

PYTHONPATH=src ../../.venv/bin/python -m finetune_demo.main list-exports \
  --history ./outputs/export_history.jsonl \
  --output ./outputs/export_index.json \
  --markdown-output ./outputs/export_index.md
```

## 选择命令的简单规则

| 你想做什么 | 优先命令 |
| --- | --- |
| 检查文档导航和链接 | `make docs-quality` |
| 生成课程结构盘点 | `make docs-inventory` |
| 生成可带练课程目录 | `make course-catalog` |
| 确认代码和文档都没坏 | `make infra-check` |
| 公开上传前检查安全、个人信息和质量 | `make public-check` |
| 确认四项目链路仍然通 | `make infra-smoke` |
| 整理 smoke 输出证据 | `make infra-evidence` |
| 生成公开发布摘要 | `make release-brief` |
| 生成公开共学包 | `make workshop-packet` |
| 生成模块测评包 | `make assessment-pack` |
| 生成路线图 issue 种子 | `make roadmap-pack` |
| 生成 release notes、starter issues 和发布后检查表 | `make launch-pack` |
| 发布前最后一轮本地验收 | `make infra-release` |
| 观察请求生命周期 | inference/gateway `/events/requests` |
| 评估候选模型 | eval `run` + `compare` |
| 复盘历史评测 | eval `leaderboard` + `list-runs` |
| 复盘训练资产 | finetune `list-runs` + `list-exports` |
