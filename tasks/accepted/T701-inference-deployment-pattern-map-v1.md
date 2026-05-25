Task ID: T701
Task Title: Inference Engines Deep-Research Pack
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
整理从单机、单服务、多服务到网关接入的部署模式。

Result:

# Inference Deployment Pattern Map v1

## 概述

本文档整理从单机到网关接入的推理部署模式，按复杂度递增排列。

---

## 模式一：单机单引擎直连

### 描述

单个 vLLM/SGLang 实例直接对外提供推理服务。

```
客户端 → vLLM/SGLang（内置 HTTP）→ 模型
```

### 适用场景

- 本地开发
- 单机测试
- 小规模推理

### 最小实践

```bash
vllm serve Qwen/Qwen2.5-0.5B-Instruct \
    --host 0.0.0.0 \
    --port 8000
```

来源：https://docs.vllm.ai/en/latest/getting_started/quickstart.html

---

## 模式二：单机多引擎并存

### 描述

同一台机器上运行多个推理引擎实例（vLLM + SGLang 或 vLLM + TensorRT-LLM）。

```
客户端
    ├── 请求 A → vLLM :8000
    └── 请求 B → SGLang :8001
```

### 适用场景

- 同时测试多种引擎
- A/B 对比

### 端口分配

| 引擎 | 默认端口 |
|------|---------|
| vLLM | 8000 |
| SGLang | 8000（可配置） |
| Triton IS | 8000 |

来源：https://docs.vllm.ai/

---

## 模式三：ai-gateway + 单后端

### 描述

ai-gateway 作为统一入口，代理到单个 inference-service。

```
客户端 → ai-gateway → inference-service（vLLM/SGLang）
```

### 适用场景

- 生产环境单模型服务
- 需要鉴权/限流

### ai-gateway 配置

```yaml
# gateway.yaml
inference:
  backend: vllm
  base_url: http://localhost:8000/v1
```

来源：https://docs.vllm.ai/en/latest/getting_started/quickstart.html

---

## 模式四：ai-gateway + 多后端负载均衡

### 描述

ai-gateway 代理到多个 inference-service 实例，实现负载均衡。

```
客户端 → ai-gateway → [inference-1 :8000]
                    → [inference-2 :8000]
                    → [inference-3 :8000]
```

### 适用场景

- 多 GPU 横向扩展
- 提高吞吐量

### 配置示例

```yaml
# gateway.yaml
inference:
  backend: vllm
  urls:
    - http://inference-1:8000/v1
    - http://inference-2:8000/v1
    - http://inference-3:8000/v1
  load_balance: round_robin
```

来源：https://docs.vllm.ai/

---

## 模式五：Triton IS 统一编排

### 描述

使用 Triton IS 管理多个模型或多个引擎。

```
客户端 → Triton IS → [TensorRT-LLM backend]
                → [vLLM backend]
                → [ONNX backend]
```

### 适用场景

- 多模型管理
- 多引擎并存
- 需要模型 ensemble

### 模型仓库结构

```
model_repository/
    ├── tensorrt_llm_model/
    │     └── config.pbtxt
    ├── vllm_model/
    │     └── config.pbtxt
    └── ensemble/
          └── config.pbtxt
```

来源：https://docs.nvidia.com/deeplearning/triton-inference-server/

---

## 模式六：Triton IS + TensorRT-LLM

### 描述

Triton IS 作为服务层，调用 TensorRT-LLM 编译后的模型。

```
客户端 → Triton IS → TensorRT-LLM backend → .engine 文件
```

### 适用场景

- 极致性能
- 多模型统一管理
- 已确定模型

### 编译+部署流程

```bash
# 1. 编译模型
trtllm-build --model_dir=Qwen/Qwen2.5-0.5B-Instruct \
    --usage=inference \
    --output_dir=/tmp/tllm_engine \
    --Fp8

# 2. 配置 Triton 模型仓库
# /model_repository/tensorrt_llm/config.pbtxt

# 3. 启动 Triton
tritonserver --model-repository=/model_repository
```

来源：https://nvidia.github.io/TensorRT-LLM/

---

## 模式七：Kubernetes 部署

### 描述

在 K8s 环境中部署推理服务，支持自动扩缩容。

```
K8s Service → [inference Pod 1]
            → [inference Pod 2]
            → [inference Pod N]
```

### 适用场景

- 生产环境大规模部署
- 需要弹性伸缩

### K8s 部署要点

| 组件 | 说明 |
|------|------|
| Deployment | 推理服务副本数 |
| Service | 内部负载均衡 |
| HPA | 根据 metrics 自动扩缩容 |
| PVC | 模型文件存储 |

来源：https://docs.vllm.ai/

---

## 模式八：混合部署（研发+生产）

### 描述

研发环境用 vLLM 直连，生产环境用 TensorRT-LLM + Triton。

```
研发：客户端 → vLLM（直连，快速迭代）
生产：客户端 → ai-gateway → Triton IS → TensorRT-LLM
```

### 适用场景

- 研发生产分离
- 不同场景用不同引擎

---

## 部署模式选择决策树

```
输入：场景
    │
    ├── 本地开发/测试
    │     → 模式一（单机单引擎直连）
    │
    ├── 小规模生产（< 1万 QPS）
    │     → 模式三（gateway + 单后端）
    │     或 模式四（gateway + 多后端）
    │
    ├── 多模型管理
    │     → 模式五（Triton IS 统一编排）
    │
    ├── 极致性能（已确定模型）
    │     → 模式六（Triton IS + TensorRT-LLM）
    │
    └── 大规模弹性
          → 模式七（Kubernetes 部署）
```

---

## 部署模式与引擎对应

| 模式 | 推荐引擎 | 说明 |
|------|---------|------|
| 模式一 | vLLM / SGLang | 内置 HTTP，快速启动 |
| 模式二 | vLLM + SGLang | 同时测试多种引擎 |
| 模式三/四 | vLLM / SGLang | gateway 代理 |
| 模式五 | Triton IS + 任意 | 多模型编排 |
| 模式六 | Triton IS + TensorRT-LLM | 极致性能 |
| 模式七 | 任意 | K8s 部署 |

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://sglang.readthedocs.io/ — SGLang
3. https://docs.nvidia.com/deeplearning/triton-inference-server/ — Triton IS
4. https://nvidia.github.io/TensorRT-LLM/ — TensorRT-LLM

Risk of Staleness:
- 部署方式可能随 K8s 版本和云厂商变化

Out of Scope Kept:
- 未写完整 K8s 配置
- 未写 Helm Chart
- 未写 CI/CD 集成
