Task ID: T701
Task Title: Inference Engines Deep-Research Pack
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
澄清推理引擎 vs 推理服务、Triton IS vs TensorRT-LLM、vLLM/SGLang 职责边界。

Result:

# Inference Boundary Matrix v1

## 边界一：推理引擎 vs 推理服务

### 推理引擎

| 属性 | 内容 |
|------|------|
| **定义** | 实际执行模型推理计算的核心库 |
| **职责** | 张量计算、显存管理、CUDA kernel 调用 |
| **代表** | vLLM、SGLang、TensorRT-LLM |
| **边界说明** | 引擎不直接暴露 HTTP 接口，需要包装 |

### 推理服务

| 属性 | 内容 |
|------|------|
| **定义** | 对外提供推理 API 服务的完整系统 |
| **职责** | 请求接收、路由、推理执行、响应返回 |
| **代表** | Triton IS、自定义 FastAPI 包装 |
| **边界说明** | 服务包含引擎 + HTTP 接口 + 批处理逻辑 |

### 边界澄清

- **vLLM** 既是引擎也是服务：内置 FastAPI/OpenAI 兼容接口，可独立对外服务
- **SGLang** 既是引擎也是服务：内置 HTTP 接口
- **TensorRT-LLM** 纯引擎，需要配合 Triton IS 或自定义服务包装才能对外
- **Triton IS** 纯服务编排，不包含推理计算

来源：https://docs.vllm.ai/
来源：https://sglang.readthedocs.io/
来源：https://nvidia.github.io/TensorRT-LLM/

---

## 边界二：Triton IS vs TensorRT-LLM

### Triton IS

| 属性 | 内容 |
|------|------|
| **定位** | 推理服务编排层 |
| **是否包含推理计算** | 否（调用后端执行） |
| **支持后端** | TensorRT、ONNX、Python、TensorRT-LLM |
| **模型格式** | 通用（TensorRT plan / ONNX / 自由格式） |
| **是否需要编译** | 否（支持动态加载部分模型） |

### TensorRT-LLM

| 属性 | 内容 |
|------|------|
| **定位** | 高性能推理引擎 |
| **是否包含推理计算** | 是（CUDA kernel 优化） |
| **支持模型** | 主要 LLM（GPT、LLaMA、Mistral 等） |
| **模型格式** | 编译后 .engine 文件 |
| **是否需要编译** | 是（必须先编译） |

### 关系澄清

```
Triton IS
    ├── backend: tensorrtllm → TensorRT-LLM 引擎
    ├── backend: onnx → ONNX Runtime
    └── backend: python → 自定义 Python 模型
```

Triton IS 可以作为 TensorRT-LLM 的服务包装层，但不是必须。

来源：https://docs.nvidia.com/deeplearning/triton-inference-server/
来源：https://nvidia.github.io/TensorRT-LLM/

---

## 边界三：vLLM vs SGLang

### 相同点

| 维度 | vLLM | SGLang |
|------|------|--------|
| 支持的模型 | 高度重叠 | 高度重叠 |
| Continuous Batching | 是 | 是 |
| Paged Attention | 是 | 是（原生） |
| Tensor Parallel | 是 | 是 |
| OpenAI 兼容 API | 是 | 是 |

### 核心差异

| 维度 | vLLM | SGLang |
|------|------|--------|
| **前缀缓存** | 部分支持 | RadixAttention 原生支持 |
| **调度粒度** | 请求级 | Token 级 |
| **生态** | 更大，更成熟 | 较小，调度更灵活 |
| **多轮对话优化** | 一般 | 更好（前缀复用） |

### 选择指引

| 场景 | 推荐 | 原因 |
|------|------|------|
| 快速部署/研发 | vLLM | 生态大，问题易解 |
| 多轮对话/前缀共享 | SGLang | RadixAttention 优势 |
| 极致性能（已确定模型） | TensorRT-LLM | 编译优化最强 |
| 需要统一服务编排 | Triton IS | 多后端支持 |

来源：https://docs.vllm.ai/
来源：https://sglang.readthedocs.io/

---

## 边界四：生产部署模式

| 模式 | 引擎 | 服务层 | 适用场景 |
|------|------|-------|---------|
| **快速研发** | vLLM/SGLang（直连） | 内置 HTTP | 本地开发/测试 |
| **单引擎生产** | vLLM/SGLang | 内置 HTTP 或 Triton | 单模型服务 |
| **多引擎编排** | TensorRT-LLM/vLLM/SGLang | Triton IS | 多模型/多版本管理 |
| **极致性能** | TensorRT-LLM | 自定义服务或 Triton | 已确定模型，追求性能 |

---

## 常见混淆

| 混淆 | 事实 |
|------|------|
| "Triton 是推理引擎" | Triton 是服务编排层，需要 backend 执行推理 |
| "vLLM 和 SGLang 是一样的" | 调度策略不同，SGLang 对前缀复用场景更好 |
| "TensorRT-LLM 可以直接部署" | 需要先编译，且与 GPU 型号强相关 |

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://sglang.readthedocs.io/ — SGLang
3. https://docs.nvidia.com/deeplearning/triton-inference-server/ — Triton IS
4. https://nvidia.github.io/TensorRT-LLM/ — TensorRT-LLM

Risk of Staleness:
- 各引擎版本更新可能改变边界

Out of Scope Kept:
- 未写代码实现
- 未写性能 benchmark 对比
