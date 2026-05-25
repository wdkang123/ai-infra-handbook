# Repo Task Runner Map v1

## Task ID: T905
## Title: Developer Workflow Scaffold Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T815 implementation order 和各模块 repo layout，产出各模块 CLI/Makefile 速查表。

---

# Repo Task Runner Map v1

## 概述

本文档定义各模块的 CLI 入口和 Makefile target 速查表。

## 快速对照表

| 模块 | CLI 命令 | Makefile target | 配置文件 |
|------|---------|----------------|---------|
| inference-service | `inference-service serve ...` | `make serve` | `config.yaml` |
| ai-gateway | `ai-gateway serve ...` | `make serve` | `config.yaml` |
| eval-module | `eval-module run ...` | `make run-mmlu` | `config.yaml` |
| finetune-demo | `finetune-demo train ...` | `make train-lora` | `configs/*.yaml` |

---

## inference-service

### CLI 入口

```bash
# 安装（从 inference-service/ 目录执行）
pip install -e "."

# 启动
inference-service serve \
  --engine vllm \
  --model Qwen/Qwen2.5-0.5B-Instruct \
  --port 8000

# 关键参数
--engine          # vllm | sglang | triton
--model           # HuggingFace model name
--port            # HTTP port (default: 8000)
--metrics-port    # Prometheus port (default: 9090)
--vllm-gpu-memory-utilization  # 0.0~1.0
```

### Makefile targets

| Target | 说明 |
|--------|------|
| `make install` | 安装 |
| `make serve` | 启动服务 |
| `make serve-dev` | 开发模式（热重载） |
| `make health` | 健康检查 |
| `make curl-chat` | 测试 chat completions |
| `make curl-stream` | 测试流式输出 |
| `make test` | 运行单元测试 |
| `make lint` | 代码检查 |

### 端口

| 端口 | 用途 |
|------|------|
| 8000 | HTTP API |
| 9090 | Prometheus metrics |

---

## ai-gateway

### CLI 入口

```bash
# 安装（从 ai-gateway/ 目录执行）
pip install -e "."

# 启动
ai-gateway serve \
  --port 8080

# 关键参数
--port           # HTTP port (default: 8080)
--metrics-port   # Prometheus port (default: 9091)
--no-auth        # 禁用鉴权（开发用）
--no-rate-limit  # 禁用限流（开发用）
```

### Makefile targets

| Target | 说明 |
|--------|------|
| `make install` | 安装 |
| `make serve` | 启动服务 |
| `make health` | 健康检查 |
| `make curl-chat` | 测试（含 auth） |
| `make curl-chat-no-auth` | 测试（无 auth） |
| `make test` | 运行单元测试 |

### 端口

| 端口 | 用途 |
|------|------|
| 8080 | HTTP Gateway |
| 9091 | Prometheus metrics |

### Auth Key（默认）

| Key | 用途 |
|-----|------|
| `dev-gateway-key-1` | 默认测试 key |
| `dev-gateway-key-2` | 备用测试 key |

---

## eval-module

### CLI 入口

```bash
# 安装（从 eval-module/ 目录执行）
pip install -e "."

# 运行评测
eval-module run \
  --task mmlu \
  --model Qwen/Qwen2.5-0.5B-Instruct \
  --backend-url http://localhost:8000/v1 \
  --num-fewshot 5

# 对比结果
eval-module compare \
  --baseline ./results/baseline.json \
  --candidate ./results/candidate.json

# 列出可用任务
eval-module list-tasks
```

### Makefile targets

| Target | 说明 |
|--------|------|
| `make install` | 安装 |
| `make run-mmlu` | 运行 MMLU |
| `make run-gsm8k` | 运行 GSM8K |
| `make compare` | 对比结果 |
| `make test` | 运行测试 |

### lm-eval 直接命令（绕过 CLI 封装）

```bash
lm_eval \
    --model vllm \
    --model_args "base_url=http://localhost:8000/v1,pretrained=Qwen/Qwen2.5-0.5B-Instruct" \
    --tasks mmlu \
    --num_fewshot 5 \
    --limit 10
```

---

## finetune-demo

### CLI 入口

```bash
# 安装（从 finetune-demo/ 目录执行）
pip install -e "."

# 训练 LoRA
finetune-demo train \
  --method lora \
  --model Qwen/Qwen2.5-0.5B-Instruct \
  --dataset ./data/train.jsonl \
  --epochs 3 \
  --output ./models/lora

# 保存 adapter
finetune-demo save \
  --checkpoint ./models/lora/checkpoint-500 \
  --output ./models/lora/adapter
```

### Makefile targets

| Target | 说明 |
|--------|------|
| `make install` | 安装 |
| `make train-lora` | LoRA 训练 |
| `make train-qlora` | QLoRA 训练 |
| `make save-checkpoint` | 保存 adapter |
| `make list-checkpoints` | 列出 checkpoint |
| `make test` | 运行测试 |

---

## Root Makefile（跨项目）

```bash
# 安装所有模块
make infra-install

# 启动所有服务
make all-serve

# 停止所有服务
make all-stop

# 运行冒烟测试
make infra-smoke

# 运行所有测试
make infra-test
```

---

## 共享环境变量

| 变量 | 默认值 | 适用模块 |
|------|-------|---------|
| `MODEL_NAME` | `Qwen/Qwen2.5-0.5B-Instruct` | 所有 |
| `INFERENCE_PORT` | `8000` | inference-service |
| `GATEWAY_PORT` | `8080` | ai-gateway |
| `INFERENCE_BASE_URL` | `http://localhost:8000/v1` | gateway, eval |

---

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval
3. https://github.com/huggingface/peft — PEFT

Risk of Staleness:
- CLI 参数尚未最终确定（取决于 FastAPI/Typer 实现）

Out of Scope Kept:
- 未写各模块的完整 CLI help
