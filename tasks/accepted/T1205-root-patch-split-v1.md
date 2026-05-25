# Root Integration Patch Split v1

## Task ID: T1205
## Title: Root Integration Implementation Map Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# Root Integration Patch Split Proposal

本文档定义根级联调流程的分批实现顺序。

## Patch 批次概览

| Patch | 名称 | 目标文件 | 验证方式 |
|---|---|---|---|
| P0 | 根骨架 | `Makefile / .env.example / BLOCKERS.md` | `make help` 输出正确 |
| P1 | 联调脚本 | `scripts/local_dev_sequence.sh` | 顺序启动所有服务 |
| P2 | 冒烟测试 | `scripts/integration_smoke_test.sh` | `make infra-smoke` 通过 |
| P3 | Fixture 对齐 | `tests/fixtures/smoke_expected/*.json` | smoke test 输出匹配 |
| P4 | Blocker 文档 | `docs/blockers/*.md` | blocker 状态正确 |

---

## Patch 0: 根骨架

**文件：**
- `Makefile`
- `.env.example`
- `BLOCKERS.md`
- `pyproject.toml`（根）

**验证：**
```bash
make help
# 期望输出：
# all-serve    - Start all services
# infra-smoke - Run smoke tests
# all-stop     - Stop all services
# eval-run-*  - Run eval tasks
# finetune-train - Run finetuning
```

---

## Patch 1: 联调脚本

**文件：**
- `scripts/local_dev_sequence.sh`

**验证：**
```bash
bash scripts/local_dev_sequence.sh
# 期望输出：
# Starting inference-service...
# inference-service ready
# Starting ai-gateway...
# ai-gateway ready
# All services started
```

---

## Patch 2: 冒烟测试

**文件：**
- `scripts/integration_smoke_test.sh`

**验证：**
```bash
# 先启动所有服务
make all-serve
sleep 5

# 运行冒烟测试
make infra-smoke
# 期望：IT-01b, IT-01, IT-02, IT-03, IT-04, IT-05, IT-06, IT-07 全部 PASS

make all-stop
```

**对应 fixture：** T1105 `T1105-root-smoke-expected-output-v1.md`

---

## Patch 3: Fixture 对齐

**文件：**
- `tests/fixtures/smoke_expected/*.json`
- `tests/fixtures/smoke_expected/*.txt`

**验证：**
```bash
# 冒烟测试输出与 fixture 比对
bash scripts/integration_smoke_test.sh > /tmp/smoke_output.txt

# IT-01: gateway proxy
diff <(cat /tmp/smoke_output.txt | grep -A50 "IT-01" | head -30) \
        tests/fixtures/smoke_expected/it01_expected.json

# IT-04: no auth 401
grep '"401"' /tmp/smoke_output.txt
```

---

## Patch 4: Blocker 文档

**文件：**
- `docs/blockers/BLK-001-vllm-engine-timeout.md`
- `docs/blockers/BLK-002-gateway-routing-missing.md`
- `docs/blockers/BLK-003-eval-auth-blocked.md`
- `docs/blockers/DEBT-001-no-cors-headers.md`

**验证：**
```bash
# BLK-001 和 BLK-002 状态应为 RESOLVED
grep "Status: RESOLVED" docs/blockers/BLK-001-vllm-engine-timeout.md
grep "Status: RESOLVED" docs/blockers/BLK-002-gateway-routing-missing.md

# BLK-003 状态应为 IN_PROGRESS
grep "Status: IN_PROGRESS" docs/blockers/BLK-003-eval-auth-blocked.md
```

---

## Patch 依赖关系图

```
P0 (根骨架)
  │
  ├── P1 (联调脚本)           ← 依赖 P0
  │       │
  │       └── P2 (冒烟测试) ← 依赖 P1
  │               │
  │               └── P3 (Fixture对齐) ← 依赖 P2
  │
  └── P4 (Blocker 文档)      ← 独立可写
```

**注意：** P1-P2 需要各子服务可运行。P4 Blocker 文档可独立于服务编写。

---

Sources:
- T1005: root dev starter file pack
- T1105: root integration fixture manifest

Risk of Staleness:
- Makefile interface and smoke test contract are project-internal; stable
