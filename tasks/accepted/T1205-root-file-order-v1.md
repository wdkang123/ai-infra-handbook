# Root Integration File Order v1

## Task ID: T1205
## Title: Root Integration Implementation Map Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# Root Integration File Implementation Order

本文档定义 `ai-infra/` 根目录的编码实现顺序，基于 accepted `T1005 / T1105 / T805` blueprints。

## 文件实现顺序

### Phase 0: 根级骨架

| Order | 文件路径 | 目的 | 依赖 |
|---|---|---|---|
| 0.1 | `Makefile` | 统一入口（`$(MAKE) -C ...` 驱动子项目） | 无 |
| 0.2 | `.env.example` | 环境变量模板 | 无 |
| 0.3 | `.env.local` | 本地开发环境 | Phase 0.2 |
| 0.4 | `pyproject.toml`（根） | 项目元数据 | 无 |
| 0.5 | `BLOCKERS.md` | 阻塞问题追踪 | 无 |

### Phase 1: 联调脚本

| Order | 文件路径 | 目的 | 依赖 |
|---|---|---|---|
| 1.1 | `scripts/local_dev_sequence.sh` | 本地开发顺序启动 | Phase 0 |
| 1.2 | `scripts/integration_smoke_test.sh` | 冒烟测试 | Phase 0 |

### Phase 2: 配置

| Order | 文件路径 | 目的 | 依赖 |
|---|---|---|---|
| 2.1 | `configs/service_matrix.yaml` | 服务端口/依赖矩阵 | Phase 0 |

### Phase 3: 集成测试 Fixtures

| Order | 文件路径 | 目的 | 依赖 |
|---|---|---|---|
| 3.1 | `tests/fixtures/smoke_expected/it01b_expected.json` | Direct inference 200 | Phase 1 |
| 3.2 | `tests/fixtures/smoke_expected/it01_expected.json` | Gateway proxy 200 | Phase 1 |
| 3.3 | `tests/fixtures/smoke_expected/it02_expected.txt` | Streaming SSE | Phase 1 |
| 3.4 | `tests/fixtures/smoke_expected/it03_expected.json` | Health both | Phase 1 |
| 3.5 | `tests/fixtures/smoke_expected/it04_expected.json` | No auth 401 | Phase 1 |
| 3.6 | `tests/fixtures/smoke_expected/it05_expected.json` | Invalid token 401 | Phase 1 |
| 3.7 | `tests/fixtures/smoke_expected/it06_expected.json` | Unknown model 404 | Phase 1 |
| 3.8 | `tests/fixtures/smoke_expected/it07_expected.txt` | Metrics Prometheus | Phase 1 |

### Phase 4: Blocker 文档

| Order | 文件路径 | 目的 | 依赖 |
|---|---|---|---|
| 4.1 | `docs/blockers/BLK-001-vllm-engine-timeout.md` | P0 已解决 | Phase 0 |
| 4.2 | `docs/blockers/BLK-002-gateway-routing-missing.md` | P0 已解决 | Phase 0 |
| 4.3 | `docs/blockers/BLK-003-eval-auth-blocked.md` | P1 进行中 | Phase 0 |
| 4.4 | `docs/blockers/DEBT-001-no-cors-headers.md` | P2 进行中 | Phase 0 |

---

## 目录结构

```
ai-infra/
├── Makefile                        ← Phase 0 (root entry, $(MAKE) -C ...)
├── pyproject.toml                  ← Phase 0
├── .env.example                    ← Phase 0
├── .env.local                      ← Phase 0
├── .env.smoke                      ← Phase 0
├── .env.ci                         ← Phase 0
├── BLOCKERS.md                     ← Phase 0
│
├── scripts/
│   ├── local_dev_sequence.sh       ← Phase 1
│   └── integration_smoke_test.sh  ← Phase 1
│
├── configs/
│   └── service_matrix.yaml        ← Phase 2
│
├── tests/
│   └── fixtures/
│       └── smoke_expected/         ← Phase 3
│           ├── it01b_expected.json
│           ├── it01_expected.json
│           ├── it02_expected.txt
│           ├── it03_expected.json
│           ├── it04_expected.json
│           ├── it05_expected.json
│           ├── it06_expected.json
│           ├── it07_expected.txt
│           └── summary_expected.txt
│
├── docs/
│   └── blockers/                   ← Phase 4
│       ├── BLK-001-vllm-engine-timeout.md
│       ├── BLK-002-gateway-routing-missing.md
│       ├── BLK-003-eval-auth-blocked.md
│       └── DEBT-001-no-cors-headers.md
│
├── inference-service/             ← T1201
│   └── ...
├── ai-gateway/                     ← T1202
│   └── ...
├── eval-module/                    ← T1203
│   └── ...
└── finetune-demo/                  ← T1204
    └── ...
```

---

Sources:
- T1005: root dev starter file pack
- T1105: root integration fixture manifest
- T805: cross-project integration prep pack

Risk of Staleness:
- Makefile targets and script interface are project-internal; stable
