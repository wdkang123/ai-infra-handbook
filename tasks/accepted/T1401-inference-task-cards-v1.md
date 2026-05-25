# inference-service Task Cards v1

## Task ID: T1401
## Title: inference-service Codex Task Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# inference-service Task Cards

本文档定义每个任务卡的具体输入资产、目标文件、验收命令、完成信号和 cut line。

---

## T1401-T01: 包骨架 + 配置

**Task Name:** 包骨架 + 配置

**对应 Slice:** S1

**输入资产：**
- `T1001-inference-starter-manifest.md` — 目录结构蓝本
- `T1001-inference-config-py-blueprint-v1.md` — config.py 模板

**目标文件：**
```
inference-service/
├── pyproject.toml
├── src/inference_service/
│   ├── __init__.py
│   ├── __version__.py
│   └── config.py
├── config.yaml
├── config.local.yaml
└── config.smoke.yaml
```

**验收命令：**
```bash
cd inference-service
python -c "from inference_service import config; print('OK')"
```

**完成信号：** `import inference_service` 无报错，`config.yaml` 可读

**Cut Line：** 不写 server.py、main.py、engines/

---

## T1401-T02: FastAPI 骨架

**Task Name:** FastAPI 骨架

**对应 Slice:** S2

**输入资产：**
- `T1001-inference-server-py-blueprint-v1.md` — server.py 模板
- `T1001-inference-config-py-blueprint-v1.md` — config.py 模板（from T1401-T01）
- `T1001-T01/` — 目标文件（from T1401-T01）

**目标文件：**
```
inference-service/src/inference_service/
├── server.py
└── main.py
```

**验收命令：**
```bash
cd inference-service && python -m inference_service.main &
sleep 3

curl -s http://localhost:8000/health
# 期望：{"status": "healthy", "engine": "mock", "model": "Qwen2.5-0.5B-Instruct", "gpu_available": false}

curl -s -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "Qwen2.5-0.5B-Instruct", "messages": [{"role": "user", "content": "Hi"}]}'
# 期望：200 + ChatCompletionsResponse

pkill -f "inference_service.main"
```

**完成信号：** `/health` 返回 200，`/v1/chat/completions` mock 返回 200

**Cut Line：** 不实现真实 vLLM engine（S3），不实现 `/metrics`（S5），不写测试骨架（S6）

---

Sources:
- T1001: accepted starter manifest
- T1101: fixture assets
- T1301: accepted execution slice
- T811: accepted API contract
