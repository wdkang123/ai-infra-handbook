# Root Integration Codex Handoff v1

## Task ID: T1405
## Title: Root Integration Codex Task Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# Root Integration Codex Handoff

本文档是可直接复制给 Codex 的任务卡 handoff 文本。

---

## T1405-R1: Makefile 入口

**任务：** 创建仓库根目录 `Makefile`。

**Makefile 要求：**
- 使用 `$(MAKE) -C <subdir>` 模式驱动子项目
- 共享配置变量：`MODEL ?= Qwen/Qwen2.5-0.5B-Instruct`、`INFERENCE_PORT ?= 8000`、`GATEWAY_PORT ?= 8080`
- `inference-serve`：调用 `$(MAKE) serve MODEL=$(MODEL) PORT=$(INFERENCE_PORT) -C inference-service &`
- `gateway-serve`：调用 `$(MAKE) serve PORT=$(GATEWAY_PORT) -C ai-gateway &`
- `all-serve`：先启动 inference-service，sleep 30 后验证 health，再启动 gateway
- `all-stop`：pkill inference-service 和 ai-gateway
- `infra-smoke`：调用 `bash scripts/integration_smoke_test.sh`
- `eval-install / eval-run-mmlu / eval-run-gsm8k`：代理到 eval-module Makefile
- `finetune-install / finetune-train`：代理到 finetune-demo Makefile

**Makefile 格式（来自 T1005 v2）：**
```makefile
MODEL ?= Qwen/Qwen2.5-0.5B-Instruct
INFERENCE_PORT ?= 8000
GATEWAY_PORT ?= 8080
INFERENCE_BASE_URL ?= http://localhost:$(INFERENCE_PORT)/v1

all-serve: inference-serve
	@sleep 30 && inference-health && gateway-serve

inference-serve:
	@$(MAKE) serve MODEL=$(MODEL) PORT=$(INFERENCE_PORT) -C inference-service &

gateway-serve:
	@$(MAKE) serve PORT=$(GATEWAY_PORT) -C ai-gateway &
```

**禁止事项：** 不写 CI/CD 目标，不写 Kubernetes 部署目标

---

## T1405-R2: 本地开发顺序

**任务：** 创建 `scripts/local_dev_sequence.sh`。

**关键实现：**
- `start_inference_service()`：先停再启，调用 `cd inference-service && make serve MODEL="$MODEL" PORT="$INFERENCE_PORT" &`
- `start_ai_gateway()`：先停再启，调用 `cd ai-gateway && make serve PORT="$GATEWAY_PORT" &`
- `wait_for_url()`：轮询 `/health`，最多等待 60 秒
- `stop_all()`：通过 `pgrep -f` 查找 PID 并 kill

**服务端口：**
- inference-service: `localhost:8000`
- ai-gateway: `localhost:8080`
- eval-module: CLI only（不启动 server）
- finetune-demo: CLI only（不启动 server）

**验证命令：**
```bash
bash scripts/local_dev_sequence.sh start
sleep 35
curl -s http://localhost:8000/health
curl -s http://localhost:8080/health
bash scripts/local_dev_sequence.sh stop
```

**禁止事项：** 不写定时重启脚本，不写日志收集

---

## T1405-R3: 冒烟测试

**任务：** 创建 `scripts/integration_smoke_test.sh`。

**冒烟测试覆盖（IT-01b ~ IT-07）：**

| ID | 场景 | 验证命令 | 预期结果 |
|---|---|---|---|
| IT-01b | Direct inference | `curl localhost:8000/v1/chat/completions` | 200 + choices |
| IT-01 | Gateway proxy | `curl localhost:8080/v1/chat/completions` (Bearer) | 200 + choices |
| IT-04 | No auth 401 | `curl localhost:8080/v1/chat/completions` (no auth) | 401 |
| IT-06 | Unknown model 404 | `curl ... -d '{"model":"unknown"}'` | 404 |
| IT-07 | Prometheus metrics | `curl localhost:8080/metrics \| grep ai_gateway_` | 有输出 |

**IT-01 验证（gateway）：**
```bash
curl -s -w "\n%{http_code}" -X POST "http://localhost:8080/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer dev-gateway-key-1" \
  -d '{"model": "vllm-local", "messages": [{"role": "user", "content": "What is 2+2?"}]}'
```

**IT-04 验证（无 token）：**
```bash
curl -s -o /dev/null -w "%{http_code}" -X POST "http://localhost:8080/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{"model": "vllm-local", "messages": [{"role": "user", "content": "Hi"}]}'
# 期望 401
```

**IT-07 验证（gateway metrics）：**
```bash
curl -s http://localhost:8080/metrics | grep ai_gateway_
# 注意：是 ai_gateway_ 不是 vllm_（vllm_ 是 inference-service 的）
```

**禁止事项：** 不写端到端 benchmark，不写 load test

---

## T1405-R4: 跨项目 Handoff

**任务：** 创建 `CODEX_IMPLEMENTATION_HANDOFF.md`。

**文档结构：**
1. 项目概述
2. 服务依赖关系图
3. 各子项目交接边界
4. 端点映射（端口、URL）
5. 验证命令

**交接边界（来自 T1305）：**

| 子项目 | 交接对象 | 交接内容 |
|---|---|---|
| inference-service | ai-gateway | `http://localhost:8000/v1` 作为下游 |
| inference-service | eval-module | `http://localhost:8000/v1` 作为评测 backend |
| inference-service | finetune-demo | adapter 权重文件，加载到 vLLM |
| ai-gateway | eval-module | `http://localhost:8080/v1` 作为可选入口 |

**服务端口汇总：**
- inference-service: `localhost:8000`
- ai-gateway: `localhost:8080`
- eval-module: CLI only
- finetune-demo: CLI only

**禁止事项：** 不写 production 部署文档，不写 CI/CD 配置

---

Sources:
- T1005: accepted root makefile blueprint v2
- T1005: accepted local dev sequence blueprint v2
- T1005: accepted integration smoke blueprint v2
- T1305: accepted root slice contracts
- T1105: root integration fixture manifest
