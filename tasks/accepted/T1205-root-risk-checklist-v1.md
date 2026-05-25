# Root Integration Risk Checklist v1

## Task ID: T1205
## Title: Root Integration Implementation Map Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# Root Integration Risk & Blocker Checklist

本文档定义根级联调实现过程中的风险点与阻塞检查项。

## P0 阻塞风险

| Risk | 描述 | 缓解方案 |
|---|---|---|
| **子服务不可用** | 任何子服务未启动导致 smoke test 失败 | smoke test 前确保 `make all-serve` 成功 |
| **端口冲突** | 8000/8080 端口被占用 | `lsof -i :8000 -i :8080` 确认空闲 |
| **GPU 显存不足** | inference-service + 其他服务争抢 GPU | 确保 GPU >= 24GB 或只跑 CPU 模型 |

---

## P1 风险

| Risk | 描述 | 检测方式 | 缓解 |
|---|---|---|---|
| **inference-service 启动慢** | vLLM engine 初始化需要 30s+ | `local_dev_sequence.sh` 中 `sleep 10` | 等待 `/health` 返回 200 再启动下游 |
| **gateway 依赖 inference** | gateway 启动过早，proxy 请求失败 | R08 失败 | `local_dev_sequence.sh` 中加 health poll |
| **auth token 失效** | 测试用 `sk-test-key-1` 被修改 | R09 失败 | 检查 `ai-gateway` 中 `api_keys` 配置 |
| **eval-module 依赖 GPU** | lm-eval runner 需要真实 GPU | R12 失败 | P0 阶段用 mock runner |

---

## P2 风险

| Risk | 描述 | 检测方式 | 缓解 |
|---|---|---|---|
| **smoke test 时序问题** | health check 还没好就发请求 | `make infra-smoke` 偶发失败 | 增加 `sleep 5` 或 health poll 重试 |
| **inference-service OOM** | 大 batch 导致 vLLM OOM | R06 返回 500 | 降低 `gpu_memory_utilization=0.5` |
| **model 不匹配** | inference 用 Qwen 但 gateway 路由配置缺失 | R10 偶发 | `configs/models.yaml` 添加 Qwen 路由 |
| **metrics 端点无数据** | inference-service metrics 未暴露 | R11 grep 0 | 检查 `server.py` 中 `add_metrics` |

---

## P3 风险

| Risk | 描述 | 检测方式 | 缓解 |
|---|---|---|---|
| **.env 变量未传递** | 子脚本读不到 `INFERENCE_BASE_URL` | eval-module 连不上 backend | `export` 变量或 `source .env.local` |
| **finetune 与 eval 竞争 GPU** | 同时运行显存冲突 | — | 分开运行，或错峰 |
| **smoke test fixture 漂移** | 新版 API 响应格式变了 | R04 偶发 diff | fixture 由 T1105 锁定版本 |

---

## 测试阶段风险

| Risk | 描述 | 检测方式 | 缓解 |
|---|---|---|---|
| **subprocess 未清理** | `make all-serve` 后台进程残留 | `pgrep -f "server\|uvicorn"` 非空 | `make all-stop` 确保 kill |
| **parallel make** | `make -j4 all-serve` 启动顺序乱 | R03 残留进程 | 不用 `-j`，串行启动 |
| **smoke test 非幂等** | 多次运行产生状态污染 | `make infra-smoke` 第二次失败 | 测试后 `make all-stop` 再 `make all-serve` |

---

## Blocker Checklist

- [ ] Python ≥ 3.10
- [ ] `make help` 输出正确：`cd ai-infra && make help`
- [ ] 端口空闲：`lsof -i :8000 -i :8080`
- [ ] `inference-service` 可启动：`$(MAKE) -C inference-service serve &`
- [ ] `ai-gateway` 可启动：`$(MAKE) -C ai-gateway serve &`
- [ ] `eval-module` CLI 可用：`python -m eval_module.main --help`
- [ ] `finetune-demo` CLI 可用：`python -m finetune_demo.main --help`
- [ ] `.env.local` 已配置：`source .env.local && echo $INFERENCE_BASE_URL`
- [ ] `BLOCKERS.md` 已创建：`ls docs/blockers/`
- [ ] `configs/service_matrix.yaml` 已创建：内容覆盖端口和依赖

---

## 当前已知 Blockers

| Blocker ID | 描述 | 状态 | 阻塞影响 |
|---|---|---|---|
| BLK-001 | vLLM engine timeout on startup | **RESOLVED** | — |
| BLK-002 | Gateway routing model not found | **RESOLVED** | — |
| BLK-003 | eval-module blocked by auth | **IN_PROGRESS** | eval-run-* 无法直连 inference |
| DEBT-001 | No CORS headers on gateway | P2 | 浏览器前端无法调用 |

来源：T1105 `T1105-root-blocker-entry-examples-v1.md`

---

Sources:
- T1005: root dev starter file pack
- T1105: root integration fixture manifest, blocker entries
- T805: cross-project integration prep pack (blocker escalation map)

Risk of Staleness:
- Service startup order and port assignments are project-internal; stable per T805
