# eval-module Risk Checklist v1

## Task ID: T1203
## Title: eval-module Implementation Map Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# eval-module Risk & Blocker Checklist

本文档定义 eval-module 实现过程中的风险点与阻塞检查项。

## P0 阻塞风险

| Risk | 描述 | 缓解方案 |
|---|---|---|
| **lm-eval 版本兼容** | `lm-evaluation-harness` API 在 0.4 → 0.5 有 breaking change | 锁定 `lm-eval>=0.4.7,<0.6`，优先用 0.4.7 |
| **inference-service 不可用** | runner 需要真实推理 backend | P0 阶段用 mock runner；P2 阶段确保 inference-service 运行 |
| **lm-eval task name 不匹配** | lm-eval 的 task id（如 `mmlu`）与 CLI `--task` 参数不一致 | `LmEvalRunner.list_tasks()` 先行确认 |

---

## P1 风险

| Risk | 描述 | 检测方式 | 缓解 |
|---|---|---|---|
| **lm-eval vLLM backend 配置** | `lm-eval` 的 vLLM backend config key 变化 | `lm_eval.api.list_tasks()` 失败 | 查看 lm-eval 源码确认 config key |
| **HF token 缺失** | gated model（如 Llama）需要 `--token` | 直接测 Qwen 系列免 token 模型 | 从 Qwen2.5-0.5B-Instruct 开始 |
| **num_samples 限制** | lm-eval `--limit` 参数非所有 task 都支持 | `lm-eval --help` 确认 | 仅 gsm8k/humaneval 支持 limit |

---

## P2 风险

| Risk | 描述 | 检测方式 | 缓解 |
|---|---|---|---|
| **result JSON `backend` 字段** | 之前错误写成 URL，现在应该是 backend 类型字符串 | JSON `backend` 字段是否为 `"vllm"` 而非 URL | 对照 T1103 EvalResult fixture |
| **timestamp 格式** | lm-eval 返回的 timestamp 可能不是 ISO8601 | 验证 JSON timestamp 是否 ISO8601 | 使用 `datetime.utcnow().isoformat()` 统一 |
| **raw_output 泄漏** | `raw_output` 可能含大量调试信息导致 JSON 过大 | 观察输出文件大小 | 默认 `raw_output: null`，调试时显式启用 |

---

## P3 风险

| Risk | 描述 | 检测方式 | 缓解 |
|---|---|---|---|
| **ResultStore 路径穿越** | 用户指定 `--output ../../etc/passwd` | `ResultStore.save` 拒绝绝对路径或 `..` | `path.resolve().relative_to(base_dir)` 检查 |
| **comparator 处理缺失字段** | baseline 有 `metrics.pass@8` 但 candidate 没有 | E07 测试失败 | `delta` 计算时 `candidate.get("metrics", {}).get("pass@8", None)` |
| **compare 0 做除数** | `accuracy_relative_pct = (delta / baseline) * 100`，baseline=0 时 NaN | E07 | `if baseline == 0: delta = None` |

---

## 测试阶段风险

| Risk | 描述 | 检测方式 | 缓解 |
|---|---|---|---|
| **lm-eval mock** | 单元测试不应调真实 lm-eval | `pytest tests/test_runner.py` 走真实路径 | P0 用 `@pytest.mark.unit`，mock runner 结果 |
| **pytest-asyncio 冲突** | runner.run() 是同步函数，lm-eval 内部异步 | `pytest tests/test_runner.py` 报错 | `pytest-asyncio>=0.23` |

---

## Blocker Checklist

- [ ] Python ≥ 3.10
- [ ] `lm-eval>=0.4.7,<0.6` 已安装：`python -c "import lm_eval; print(lm_eval.__version__)"`
- [ ] `typer>=0.9` 已安装
- [ ] `rich>=13.0` 已安装
- [ ] inference-service 运行（用于 P2 端到端测试）：`curl localhost:8000/health`
- [ ] `pyproject.toml` 依赖已安装：`pip install -e eval-module`

---

Sources:
- T1003: main.py, runner blueprint
- T1103: result JSON samples (corrected: backend is string)
- T303: accepted MVP design
- T813: accepted validation checklist

Risk of Staleness:
- lm-eval API stability is the main risk; mitigated by version pinning
