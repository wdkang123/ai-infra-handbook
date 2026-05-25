# inference-service Test Plan v1

## Task ID: T801
## Task Title: inference-service Execution Prep Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T301 MVP 设计，准备 inference-service 实施前包。

---

# inference-service Test Plan v1

## 概述

本文档定义 inference-service 的测试计划，覆盖单元测试、集成测试、端到端测试。

---

## 测试分层

| 测试类型 | 覆盖范围 | 测试对象 | Mock 程度 |
|---------|---------|---------|----------|
| 单元测试 | 引擎抽象层、配置加载 | `engines/`, `config.py` | 完全 Mock |
| 集成测试 | API 端点、引擎调用 | `api/`, `server.py` | 部分 Mock |
| 端到端测试 | 完整推理链路 | 实际 vLLM 服务 | 无 Mock |

---

## 单元测试

### engines/base.py

| 测试用例 | 输入 | 预期输出 |
|---------|------|---------|
| `test_base_engine_interface` | 实例化 BaseEngine | 抛出 NotImplementedError |
| `test_load_model_not_implemented` | 调用 load_model | 抛出 NotImplementedError |
| `test_infer_not_implemented` | 调用 infer | 抛出 NotImplementedError |

### engines/vllm_engine.py

| 测试用例 | 输入 | 预期输出 |
|---------|------|---------|
| `test_vllm_engine_init` | 有效 model_path | 引擎实例创建成功 |
| `test_vllm_engine_load` | Mock vLLM client | load_model 调用成功 |
| `test_vllm_engine_infer` | Mock prompt | 返回 Mock 响应 |

### config.py

| 测试用例 | 输入 | 预期输出 |
|---------|------|---------|
| `test_load_config_from_yaml` | 有效 config.yaml | 配置对象正确 |
| `test_load_config_from_env` | 有效环境变量 | 环境变量覆盖 YAML |
| `test_default_values` | 空配置 | 使用默认值 |
| `test_invalid_config` | 无效配置 | 抛出 ValidationError |

---

## 集成测试

### API 端点测试

#### `POST /v1/chat/completions`

| 测试用例 | 输入 | 预期输出 |
|---------|------|---------|
| `test_chat_completions_basic` | 有效 messages | 200 + valid response |
| `test_chat_completions_with_stream` | `stream: true` | SSE 流式响应 |
| `test_chat_completions_invalid_model` | 无效 model | 404 error |
| `test_chat_completions_empty_messages` | 空 messages | 422 validation error |
| `test_chat_completions_with_stop` | 有效 stop 参数 | 截断生成 |

#### `GET /health`

| 测试用例 | 输入 | 预期输出 |
|---------|------|---------|
| `test_health_check_healthy` | 服务正常 | `{"status": "healthy"}` |
| `test_health_check_engine_error` | 引擎加载失败 | `{"status": "unhealthy"}` |

#### `GET /metrics`

| 测试用例 | 输入 | 预期输出 |
|---------|------|---------|
| `test_metrics_endpoint` | 服务运行中 | Prometheus 格式 metrics |

---

## 端到端测试

### 基本推理测试

```bash
# 1. 启动服务
inference-service serve --engine vllm --model Qwen/Qwen2.5-0.5B-Instruct &

# 2. 等待服务就绪
sleep 30

# 3. 健康检查
curl http://localhost:8000/health

# 4. 基本推理
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"Qwen2.5-0.5B-Instruct","messages":[{"role":"user","content":"Hello"}]}'

# 5. Metrics 检查
curl http://localhost:8000/metrics | grep vllm
```

### 预期输出

| 步骤 | 预期结果 |
|------|---------|
| 健康检查 | `{"status": "healthy", "engine": "vllm"}` |
| 基本推理 | `choices[0].message.content` 非空 |
| Metrics | 包含 `vllm_num_requests_running` 指标 |

---

## 测试工具建议

| 工具 | 用途 | 安装 |
|------|------|------|
| `pytest` | 测试框架 | `pip install pytest pytest-asyncio` |
| `pytest-asyncio` | 异步测试 | `pip install pytest-asyncio` |
| `pytest-cov` | 覆盖率 | `pip install pytest-cov` |
| `httpx` | HTTP 客户端 | `pip install httpx` |
| `pytest-mock` | Mock 工具 | `pip install pytest-mock` |

---

## CI 配置建议

```yaml
# .github/workflows/test.yml
name: test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-22.04
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -e ".[test]"
      - name: Run unit tests
        run: pytest tests/test_engine.py tests/test_config.py -v
      - name: Run integration tests
        run: pytest tests/test_api.py -v
```

---

## 测试覆盖率目标

| 模块 | 目标覆盖率 |
|------|----------|
| `engines/` | 90% |
| `config.py` | 95% |
| `api/` | 85% |
| `metrics.py` | 80% |
| `health.py` | 90% |
| **总体** | **85%** |

---

## 测试数据管理

| 数据类型 | 存储位置 | 说明 |
|---------|---------|------|
| Mock 模型响应 | `tests/fixtures/` | JSON 文件 |
| 测试配置 | `tests/configs/` | YAML 文件 |
| 小模型（测试用） | HuggingFace 缓存 | Qwen2.5-0.5B |

---

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://pytest.org/ — pytest
3. https://www.python-httpx.org/ — httpx

Risk of Staleness:
- 测试命令可能因框架版本变化

Out of Scope Kept:
- 未写性能测试
- 未写压力测试
