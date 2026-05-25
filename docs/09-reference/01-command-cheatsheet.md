# 命令速查

这页把常用命令集中放在一起。

如果你不知道“现在该跑什么”，优先看这里。

## 根目录命令

### 安装开发依赖

```bash
PYTHON=.venv/bin/python make infra-dev-install
```

用途：

- 安装四个 Python 子项目
- 安装 Ruff 等开发检查工具

### 格式化和自动修复

```bash
PYTHON=.venv/bin/python make infra-format
```

用途：

- 格式化 Python 代码
- 自动修复部分 lint 问题

### 全量检查

```bash
PYTHON=.venv/bin/python make infra-check
```

用途：

- Python lint
- 四个项目单元测试
- 文档内链、heading 锚点、H1 结构、VitePress nav/sidebar 路由、首页配置与 Vue 组件链接、README 关键入口和首页统计检查
- VitePress 文档构建

### 公开上传检查

```bash
PYTHON=.venv/bin/python make public-check
```

用途：

- 先运行 `security-check`
- 再运行 `infra-check`
- 适合发 PR、上传 GitHub 或公开发布前确认内容没有明显安全和个人信息问题

### 安全与个人信息检查

```bash
PYTHON=.venv/bin/python make security-check
```

用途：

- 扫描 Git 候选入库文件
- 检查高置信密钥、私钥、连接串和本机路径
- 检查本机用户名、常见个人邮箱、手机号和身份证号
- 检查日志、数据库、模型权重、证书、压缩包等不适合公开提交的文件类型

### 脚本测试

```bash
PYTHON=.venv/bin/python make scripts-test
```

用途：

- 验证 `scripts/` 下的仓库级工具
- 当前覆盖证据包生成器、学习站清单生成器、课程目录生成器、发布摘要生成器、共学包生成器、测评包生成器和路线图包生成器

### 生成学习站清单

```bash
PYTHON=.venv/bin/python make docs-inventory
```

用途：

- 扫描 `docs/` 下的学习页面
- 汇总章节、路由、课程主线、内容信号和 Makefile 目标
- 生成 `.tmp/docs-inventory/learning_inventory.json`
- 生成 `.tmp/docs-inventory/learning_inventory.md`
- 帮助 GitHub 发布、共学带练和课程结构维护

### 生成课程目录

```bash
PYTHON=.venv/bin/python make course-catalog
```

用途：

- 先生成学习站清单
- 把 7 条课程主线整理成可带练模块
- 生成 `.tmp/course-catalog/course_catalog.json`
- 生成 `.tmp/course-catalog/course_catalog.md`
- strict 校验课程目录引用的页面和学习主线是否完整
- 帮助讲师、学习小组、GitHub README 和公开演示复用同一份课程目录

### 文档质量检查

```bash
PYTHON=.venv/bin/python make docs-quality
```

用途：

- 检查 Markdown 本地链接和 heading 锚点是否能解析
- 检查每个文档页是否有且只有一个 H1
- 检查 VitePress nav/sidebar 内部路由是否能解析
- 检查首页 frontmatter 入口、Vue 静态链接和数据驱动链接是否能解析
- 检查所有文档页是否进入 VitePress sidebar
- 检查首页文档页统计是否和真实页面数一致
- 检查 README 和公开发布页是否保留关键入口

### 端到端 smoke

```bash
PYTHON=.venv/bin/python make infra-smoke
```

用途：

- 临时启动 inference-service
- 临时启动 ai-gateway
- 验证 gateway / inference / eval / finetune 最小链路
- 生成 `.tmp/smoke/evidence/evidence_packet.json` 和 `.md`

### 生成证据包

```bash
PYTHON=.venv/bin/python make infra-evidence
```

用途：

- 读取 `.tmp/smoke` 中的 serving、eval、finetune 产物
- 汇总成 `.tmp/evidence/evidence_packet.json`
- 生成 `.tmp/evidence/evidence_packet.md`
- 帮助 PR、issue、学习者工作簿和公开演示引用同一份证据

### 生成发布摘要

```bash
PYTHON=.venv/bin/python make release-brief
```

用途：

- 先生成学习站清单和证据包
- 合成 `.tmp/release/release_brief.json`
- 生成 `.tmp/release/release_brief.md`
- strict 校验课程主线和端到端证据是否完整
- 帮助 GitHub 首发、PR 复盘和公开演示使用同一份发布摘要

### 生成共学包

```bash
PYTHON=.venv/bin/python make workshop-packet
```

用途：

- 先生成课程目录和发布摘要
- 合成 `.tmp/workshop/workshop_packet.json`
- 生成 `.tmp/workshop/workshop_packet.md`
- strict 校验课程目录和发布摘要是否适合公开带练
- 帮助讲师、学习小组和公开分享复用同一份议程、模块卡片、学习者交付和复盘问题

### 生成测评包

```bash
PYTHON=.venv/bin/python make assessment-pack
```

用途：

- 先生成课程目录和共学包
- 合成 `.tmp/assessment/assessment_pack.json`
- 生成 `.tmp/assessment/assessment_pack.md`
- strict 校验课程目录和共学包是否适合公开测评
- 帮助学习者、讲师和 reviewer 复用同一份模块题目、证据要求和评分标准

### 生成路线图包

```bash
PYTHON=.venv/bin/python make roadmap-pack
```

用途：

- 先生成发布摘要和测评包
- 合成 `.tmp/roadmap/roadmap_pack.json`
- 生成 `.tmp/roadmap/roadmap_pack.md`
- strict 校验发布摘要和测评包是否适合公开路线图
- 帮助维护者把模块弱点、发布反馈和后续方向整理成 GitHub issue 种子

### 发布前完整检查

```bash
PYTHON=.venv/bin/python make infra-release
```

用途：

- 运行格式化、学习站清单、课程目录、全量检查、smoke、证据包、发布摘要、共学包、测评包和路线图包
- 其中 `public-check` 会覆盖安全、个人信息、lint、测试、文档质量和文档站构建
- 适合公开发布前最后一轮，不适合每次小改都跑

### 构建文档站

```bash
nvm use
npm run docs:build
```

用途：

- 检查 VitePress 页面能否构建
- 检查内部链接是否基本正确

### 本地启动文档站

```bash
nvm use
npm run docs:dev
```

默认地址：

```text
http://localhost:5173
```

## inference-service

### 启动服务

```bash
cd /path/to/ai-infra/projects/inference-service
PYTHONPATH=src ../../.venv/bin/python -m inference_service.main serve
```

### 查看 health

```bash
curl -s http://localhost:8000/health
```

### 查看 metrics

```bash
curl -s http://localhost:8000/metrics
```

重点看：

- `vllm_prompt_tokens_total`
- `vllm_completion_tokens_total`
- `vllm_num_tokens_total`

### 查看最近事件

```bash
curl -s 'http://localhost:8000/events?limit=20'
curl -s 'http://localhost:8000/events?event_type=request_success&requested_model=Qwen/Qwen2.5-0.5B-Instruct'
curl -s 'http://localhost:8000/events/summary?event_type=request_success&requested_model=Qwen/Qwen2.5-0.5B-Instruct'
curl -s 'http://localhost:8000/events/requests?requested_model=Qwen/Qwen2.5-0.5B-Instruct'
curl -s 'http://localhost:8000/events/requests/req_demo_direct_1'
```

重点看：

- `request_received`
- `engine_generate_start` / `engine_stream_start`
- `request_success`
- `engine_error`
- `event_type_counts`
- `requested_model_counts`
- `matched_request_count`
- `event_types`
- `duration_seconds`

### 查看模型列表

```bash
curl -s http://localhost:8000/v1/models
```

重点看：

- `id`
- `metadata.engine`

### 普通请求

```bash
curl -s http://localhost:8000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"Qwen/Qwen2.5-0.5B-Instruct","messages":[{"role":"user","content":"Hello inference"}]}'
```

### Streaming 请求

```bash
curl -N http://localhost:8000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"Qwen/Qwen2.5-0.5B-Instruct","messages":[{"role":"user","content":"Hello stream"}],"stream":true}'
```

### 单项目测试

```bash
cd /path/to/ai-infra/projects/inference-service
PYTHONPATH=src ../../.venv/bin/python -m pytest tests -v
```

## ai-gateway

### 启动服务

```bash
cd /path/to/ai-infra/projects/ai-gateway
PYTHONPATH=src ../../.venv/bin/python -m ai_gateway.main serve
```

### 查看 health

```bash
curl -s http://localhost:8080/health
```

### 查看模型列表

```bash
curl -s http://localhost:8080/v1/models
```

重点看：

- `id`
- `metadata.target_model`
- `metadata.fallback_count`
- `metadata.upstream_health`

### 带鉴权请求

```bash
curl -i -s http://localhost:8080/v1/chat/completions \
  -H 'Authorization: Bearer dev-gateway-key-1' \
  -H 'Content-Type: application/json' \
  -d '{"model":"vllm-local","messages":[{"role":"user","content":"Hello gateway"}]}'
```

重点看响应 header：

- `x-request-id`
- `x-cache`
- `x-upstream-model`
- `x-fallback-used`

查看 gateway metrics：

```bash
curl -s http://localhost:8080/metrics
```

重点看：

- `ai_gateway_fallback_attempts_total`
- `ai_gateway_fallback_successes_total`

查看 gateway 最近事件：

```bash
curl -s 'http://localhost:8080/events?limit=20'
curl -s 'http://localhost:8080/events?event_type=request_success&upstream_model=vllm-local'
curl -s 'http://localhost:8080/events/summary?event_type=request_success&upstream_model=vllm-local'
curl -s 'http://localhost:8080/events/failures'
curl -s 'http://localhost:8080/events/requests?requested_model=vllm-local&upstream_model=vllm-local'
curl -s 'http://localhost:8080/events/requests/req_demo_gateway_1'
```

重点看：

- `request_received`
- `upstream_attempt`
- `fallback_attempt`
- `fallback_success`
- `cache_hit` / `cache_miss`
- `request_success`
- `upstream_model_counts`
- `status_code_counts`
- `failed_upstream_model_counts`
- `matched_request_count`
- `event_types`
- `upstream_models`
- `duration_seconds`

### Streaming 代理

```bash
curl -N http://localhost:8080/v1/chat/completions \
  -H 'Authorization: Bearer dev-gateway-key-1' \
  -H 'Content-Type: application/json' \
  -d '{"model":"vllm-local","messages":[{"role":"user","content":"Hello stream"}],"stream":true}'
```

### 不带 token

```bash
curl -i -s http://localhost:8080/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"vllm-local","messages":[{"role":"user","content":"Hello"}]}'
```

预期：

- `401`

## eval-module

### 跑一次 run

```bash
cd /path/to/ai-infra/projects/eval-module
PYTHONPATH=src ../../.venv/bin/python -m eval_module.main run \
  --task mmlu \
  --model Qwen/Qwen2.5-0.5B-Instruct \
  --backend-url http://localhost:8000/v1 \
  --output ./results/mmlu_eval_result.json
```

### 跑一次 compare

```bash
PYTHONPATH=src ../../.venv/bin/python -m eval_module.main compare \
  --baseline ./results/mmlu_eval_result.json \
  --candidate ./results/mmlu_eval_result.json \
  --min-delta 0.01 \
  --output ./results/mmlu_compare.json
```

重点看：

- `summary.verdict`
- `summary.release_recommendation`
- `summary.release_reasons`
- `results/mmlu_eval_result/sample_outputs.json`
- `results/mmlu_eval_result/sample_summary.json`
- `results/mmlu_eval_result/sample_analysis.json`

### 生成 leaderboard

```bash
PYTHONPATH=src ../../.venv/bin/python -m eval_module.main leaderboard \
  --results-dir ./results \
  --backend vllm \
  --num-fewshot 5 \
  --output ./results/leaderboard.json
```

重点看：

- `results/leaderboard.json`
- `results/leaderboard.md`
- `best_accuracy`
- `latest_accuracy`
- `run_count`
- `backend_groups`
- `fewshot_groups`
- `best_result_file`
- `latest_result_file`

### 列出历史 run

```bash
PYTHONPATH=src ../../.venv/bin/python -m eval_module.main list-runs \
  --results-dir ./results \
  --model Qwen/Qwen2.5-0.5B-Instruct \
  --backend vllm \
  --num-fewshot 5 \
  --output ./results/run_index.json
```

重点看：

- `results/run_index.json`
- `results/run_index.md`
- `report_type`
- `result_file`
- `sample_summary`
- `sample_analysis`
- `task_summaries`

### 列出历史 compare

```bash
PYTHONPATH=src ../../.venv/bin/python -m eval_module.main list-comparisons \
  --results-dir ./results \
  --output ./results/comparison_index.json
```

重点看：

- `results/comparison_index.json`
- `results/comparison_index.md`
- `baseline_model`
- `candidate_model`
- `release_recommendation`
- `verdict_counts`
- `recommendation_counts`
- `task_summaries`
- `average_delta`
- `comparison_file`

### 列出 task

```bash
PYTHONPATH=src ../../.venv/bin/python -m eval_module.main list-tasks
```

## finetune-demo

### 跑一次训练

```bash
cd /path/to/ai-infra/projects/finetune-demo
PYTHONPATH=src ../../.venv/bin/python -m finetune_demo.main train \
  --method lora \
  --model Qwen/Qwen2.5-0.5B-Instruct \
  --dataset ./data/train.jsonl \
  --output ./outputs/demo-run \
  --epochs 1
```

训练后重点看：

- `outputs/demo-run/data/dataset_summary.json` 里的 `role_counts`
- `outputs/demo-run/data/dataset_summary.json` 里的 `dataset_version`
- `outputs/demo-run/data/dataset_summary.json` 里的 `dataset_sha256`
- `outputs/demo-run/data/dataset_registry_entry.json` 里的 `dataset_id`
- `outputs/demo-run/checkpoints/checkpoint_index.json` 里的 `latest_checkpoint`
- `outputs/dataset_registry.jsonl` 里的追加式 dataset registry 记录

### 查询 dataset registry

```bash
PYTHONPATH=src ../../.venv/bin/python -m finetune_demo.main list-datasets \
  --registry ./outputs/dataset_registry.jsonl \
  --method lora \
  --model Qwen/Qwen2.5-0.5B-Instruct \
  --output ./outputs/dataset_registry_report.json \
  --markdown-output ./outputs/dataset_registry_report.md
```

重点看：

- `outputs/dataset_registry_report.json`
- `outputs/dataset_registry_report.md`
- `entry_count`
- `dataset_count`
- `registered_count`
- `method_filter`
- `model_filter`
- `duplicate_entry_count`

### 比较 dataset registry

```bash
PYTHONPATH=src ../../.venv/bin/python -m finetune_demo.main diff-datasets \
  --registry ./outputs/dataset_registry.jsonl \
  --left train@sha256:example_a \
  --right train@sha256:example_b \
  --output ./outputs/dataset_registry_diff.json \
  --markdown-output ./outputs/dataset_registry_diff.md
```

重点看：

- `identical_dataset_sha256`
- `identical_dataset_version`
- `changed_fields`
- `field_diffs`

### 查询 finetune run history

```bash
PYTHONPATH=src ../../.venv/bin/python -m finetune_demo.main list-runs \
  --history ./outputs/run_history.jsonl \
  --method lora \
  --model Qwen/Qwen2.5-0.5B-Instruct \
  --output ./outputs/run_index.json \
  --markdown-output ./outputs/run_index.md
```

重点看：

- `runs`
- `run_manifest_file`
- `checkpoint_index_file`
- `method_counts`
- `model_summaries`
- `dataset_summaries`

### 查询 export history

```bash
PYTHONPATH=src ../../.venv/bin/python -m finetune_demo.main list-exports \
  --history ./outputs/export_history.jsonl \
  --output ./outputs/export_index.json \
  --markdown-output ./outputs/export_index.md
```

重点看：

- `exports`
- `dataset_id`
- `dataset_version`
- `adapter_model_sha256`
- `export_manifest_file`
- `status_counts`
- `average_duration_seconds`
- `model_summaries`
- `dataset_summaries`

### 导出 adapter

```bash
PYTHONPATH=src ../../.venv/bin/python -m finetune_demo.main export \
  --checkpoint ./outputs/demo-run/checkpoint-0001 \
  --output ./outputs/demo-export
```

导出后重点看：

- `outputs/demo-export/export_manifest.json` 里的 `lineage`
- `outputs/demo-export/export_manifest.json` 里的 `status` 和 `duration_seconds`
- `outputs/demo-export/export_manifest.json` 里的 `dataset_id`
- `outputs/export_history.jsonl` 里的 `status`
- `outputs/export_history.jsonl` 里的 `duration_seconds`
- `outputs/export_history.jsonl` 里的 `dataset_version`
- `outputs/export_history.jsonl` 里的 `adapter_model_sha256`

## 最常用组合

### 改文档后

```bash
npm run docs:build
```

### 改 Python 代码后

```bash
PYTHON=.venv/bin/python make infra-format
PYTHON=.venv/bin/python make public-check
```

### 改跨服务链路后

```bash
PYTHON=.venv/bin/python make public-check
PYTHON=.venv/bin/python make infra-smoke
```
