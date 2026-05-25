# Root Integration Codex Task Cards v1

## Task ID: T1405
## Title: Root Integration Codex Task Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# Root Integration Codex Task Cards

本文档定义每个任务卡的具体输入资产、目标文件、验收命令、完成信号和 cut line。

---

## T1405-R1: Makefile 入口

**Task Name:** Makefile 入口

**对应 Slice:** R1

**输入资产：**
- `T1005-root-makefile-blueprint-v2.md`

**目标文件：**
```
Makefile
```

**验收命令：**
```bash
make help
# 期望输出包含：
# inference-serve, inference-health, inference-test
# gateway-serve, gateway-health, gateway-test
# eval-install, eval-run-mmlu, eval-run-gsm8k
# finetune-install, finetune-train
# all-serve, all-stop, infra-smoke
```

**完成信号：** `make help` 输出所有 target，且 `make all-serve` 和 `make all-stop` 可执行

**Cut Line：** 不写 CI/CD 目标，不写 Kubernetes 部署目标，不写多环境配置

---

## T1405-R2: 本地开发顺序

**Task Name:** 本地开发顺序

**对应 Slice:** R2

**输入资产：**
- `T1005-local-dev-sequence-sh-blueprint-v2.md`
- `T1405-R1/`

**目标文件：**
```
scripts/local_dev_sequence.sh
```

**验收命令：**
```bash
# 1. 启动所有服务（inference + gateway）
make all-serve
sleep 35

# 2. 验证 inference-service
curl -s http://localhost:8000/health | python -m json.tool
# 期望：{"status": "healthy", "engine": "vllm", ...}

# 3. 验证 ai-gateway
curl -s http://localhost:8080/health | python -m json.tool
# 期望：{"status": "healthy", "version": "0.1.0", ...}

# 4. 停止所有服务
make all-stop
```

**完成信号：** 所有服务按顺序启动，健康检查全部返回 200

**Cut Line：** 不写定时重启脚本，不写日志收集，不写 helper script 主线

---

## T1405-R3: 冒烟测试

**Task Name:** 冒烟测试

**对应 Slice:** R3

**输入资产：**
- `T1005-integration-smoke-sh-blueprint-v2.md`
- `T1405-R1/`

**目标文件：**
```
scripts/integration_smoke_test.sh
```

**验收命令：**
```bash
# 1. 启动所有服务
make all-serve
sleep 35

# 2. 运行冒烟测试
make infra-smoke
# 期望：IT-01b ~ IT-07 全部 PASS

# 3. 停止
make all-stop
```

**冒烟测试内容（IT-01b ~ IT-07）：**

| ID | 场景 | 验证命令 | 预期结果 |
|---|---|---|---|
| IT-01b | Direct inference | `curl localhost:8000/v1/chat/completions` | 200 + choices |
| IT-01 | Gateway proxy | `curl localhost:8080/v1/chat/completions` (Bearer) | 200 + choices |
| IT-04 | No auth 401 | `curl localhost:8080/v1/chat/completions` (no auth) | 401 |
| IT-06 | Unknown model 404 | `curl ... -d '{"model":"unknown"}'` | 404 |
| IT-07 | Prometheus metrics | `curl localhost:8080/metrics \| grep ai_gateway_` | 有输出 |

**完成信号：** 所有 IT-* 测试 PASS

**Cut Line：** 不写端到端 benchmark，不写 load test

---

## T1405-R4: 跨项目 Handoff

**Task Name:** 跨项目 Handoff

**对应 Slice:** R4

**输入资产：**
- `T1305-root-slice-contracts-v1.md`
- `T1405-R1/` + `T1405-R2/` + `T1405-R3/`

**目标文件：**
```
CODEX_IMPLEMENTATION_HANDOFF.md
```

**验收命令：**
```bash
# 1. inference-service 可被 ai-gateway 调用
# （R3 IT-01 已验证）

# 2. eval-module 可调用 inference-service
cd eval-module
MODEL=Qwen/Qwen2.5-0.5B-Instruct \
INFERENCE_BASE_URL=http://localhost:8000/v1 \
make run-mmlu
# 期望：mmlu result JSON 生成

# 3. finetune-demo 产出的 adapter 可被 inference-service 加载
# （adapter export 由 F5 验证）

# 4. 根级 Makefile all-serve 统一管理
make all-serve && sleep 35 && make infra-smoke && make all-stop
# 期望：完整流程通过
```

**完成信号：** 文档描述清楚四个子项目的交接边界，服务间正确对接

**Cut Line：** 不写 production 部署文档

---

Sources:
- T1005: accepted root makefile blueprint v2
- T1305: accepted execution slice pack
- T1105: root integration fixture manifest
- T805: cross-project integration prep pack
