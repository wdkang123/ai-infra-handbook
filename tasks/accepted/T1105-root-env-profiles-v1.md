# Root Integration Env Profiles v1

## Task ID: T1105
## Title: Root Integration Fixture Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# Root Integration Env Profiles

本文档定义仓库根级联调的环境配置模板，对应真实文件 `ai-infra/.env*` 和 `ai-infra/configs/`。

---

## Profile A: Local Development

**对应文件：** `ai-infra/.env.local`

```bash
# ============================================================
# ai-infra — Local Development Environment
# 使用方法: cp .env.local .env && 按需修改
# ============================================================

# --- 模型配置 ---
MODEL=Qwen/Qwen2.5-0.5B-Instruct

# --- inference-service ---
INFERENCE_PORT=8000
INFERENCE_HOST=0.0.0.0
INFERENCE_BASE_URL=http://localhost:8000/v1
INFERENCE_ENGINE=vllm
VLLMTensorizerMode=awq
VLLMDtype=float16
VLLMGpuMemoryUtilization=0.85

# --- ai-gateway ---
GATEWAY_PORT=8080
GATEWAY_HOST=0.0.0.0
GATEWAY_BASE_URL=http://localhost:8080
SMOKE_AUTH_KEY=sk-test-key-1

# --- eval-module ---
EVAL_BACKEND_URL=http://localhost:8000/v1
EVAL_OUTPUT_DIR=./results/eval

# --- finetune-demo ---
FINETUNE_BASE_MODEL=Qwen/Qwen2.5-0.5B-Instruct
FINETUNE_OUTPUT_DIR=./outputs/finetune

# --- 通用 ---
LOG_LEVEL=info
PYTHONPATH=.
```

---

## Profile B: Smoke Test

**对应文件：** `ai-infra/.env.smoke`

```bash
# ============================================================
# ai-infra — Smoke Test Environment
# 使用方法: cp .env.smoke .env && bash scripts/integration_smoke_test.sh
# ============================================================

# --- 模型配置（固定用于冒烟测试）---
MODEL=Qwen/Qwen2.5-0.5B-Instruct

# --- inference-service ---
INFERENCE_PORT=8000
INFERENCE_HOST=127.0.0.1
INFERENCE_BASE_URL=http://localhost:8000/v1
VLLMDtype=float16
VLLMGpuMemoryUtilization=0.5
VLLMEnforceEager=true          # 方便调试

# --- ai-gateway ---
GATEWAY_PORT=8080
GATEWAY_HOST=127.0.0.1
GATEWAY_BASE_URL=http://localhost:8080
SMOKE_AUTH_KEY=sk-test-key-1

# --- 冒烟测试专用 ---
SMOKE_RESULTS_DIR=./results/smoke

# --- 通用 ---
LOG_LEVEL=warning
PYTHONPATH=.
```

---

## Profile C: CI / CD

**对应文件：** `ai-infra/.env.ci`

```bash
# ============================================================
# ai-infra — CI/CD Environment
# ============================================================

MODEL=Qwen/Qwen2.5-0.5B-Instruct
INFERENCE_PORT=8000
INFERENCE_BASE_URL=http://localhost:8000/v1
GATEWAY_PORT=8080
GATEWAY_BASE_URL=http://localhost:8080
SMOKE_AUTH_KEY=${SMOKE_AUTH_KEY:-sk-test-key-1}
LOG_LEVEL=error
PYTHONPATH=.
```

---

## Config 统一变量名（根级 Makefile 对齐）

根据 T1005 review findings，`MODEL` 是根级 Makefile 暴露的统一变量名：

| 变量名 | Makefile (T1005) | .env.local | .env.smoke |
|---|---|---|---|
| 模型名 | `MODEL` | `MODEL` | `MODEL` |
| inference 端口 | `INFERENCE_PORT` | `INFERENCE_PORT` | `INFERENCE_PORT` |
| gateway 端口 | `GATEWAY_PORT` | `GATEWAY_PORT` | `GATEWAY_PORT` |
| 认证 key | — | `SMOKE_AUTH_KEY` | `SMOKE_AUTH_KEY` |

---

## 环境 profile 使用场景

| Profile | 使用场景 | 命令 |
|---|---|---|
| `.env.local` | 本地开发 | `cp .env.local .env` |
| `.env.smoke` | 冒烟测试 | `cp .env.smoke .env && make infra-smoke` |
| `.env.ci` | CI pipeline | 由 CI 系统自动注入 |

---

Sources:
1. https://github.com/EleutherAI/lm-evaluation-harness — eval config reference
2. https://docs.vllm.ai/en/latest/serving/configuration.html — vLLM env

Risk of Staleness:
- Environment variable schema is project-internal; stable
