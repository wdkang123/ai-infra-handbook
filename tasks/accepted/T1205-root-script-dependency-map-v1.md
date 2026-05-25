# Root Script Dependency Map v1

## Task ID: T1205
## Title: Root Integration Implementation Map Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# Root Script Dependency Map

本文档定义根级脚本与四个子项目的调用关系，基于 accepted `T805 / T1105` blueprints。

## Script Dependency Graph

```
ai-infra/
│
├── Makefile
│   ├── make all-serve
│   │       ├── $(MAKE) -C inference-service serve
│   │       └── $(MAKE) -C ai-gateway serve
│   │
│   ├── make infra-smoke
│   │       └── bash scripts/integration_smoke_test.sh
│   │               ├── curl localhost:8000/health        (inference-service)
│   │               ├── curl localhost:8080/health        (ai-gateway)
│   │               ├── curl localhost:8080/v1/chat/completions (gateway proxy)
│   │               └── curl localhost:8080/metrics      (ai-gateway metrics)
│   │
│   ├── make eval-run-mmlu
│   │       └── python -m eval_module.main run --task mmlu ...
│   │
│   ├── make eval-run-gsm8k
│   │       └── python -m eval_module.main run --task gsm8k ...
│   │
│   ├── make finetune-train
│   │       └── $(MAKE) -C finetune-demo train ...
│   │
│   └── make all-stop
│           ├── pkill -f "inference_service"
│           └── pkill -f "uvicorn"
│
├── scripts/
│   ├── local_dev_sequence.sh
│   │       ├── source .env.local
│   │       ├── $(MAKE) -C inference-service serve &
│   │       ├── sleep 5  # wait for inference
│   │       ├── $(MAKE) -C ai-gateway serve &
│   │       └── echo "All services started"
│   │
│   └── integration_smoke_test.sh
│           ├── (健康检查 + 冒烟测试)
│           └── exits 0 on success, non-zero on failure
│
└── .env.local
        ├── INFERENCE_BASE_URL=http://localhost:8000/v1
        ├── GATEWAY_BASE_URL=http://localhost:8080/v1
        └── MODEL=Qwen2.5-0.5B-Instruct
```

## Service Port Matrix

| Service | Port | URL | 依赖 | 冒烟测试 ID |
|---|---|---|---|---|
| inference-service | 8000 | `http://localhost:8000` | 无 | IT-01b |
| ai-gateway | 8080 | `http://localhost:8080` | inference-service | IT-01, IT-02, IT-03, IT-04, IT-05, IT-06 |
| eval-module | CLI only | — | inference-service | — |
| finetune-demo | — | CLI only | 无 | — |

来源：T1105 `T1105-root-service-port-matrix-v1.md`

## 子项目 CLI 入口

| 子项目 | CLI 入口 | 主要命令 |
|---|---|---|
| `eval-module` | `python -m eval_module.main` | `run`, `compare`, `list-tasks` |
| `finetune-demo` | `python -m finetune_demo.main` | `train`, `merge` |
| `inference-service` | `python -m server`（内部用） | — |
| `ai-gateway` | `uvicorn server:app`（内部用） | — |

## Makefile Target 依赖链

```
make all-serve
    ├── $(MAKE) -C inference-service serve (inference-service on :8000)
    └── $(MAKE) -C ai-gateway serve (ai-gateway on :8080)

make infra-smoke
    └── integration_smoke_test.sh
            ├── inference :8000/health
            ├── gateway :8080/health
            ├── gateway :8080/v1/chat/completions
            └── gateway :8080/metrics

make eval-run-mmlu
    └── eval-module CLI (调用 inference-service :8000)

make finetune-train
    └── $(MAKE) -C finetune-demo train ...

make all-stop
    └── (kill all service processes)
```

## 环境变量传递

```
.env.local
    │
    ├── INFERENCE_BASE_URL ──→ eval-module CLI ──→ inference-service :8000
    │                              │
    ├── GATEWAY_BASE_URL ─────────┘
    │
    └── MODEL ───────────────────→ 所有服务
```

---

Sources:
- T805: cross-project integration prep pack
- T1105: root integration fixture manifest (service port matrix)

Risk of Staleness:
- Port assignments and Makefile target interface are project-internal; stable per T805
