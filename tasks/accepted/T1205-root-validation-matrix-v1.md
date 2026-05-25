# Root Integration Validation Matrix v1

## Task ID: T1205
## Title: Root Integration Implementation Map Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# Root Integration Validation Matrix

本文档定义根级联调各 patch 的验收测试矩阵。

## Validation Matrix

| ID | 命令 | 场景 | 预期结果 | 验证命令 | 依赖 Patch |
|---|---|---|---|---|---|
| R01 | `make help` | Makefile 帮助 | 输出所有 target | `make help` | P0 |
| R02 | `make all-serve` | 启动所有服务 | 服务启动无报错 | `make all-serve & sleep 5; curl localhost:8000/health; curl localhost:8080/health` | P0 |
| R03 | `make all-stop` | 停止所有服务 | 服务退出 | `make all-stop; pgrep -f "server\|uvicorn" | wc -l` → 0 | P0 |
| R04 | `make infra-smoke` | 冒烟测试 | IT-01b ~ IT-07 全部 PASS | `make all-serve && sleep 5 && make infra-smoke` | P3 |
| R05 | `bash scripts/local_dev_sequence.sh` | 本地开发顺序 | 所有服务健康 | `bash scripts/local_dev_sequence.sh && curl localhost:8000/health && curl localhost:8080/health` | P2 |
| R06 | `curl localhost:8000/health` | inference 健康 | 200 OK | `curl -s localhost:8000/health` | P1 |
| R07 | `curl localhost:8080/health` | gateway 健康 | 200 OK | `curl -s localhost:8080/health` | P1 |
| R08 | `curl localhost:8080/v1/chat/completions` | Gateway 代理 | 200 OK + choices | `curl -s -X POST localhost:8080/v1/chat/completions -H "Authorization: Bearer dev-gateway-key-1" -d '{"model":"Qwen2.5-0.5B-Instruct","messages":[{"role":"user","content":"2+2=?"}]}'` | P1 |
| R09 | `curl localhost:8080/v1/chat/completions` (无 auth) | 无认证 401 | 401 Unauthorized | `curl -s -w "%{http_code}" localhost:8080/v1/chat/completions` → `401` | P1 |
| R10 | `curl localhost:8080/v1/chat/completions` (unknown model) | 未知模型 404 | 404 | `curl -s -w "%{http_code}" -X POST localhost:8080/v1/chat/completions -H "Authorization: Bearer dev-gateway-key-1" -d '{"model":"unknown-model","messages":[{"role":"user","content":"hi"}]}'` → `404` | P1 |
| R11 | `curl localhost:8080/metrics` | Prometheus metrics | 200 + vllm_/inference_service_ metrics | `curl -s localhost:8080/metrics | grep -c "vllm_"` | P1 |
| R12 | `make eval-run-mmlu` | 运行 MMLU 评测 | 结果 JSON 生成 | `make eval-run-mmlu MODEL=Qwen2.5-0.5B-Instruct && ls results/mmlu_result.json` | P2 |
| R13 | `make finetune-train` | 运行微调训练 | adapter 产物 | `make finetune-train MODEL=Qwen2.5-0.5B-Instruct && ls finetune-demo/outputs/` | P2 |

---

## R01: Makefile Help Verification

```bash
make help
# 期望输出：
# all-serve       Start all services (inference + gateway)
# infra-smoke     Run integration smoke tests
# all-stop        Stop all services
# eval-run-mmlu   Run MMLU benchmark via eval-module
# eval-run-gsm8k  Run GSM8K benchmark via eval-module
# finetune-train  Run finetuning via finetune-demo
# help            Show this help
```

---

## R04: Smoke Test Verification

```bash
# IT-01b: Direct inference
curl -s -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"Qwen2.5-0.5B-Instruct","messages":[{"role":"user","content":"hi"}],"max_tokens":10}' \
  | python -c "import json,sys; r=json.load(sys.stdin); print('IT-01b:', 'choices' in r)"

# IT-01: Gateway proxy
curl -s -X POST http://localhost:8080/v1/chat/completions \
  -H "Authorization: Bearer dev-gateway-key-1" \
  -H "Content-Type: application/json" \
  -d '{"model":"Qwen2.5-0.5B-Instruct","messages":[{"role":"user","content":"hi"}],"max_tokens":10}' \
  | python -c "import json,sys; r=json.load(sys.stdin); print('IT-01:', 'choices' in r)"

# IT-04: No auth 401
curl -s -w "%{http_code}" http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"Qwen2.5-0.5B-Instruct","messages":[{"role":"user","content":"hi"}]}' \
  | tail -c 3
# 期望：401

# IT-06: Unknown model 404
curl -s -w "%{http_code}" -X POST http://localhost:8080/v1/chat/completions \
  -H "Authorization: Bearer dev-gateway-key-1" \
  -H "Content-Type: application/json" \
  -d '{"model":"unknown-model-xyz","messages":[{"role":"user","content":"hi"}]}' \
  | tail -c 3
# 期望：404

# IT-07: Prometheus metrics
curl -s http://localhost:8080/metrics | grep "vllm_"
# 期望：输出包含 vllm_ 开头的 metric 行
```

**对应 fixture：** T1105 `T1105-root-smoke-expected-output-v1.md`

---

## R12: eval-module via Makefile Verification

```bash
make eval-run-mmlu \
  MODEL=Qwen2.5-0.5B-Instruct \
  INFERENCE_BASE_URL=http://localhost:8000/v1 \
  OUTPUT=./results/mmlu_result.json

python -c "
import json
with open('./results/mmlu_result.json') as f:
    r = json.load(f)
print('task:', r['task'])
print('accuracy:', r['accuracy'])
print('backend:', r['backend'])  # 期望: 'vllm'
"
```

---

## Service Port Matrix Reference

| Service | Port | 健康检查 | 主要端点 |
|---|---|---|---|
| inference-service | 8000 | `/health` | `/v1/chat/completions`, `/metrics` |
| ai-gateway | 8080 | `/health` | `/v1/chat/completions`, `/metrics` |
| eval-module | CLI only | — | CLI only |

来源：T1105 `T1105-root-service-port-matrix-v1.md`

---

Sources:
- T1005: root dev starter file pack
- T1105: root integration fixture manifest, smoke expected outputs, service port matrix
- T805: cross-project integration prep pack

Risk of Staleness:
- Smoke test contract and Makefile interface are project-internal; stable per T805
