# Root Integration Fixture Manifest v1

## Task ID: T1105
## Title: Root Integration Fixture Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# Root Integration Fixture Manifest

本文档是根级联调全部 fixture 资产的索引清单，对应真实路径 `ai-infra/.env*`、`ai-infra/configs/`、`ai-infra/tests/fixtures/smoke_expected/`、`ai-infra/docs/blockers/`。

## Fixture 文件清单

### Env Profile Fixtures

| 文件路径 | 场景 |
|---|---|
| `.env.local` | 本地开发环境 |
| `.env.smoke` | 冒烟测试环境 |
| `.env.ci` | CI/CD 环境 |

### Smoke Expected Output Fixtures

| 文件路径 | 测试 ID | 场景 |
|---|---|---|
| `tests/fixtures/smoke_expected/it01b_expected.json` | IT-01b | Direct inference 200 |
| `tests/fixtures/smoke_expected/it01_expected.json` | IT-01 | Gateway proxy 200 |
| `tests/fixtures/smoke_expected/it02_expected.txt` | IT-02 | Streaming SSE |
| `tests/fixtures/smoke_expected/it03_expected.json` | IT-03 | Health both |
| `tests/fixtures/smoke_expected/it04_expected.json` | IT-04 | No auth 401 |
| `tests/fixtures/smoke_expected/it05_expected.json` | IT-05 | Invalid token 401 |
| `tests/fixtures/smoke_expected/it06_expected.json` | IT-06 | Unknown model 404 |
| `tests/fixtures/smoke_expected/it07_expected.txt` | IT-07 | Metrics Prometheus |
| `tests/fixtures/smoke_expected/summary_expected.txt` | — | Smoke 汇总输出格式 |

### Service Port Matrix

| 文件路径 | 场景 |
|---|---|
| `configs/service_matrix.yaml` | 模块/端口/依赖关系矩阵 |

### Blocker Entries

| 文件路径 | 场景 |
|---|---|
| `docs/blockers/BLK-001-vllm-engine-timeout.md` | P0 已解决 |
| `docs/blockers/BLK-002-gateway-routing-missing.md` | P0 已解决 |
| `docs/blockers/BLK-003-eval-auth-blocked.md` | P1 进行中 |
| `docs/blockers/DEBT-001-no-cors-headers.md` | P2 进行中 |

---

## 与其他 Fixture Pack 的交叉依赖

| 依赖 Pack | 依赖内容 | 本 Pack 来源 |
|---|---|---|
| T1101 inference fixtures | `/health`、`/metrics` 契约 | `smoke_expected/it03/it07` |
| T1102 gateway fixtures | 路由配置、错误响应 | `service_matrix.yaml`、`smoke_expected/it04~06` |
| T1103 eval fixtures | eval 结果 JSON 格式 | `smoke_expected/` 无直接依赖 |
| T1104 finetune fixtures | 无直接依赖 | — |

---

## 与 T805 Integration Contract 对齐

| 集成检查项 | Fixture 对应 |
|---|---|
| IT-01: Gateway → Inference | `it01_expected.json` |
| IT-02: Streaming | `it02_expected.txt` |
| IT-03: Health both | `it03_expected.json` |
| IT-04: No auth | `it04_expected.json` |
| IT-05: Invalid token | `it05_expected.json` |
| IT-06: Unknown model | `it06_expected.json` |
| IT-07: Metrics | `it07_expected.txt` |
| 服务端口矩阵 | `configs/service_matrix.yaml` |

---

## 根 Makefile 入口与 Fixture 对应

| Makefile Target | 调用的脚本 | Fixture 覆盖 |
|---|---|---|
| `make infra-smoke` | `bash scripts/integration_smoke_test.sh` | `smoke_expected/*.json/txt` |
| `make all-serve` | `inference-serve && gateway-serve` | `service_matrix.yaml` |
| `make eval-run-mmlu` | `eval-module` CLI | T1103 eval fixtures |
| `make finetune-train` | `finetune-demo` CLI | T1104 finetune fixtures |

---

Sources:
1. https://docs.vllm.ai/en/latest/serving/configuration.html
2. https://github.com/Portkey-AI/gateway

Risk of Staleness:
- Service port matrix and smoke test format are project-internal; stable per T805
