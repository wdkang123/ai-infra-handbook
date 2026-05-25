# Root Integration Blocker Entry Examples v1

## Task ID: T1105
## Title: Root Integration Fixture Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# Root Integration Blocker Entry Examples

本文档定义根级联调中的 blocker（阻塞问题）记录示例，对应真实文件 `ai-infra/docs/blockers/` 和 `tasks/blocker-log.md`。

## Blocker vs Technical Debt

| 类型 | 状态 | 说明 |
|---|---|---|
| Blocker | `BLOCKED` | 阻塞后续开发，必须修完才能继续 |
| Tech Debt | `DEBT` | 已知问题，暂可继续，记录在案 |

---

## Blocker Entry Format

```yaml
blocker_id: "BLK-001"
title: "<简短标题>"
severity: "P0 | P1 | P2"
status: "OPEN | IN_PROGRESS | RESOLVED"
created_date: "YYYY-MM-DD"
owner: "<team or person>"
description: |
  <详细描述>
impact: |
  <对谁/什么造成影响>
reproduction: |
  <复现步骤>
workaround: |
  <临时规避方案（如果有）>
resolution: |
  <解决方案（RESOLVED 后填写）>
related_tasks:
  - "Txxx"
  - "Tyyy"
```

---

## Blocker Example 1: vLLM 引擎启动超时

**对应文件：** `ai-infra/docs/blockers/BLK-001-vllm-engine-timeout.md`

```yaml
blocker_id: "BLK-001"
title: "vLLM 引擎启动超过 startup_timeout=120s"
severity: "P0"
status: "RESOLVED"
created_date: "2026-04-01"
owner: "MINIMAX"
description: |
  使用 `make inference-serve` 启动 inference-service 时，
  vLLM 引擎初始化（加载 Qwen2.5-0.5B-Instruct AWQ 量化模型）
  超过 120 秒，导致 health check 超时失败。
impact: |
  - 本地开发无法启动
  - CI smoke test 必然失败
reproduction: |
  1. `cd ai-infra && cp .env.local .env`
  2. `make inference-serve MODEL=Qwen/Qwen2.5-0.5B-Instruct PORT=8000`
  3. 等待 120 秒后看到 `RuntimeError: Engine startup timeout`
workaround: |
  `VLLMEnforceEager=true` + `VLLMGpuMemoryUtilization=0.5` 减少预加载量
resolution: |
  将 `startup_timeout` 从 120s 提高到 300s（配置文件 T1101）
  将 `VLLMGpuMemoryUtilization` 默认从 0.85 改为 0.8
related_tasks:
  - "T811"
  - "T901"
  - "T1101"
```

---

## Blocker Example 2: ai-gateway 路由配置缺失导致 404

**对应文件：** `ai-infra/docs/blockers/BLK-002-gateway-routing-missing.md`

```yaml
blocker_id: "BLK-002"
title: "ai-gateway 路由配置缺失，vllm-local 模型返回 404"
severity: "P0"
status: "RESOLVED"
created_date: "2026-04-02"
owner: "MINIMAX"
description: |
  ai-gateway 的 `models.yaml` 中缺少 `vllm-local` 的路由配置，
  导致所有经过 gateway 的请求即使 model 名为 `vllm-local` 也返回 404。
impact: |
  - IT-01 (gateway proxy) smoke test 失败
  - 所有通过 gateway 的推理请求失败
reproduction: |
  1. `make all-serve`
  2. `curl -X POST http://localhost:8080/v1/chat/completions \
       -H "Authorization: Bearer dev-gateway-key-1" \
       -d '{"model": "vllm-local", "messages": [{"role": "user", "content": "Hi"}]}'`
  3. 返回 404
workaround: |
  临时在 `ai-gateway/configs/models.yaml` 中添加 `vllm-local` 路由
resolution: |
  在 `ai-gateway/configs/models.yaml` 中添加：
  ```yaml
  - name: "vllm-local"
    downstream: "http://localhost:8000/v1"
    enabled: true
  ```
related_tasks:
  - "T812"
  - "T902"
  - "T1102"
```

---

## Blocker Example 3: eval-module 无法连接 inference-service（认证问题）

**对应文件：** `ai-infra/docs/blockers/BLK-003-eval-auth-blocked.md`

```yaml
blocker_id: "BLK-003"
title: "eval-module 通过 ai-gateway 评测时收到 401"
severity: "P1"
status: "OPEN"
created_date: "2026-04-05"
owner: "MINIMAX"
description: |
  eval-module 向 ai-gateway 发送评测请求时，
  ai-gateway 要求 Authorization header，
  但 eval-module 评测请求不带 token。
impact: |
  - eval-module 无法通过 ai-gateway 评测
  - 必须直连 inference-service 才能评测
reproduction: |
  `python -m eval_module.main run --task gsm8k --model Qwen2.5-0.5B-Instruct \
     --backend-url http://localhost:8080/v1`
  → 返回 401
workaround: |
  eval-module 评测时直连 inference-service（--backend-url http://localhost:8000/v1）
resolution: |
  方案 A: eval-module 添加 `--auth-key` 参数透传到下游
  方案 B: ai-gateway 在 `bypass_paths` 中添加 eval-module 健康检查路径
  方案 C: eval-module 配置文件中维护白名单 token
related_tasks:
  - "T303"
  - "T813"
  - "T1103"
```

---

## Technical Debt Entry Example

**对应文件：** `ai-infra/docs/blockers/DEBT-001-no-cors-headers.md`

```yaml
debt_id: "DEBT-001"
title: "ai-gateway 缺少 CORS headers"
severity: "P2"
status: "OPEN"
created_date: "2026-04-03"
owner: "MINIMAX"
description: |
  ai-gateway 当前响应没有 CORS Access-Control-* headers，
  浏览器前端无法直接从客户端调用 gateway。
impact: |
  - 前端 Demo 无法集成
  - 只能通过后端服务间调用
workaround: |
  使用服务器端代理转发请求
resolution: |
  在 ai-gateway FastAPI app 中添加 CORSMiddleware
related_tasks:
  - "T302"
```

---

## Active Blockers Summary

| ID | Title | Severity | Status |
|---|---|---|---|
| BLK-001 | vLLM 启动超时 | P0 | RESOLVED |
| BLK-002 | Gateway 路由缺失 | P0 | RESOLVED |
| BLK-003 | eval 评测 401 | P1 | OPEN |

---

## 与任务系统对齐

Blocker 与任务系统（task-board.md）的关系：
- `OPEN` blocker → 对应任务进入 `BLOCKED` 状态
- `RESOLVED` blocker → 解锁对应任务
- `DEBT` → 记录在 `DEBT` 列表，不阻塞任务推进

---

Sources:
1. https://github.com/anthropics/claude-code — blocker workflow reference

Risk of Staleness:
- Blocker entry format is project-internal; defined per T805 integration contract
