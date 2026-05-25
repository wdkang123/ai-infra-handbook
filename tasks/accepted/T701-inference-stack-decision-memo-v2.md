Task ID: T701
Task Title: Inference Engines Deep-Research Pack
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
在 v1 基础上进一步收紧默认路线与引入时机，但仍不下最终结论。

Result:

# Inference Stack Decision Memo v2

## 概述

本文档在 v1 基础上进一步收紧推理栈选型的关键决策点，给出资料级输入，帮助 Codex 做最终判断。

---

## 决策点一：本地开发推理栈默认路线

### 推荐候选：vLLM（收紧）

**理由**：
- **接入成本低**：pip install vllm，无需编译
- **动态加载**：模型切换灵活，适合研发迭代
- **生态成熟**：文档完善，社区活跃，问题易解
- **OpenAI 兼容**：API 与 OpenAI 接口一致，降低 gateway 适配成本
- **v0.6.x 稳定版**：生产可用，API 稳定性改善

### 备选：SGLang（收紧）

**适用条件**：
- 多轮对话场景（prefix caching 收益大）
- 需要更细粒度的调度控制
- 需要 RadixAttention 特有能力

**不作为默认的理由**：
- 生态比 vLLM 小，问题解决资源少
- API 稳定性略低于 vLLM

### 不推荐作为默认：TensorRT-LLM（收紧）

**原因**：
- 必须预编译，模型切换成本高
- 编译时间长（数 GB 模型可能需要数十分钟）
- 适合明确模型、固定部署的生产环境，不适合快速迭代

### 资料级建议（v2 收紧）

| 阶段 | 推荐默认 | 收紧理由 |
|------|---------|---------|
| 本地开发 / 快速验证 | vLLM | 动态加载，切换灵活，生态成熟 |
| 多轮对话为主 | SGLang | RadixAttention 前缀复用优势明显 |
| 生产环境（已确定模型） | vLLM 或 TensorRT-LLM | 视性能需求和模型是否固定而定 |

来源：https://docs.vllm.ai/
来源：https://sglang.readthedocs.io/

---

## 决策点二：服务化分工边界（收紧）

### 分工框架（v2 收紧）

```
ai-gateway（路由 / 鉴权 / 限流）
    ↓
inference-service（vLLM/SGLang 直连）
    或
Triton IS（多模型编排时引入）
    ↓
vLLM / SGLang / TensorRT-LLM
```

### 何时需要 Triton IS（收紧）

**需要 Triton**：
- 需要同时管理多个推理引擎（TensorRT-LLM + vLLM）
- 需要统一 HTTP/gRPC 接口
- 需要模型 ensemble（多模型串联）
- 生产环境需要动态批处理和请求路由

**不需要 Triton（v2 收紧）**：
- MVP 阶段只需要 vLLM/SGLang 之一
- 模型数量少，不需要统一编排
- 追求简单，不想增加运维复杂度

### 什么时候引入 Triton（v2 收紧）

| 阶段 | 是否引入 Triton | 理由 |
|------|---------------|------|
| MVP | 否 | 增加复杂度，vLLM 内置已够用 |
| 多模型上线后 | 按需 | 需要统一管理时引入 |
| 生产环境（多团队） | 是 | 需要服务编排和流量管理 |

来源：https://docs.nvidia.com/deeplearning/triton-inference-server/

---

## 决策点三：TensorRT-LLM 引入时机（收紧）

### TensorRT-LLM 的定位（v2 收紧）

TensorRT-LLM 是"极致性能"路线，适合已确定模型、不需要频繁切换的生产环境。

### 必要前提条件（v2 收紧）

| 条件 | 说明 | 收紧程度 |
|------|------|---------|
| **模型已确定** | 编译耗时，频繁切换则不适合 | 必须 |
| **性能是主要矛盾** | 对延迟/吞吐量有明确 SLA | 必须 |
| **GPU 型号明确** | TensorRT-LLM 与 GPU 型号强相关（Hopper/Ampere） | 必须 |
| **编译时间可接受** | 数 GB 模型可能需要数十分钟编译 | 评估 |
| **运维能力足够** | 编译 + 部署流程比 vLLM 复杂 | 评估 |

### 引入时机决策（v2 收紧）

```
是否有关键性能指标（延迟/SLA）？
    ├── 否 → vLLM 直连，不引入 TRT-LLM
    └── 是 → 模型是否已确定且不再频繁更换？
              ├── 否 → vLLM，持续观察
              └── 是 → 是否有 NVIDIA Hopper/Ampere GPU？
                        ├── 否 → vLLM（其他 GPU 对 TRT-LLM 支持有限）
                        └── 是 → TensorRT-LLM 引入评估
```

### 不适合 TensorRT-LLM 的场景（v2 收紧）

- 本地开发、快速验证（模型频繁切换）
- 模型种类多、需要动态路由
- 团队没有 NVIDIA GPU 使用经验
- 非 NVIDIA GPU（AMD/Apple Silicon）

来源：https://nvidia.github.io/TensorRT-LLM/

---

## 决策点四：SGLang vs vLLM 选择（新增）

### v2 新增决策点

| 场景 | 推荐 | 关键依据 |
|------|------|---------|
| 通用场景 | vLLM | 生态大，稳定 |
| 多轮对话 / 前缀复用 | SGLang | RadixAttention 优势 |
| 需要细粒度 token 级调度 | SGLang | 调度更灵活 |
| 需要快速切换模型 | vLLM | 动态加载 |

来源：https://sglang.readthedocs.io/

---

## 总结：资料级建议（v2 收紧，不下结论）

| 决策点 | 建议方向 | 收紧程度 |
|--------|---------|---------|
| 本地开发默认 | vLLM | 明确 |
| SGLang 定位 | 备选（多轮对话场景） | 明确 |
| Triton IS 引入 | MVP 不引入，后续按需 | 明确 |
| TensorRT-LLM 时机 | 模型确定 + 性能优先 + GPU 支持 | 明确 |
| 多引擎切换 | MVP 单引擎，后续按需 | 明确 |

---

## 需要 Codex 最终判断

1. **本地开发默认是否确认用 vLLM**？
2. **SGLang 是否作为多轮对话场景的备选引擎**？
3. **Triton IS 是否在 MVP 阶段排除**？
4. **TensorRT-LLM 是否作为后续性能优化的必选**？
5. **GPU 型号是否支持 TensorRT-LLM**？

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://sglang.readthedocs.io/ — SGLang
3. https://docs.nvidia.com/deeplearning/triton-inference-server/ — Triton IS
4. https://nvidia.github.io/TensorRT-LLM/ — TensorRT-LLM

Risk of Staleness:
- 各引擎版本更新快，具体功能以实际版本为准
- TensorRT-LLM 与 GPU 型号相关

Out of Scope Kept:
- 未写代码实现
- 未写部署配置文件
- 未写性能 benchmark 结果
