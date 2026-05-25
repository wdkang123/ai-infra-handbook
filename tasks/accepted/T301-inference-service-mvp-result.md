Task ID: T301
Task Title: inference-service MVP 目录与边界设计
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于已通过的 vLLM、SGLang、Triton IS、TensorRT-LLM 资料包，定义 inference-service 模块的 MVP 边界和目录结构。

Result:

## 一、定位说明

**inference-service** 是 AI Infra 项目中负责**模型推理服务化**的模块。它的核心职责：

- 将训练好的模型部署为可对外提供服务的 API 端点
- 管理模型的加载、卸载、版本切换
- 提供推理请求的调度、batch 管理、资源分配
- 暴露 Prometheus metrics 支持可观测性

**inference-service 不做的事**：
- 模型训练（属于 finetune-demo 或外部训练流水线）
- 流量路由和负载均衡策略（属于 ai-gateway）
- 模型评测和对比（属于 eval-module）

## 二、目录结构（最小骨架）

```
inference-service/
├── README.md                    # 模块说明、快速启动
├── pyproject.toml               # Python 依赖定义
├── src/
│   └── inference_service/
│       ├── __init__.py
│       ├── server.py           # 主服务入口，统一 HTTP/gRPC 端点
│       ├── engines/             # 推理引擎抽象层
│       │   ├── __init__.py
│       │   ├── base.py         # Engine 抽象基类
│       │   ├── vllm_engine.py  # vLLM 引擎适配
│       │   ├── sglang_engine.py # SGLang 引擎适配
│       │   └── triton_engine.py # Triton IS 引擎适配
│       ├── config.py           # 服务配置（端口、资源分配）
│       └── metrics.py          # Prometheus metrics 封装
├── tests/
│   └── test_inference.py       # 基本推理调用测试
└── examples/
    └── quickstart.py           # 快速启动示例（vLLM + Qwen）
```

## 三、核心接口

### HTTP API（OpenAI 兼容）

| 端点 | 方法 | 说明 |
|------|------|------|
| `/v1/chat/completions` | POST | 聊天补全（流式/非流式） |
| `/v1/completions` | POST | 文本补全 |
| `/v1/models` | GET | 列出可用模型 |
| `/health` | GET | 健康检查 |

### Python SDK 接口

```python
from inference_service import InferenceService

service = InferenceService(engine="vllm", model="Qwen/Qwen2.5-7B-Instruct")
response = service.chat(messages=[{"role": "user", "content": "Hello"}])
```

### CLI 接口

```bash
# 启动服务
inference-service serve --engine vllm --model Qwen/Qwen2.5-7B-Instruct --port 8000

# 查看版本
inference-service version
```

## 四、依赖关系

```
ai-gateway（上层，流量入口）
    ↓ 请求
inference-service（本案）
    ↓ 调用
├── vLLM Engine（SGLang/Triton IS 可选）
├── 模型文件（HuggingFace / 本地路径）
└── GPU 资源（CUDA）
```

- **下游**：依赖 vLLM、SGLang、Triton IS 等推理引擎的 Python 包
- **上游**：被 ai-gateway 调用，或直接被应用层调用

## 五、边界说明

| 边界 | 说明 |
|------|------|
| vs ai-gateway | ai-gateway 负责流量管理（路由、限流、鉴权），inference-service 负责模型推理本身 |
| vs eval-module | eval-module 通过调用 inference-service 的 API 发送推理请求进行评测，inference-service 不做评测逻辑 |
| vs finetune-demo | finetune-demo 负责模型训练和微调，训练产出的模型由 inference-service 部署 |

## 六、最小可运行路径

**目标**：拉起一个 vLLM 推理服务，验证单个请求成功返回。

```bash
# 1. 安装依赖
pip install inference-service

# 2. 启动服务（单行命令）
inference-service serve --engine vllm --model Qwen/Qwen2.5-7B-Instruct --port 8000

# 3. 验证
curl http://localhost:8000/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{"model": "Qwen/Qwen2.5-7B-Instruct", "messages": [{"role": "user", "content": "Hello"}]}'

# 4. 查看 metrics
curl http://localhost:8000/metrics
```

**预期输出**：JSON 格式的 chat completion 响应。

## 七、引擎抽象设计

每个引擎实现 `BaseEngine` 接口：

```python
class BaseEngine(ABC):
    @abstractmethod
    def load_model(self, model_path: str) -> None: ...

    @abstractmethod
    def infer(self, prompt: str, **kwargs) -> str: ...

    @abstractmethod
    def stream(self, prompt: str, **kwargs) -> Iterator[str]: ...
```

Sources:
1. https://github.com/vllm-project/vllm — vLLM 引擎
2. https://github.com/sgl-project/sglang — SGLang 引擎
3. https://github.com/triton-inference-server/server — Triton IS 引擎
4. https://github.com/NVIDIA/TensorRT-LLM — TensorRT-LLM 引擎

Risk of Staleness:
- 引擎接口抽象需随 vLLM/SGLang/Triton IS API 变化迭代
- 具体 engine 参数以各引擎文档为准

Out of Scope Kept:
- 未写完整的模型管理子系统（版本、灰度）
- 未写 GPU 集群调度
- 未写多模型混合部署
